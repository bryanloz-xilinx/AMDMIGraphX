#include <migraphx/dead_code_elimination.hpp>
#include <migraphx/program.hpp>
#include <migraphx/instruction.hpp>
#include <migraphx/iterator_for.hpp>
#include <migraphx/functional.hpp>
#include <migraphx/ranges.hpp>
#include <unordered_set>

namespace migraphx {
inline namespace MIGRAPHX_INLINE_NS {

template <class Range, class Iterator>
std::ptrdiff_t bidistance(const Range& r, Iterator start, Iterator last)
{
    auto start_forward   = start;
    auto start_backwards = start;
    std::size_t n        = 0;
    while(start_forward != last and start_backwards != last)
    {
        n++;
        if(start_forward != r.end())
            start_forward++;
        if(start_backwards != r.begin())
            start_backwards--;
    }
    if(start_forward == last)
        return n;
    else
        return -n;
}

void dead_code_elimination::apply(program& p) const { p.remove_unused_modules(); }

void dead_code_elimination::apply(module& m) const
{
    auto last = std::prev(m.end());
    for(auto ins : iterator_for(m))
    {
        // Skip the first instruction, since we always process the previous
        // instruction
        if(ins == m.begin())
            continue;
        const auto i = std::prev(ins);
        // Skip the last instruction
        if(i == last)
            break;
        // Skip instruction with empty shape as output unless its a builtin or undefined or identity
        if(i->get_shape().elements() == 0 and i->name().front() != '@' and
           i->name() != "undefined" and i->name() != "identity")
            continue;
        assert(bidistance(m, i, last) > 0);
        fix([&](auto self, auto leaf) {
            if(not m.has_instruction(leaf))
                return;

            if(leaf->outputs().empty())
            {
                std::unordered_set<instruction_ref> args(leaf->inputs().begin(),
                                                         leaf->inputs().end());
                leaf->clear_arguments();
                assert(bidistance(m, last, leaf) < 0);
                assert(leaf != ins);
                if(leaf->name() != "@param")
                    m.move_instruction(leaf, m.end());
                for(auto arg : args)
                    self(arg);
            }
        })(i);
    }
    m.remove_instructions(std::next(last), m.end());
}

} // namespace MIGRAPHX_INLINE_NS
} // namespace migraphx
