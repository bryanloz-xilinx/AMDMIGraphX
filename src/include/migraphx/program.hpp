#ifndef MIGRAPHX_GUARD_MIGRAPHLIB_PROGRAM_HPP
#define MIGRAPHX_GUARD_MIGRAPHLIB_PROGRAM_HPP

#include <list>
#include <unordered_map>
#include <migraphx/operation.hpp>
#include <migraphx/module.hpp>
#include <migraphx/literal.hpp>
#include <migraphx/builtin.hpp>
#include <migraphx/instruction_ref.hpp>
#include <migraphx/target.hpp>
#include <migraphx/compile_options.hpp>
#include <migraphx/env.hpp>
#include <migraphx/config.hpp>
#include <algorithm>
#include <iostream>

namespace migraphx {
inline namespace MIGRAPHX_INLINE_NS {

MIGRAPHX_DECLARE_ENV_VAR(MIGRAPHX_TRACE_COMPILE)
MIGRAPHX_DECLARE_ENV_VAR(MIGRAPHX_TRACE_EVAL)

struct program_impl;

struct marker;

/**
 * @brief Stores the instruction stream
 */
struct program
{
    program();

    // move constructor
    program(program&&) noexcept;

    // copy constructor
    program(const program&);

    // copy assignment operator
    program& operator=(program);

    ~program() noexcept;

    std::vector<std::string> get_parameter_names() const;

    shape get_parameter_shape(std::string name) const;

    instruction_ref get_parameter(std::string name) const;

    std::unordered_map<std::string, shape> get_parameter_shapes() const;

    std::vector<argument> eval(parameter_map params) const;

    std::size_t size() const;

    std::vector<shape> get_output_shapes() const;

    context& get_context() const;

    instruction_ref validate() const;

    void compile(const target& t, compile_options options = compile_options{});

    bool is_compiled() const;

    void finalize();

    void
    perf_report(std::ostream& os, std::size_t n, parameter_map params, std::size_t batch = 1) const;

    void mark(const parameter_map& params, marker&& m);

    value to_value() const;
    void from_value(const value& v);

    void debug_print() const;
    void debug_print(instruction_ref ins) const;
    void print(std::unordered_map<instruction_ref, std::string>& names,
               const std::function<void(instruction_ref,
                                        std::unordered_map<instruction_ref, std::string>)>&
                   print_func) const;

    void print_graph(std::ostream& os, bool brief = false) const;
    void print_cpp(std::ostream& os) const;

    void dry_run(parameter_map params) const;

    void annotate(std::ostream& os, const std::function<void(instruction_ref)>& a) const;

    program& sort();

    friend std::ostream& operator<<(std::ostream& os, const program& p);
    friend bool operator==(const program& x, const program& y);
    friend bool operator!=(const program& x, const program& y) { return !(x == y); }

    // module related api
    module* create_module(const std::string& name);
    module* get_module(const std::string& name);
    const module* get_module(const std::string& name) const;

    module* get_main_module();
    const module* get_main_module() const;

    std::vector<const module*> get_modules() const;
    std::vector<module*> get_modules();

    void remove_module(const std::string& name);
    void remove_unused_modules();

    private:
    void assign(const program& p);
    std::unique_ptr<program_impl> impl;
};

} // namespace MIGRAPHX_INLINE_NS
} // namespace migraphx

#endif
