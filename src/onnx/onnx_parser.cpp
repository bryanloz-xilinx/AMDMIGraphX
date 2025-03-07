#include <migraphx/onnx/onnx_parser.hpp>
#include <migraphx/onnx/op_parser.hpp>
#include <migraphx/fallthrough.hpp>
#include <migraphx/make_op.hpp>
#include <migraphx/stringutils.hpp>
#include <migraphx/ranges.hpp>
#include <migraphx/instruction.hpp>
#include <migraphx/pad_calc.hpp>
#include <migraphx/common.hpp>
#include <migraphx/type_traits.hpp>
#include <migraphx/float_equal.hpp>
#include <migraphx/file_buffer.hpp>
#include <migraphx/filesystem.hpp>
#include <migraphx/op/unknown.hpp>

namespace migraphx {
inline namespace MIGRAPHX_INLINE_NS {
namespace onnx {

static onnx_parser::attribute_map get_attributes(const onnx::NodeProto& node)
{
    std::unordered_map<std::string, onnx::AttributeProto> result;
    for(auto&& attr : node.attribute())
    {
        result[attr.name()] = attr;
    }
    return result;
}

static literal
create_literal(shape::type_t shape_type, const std::vector<size_t>& dims, const char* data)
{
    // empty input
    auto elem_num =
        std::accumulate(dims.begin(), dims.end(), std::size_t(1), std::multiplies<std::size_t>());
    if(elem_num == 0)
    {
        return {};
    }

    // in case of scalar constants in onnx file, use dims=1 to fill initializer data
    if(dims.empty())
        return literal{{shape_type}, data};
    return literal{{shape_type, dims}, data};
}

template <class T, MIGRAPHX_REQUIRES(not std::is_pointer<T>{})>
static literal create_literal(shape::type_t shape_type, const std::vector<size_t>& dims, T data)
{
    // empty input
    auto elem_num =
        std::accumulate(dims.begin(), dims.end(), std::size_t(1), std::multiplies<std::size_t>());
    if(elem_num == 0)
    {
        return {};
    }

    // scalar input
    if(dims.empty())
        return literal{{shape_type}, data.begin(), data.end()};
    return literal{{shape_type, dims}, data.begin(), data.end()};
}

template <class T>
static literal from_repeated(shape::type_t t, const T& r)
{
    std::size_t size = r.size();
    return literal{{t, {size}}, r.begin(), r.end()};
}

instruction_ref onnx_parser::node_info::make_contiguous(instruction_ref ins) const
{
    if(ins->get_shape().standard())
    {
        return ins;
    }

    return add_instruction(make_op("contiguous"), ins);
}

instruction_ref onnx_parser::node_info::add_bias(const std::vector<instruction_ref>& args,
                                                 instruction_ref curr_ins,
                                                 uint64_t axis) const
{
    if(args.size() == 3)
    {
        auto bias_bcast = mod->add_instruction(
            make_op("broadcast", {{"axis", axis}, {"out_lens", curr_ins->get_shape().lens()}}),
            args[2]);
        return mod->add_instruction(make_op("add"), curr_ins, bias_bcast);
    }
    return curr_ins;
}

instruction_ref onnx_parser::node_info::add_broadcastable_binary_op(const std::string& op_name,
                                                                    instruction_ref arg0,
                                                                    instruction_ref arg1) const
{
    return add_common_op(*mod, make_op(op_name), {arg0, arg1});
}

instruction_ref
onnx_parser::node_info::add_instruction(const operation& op,
                                        const std::vector<instruction_ref>& args) const
{
    return mod->add_instruction(op, args);
}

instruction_ref onnx_parser::node_info::add_instruction(const operation& op,
                                                        const std::vector<instruction_ref>& args,
                                                        const std::vector<module_ref>& mods) const
{
    return mod->add_instruction(op, args, mods);
}

instruction_ref onnx_parser::node_info::add_literal(literal l) const
{
    return mod->add_literal(std::move(l));
}

onnx_parser::onnx_parser()
{
    // Add all registered op parsers
    for(auto&& name : get_op_parsers())
        ops.emplace(name, get_op_parser(name));
}

operation onnx_parser::load(const std::string& name, const node_info& info) const
{
    auto op = make_op(name);
    auto v  = op.to_value();
    for(auto&& x : v)
    {
        if(info.attributes.count(x.get_key()) == 0)
            continue;
        literal s = parse_value(info.attributes.at(x.get_key()));
        if(x.is_array())
        {
            std::vector<value> values;
            s.visit([&](auto y) {
                std::transform(y.begin(), y.end(), std::back_inserter(values), [](auto z) {
                    return value(z);
                });
            });
            x = values;
        }
        else
        {
            s.visit([&](auto y) { x = y.front(); });
        }
    }
    op.from_value(v);
    return op;
}

void onnx_parser::parse_undefined(module* mod, const std::string& name)
{
    if(!contains(instructions, name))
    {
        auto ins           = mod->add_instruction(make_op("undefined"));
        instructions[name] = ins;
    }
}

void onnx_parser::parse_from(std::istream& is, std::string name)
{
    auto* mm         = prog.get_main_module();
    this->filename   = std::move(name);
    auto parent_path = fs::path(this->filename).parent_path();
    if(not parent_path.empty())
        this->path = parent_path;

    onnx::ModelProto model;
    if(model.ParseFromIstream(&is))
    {
        auto version  = get_opset_version(model);
        opset_version = (version == -1) ? opset_version : version;

        if(model.has_graph())
        {
            this->parse_graph(mm, model.graph());
        }
    }
    else
    {
        MIGRAPHX_THROW("PARSE_FROM: Failed reading onnx file: " + this->filename);
    }
}

void onnx_parser::parse_from(const void* data, std::size_t size)
{
    auto* mm = prog.get_main_module();
    onnx::ModelProto model;
    if(model.ParseFromArray(data, size))
    {
        auto version  = get_opset_version(model);
        opset_version = (version == -1) ? opset_version : version;

        if(model.has_graph())
        {
            this->parse_graph(mm, model.graph());
        }
    }
    else
    {
        MIGRAPHX_THROW("Failed reading onnx file.");
    }
}

int64_t onnx_parser::get_opset_version(const onnx::ModelProto& model)
{
    const auto& opset_import = model.opset_import();
    int64_t version          = -1;
    for(const auto& opset : opset_import)
    {
        if(opset.has_version())
        {
            version = std::max(version, opset.version());
        }
    }

    return version;
}

void onnx_parser::parse_graph(module* mod, const onnx::GraphProto& graph)
{
    std::unordered_map<std::string, instruction_ref> mod_insts;
    for(auto&& f : graph.initializer())
    {
        // backup instructions in parent mod
        mod_insts[f.name()] = mod->add_literal(parse_tensor(f));
    }

    for(auto&& input : graph.input())
    {
        const std::string& name = input.name();
        // input not in initializer_data, so it is a real input
        if(!contains(mod_insts, name))
        {
            // ONNX specification does not specify hwo to deal with the
            // scenario that a nested subgraph contains a parameter with the
            // name existed in its parent graph.
            // In the current implementation, MIGraphX throws an exception for that.
            if(contains(instructions, name))
            {
                MIGRAPHX_THROW("module \"" + mod->name() + "\" has parameter name \"" + name +
                               "\" existing in parent graph!");
            }

            std::vector<std::size_t> dims;
            if(map_input_dims.count(name) > 0)
            {
                dims = map_input_dims.at(name);
            }

            shape s         = parse_type(input.type(), dims);
            mod_insts[name] = mod->add_parameter(name, s);
        }
    }

    std::copy(mod_insts.begin(), mod_insts.end(), std::inserter(instructions, instructions.end()));

    for(auto&& node : graph.node())
    {
        std::vector<instruction_ref> args;
        for(auto&& input : node.input())
        {
            if(input.empty())
            {
                this->parse_undefined(mod, input);
            }
            if(instructions.count(input) == 0)
            {
                MIGRAPHX_THROW("PARSE_GRAPH: invalid onnx file. Input \"" + input +
                               "\" is unavailable due to unordered nodes!");
            }
            args.push_back(instructions.at(input));
        }

        std::vector<instruction_ref> result;
        std::size_t output_num = static_cast<std::size_t>(node.output().size());
        if(ops.count(node.op_type()) == 0)
        {
            if(skip_unknown_operators)
                result.push_back(mod->add_instruction(op::unknown{node.op_type()}, args));
            else
                MIGRAPHX_THROW("Unknown operator: " + node.op_type());
        }
        else
        {
            std::string node_name = node.op_type() + "_" + std::to_string(mod->size());
            result                = ops[node.op_type()](
                *this, {get_attributes(node), output_num, node_name, mod}, args);
        }

        output_num = std::min<std::size_t>(output_num, result.size());
        std::transform(node.output().begin(),
                       node.output().begin() + output_num,
                       result.begin(),
                       std::inserter(instructions, instructions.end()),
                       [](auto&& x, auto&& y) { return std::make_pair(x, y); });
    }

    // Find instructions corresponding to the output
    auto prog_output = graph.output();
    std::vector<std::string> all_output_names;
    std::vector<std::string> prog_output_names;
    std::transform(prog_output.begin(),
                   prog_output.end(),
                   std::back_inserter(all_output_names),
                   [](auto& node) { return node.name(); });
    std::copy_if(
        all_output_names.begin(),
        all_output_names.end(),
        std::back_inserter(prog_output_names),
        [&](const auto& name) { return !(name.empty() or instructions.count(name) == 0); });

    std::vector<instruction_ref> output_ins;
    std::transform(prog_output_names.begin(),
                   prog_output_names.end(),
                   std::back_inserter(output_ins),
                   [&](const auto& name) { return instructions[name]; });

    // add the return instuction
    mod->add_return(output_ins);

    // remove instructions added in this mod
    erase_if(instructions, [&](auto&& p) { return mod->has_instruction(p.second); });
}

literal onnx_parser::parse_value(const onnx::AttributeProto& attr) const
{
    switch(attr.type())
    {
    case onnx::AttributeProto::FLOAT: return literal{attr.f()};
    case onnx::AttributeProto::INT: return literal{attr.i()};
    case onnx::AttributeProto::TENSOR: return parse_tensor(attr.t());
    case onnx::AttributeProto::FLOATS: return from_repeated(shape::float_type, attr.floats());
    case onnx::AttributeProto::INTS: return from_repeated(shape::int64_type, attr.ints());
    case onnx::AttributeProto::UNDEFINED:
    case onnx::AttributeProto::GRAPH:
    case onnx::AttributeProto::STRING:
    case onnx::AttributeProto::STRINGS:
    case onnx::AttributeProto::TENSORS:
    case onnx::AttributeProto::SPARSE_TENSOR:
    case onnx::AttributeProto::SPARSE_TENSORS:
    case onnx::AttributeProto::GRAPHS: return {};
    }
    MIGRAPHX_THROW("PARSE_VALUE: Invalid attribute type " + std::to_string(attr.type()));
}

literal onnx_parser::parse_tensor(const onnx::TensorProto& t) const
{
    std::vector<std::size_t> dims(t.dims().begin(), t.dims().end());
    if(not t.external_data().empty())
    {
        const std::string& data_file = t.external_data().at(0).value();
        auto raw_buffer              = read_buffer(path + "/" + data_file);
        std::string s(raw_buffer.begin(), raw_buffer.end());
        auto type = get_type(t.data_type());
        return create_literal(type, dims, s.data());
    }
    if(t.has_raw_data())
    {
        const std::string& s = t.raw_data();
        auto type            = get_type(t.data_type());
        return create_literal(type, dims, s.data());
    }

    switch(t.data_type())
    {
    case onnx::TensorProto::BOOL: return create_literal(shape::bool_type, dims, t.int32_data());
    case onnx::TensorProto::INT8: return create_literal(shape::int8_type, dims, t.int32_data());
    case onnx::TensorProto::UINT8: return create_literal(shape::uint8_type, dims, t.int32_data());
    case onnx::TensorProto::INT16: return create_literal(shape::int16_type, dims, t.int32_data());
    case onnx::TensorProto::UINT16: return create_literal(shape::uint16_type, dims, t.int32_data());
    case onnx::TensorProto::INT32: return create_literal(shape::int32_type, dims, t.int32_data());
    case onnx::TensorProto::UINT32:
        return create_literal(shape::uint32_type, dims, t.uint64_data());
    case onnx::TensorProto::INT64: return create_literal(shape::int64_type, dims, t.int64_data());
    case onnx::TensorProto::UINT64:
        return create_literal(shape::uint64_type, dims, t.uint64_data());
    case onnx::TensorProto::FLOAT16:
    {
        std::vector<uint16_t> data_uint16(t.int32_data().begin(), t.int32_data().end());
        std::vector<half> data_half;
        std::transform(data_uint16.begin(),
                       data_uint16.end(),
                       std::back_inserter(data_half),
                       [](uint16_t raw_val) { return *reinterpret_cast<half*>(&raw_val); });
        return create_literal(shape::half_type, dims, data_half);
    }
    case onnx::TensorProto::DOUBLE:
        return create_literal(shape::double_type, dims, t.double_data());
    case onnx::TensorProto::FLOAT: return create_literal(shape::float_type, dims, t.float_data());
    case onnx::TensorProto::UNDEFINED:
    case onnx::TensorProto::STRING:
    case onnx::TensorProto::COMPLEX64:
    case onnx::TensorProto::COMPLEX128: throw std::runtime_error("");
    }
    MIGRAPHX_THROW("PARSE_TENSOR: Invalid tensor type");
}
shape onnx_parser::parse_type(const onnx::TypeProto& t,
                              const std::vector<std::size_t>& input_dims) const
{
    shape::type_t shape_type = get_type(t.tensor_type().elem_type());
    if(!input_dims.empty())
    {
        return {shape_type, input_dims};
    }

    std::vector<std::size_t> dims;
    auto&& tensor_dims = t.tensor_type().shape().dim();
    std::transform(tensor_dims.begin(),
                   tensor_dims.end(),
                   std::back_inserter(dims),
                   [&](auto&& d) -> std::size_t {
                       if(d.has_dim_value())
                       {
                           if(static_cast<int>(d.dim_value()) <= 0)
                           {
                               return default_dim_value;
                           }
                           return d.dim_value();
                       }
                       else
                       {
                           return default_dim_value;
                       }
                   });

    if(dims.empty())
        return {shape_type};

    return {shape_type, dims};
}

shape::type_t get_type(int dtype)
{
    switch(dtype)
    {
    case 1: return shape::float_type;
    case 2: return shape::uint8_type;
    case 3: return shape::int8_type;
    case 4: return shape::uint16_type;
    case 5: return shape::int16_type;
    case 6: return shape::int32_type;
    case 7: return shape::int64_type;
    case 9: return shape::bool_type;
    case 10: return shape::half_type;
    case 11: return shape::double_type;
    case 12: return shape::uint32_type;
    case 13: return shape::uint64_type;
    default: { MIGRAPHX_THROW("Prototensor data type " + std::to_string(dtype) + " not supported");
    }
    }
}

} // namespace onnx
} // namespace MIGRAPHX_INLINE_NS
} // namespace migraphx
