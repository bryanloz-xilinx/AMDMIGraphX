#ifndef MIGRAPHX_GUARD_RTGLIB_MATCHER_HPP
#define MIGRAPHX_GUARD_RTGLIB_MATCHER_HPP

#include <migraphx/functional.hpp>
#include <migraphx/ranges.hpp>
#include <migraphx/instruction.hpp>
#include <migraphx/module.hpp>
#include <migraphx/optional.hpp>
#include <migraphx/iterator_for.hpp>
#include <migraphx/type_name.hpp>
#include <migraphx/config.hpp>
#include <unordered_map>
#include <unordered_set>

namespace migraphx {
inline namespace MIGRAPHX_INLINE_NS {

namespace match {

struct matcher_context
{
    matcher_context(module& m) : mod(&m) {}
    std::unordered_map<std::string, instruction_ref> instructions;

    template <class M>
    bool matched(M m, instruction_ref ins)
    {
        return has_value(m.match(*this, ins));
    }

    template <class M>
    bool matched(M m, optional<instruction_ref> ins)
    {
        if(ins)
            return has_value(m.match(*this, *ins));
        return false;
    }

    template <class M, class I>
    auto lazy_match(M m, I ins)
    {
        return [=] { return this->matched(m, ins); };
    }

    bool has_instruction(instruction_ref ins) const
    {
        if(mod == nullptr)
            return true;
        return mod->has_instruction(ins);
    }
    bool has_instruction(optional<instruction_ref> ins) const
    {
        if(ins)
            return this->has_instruction(*ins);
        return false;
    }

    bool is_last(instruction_ref ins) const
    {
        assert(mod->begin() != mod->end());
        assert(this->has_instruction(ins));
        return ins == std::prev(mod->end());
    }

    private:
    module* mod = nullptr;
};

/// Convert a predicate function into a matcher
template <class P>
struct predicate_matcher
{
    P p;

    optional<instruction_ref> match(const matcher_context&, instruction_ref ins) const
    {
        if(p(ins))
            return optional<instruction_ref>{ins};
        return nullopt;
    }
};

/// Convert a function into a matcher
template <class F>
struct function_matcher
{
    F f;

    auto match(matcher_context& ctx, instruction_ref ins) const { return f(ctx, ins); }
};

/// Convert a function into a matcher
template <class F>
function_matcher<F> make_function_matcher(F f)
{
    return {f};
}

/// Converts a matcher to bind the instruction to name
template <class M>
auto bind_match(M m, std::string name)
{
    return make_function_matcher(
        [ =, name = std::move(name) ](matcher_context & ctx, instruction_ref ins)
            ->optional<instruction_ref> {
                auto result = m.match(ctx, ins);
                if(result)
                {
                    if(not ctx.has_instruction(ins))
                        return nullopt;
                    ctx.instructions[name] = ins;
                }
                return result;
            });
}

/// Convert a matcher to a bindable matcher
template <class M>
struct bindable_matcher
{
    M m;

    auto bind(std::string name) const { return bind_match(m, std::move(name)); }

    auto match(matcher_context& ctx, instruction_ref ins) const { return m.match(ctx, ins); }
};

/// Create a bindable matcher
template <class M>
bindable_matcher<M> make_bindable_matcher(M m)
{
    return {m};
}

/// Create a bindable matcher from a function
template <class F>
bindable_matcher<function_matcher<F>> make_bf_matcher(F f)
{
    return {{f}};
}

/// Create a bindable matcher from a predicate function
template <class F>
bindable_matcher<predicate_matcher<F>> make_bp_matcher(F f)
{
    return {{f}};
}

using bool_list = std::initializer_list<bool>;

struct id_matcher
{
    auto match(matcher_context&, instruction_ref ins) const
    {
        return optional<instruction_ref>{ins};
    }
};

/// The basic matcher provides the all_of composability of the matcher
template <class M>
struct basic_matcher
{
    M m;

    template <class... Ts>
    auto operator()(Ts... ms) const
    {
        // Copy m because we cant capture `this` by value
        auto mm = m;
        return make_bf_matcher([=](matcher_context& ctx,
                                   instruction_ref ins) -> optional<instruction_ref> {
            auto result = mm.match(ctx, ins);
            if(result)
            {
                bool matches =
                    fold([&](auto x, auto y) { return x and ctx.matched(y, result); })(true, ms...);
                if(matches)
                    return result;
            }
            return nullopt;
        });
    }

    auto bind(std::string name) const { return bind_match(m, std::move(name)); }

    auto match(matcher_context& ctx, instruction_ref ins) const { return m.match(ctx, ins); }
};

/// Create a basic matcher from a matcher
template <class M>
basic_matcher<M> make_basic_matcher(M m)
{
    return {m};
}

/// Create a basic matcher from a function
template <class F>
basic_matcher<function_matcher<F>> make_basic_fun_matcher(F f)
{
    return {{f}};
}

/// Create a basic matcher from a predicate function
template <class P>
basic_matcher<predicate_matcher<P>> make_basic_pred_matcher(P p)
{
    return {{p}};
}

/// Create a typed-erased matcher
using any_matcher_base = basic_matcher<
    function_matcher<std::function<optional<instruction_ref>(matcher_context&, instruction_ref)>>>;
struct any_matcher : any_matcher_base
{
    template <class M>
    any_matcher(M mm) : any_matcher_base({[=](auto& ctx, auto ins) { return mm.match(ctx, ins); }})
    {
    }
};

/// This macro takes care of the boilerplate for defining a matcher
#define MIGRAPHX_BASIC_MATCHER(name, ...)                                     \
    struct name##_m                                                           \
    {                                                                         \
        optional<instruction_ref> match(__VA_ARGS__) const;                   \
    };                                                                        \
    const constexpr auto name = migraphx::match::basic_matcher<name##_m>{{}}; \
    inline optional<instruction_ref> name##_m::match(__VA_ARGS__) const

/// This macro takes care of the boilerplate for defining a predicate matcher
#define MIGRAPHX_PRED_MATCHER(name, ...)                                                  \
    struct name##_m                                                                       \
    {                                                                                     \
        bool operator()(__VA_ARGS__) const;                                               \
    };                                                                                    \
    const constexpr auto name =                                                           \
        migraphx::match::basic_matcher<migraphx::match::predicate_matcher<name##_m>>{{}}; \
    inline bool name##_m::operator()(__VA_ARGS__) const

struct matcher_result
{
    std::unordered_map<std::string, instruction_ref> instructions;
    instruction_ref result;
};

/// Match a single instruction
template <class M>
matcher_result match_instruction(module& mod, instruction_ref ins, M&& m)
{
    assert(ins != mod.end());
    assert(mod.has_instruction(ins));
    matcher_context ctx{mod};
    matcher_result result;
    if(m.match(ctx, ins))
    {
        result.result       = ins;
        result.instructions = ctx.instructions;
    }
    else
    {
        result.result = mod.end();
    }
    return result;
}

/// Find first instance of a matching instruction in a module
template <class M>
match::matcher_result find_match(module& modl, M&& m)
{
    match::matcher_result result;
    for(auto ins : iterator_for(modl))
    {
        result = match::match_instruction(modl, ins, m);
        if(result.result != modl.end())
            return result;
    }
    return result;
}

MIGRAPHX_DECLARE_ENV_VAR(MIGRAPHX_TRACE_MATCHES)

/// Find matches for an instruction in the module
template <class... Ms>
void find_matches(module& mod, instruction_ref ins, Ms&&... ms)
{
#if !defined(__GNUC__) || defined(__clang__) || __GNUC__ > 5
    const
#endif
        bool trace = enabled(MIGRAPHX_TRACE_MATCHES{});
    bool match     = false;
    each_args(
        [&](auto&& m) {
            if(match)
                return;
            auto r = match_instruction(mod, ins, m.matcher());
            if(r.result == mod.end())
                return;
            if(trace)
            {
                std::cout << "Matched by " << get_type_name(m) << std::endl;
                mod.debug_print(ins);
            }
            m.apply(mod, r);
            match = true;
        },
        ms...);
}

/// Find matches in a module
template <class... Ms>
void find_matches(module& mod, Ms&&... ms)
{
    for(auto ins : iterator_for(mod))
    {
        find_matches(mod, ins, ms...);
    }
}

template <class M, class F>
struct find_generic_match
{
    M m;
    F f;
    M matcher() const { return m; }

    void apply(module& mod, const matcher_result& mr) const { f(mod, mr); }
};

template <class M, class F>
find_generic_match<M, F> make_match_finder(M m, F f)
{
    return {m, f};
}

template <class M>
struct find_skip
{
    M m;
    M matcher() const { return m; }

    void apply(module&, const matcher_result&) const {}
};

template <class M>
find_skip<M> make_find_skip(M m)
{
    return {m};
}

struct lazy_and
{
    template <class F, class G>
    auto operator()(F f, G g) const
    {
        return [=] { return f() and g(); };
    }
};

struct lazy_or
{
    template <class F, class G>
    auto operator()(F f, G g) const
    {
        return [=] { return f() or g(); };
    }
};

template <class Op, bool Start, bool Matches>
struct match_fold_f
{
    template <class... Ms>
    static bool fold_matchers(matcher_context& ctx, instruction_ref ins, Ms... ms)
    {
        Op op;
        auto matched = [&](auto m) { return [=, &ctx] { return ctx.matched(m, ins); }; };
        return fold(op)(always(Start), matched(ms)...)();
    }

    template <class Pack>
    static bool fold_matchers_pack(matcher_context& ctx, instruction_ref ins, Pack p)
    {
        return p([&](auto... ms) { return match_fold_f::fold_matchers(ctx, ins, ms...); });
    }

    template <class... Ts>
    auto operator()(Ts... ms) const
    {
        return make_bf_matcher(
            [=](matcher_context& ctx, instruction_ref ins) -> optional<instruction_ref> {
                bool matches = match_fold_f::fold_matchers(ctx, ins, ms...);
                if(matches == Matches)
                    return {ins};
                return nullopt;
            });
    }

    template <class Selector>
    auto operator[](Selector select) const
    {
        return [=](auto... ms) {
            // Workaround ICE on gcc by packing matchers into an object
            auto mpack = pack(ms...);
            return make_bf_matcher(
                [=](matcher_context& ctx, instruction_ref start) -> optional<instruction_ref> {
                    Op op;
                    bool matches = Start;
                    select(start, [&](auto ins) {
                        auto fm = [&] { return match_fold_f::fold_matchers_pack(ctx, ins, mpack); };
                        matches = op(always(matches), fm)();
                    });
                    if(matches == Matches)
                        return {start};
                    return nullopt;
                });
        };
    }
};

const constexpr auto all_of  = match_fold_f<lazy_and, true, true>{};
const constexpr auto any_of  = match_fold_f<lazy_or, false, true>{};
const constexpr auto none_of = match_fold_f<lazy_or, false, false>{};

template <class... Ms>
auto skip_matches(Ms... ms)
{
    return make_find_skip(any_of(ms...));
}

inline auto inputs()
{
    return [](auto ins, auto f) {
        for(auto&& x : ins->inputs())
            f(x);
    };
}

inline auto outputs()
{
    return [](auto ins, auto f) {
        for(auto&& x : ins->outputs())
            f(x);
    };
}

MIGRAPHX_PRED_MATCHER(any, instruction_ref) { return true; }
MIGRAPHX_PRED_MATCHER(none, instruction_ref) { return false; }
MIGRAPHX_PRED_MATCHER(standard_shape, instruction_ref ins) { return ins->get_shape().standard(); }
MIGRAPHX_PRED_MATCHER(not_standard_shape, instruction_ref ins)
{
    return not ins->get_shape().standard();
}
MIGRAPHX_PRED_MATCHER(broadcast_shape, instruction_ref ins)
{
    return ins->get_shape().broadcasted();
}

MIGRAPHX_PRED_MATCHER(transpose_shape, instruction_ref ins)
{
    return ins->get_shape().transposed();
}

MIGRAPHX_PRED_MATCHER(same_input_shapes, instruction_ref ins)
{
    if(ins->inputs().empty())
        return false;
    auto s = ins->inputs().front()->get_shape();
    return std::all_of(
        ins->inputs().begin(), ins->inputs().end(), [&](auto x) { return x->get_shape() == s; });
}

MIGRAPHX_BASIC_MATCHER(output, const matcher_context&, instruction_ref ins)
{
    if(ins->outputs().size() == 1)
        return {ins->outputs().front()};
    return nullopt;
}

MIGRAPHX_BASIC_MATCHER(used_once, const matcher_context& ctx, instruction_ref ins)
{
    if(ins->outputs().size() == 1)
        return {ins};
    if(ins->outputs().empty() and ctx.is_last(ins))
        return {ins};
    return nullopt;
}

MIGRAPHX_PRED_MATCHER(is_constant, instruction_ref ins) { return ins->can_eval(); }

MIGRAPHX_BASIC_MATCHER(is_unused, const matcher_context& ctx, instruction_ref ins)
{
    if(ins->outputs().empty() and not ctx.is_last(ins))
        return {ins};
    return nullopt;
}

template <class... Ms>
auto skip(Ms... ms)
{
    auto m = any_of(ms...);
    return make_basic_fun_matcher([=](matcher_context& ctx, instruction_ref start) {
        return fix<optional<instruction_ref>>(
            [&](auto self, auto ins) -> optional<instruction_ref> {
                if(ins->inputs().size() == 1 and ctx.matched(m, ins))
                {
                    auto next = ins->inputs().front();
                    return self(next);
                }
                return ins;
            })(start);
    });
}

template <class... Ms>
auto skip_output(Ms... ms)
{
    auto m = any_of(ms...);
    return make_basic_fun_matcher([=](matcher_context& ctx, instruction_ref start) {
        return fix<optional<instruction_ref>>(
            [&](auto self, auto ins) -> optional<instruction_ref> {
                if(ins->outputs().size() == 1)
                {
                    auto next = ins->outputs().front();
                    if(ctx.matched(m, next))
                    {
                        auto skipped_next = self(next);
                        if(skipped_next)
                            return skipped_next;
                    }
                    return next;
                }
                return nullopt;
            })(start);
    });
}

inline auto name(std::string s)
{
    return make_basic_pred_matcher(
        [ =, s = std::move(s) ](instruction_ref ins) { return ins->name() == s; });
}

inline auto name_contains(const std::string& name)
{
    return make_basic_pred_matcher(
        [=](instruction_ref ins) { return contains(ins->get_operator().name(), name); });
}

inline auto name(std::unordered_set<std::string> names)
{
    return make_basic_pred_matcher([ =, names = std::move(names) ](instruction_ref ins) {
        return names.count(ins->name()) > 0;
    });
}

template <class... Ts>
inline auto name(std::string s, Ts... xs) // NOLINT
{
    return name(std::unordered_set<std::string>{std::move(s), std::move(xs)...});
}

inline auto nargs(std::size_t n)
{
    return make_basic_pred_matcher([=](instruction_ref ins) { return ins->inputs().size() == n; });
}

inline auto arg(std::size_t i)
{
    return make_basic_fun_matcher(
        [=](const matcher_context&, instruction_ref ins) -> optional<instruction_ref> {
            if(i < ins->inputs().size())
                return ins->inputs()[i];
            return nullopt;
        });
}

// Workaround for bugs in clang
template <std::size_t...>
struct args_impl_ints
{
};

template <std::size_t... Ns, class... Ms>
auto args_impl(args_impl_ints<Ns...>, Ms... ms)
{
    return match::all_of(nargs(sizeof...(Ns)), arg(Ns)(ms)...);
}

template <class... Ms>
auto args(Ms... ms)
{
    return sequence_c<sizeof...(Ms)>([=](auto... is) {
        // It needs to be written as `decltype(is)::value` for gcc 5
        return args_impl(args_impl_ints<decltype(is)::value...>{}, ms...);
    });
}

inline auto either_arg(std::size_t i, std::size_t j)
{
    return [=](auto m1, auto m2) {
        return match::any_of(match::all_of(arg(i)(m1), arg(j)(m2)),
                             match::all_of(arg(j)(m1), arg(i)(m2)));
    };
}

inline auto any_arg(std::size_t i, std::size_t j)
{
    return [=](auto m) { return match::any_of(arg(i)(m), arg(j)(m)); };
}

template <std::size_t N, class M>
std::size_t tree_leafs_impl(matcher_context& ctx,
                            std::array<instruction_ref, N>& leafs,
                            M m,
                            instruction_ref ins)
{
    std::size_t idx = 0;
    fix([&](auto self, auto i) {
        if(idx == leafs.size())
            return;
        if(ctx.matched(m, i) and i->inputs().size() >= 2)
        {
            self(i->inputs()[0]);
            self(i->inputs()[1]);
            return;
        }
        leafs[idx] = i;
        idx++;
    })(ins);
    return idx;
}

template <class M, class... Ms>
auto tree(M main_op, Ms... ms)
{
    return make_basic_fun_matcher(
        [=](matcher_context& ctx, instruction_ref ins) -> optional<instruction_ref> {
            // Flatten leaf nodes
            std::array<instruction_ref, sizeof...(Ms)> leafs;
            std::size_t idx = tree_leafs_impl(ctx, leafs, main_op, ins);
            if(idx != leafs.size())
                return nullopt;
            // Use explicit captures to workaround ICE on gcc
            // Capture by value to workaround compile error on gcc 9
            bool found = sequence_c<sizeof...(Ms)>([ms..., &ctx, &leafs](auto... is) {
                return fold(lazy_and{})(ctx.lazy_match(ms, leafs[is])...)();
            });
            if(not found)
                return nullopt;
            return ins;
        });
}

template <class M, class... Ms>
auto unordered_tree(M main_op, Ms... ms)
{
    return make_basic_fun_matcher(
        [=](matcher_context& ctx, instruction_ref ins) -> optional<instruction_ref> {
            // Flatten leaf nodes
            std::array<instruction_ref, sizeof...(Ms)> leafs;
            std::size_t idx = tree_leafs_impl(ctx, leafs, main_op, ins);
            if(idx != leafs.size())
                return nullopt;
            // Use explicit captures to workaround ICE on gcc
            bool found = sequence_c<sizeof...(Ms)>([ms..., &ctx, &leafs](auto... is) {
                return by(fold(lazy_and{}), [is..., &ctx, &leafs](auto m) {
                    return fold(lazy_or{})(ctx.lazy_match(m, leafs[is])...);
                })(ms...)();
            });
            if(not found)
                return nullopt;
            return ins;
        });
}

template <class M>
auto same_shape(M m)
{
    return make_basic_fun_matcher(
        [=](matcher_context& ctx, instruction_ref ins) -> optional<instruction_ref> {
            auto i = m.match(ctx, ins);
            if(i and (*i)->get_shape() == ins->get_shape())
                return ins;
            return nullopt;
        });
}

template <class... Ms>
auto same_shape(Ms... ms)
{
    return all_of(same_shape(ms)...);
}

template <class... Ms>
auto skip_broadcasts(Ms... ms)
{
    return skip(name("broadcast", "multibroadcast", "contiguous"))(ms...);
}

template <class T>
inline auto has_value(T x, float tolerance = 1e-6)
{
    return skip_broadcasts(make_basic_pred_matcher([=](instruction_ref ins) {
        if(ins->name() != "@literal")
            return false;
        auto l = ins->get_literal();
        if(l.empty())
            return false;
        bool b = false;
        l.visit([&](auto v) {
            if(std::all_of(
                   v.begin(), v.end(), [&](auto val) { return std::fabs(val - x) < tolerance; }))
                b = true;
        });
        return b;
    }));
}

inline auto has_attribute(const std::string& name)
{
    return make_basic_pred_matcher(
        [=](instruction_ref ins) { return ins->get_operator().attributes().contains(name); });
}

template <class... Ms>
auto pointwise(Ms... ms)
{
    return match::has_attribute("pointwise")(match::any_of(match::nargs(1), match::nargs(2)),
                                             ms...);
}

} // namespace match
} // namespace MIGRAPHX_INLINE_NS
} // namespace migraphx

#endif
