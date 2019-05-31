#ifndef MIGRAPHX_GUARD_RTGLIB_VALUE_NUMBERING_HPP
#define MIGRAPHX_GUARD_RTGLIB_VALUE_NUMBERING_HPP
#include <migraphx/program.hpp>
#include <migraphx/stringutils.hpp>
#include <migraphx/instruction.hpp>
#include <migraphx/operators.hpp>
#include <migraphx/iterator_for.hpp>
#include <migraphx/config.hpp>

#include <set>
#include <stack>
#include <vector>

namespace migraphx {

inline namespace MIGRAPHX_INLINE_NS {

//#define MIGRAPHX_DEBUG_OPT

#ifdef MIGRAPHX_DEBUG_OPT
#define MIGRAPHX_DEBUG(s) s
#else
#define MIGRAPHX_DEBUG(s)
#endif // MIGRAPHX_DEBUG_OPT

// Nodes representing hashed instructions.
struct hash_value
{
    unsigned id   = 0;
    int cur_point = 0;
};

using hash_value_ptr = hash_value*;
using key_type       = unsigned long long;

//  Instruction encoding information, used to hash instructions.
struct encode_info
{
    key_type key;
    bool valid;
    encode_info(key_type k, bool v) : key(k), valid(v) {}

    void add_input(hash_value_ptr p) { inputs.push_back(p); }
    key_type get_key() const { return key; }
    void set_key(key_type k) { key = k; }
    const std::vector<hash_value_ptr>& get_inputs() const { return inputs; }
    bool is_valid() const { return valid; }

    private:
    std::vector<hash_value_ptr> inputs;
};

using ins2_val    = std::unordered_map<instruction_ref, hash_value_ptr>;
using string2_val = std::unordered_map<std::string, unsigned>;

using encoder = std::function<encode_info(instruction_ref, ins2_val&, unsigned)>;

struct value_numbering
{
    value_numbering(program* p) : p_program(p)
    {
        instr2_hash.clear();
        instr2_value.clear();
        point2_instr.clear();
        encode2_value.clear();
        cur_point = 0;
        opcode_id = 0;
        hash_inputs.clear();
        hash_outputs.clear();
        hash_instrs.clear();
        values.reserve(p_program->size());
        opcode_table.clear();
        op_registry = get_op_registery();
    }

    void run();
    void process(instruction_ref ins);
    hash_value_ptr hash(instruction_ref ins);
    hash_value& get_value(unsigned id) { return values[id]; }

    hash_value& create_value(instruction_ref ins);

    void add_instr(unsigned id) { hash_instrs[id].insert(cur_point); }

    void add_input(unsigned id, hash_value_ptr ptr) { hash_inputs[id].insert(ptr); }

    void add_output(unsigned id, hash_value_ptr ptr) { hash_outputs[id].insert(ptr); }
    unsigned hash_opcode(instruction_ref ins)
    {
        std::ostringstream stream;
        stream << ins->get_operator();
        std::string str = stream.str();
        if(opcode_table.find(str) == opcode_table.end())
            opcode_table[str] = opcode_id++;
        return opcode_table[str];
    }

    std::vector<instruction_ref> get_instrs(unsigned hash_id)
    {
        assert(hash_instrs.find(hash_id) != hash_instrs.end());
        std::vector<instruction_ref> instrs;
        for(auto&& point : hash_instrs[hash_id])
        {
            assert(point2_instr.find(point) != point2_instr.end());
            instrs.push_back(point2_instr[point]);
        }
        return instrs;
    }

    void update_hash_tree(unsigned hash_id);
    static const std::unordered_map<std::string, encoder>& get_op_registery();

#ifdef MIGRAPHX_DEBUG_OPT
    void dump_program();
    void dump_hash_value(hash_value&);
    void dump_hash_tree();
#endif
    // Map an operation name to its encoder function.
    std::unordered_map<std::string, encoder> op_registry;
    // Flag an instruction to hash.
    std::unordered_map<instruction_ref, bool> instr2_hash;
    // Map an instruction to a hash value pointer.
    ins2_val instr2_value;
    std::unordered_map<unsigned, instruction_ref> point2_instr;
    // Map an encoding to a hash value pointer.
    std::unordered_map<key_type, hash_value_ptr> encode2_value;
    // Map an opcode string to a value.
    string2_val opcode_table;
    // Universe of hash values.
    std::vector<hash_value> values;
    // Map of hash value id to hash-value inputs.
    std::unordered_map<unsigned, std::set<hash_value_ptr>> hash_inputs;
    // Map of hash value id to hash-value outputs.
    std::unordered_map<unsigned, std::set<hash_value_ptr>> hash_outputs;
    // Map of hash value id to instructions having the same hash value.
    std::unordered_map<unsigned, std::set<unsigned>> hash_instrs;
    // Current program point.
    int cur_point;
    // Opcode id.
    unsigned opcode_id;

    private:
    program* p_program;
};

// Encoding functions.
encode_info encode_common(instruction_ref ins, ins2_val& instr2_value, unsigned);
encode_info encode_conv_common(instruction_ref ins, ins2_val& instr2_value, unsigned);
} // namespace MIGRAPHX_INLINE_NS
} // namespace migraphx
#endif
