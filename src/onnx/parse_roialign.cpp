#include <migraphx/onnx/op_parser.hpp>
#include <migraphx/onnx/checks.hpp>
#include <migraphx/ranges.hpp>
#include <migraphx/instruction.hpp>
#include <migraphx/make_op.hpp>

namespace migraphx {
inline namespace MIGRAPHX_INLINE_NS {
namespace onnx {

struct parse_roialign : op_parser<parse_roialign>
{
    std::vector<op_desc> operators() const { return {{"RoiAlign"}}; }

    instruction_ref parse(const op_desc& /*opd*/,
                          const onnx_parser& /*parser*/,
                          onnx_parser::node_info info,
                          const std::vector<instruction_ref>& args) const
    {
        std::string coord_trans_mode = "half_pixel";
        if(contains(info.attributes, "coordinate_transformation_mode"))
        {
            coord_trans_mode = info.attributes.at("coordinate_transformation_mode").s();
        }
        if(not contains({"half_pixel", "output_half_pixel"}, coord_trans_mode))
        {
            MIGRAPHX_THROW("coordinate_transformation_mode \"" + coord_trans_mode +
                           "\": invalid value!");
        }

        std::string mode = "avg";
        if(contains(info.attributes, "mode"))
        {
            mode = info.attributes.at("mode").s();
        }

        int64_t output_height = 1;
        if(contains(info.attributes, "output_height"))
        {
            output_height = info.attributes.at("output_height").i();
        }

        int64_t output_width = 1;
        if(contains(info.attributes, "output_width"))
        {
            output_width = info.attributes.at("output_width").i();
        }

        int64_t sampling_ratio = 0;
        if(contains(info.attributes, "sampling_ratio"))
        {
            sampling_ratio = info.attributes.at("sampling_ratio").i();
        }

        float spatial_scale = 1.0f;
        if(contains(info.attributes, "spatial_scale"))
        {
            spatial_scale = info.attributes.at("spatial_scale").f();
        }

        return info.add_instruction(make_op("roialign",
                                            {{"coordinate_transformation_mode", coord_trans_mode},
                                             {"mode", mode},
                                             {"output_height", output_height},
                                             {"output_width", output_width},
                                             {"sampling_ratio", sampling_ratio},
                                             {"spatial_scale", spatial_scale}}),
                                    args);
    }
};

} // namespace onnx
} // namespace MIGRAPHX_INLINE_NS
} // namespace migraphx
