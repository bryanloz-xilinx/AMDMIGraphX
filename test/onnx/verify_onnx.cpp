#include <iostream>
#include <vector>
#include <migraphx/literal.hpp>
#include <migraphx/operators.hpp>
#include <migraphx/program.hpp>
#include <migraphx/ref/target.hpp>
#include <migraphx/pass_manager.hpp>
#include <migraphx/verify.hpp>
#include <migraphx/onnx.hpp>
#include "test.hpp"

TEST_CASE(averagepool_notset_test)
{
    auto p = migraphx::parse_onnx("averagepool_notset_test.onnx");
    p.compile(migraphx::ref::target{});
    std::vector<float> data_x = {0,  1,  2,  3,  4,  5,  6,  7,  8,  9,  10, 11, 12,
                                 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24};
    migraphx::shape s_x{migraphx::shape::float_type, {1, 1, 5, 5}};
    migraphx::parameter_map pp;
    pp["x"] = migraphx::argument(s_x, data_x.data());

    auto result = p.eval(pp).back();
    std::vector<float> result_vector;
    result.visit([&](auto output) { result_vector.assign(output.begin(), output.end()); });

    std::vector<float> gold = {12};
    EXPECT(migraphx::verify_range(result_vector, gold));
}

TEST_CASE(averagepool_nt_cip_test)
{
    auto p = migraphx::parse_onnx("averagepool_nt_cip_test.onnx");
    p.compile(migraphx::ref::target{});
    std::vector<float> data_x = {0,  1,  2,  3,  4,  5,  6,  7,  8,  9,  10, 11, 12,
                                 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24};
    migraphx::shape s_x{migraphx::shape::float_type, {1, 1, 5, 5}};
    migraphx::parameter_map pp;
    pp["x"] = migraphx::argument(s_x, data_x.data());

    auto result = p.eval(pp).back();
    std::vector<float> result_vector;
    result.visit([&](auto output) { result_vector.assign(output.begin(), output.end()); });

    std::vector<float> gold = {8.33333};
    EXPECT(migraphx::verify_range(result_vector, gold));
}

TEST_CASE(depthtospace_simple_test)
{
    auto p = migraphx::parse_onnx("depthtospace_simple_test.onnx");
    p.compile(migraphx::ref::target{});
    std::vector<float> data_in(48);
    std::iota(std::begin(data_in), std::end(data_in), 0);
    migraphx::shape s_x{migraphx::shape::float_type, {1, 8, 2, 3}};
    migraphx::parameter_map pp;
    pp["x"]     = migraphx::argument(s_x, data_in.data());
    auto result = p.eval(pp).back();
    std::vector<float> result_vector;
    result.visit([&](auto output) { result_vector.assign(output.begin(), output.end()); });
    std::vector<float> gold = {0,  12, 1,  13, 2,  14, 24, 36, 25, 37, 26, 38, 3,  15, 4,  16,
                               5,  17, 27, 39, 28, 40, 29, 41, 6,  18, 7,  19, 8,  20, 30, 42,
                               31, 43, 32, 44, 9,  21, 10, 22, 11, 23, 33, 45, 34, 46, 35, 47};
    EXPECT(migraphx::verify_range(result_vector, gold));
}

TEST_CASE(spacetodepth_simple_test)
{
    auto p = migraphx::parse_onnx("spacetodepth_simple_test.onnx");
    p.compile(migraphx::ref::target{});
    std::vector<float> data_in(48);
    std::iota(std::begin(data_in), std::end(data_in), 0);
    migraphx::shape s_x{migraphx::shape::float_type, {1, 2, 4, 6}};
    migraphx::parameter_map pp;
    pp["x"]     = migraphx::argument(s_x, data_in.data());
    auto result = p.eval(pp).back();
    std::vector<float> result_vector;
    result.visit([&](auto output) { result_vector.assign(output.begin(), output.end()); });
    std::vector<float> gold = {0,  2,  4,  12, 14, 16, 24, 26, 28, 36, 38, 40, 1,  3,  5,  13,
                               15, 17, 25, 27, 29, 37, 39, 41, 6,  8,  10, 18, 20, 22, 30, 32,
                               34, 42, 44, 46, 7,  9,  11, 19, 21, 23, 31, 33, 35, 43, 45, 47};
    EXPECT(migraphx::verify_range(result_vector, gold));
}

TEST_CASE(spacetodepth_depthtospace_test)
{
    // space to depth
    auto p1 = migraphx::parse_onnx("spacetodepth_simple_test.onnx");
    p1.compile(migraphx::ref::target{});
    std::vector<float> data_in(48);
    std::iota(std::begin(data_in), std::end(data_in), 0);
    migraphx::shape s_x_1{migraphx::shape::float_type, {1, 2, 4, 6}};
    migraphx::parameter_map pp1;
    pp1["x"]     = migraphx::argument(s_x_1, data_in.data());
    auto result1 = p1.eval(pp1).back();
    // depth to space
    auto p2 = migraphx::parse_onnx("depthtospace_simple_test.onnx");
    p2.compile(migraphx::ref::target{});
    migraphx::parameter_map pp2;
    pp2["x"]     = result1;
    auto result2 = p2.eval(pp2).back();
    std::vector<float> result_vector2;
    result2.visit([&](auto output) { result_vector2.assign(output.begin(), output.end()); });
    EXPECT(migraphx::verify_range(result_vector2, data_in));
}

TEST_CASE(gather_elements)
{
    migraphx::program p = migraphx::parse_onnx("gather_elements_axis0_test.onnx");
    p.compile(migraphx::ref::target{});
    migraphx::shape s_data{migraphx::shape::float_type, {3, 4}};
    std::vector<float> data = {
        0.25, 0.75, 0.9375, 0.4375, 0.6875, 0.5625, -0.875, 0.1875, -0.125, 0.5, -0.9375, -0.0625};

    migraphx::shape s_ind{migraphx::shape::int32_type, {2, 3}};
    std::vector<int> ind = {2, 1, 2, 0, 1, 0};

    migraphx::parameter_map pp;
    pp["data"]    = migraphx::argument(s_data, data.data());
    pp["indices"] = migraphx::argument(s_ind, ind.data());

    auto result = p.eval(pp).back();
    std::vector<float> result_vector;
    result.visit([&](auto output) { result_vector.assign(output.begin(), output.end()); });

    std::vector<float> gold = {-0.125, 0.5625, -0.9375, 0.25, 0.5625, 0.9375};
    EXPECT(migraphx::verify_range(result_vector, gold));
}

TEST_CASE(greaterorequal_test)
{
    migraphx::program p = migraphx::parse_onnx("greaterorequal_test.onnx");
    p.compile(migraphx::ref::target{});

    migraphx::shape s{migraphx::shape::float_type, {3}};
    std::vector<float> data1 = {0.25, 0.75, 0.9375};
    std::vector<float> data2 = {0.25, 0.74, 0.9411};

    migraphx::parameter_map pp;
    pp["x1"] = migraphx::argument(s, data1.data());
    pp["x2"] = migraphx::argument(s, data2.data());

    auto result = p.eval(pp).back();
    std::vector<float> result_vector;
    result.visit([&](auto output) { result_vector.assign(output.begin(), output.end()); });

    std::vector<float> gold = {1.0, 1.0, 0.0};
    EXPECT(migraphx::verify_range(result_vector, gold));
}

TEST_CASE(hardsigmoid_verify_test)
{
    migraphx::program p = migraphx::parse_onnx("hardsigmoid_verify_test.onnx");
    p.compile(migraphx::ref::target{});

    migraphx::shape s{migraphx::shape::float_type, {2, 5}};
    std::vector<float> data = {-10.0, -2.5, -1.0, -0.5, 0, 1.0, 2.0, 2.5, 2.6, 100.0};

    float alpha = 0.2;
    float beta  = 0.5;
    migraphx::parameter_map pp;
    pp["x"] = migraphx::argument(s, data.data());

    auto result = p.eval(pp).back();
    std::vector<float> result_vector;
    result.visit([&](auto output) { result_vector.assign(output.begin(), output.end()); });

    std::vector<float> gold(10);
    std::transform(data.begin(), data.end(), gold.begin(), [&](auto x) {
        return std::max(0.0f, std::min(x * alpha + beta, 1.0f));
    });
    EXPECT(migraphx::verify_range(result_vector, gold));
}

TEST_CASE(if_else_test)
{
    migraphx::program p = migraphx::parse_onnx("if_else_test.onnx");
    p.compile(migraphx::ref::target{});
    migraphx::shape s_data{migraphx::shape::float_type, {2, 3}};
    std::vector<float> data = {0.0625, 0.75, -0.0625, 0.125, -0.125, -0.5625};

    migraphx::parameter_map pp;
    pp["x"] = migraphx::argument(s_data, data.data());
    pp["y"] = migraphx::argument(s_data, data.data());

    auto result = p.eval(pp).back();
    std::vector<float> result_vector;
    result.visit([&](auto output) { result_vector.assign(output.begin(), output.end()); });

    std::vector<float> gold = {
        -0.0364609435, 0.475317657, -0.00417715637, -0.0599277429, 0.0755792186, -0.0218581557};
    EXPECT(migraphx::verify_range(result_vector, gold));
}

TEST_CASE(if_literal_test)
{
    auto run_prog = [](bool cond) {
        migraphx::program p = migraphx::parse_onnx("if_literal_test.onnx");
        p.compile(migraphx::ref::target{});
        migraphx::shape s_data{migraphx::shape::bool_type};
        std::vector<char> data = {static_cast<char>(cond)};

        migraphx::parameter_map pp;
        pp["cond"] = migraphx::argument(s_data, data.data());

        auto result = p.eval(pp).back();
        std::vector<float> result_vector;
        result.visit([&](auto output) { result_vector.assign(output.begin(), output.end()); });

        return result_vector;
    };

    // then branch
    {
        auto result_vector      = run_prog(true);
        std::vector<float> gold = {1, 2, 3, 4, 5};
        EXPECT(migraphx::verify_range(result_vector, gold));
    }

    // else branch
    {
        auto result_vector      = run_prog(false);
        std::vector<float> gold = {5, 4, 3, 2, 1};
        EXPECT(migraphx::verify_range(result_vector, gold));
    }
}

TEST_CASE(if_pl_test)
{
    auto run_prog = [](bool cond) {
        migraphx::program p = migraphx::parse_onnx("if_pl_test.onnx");
        p.compile(migraphx::ref::target{});
        migraphx::shape xs{migraphx::shape::float_type, {2, 3}};
        migraphx::shape ys{migraphx::shape::float_type, {3, 3}};
        migraphx::shape cond_s{migraphx::shape::bool_type};

        std::vector<float> x_data(xs.elements(), 1.0f);
        std::vector<float> y_data(ys.elements(), 2.0f);
        std::vector<char> cond_data{static_cast<char>(cond)};

        migraphx::parameter_map pp;
        pp["x"]    = migraphx::argument(xs, x_data.data());
        pp["y"]    = migraphx::argument(ys, y_data.data());
        pp["cond"] = migraphx::argument(cond_s, cond_data.data());

        auto result = p.eval(pp).back();
        std::vector<float> ret;
        result.visit([&](auto output) { ret.assign(output.begin(), output.end()); });

        return ret;
    };

    // then branch
    {
        auto result_vector      = run_prog(true);
        std::vector<float> gold = {2, 3, 4, 5, 6, 7};
        EXPECT(migraphx::verify_range(result_vector, gold));
    }

    // else branch
    {
        auto result_vector      = run_prog(false);
        std::vector<float> gold = {1, 2, 3, 4, 5, 6};
        EXPECT(migraphx::verify_range(result_vector, gold));
    }
}

TEST_CASE(if_tuple_test)
{
    auto run_prog = [](bool cond) {
        migraphx::program p = migraphx::parse_onnx("if_tuple_test.onnx");
        p.compile(migraphx::ref::target{});
        migraphx::shape xs{migraphx::shape::float_type, {1, 4}};
        migraphx::shape ys{migraphx::shape::float_type, {3, 4}};
        migraphx::shape cond_s{migraphx::shape::bool_type};

        std::vector<float> x_data(xs.elements(), 1.0f);
        std::vector<float> y_data(ys.elements(), 2.0f);
        std::vector<char> cond_data{static_cast<char>(cond)};

        migraphx::parameter_map pp;
        pp["x"]    = migraphx::argument(xs, x_data.data());
        pp["y"]    = migraphx::argument(ys, y_data.data());
        pp["cond"] = migraphx::argument(cond_s, cond_data.data());

        auto results = p.eval(pp);
        std::vector<std::vector<float>> rets;
        for(const auto& arg : results)
        {
            std::vector<float> vec;
            arg.visit([&](auto output) { vec.assign(output.begin(), output.end()); });
            rets.push_back(vec);
        }

        return rets;
    };

    // then branch
    {
        auto results = run_prog(true);
        std::vector<float> gold0(4, 2.0f);
        std::vector<float> gold1(12, 4.0f);
        EXPECT(migraphx::verify_range(results.at(0), gold0));
        EXPECT(migraphx::verify_range(results.at(1), gold1));
    }

    // else branch
    {
        auto results = run_prog(false);
        std::vector<float> gold0(4, 3.0f);
        std::vector<float> gold1(12, 5.0f);
        EXPECT(migraphx::verify_range(results.at(0), gold0));
        EXPECT(migraphx::verify_range(results.at(1), gold1));
    }
}

TEST_CASE(instance_norm_test)
{
    migraphx::program p = migraphx::parse_onnx("instance_norm_val_test.onnx");

    p.compile(migraphx::ref::target{});
    auto result = p.eval({}).back();
    std::vector<float> result_vector(9);
    result.visit([&](auto output) { result_vector.assign(output.begin(), output.end()); });

    std::vector<float> gold = {-1.54919,
                               -1.16189,
                               -0.774596,
                               -0.387298,
                               0,
                               0.387298,
                               0.774596,
                               1.16189,
                               1.54919,
                               -2.09838,
                               -1.32379,
                               -0.549192,
                               0.225404,
                               1,
                               1.7746,
                               2.54919,
                               3.32379,
                               4.09838};
    EXPECT(migraphx::verify_range(result_vector, gold));
}

TEST_CASE(instance_norm_3d_test)
{
    migraphx::program p = migraphx::parse_onnx("instance_norm_val_3d_test.onnx");

    p.compile(migraphx::ref::target{});
    auto result = p.eval({}).back();
    std::vector<float> result_vector(16);
    result.visit([&](auto output) { result_vector.assign(output.begin(), output.end()); });

    std::vector<float> gold = {-1.52752,
                               -1.09109,
                               -0.654653,
                               -0.218218,
                               0.218218,
                               0.654653,
                               1.09109,
                               1.52752,
                               -2.05505,
                               -1.18218,
                               -0.309306,
                               0.563565,
                               1.43644,
                               2.30931,
                               3.18218,
                               4.05505};

    EXPECT(migraphx::verify_range(result_vector, gold));
}

TEST_CASE(lessorequal_test)
{
    migraphx::program p = migraphx::parse_onnx("lessorequal_test.onnx");
    p.compile(migraphx::ref::target{});

    migraphx::shape s{migraphx::shape::float_type, {3}};
    std::vector<float> data1 = {0.25, 0.75, 0.9375};
    std::vector<float> data2 = {0.25, 0.74, 0.9411};

    migraphx::parameter_map pp;
    pp["x1"] = migraphx::argument(s, data1.data());
    pp["x2"] = migraphx::argument(s, data2.data());

    auto result = p.eval(pp).back();
    std::vector<float> result_vector;
    result.visit([&](auto output) { result_vector.assign(output.begin(), output.end()); });

    std::vector<float> gold = {1, 0, 1};
    EXPECT(migraphx::verify_range(result_vector, gold));
}

TEST_CASE(nonzero_test)
{
    migraphx::program p = migraphx::parse_onnx("nonzero_dynamic_test.onnx");
    p.compile(migraphx::ref::target{});

    migraphx::shape s{migraphx::shape::bool_type, {2, 2}};
    std::vector<char> data = {1, 1, 1, 0};

    migraphx::parameter_map pp;
    pp["data"] = migraphx::argument(s, data.data());

    auto result = p.eval(pp).back();
    std::vector<float> result_vector;
    result.visit([&](auto output) { result_vector.assign(output.begin(), output.end()); });

    std::vector<float> gold = {0, 0, 1, 0, 0, 1, 0, 0};
    EXPECT(migraphx::verify_range(result_vector, gold));
}

TEST_CASE(resize_downsample_f_test)
{
    migraphx::program p = migraphx::parse_onnx("resize_downsample_f_test.onnx");
    p.compile(migraphx::ref::target{});

    migraphx::shape sx{migraphx::shape::float_type, {1, 1, 2, 4}};
    std::vector<float> dx(sx.elements());
    std::iota(dx.begin(), dx.end(), 0.0f);

    migraphx::parameter_map pp;
    pp["X"] = migraphx::argument(sx, dx.data());

    auto result = p.eval(pp).back();
    std::vector<float> result_vector;
    result.visit([&](auto output) { result_vector.assign(output.begin(), output.end()); });

    std::vector<float> gold = {0.0f, 3.0f};

    EXPECT(migraphx::verify_range(result_vector, gold));
}

TEST_CASE(resize_upsample_linear_ac_test)
{
    migraphx::program p = migraphx::parse_onnx("resize_upsample_linear_ac_test.onnx");
    p.compile(migraphx::ref::target{});

    migraphx::shape sx{migraphx::shape::float_type, {1, 1, 2, 2}};
    std::vector<float> dx = {1.0f, 2.0f, 3.0f, 4.0f};

    migraphx::parameter_map pp;
    pp["X"] = migraphx::argument(sx, dx.data());

    auto result = p.eval(pp).back();
    std::vector<float> result_vector;
    result.visit([&](auto output) { result_vector.assign(output.begin(), output.end()); });

    std::vector<float> gold = {1,
                               4.0f / 3,
                               5.0f / 3,
                               2,
                               5.0f / 3,
                               2,
                               7.0f / 3,
                               8.0f / 3,
                               7.0f / 3,
                               8.0f / 3,
                               3,
                               10.0f / 3,
                               3,
                               10.0f / 3,
                               11.0f / 3,
                               4};

    EXPECT(migraphx::verify_range(result_vector, gold));
}

TEST_CASE(resize_upsample_linear_test)
{
    migraphx::program p = migraphx::parse_onnx("resize_upsample_linear_test.onnx");
    p.compile(migraphx::ref::target{});

    migraphx::shape sx{migraphx::shape::float_type, {1, 1, 2, 2}};
    std::vector<float> dx = {1.0f, 2.0f, 3.0f, 4.0f};

    migraphx::parameter_map pp;
    pp["X"] = migraphx::argument(sx, dx.data());

    auto result = p.eval(pp).back();
    std::vector<float> result_vector;
    result.visit([&](auto output) { result_vector.assign(output.begin(), output.end()); });

    std::vector<float> gold = {
        1, 1.25, 1.75, 2, 1.5, 1.75, 2.25, 2.5, 2.5, 2.75, 3.25, 3.5, 3, 3.25, 3.75, 4};

    EXPECT(migraphx::verify_range(result_vector, gold));
}

TEST_CASE(resize_upsample_pf_test)
{
    migraphx::program p = migraphx::parse_onnx("resize_upsample_pf_test.onnx");
    p.compile(migraphx::ref::target{});

    migraphx::shape sx{migraphx::shape::float_type, {1, 1, 2, 2}};
    std::vector<float> dx = {1.0f, 2.0f, 3.0f, 4.0f};

    migraphx::parameter_map pp;
    pp["X"] = migraphx::argument(sx, dx.data());

    auto result = p.eval(pp).back();
    std::vector<float> result_vector;
    result.visit([&](auto output) { result_vector.assign(output.begin(), output.end()); });

    std::vector<float> gold = {1, 1, 1, 2, 2, 2, 1, 1, 1, 2, 2, 2,
                               3, 3, 3, 4, 4, 4, 3, 3, 3, 4, 4, 4};

    EXPECT(migraphx::verify_range(result_vector, gold));
}

TEST_CASE(selu_test)
{
    migraphx::program p = migraphx::parse_onnx("selu_test.onnx");
    p.compile(migraphx::ref::target{});

    migraphx::shape xs{migraphx::shape::double_type, {2, 3}};
    std::vector<double> x_data = {1.1, 2.1, 0.0, -1.3, -5.3, 12.0};

    migraphx::parameter_map pp;
    pp["x"] = migraphx::argument(xs, x_data.data());

    auto result = p.eval(pp).back();
    std::vector<float> result_vector;
    result.visit([&](auto output) { result_vector.assign(output.begin(), output.end()); });

    std::vector<float> gold = {0.55, 1.05, 0, -0.10912, -0.149251, 6};

    EXPECT(migraphx::verify_range(result_vector, gold));
}

TEST_CASE(slice_test)
{
    migraphx::program p = migraphx::parse_onnx("slice_test.onnx");
    p.compile(migraphx::ref::target{});

    migraphx::shape sh_data{migraphx::shape::float_type, {3, 2}};
    std::vector<float> data = {0, 1, 2, 3, 4, 5};

    migraphx::parameter_map pp;
    pp["0"] = migraphx::argument(sh_data, data.data());

    auto result = p.eval(pp).back();
    std::vector<float> result_vector;
    result.visit([&](auto output) { result_vector.assign(output.begin(), output.end()); });
    std::vector<float> gold = {2, 3};

    EXPECT(migraphx::verify_range(result_vector, gold));
}

TEST_CASE(slice_5arg_test)
{
    migraphx::program p = migraphx::parse_onnx("slice_5arg_test.onnx");
    p.compile(migraphx::ref::target{});

    migraphx::shape sh_data{migraphx::shape::float_type, {5, 5}}; // start
    std::vector<float> data = {0,  1,  2,  3,  4,  5,  6,  7,  8,  9,  10, 11, 12,
                               13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24};

    migraphx::parameter_map pp;
    pp["0"] = migraphx::argument(sh_data, data.data());

    auto result = p.eval(pp).back();
    std::vector<float> result_vector;
    result.visit([&](auto output) { result_vector.assign(output.begin(), output.end()); });

    std::vector<float> gold = {10, 11, 12, 13, 15, 16, 17, 18};
    EXPECT(migraphx::verify_range(result_vector, gold));
}

TEST_CASE(slice_reverse_test)
{
    migraphx::program p = migraphx::parse_onnx("slice_5arg_reverse_test.onnx");
    p.compile(migraphx::ref::target{});

    migraphx::shape sh_data{migraphx::shape::float_type, {5, 5}}; // start
    std::vector<float> data = {0,  1,  2,  3,  4,  5,  6,  7,  8,  9,  10, 11, 12,
                               13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24};

    migraphx::parameter_map pp;
    pp["0"] = migraphx::argument(sh_data, data.data());

    auto result = p.eval(pp).back();
    std::vector<float> result_vector;
    result.visit([&](auto output) { result_vector.assign(output.begin(), output.end()); });

    std::vector<float> gold = {14, 13, 12, 11, 19, 18, 17, 16};
    EXPECT(migraphx::verify_range(result_vector, gold));
}

TEST_CASE(slice_step_test)
{
    migraphx::program p = migraphx::parse_onnx("slice_5arg_step_test.onnx");
    p.compile(migraphx::ref::target{});

    migraphx::shape sh_data{migraphx::shape::float_type, {5, 5}}; // start
    std::vector<float> data = {0,  1,  2,  3,  4,  5,  6,  7,  8,  9,  10, 11, 12,
                               13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24};

    migraphx::parameter_map pp;
    pp["0"] = migraphx::argument(sh_data, data.data());

    auto result = p.eval(pp).back();
    std::vector<float> result_vector;
    result.visit([&](auto output) { result_vector.assign(output.begin(), output.end()); });

    std::vector<float> gold = {14, 12};
    EXPECT(migraphx::verify_range(result_vector, gold));
}

TEST_CASE(softplus_test)
{
    migraphx::program p = migraphx::parse_onnx("softplus_test.onnx");
    p.compile(migraphx::ref::target{});

    migraphx::shape s{migraphx::shape::float_type, {5}};
    std::vector<float> data = {0, 1, 2, 3, 4};

    migraphx::parameter_map pp;
    pp["x"] = migraphx::argument(s, data.data());

    auto result = p.eval(pp).back();
    std::vector<float> result_vector;
    result.visit([&](auto output) { result_vector.assign(output.begin(), output.end()); });
    std::vector<float> gold(5);
    std::transform(
        data.begin(), data.end(), gold.begin(), [](auto x) { return std::log1p(std::exp(x)); });

    EXPECT(migraphx::verify_range(result_vector, gold));
}

TEST_CASE(softsign_test)
{
    migraphx::program p = migraphx::parse_onnx("softsign_test.onnx");
    p.compile(migraphx::ref::target{});

    migraphx::shape s{migraphx::shape::float_type, {5}};
    std::vector<float> data = {0, 1, 2, 3, 4};

    migraphx::parameter_map pp;
    pp["x"] = migraphx::argument(s, data.data());

    auto result = p.eval(pp).back();
    std::vector<float> result_vector;
    result.visit([&](auto output) { result_vector.assign(output.begin(), output.end()); });
    std::vector<float> gold(5);
    std::transform(
        data.begin(), data.end(), gold.begin(), [](auto x) { return x / (1.0 + std::abs(x)); });

    EXPECT(migraphx::verify_range(result_vector, gold));
}

TEST_CASE(upsample_test)
{
    migraphx::program p = migraphx::parse_onnx("upsample_test.onnx");

    std::vector<float> x_data = {1, 2, 3, 4};
    migraphx::shape sx{migraphx::shape::float_type, {1, 1, 2, 2}};

    migraphx::parameter_map pp;
    pp["X"] = migraphx::argument(sx, x_data.data());

    auto result = p.eval(pp).back();
    std::vector<float> result_vector;
    result.visit([&](auto output) { result_vector.assign(output.begin(), output.end()); });

    std::vector<float> gold = {1, 1, 1, 2, 2, 2, 1, 1, 1, 2, 2, 2,
                               3, 3, 3, 4, 4, 4, 3, 3, 3, 4, 4, 4};
    EXPECT(migraphx::verify_range(result_vector, gold));
}

TEST_CASE(where_test)
{
    migraphx::program p = migraphx::parse_onnx("where_test.onnx");
    p.compile(migraphx::ref::target{});

    migraphx::shape c_shape{migraphx::shape::bool_type, {2}};
    std::vector<int8_t> c_data = {1, 0};

    migraphx::shape x_shape{migraphx::shape::float_type, {2, 2, 2}};
    std::vector<float> x_data(8, 1.0f);

    migraphx::shape y_shape{migraphx::shape::float_type, {2, 1, 2, 2}};
    std::vector<float> y_data(8, 2.0f);

    migraphx::parameter_map pp;
    pp["c"] = migraphx::argument(c_shape, c_data.data());
    pp["x"] = migraphx::argument(x_shape, x_data.data());
    pp["y"] = migraphx::argument(y_shape, y_data.data());

    auto result = p.eval(pp).back();
    std::vector<float> result_vector;
    result.visit([&](auto output) { result_vector.assign(output.begin(), output.end()); });

    std::vector<float> gold = {1.0f,
                               2.0f,
                               1.0f,
                               2.0f,
                               1.0f,
                               2.0f,
                               1.0f,
                               2.0f,
                               1.0f,
                               2.0f,
                               1.0f,
                               2.0f,
                               1.0f,
                               2.0f,
                               1.0f,
                               2.0f};
    EXPECT(migraphx::verify_range(result_vector, gold));
}

int main(int argc, const char* argv[]) { test::run(argc, argv); }
