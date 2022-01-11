#include "verify_program.hpp"
#include <migraphx/program.hpp>
#include <migraphx/generate.hpp>
#include <migraphx/make_op.hpp>

struct test_nonstd_scatter_brcst : verify_program<test_nonstd_scatter_brcst>
{
    migraphx::program create_program() const
    {
        migraphx::program p;
        auto* mm = p.get_main_module();
        migraphx::shape sd{migraphx::shape::float_type, {1, 3}};
        migraphx::shape si{migraphx::shape::int32_type, {2, 3}};
        std::vector<int> vi = {1, 0, 2, 0, 2, 1};
        migraphx::shape su{migraphx::shape::float_type, {2, 3}};

        auto pd = mm->add_parameter("data", sd);
        auto pd_brcst =
            mm->add_instruction(migraphx::make_op("multibroadcast", {{"out_lens", {3, 3}}}), pd);
        auto li = mm->add_literal(migraphx::literal{si, vi});
        auto pu = mm->add_parameter("update", su);
        auto r = mm->add_instruction(migraphx::make_op("scatter", {{"axis", 1}}), pd_brcst, li, pu);
        mm->add_return({r});
        return p;
    }
};
