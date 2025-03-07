#ifndef MIGRAPHX_GUARD_C_API_MIGRAPHX_H
#define MIGRAPHX_GUARD_C_API_MIGRAPHX_H

#include <stdlib.h>

// Add new types here
// clang-format off
#define MIGRAPHX_SHAPE_VISIT_TYPES(m) \
    m(bool_type, bool) \
    m(half_type, half) \
    m(float_type, float) \
    m(double_type, double) \
    m(uint8_type, uint8_t) \
    m(int8_type, int8_t) \
    m(uint16_type, uint16_t) \
    m(int16_type, int16_t) \
    m(int32_type, int32_t) \
    m(int64_type, int64_t) \
    m(uint32_type, uint32_t) \
    m(uint64_type, uint64_t)
// clang-format on

#ifdef __cplusplus
extern "C" {
#endif

// return code, more to be added later
typedef enum {
    migraphx_status_success        = 0,
    migraphx_status_bad_param      = 1,
    migraphx_status_unknown_target = 3,
    migraphx_status_unknown_error  = 4,

} migraphx_status;

#define MIGRAPHX_SHAPE_GENERATE_ENUM_TYPES(x, t) migraphx_shape_##x,
/// An enum to represent the different data type inputs
typedef enum {
    migraphx_shape_tuple_type,
    MIGRAPHX_SHAPE_VISIT_TYPES(MIGRAPHX_SHAPE_GENERATE_ENUM_TYPES)
} migraphx_shape_datatype_t;
#undef MIGRAPHX_SHAPE_GENERATE_ENUM_TYPES

typedef struct migraphx_shape* migraphx_shape_t;
typedef const struct migraphx_shape* const_migraphx_shape_t;

typedef struct migraphx_argument* migraphx_argument_t;
typedef const struct migraphx_argument* const_migraphx_argument_t;

typedef struct migraphx_target* migraphx_target_t;
typedef const struct migraphx_target* const_migraphx_target_t;

typedef struct migraphx_program_parameter_shapes* migraphx_program_parameter_shapes_t;
typedef const struct migraphx_program_parameter_shapes* const_migraphx_program_parameter_shapes_t;

typedef struct migraphx_program_parameters* migraphx_program_parameters_t;
typedef const struct migraphx_program_parameters* const_migraphx_program_parameters_t;

typedef struct migraphx_arguments* migraphx_arguments_t;
typedef const struct migraphx_arguments* const_migraphx_arguments_t;

typedef struct migraphx_shapes* migraphx_shapes_t;
typedef const struct migraphx_shapes* const_migraphx_shapes_t;

typedef struct migraphx_module* migraphx_module_t;
typedef const struct migraphx_module* const_migraphx_module_t;

typedef struct migraphx_program* migraphx_program_t;
typedef const struct migraphx_program* const_migraphx_program_t;

typedef struct migraphx_operation* migraphx_operation_t;
typedef const struct migraphx_operation* const_migraphx_operation_t;

typedef struct migraphx_onnx_options* migraphx_onnx_options_t;
typedef const struct migraphx_onnx_options* const_migraphx_onnx_options_t;

typedef struct migraphx_file_options* migraphx_file_options_t;
typedef const struct migraphx_file_options* const_migraphx_file_options_t;

typedef struct migraphx_compile_options* migraphx_compile_options_t;
typedef const struct migraphx_compile_options* const_migraphx_compile_options_t;

typedef struct migraphx_tf_options* migraphx_tf_options_t;
typedef const struct migraphx_tf_options* const_migraphx_tf_options_t;

typedef struct migraphx_quantize_op_names* migraphx_quantize_op_names_t;
typedef const struct migraphx_quantize_op_names* const_migraphx_quantize_op_names_t;

typedef struct migraphx_quantize_int8_options* migraphx_quantize_int8_options_t;
typedef const struct migraphx_quantize_int8_options* const_migraphx_quantize_int8_options_t;

migraphx_status migraphx_shape_destroy(migraphx_shape_t shape);

migraphx_status migraphx_shape_create(migraphx_shape_t* shape,
                                      migraphx_shape_datatype_t type,
                                      size_t* lengths,
                                      size_t lengths_size);

migraphx_status migraphx_shape_create_with_strides(migraphx_shape_t* shape,
                                                   migraphx_shape_datatype_t type,
                                                   size_t* lengths,
                                                   size_t lengths_size,
                                                   size_t* strides,
                                                   size_t strides_size);

migraphx_status migraphx_shape_create_scalar(migraphx_shape_t* shape,
                                             migraphx_shape_datatype_t type);

migraphx_status
migraphx_shape_lengths(const size_t** out, size_t* out_size, const_migraphx_shape_t shape);

migraphx_status
migraphx_shape_strides(const size_t** out, size_t* out_size, const_migraphx_shape_t shape);

migraphx_status migraphx_shape_type(migraphx_shape_datatype_t* out, const_migraphx_shape_t shape);

migraphx_status migraphx_shape_bytes(size_t* out, const_migraphx_shape_t shape);

migraphx_status
migraphx_shape_equal(bool* out, const_migraphx_shape_t shape, const_migraphx_shape_t x);

migraphx_status migraphx_argument_destroy(migraphx_argument_t argument);

migraphx_status
migraphx_argument_create(migraphx_argument_t* argument, const_migraphx_shape_t shape, void* buffer);

migraphx_status migraphx_argument_shape(const_migraphx_shape_t* out,
                                        const_migraphx_argument_t argument);

migraphx_status migraphx_argument_buffer(char** out, const_migraphx_argument_t argument);

migraphx_status
migraphx_argument_equal(bool* out, const_migraphx_argument_t argument, const_migraphx_argument_t x);

migraphx_status
migraphx_argument_generate(migraphx_argument_t* out, const_migraphx_shape_t s, size_t seed);

migraphx_status migraphx_target_destroy(migraphx_target_t target);

migraphx_status migraphx_target_create(migraphx_target_t* target, const char* name);

migraphx_status migraphx_program_parameter_shapes_destroy(
    migraphx_program_parameter_shapes_t program_parameter_shapes);

migraphx_status migraphx_program_parameter_shapes_size(
    size_t* out, migraphx_program_parameter_shapes_t program_parameter_shapes);

migraphx_status
migraphx_program_parameter_shapes_get(const_migraphx_shape_t* out,
                                      migraphx_program_parameter_shapes_t program_parameter_shapes,
                                      const char* name);

migraphx_status migraphx_program_parameter_shapes_names(
    const char** out, migraphx_program_parameter_shapes_t program_parameter_shapes);

migraphx_status
migraphx_program_parameters_destroy(migraphx_program_parameters_t program_parameters);

migraphx_status
migraphx_program_parameters_create(migraphx_program_parameters_t* program_parameters);

migraphx_status migraphx_program_parameters_add(migraphx_program_parameters_t program_parameters,
                                                const char* name,
                                                const_migraphx_argument_t argument);

migraphx_status migraphx_arguments_destroy(migraphx_arguments_t arguments);

migraphx_status migraphx_arguments_size(size_t* out, migraphx_arguments_t arguments);

migraphx_status
migraphx_arguments_get(const_migraphx_argument_t* out, migraphx_arguments_t arguments, size_t idx);

migraphx_status migraphx_shapes_destroy(migraphx_shapes_t shapes);

migraphx_status migraphx_shapes_size(size_t* out, migraphx_shapes_t shapes);

migraphx_status
migraphx_shapes_get(const_migraphx_shape_t* out, migraphx_shapes_t shapes, size_t idx);

migraphx_status migraphx_module_print(const_migraphx_module_t module);

migraphx_status migraphx_program_destroy(migraphx_program_t program);

migraphx_status migraphx_program_get_main_module(migraphx_module_t* out,
                                                 migraphx_program_t program);

migraphx_status migraphx_program_compile(migraphx_program_t program,
                                         migraphx_target_t target,
                                         migraphx_compile_options_t options);

migraphx_status migraphx_program_get_parameter_shapes(migraphx_program_parameter_shapes_t* out,
                                                      migraphx_program_t program);

migraphx_status migraphx_program_get_output_shapes(migraphx_shapes_t* out,
                                                   migraphx_program_t program);

migraphx_status migraphx_program_print(const_migraphx_program_t program);

migraphx_status migraphx_program_sort(migraphx_program_t program);

migraphx_status migraphx_program_run(migraphx_arguments_t* out,
                                     migraphx_program_t program,
                                     migraphx_program_parameters_t params);

migraphx_status
migraphx_program_equal(bool* out, const_migraphx_program_t program, const_migraphx_program_t x);

migraphx_status migraphx_operation_destroy(migraphx_operation_t operation);

migraphx_status migraphx_operation_create(migraphx_operation_t* operation,
                                          const char* name,
                                          const char* attributes,
                                          ...);

migraphx_status migraphx_operation_name(char* out, size_t out_size, migraphx_operation_t operation);

migraphx_status
migraphx_load(migraphx_program_t* out, const char* name, migraphx_file_options_t options);

migraphx_status
migraphx_save(migraphx_program_t p, const char* name, migraphx_file_options_t options);

migraphx_status migraphx_onnx_options_destroy(migraphx_onnx_options_t onnx_options);

migraphx_status migraphx_onnx_options_create(migraphx_onnx_options_t* onnx_options);

migraphx_status migraphx_onnx_options_set_input_parameter_shape(
    migraphx_onnx_options_t onnx_options, const char* name, size_t* dims, size_t dims_size);

migraphx_status migraphx_onnx_options_set_default_dim_value(migraphx_onnx_options_t onnx_options,
                                                            size_t value);

migraphx_status
migraphx_onnx_options_set_default_loop_iterations(migraphx_onnx_options_t onnx_options,
                                                  int64_t value);

migraphx_status migraphx_file_options_destroy(migraphx_file_options_t file_options);

migraphx_status migraphx_file_options_create(migraphx_file_options_t* file_options);

migraphx_status migraphx_file_options_set_file_format(migraphx_file_options_t file_options,
                                                      const char* format);

migraphx_status migraphx_compile_options_destroy(migraphx_compile_options_t compile_options);

migraphx_status migraphx_compile_options_create(migraphx_compile_options_t* compile_options);

migraphx_status
migraphx_compile_options_set_offload_copy(migraphx_compile_options_t compile_options, bool value);

migraphx_status migraphx_compile_options_set_fast_math(migraphx_compile_options_t compile_options,
                                                       bool value);

migraphx_status
migraphx_parse_onnx(migraphx_program_t* out, const char* name, migraphx_onnx_options_t options);

migraphx_status migraphx_parse_onnx_buffer(migraphx_program_t* out,
                                           const void* data,
                                           size_t size,
                                           migraphx_onnx_options_t options);

migraphx_status migraphx_tf_options_destroy(migraphx_tf_options_t tf_options);

migraphx_status migraphx_tf_options_create(migraphx_tf_options_t* tf_options);

migraphx_status migraphx_tf_options_set_nhwc(migraphx_tf_options_t tf_options, bool is_nhwc);

migraphx_status migraphx_tf_options_set_input_parameter_shape(migraphx_tf_options_t tf_options,
                                                              const char* name,
                                                              size_t* dims,
                                                              size_t dims_size);

migraphx_status migraphx_tf_options_set_default_dim_value(migraphx_tf_options_t tf_options,
                                                          size_t value);

migraphx_status migraphx_tf_options_set_output_names(migraphx_tf_options_t tf_options,
                                                     const char** names,
                                                     size_t names_size);

migraphx_status
migraphx_parse_tf(migraphx_program_t* out, const char* name, migraphx_tf_options_t options);

migraphx_status migraphx_quantize_op_names_destroy(migraphx_quantize_op_names_t quantize_op_names);

migraphx_status migraphx_quantize_op_names_create(migraphx_quantize_op_names_t* quantize_op_names);

migraphx_status migraphx_quantize_op_names_add(migraphx_quantize_op_names_t quantize_op_names,
                                               const char* name);

migraphx_status migraphx_quantize_fp16_with_op_names(migraphx_program_t prog,
                                                     migraphx_quantize_op_names_t name);

migraphx_status migraphx_quantize_fp16(migraphx_program_t prog);

migraphx_status
migraphx_quantize_int8_options_destroy(migraphx_quantize_int8_options_t quantize_int8_options);

migraphx_status
migraphx_quantize_int8_options_create(migraphx_quantize_int8_options_t* quantize_int8_options);

migraphx_status
migraphx_quantize_int8_options_add_op_name(migraphx_quantize_int8_options_t quantize_int8_options,
                                           const char* name);

migraphx_status migraphx_quantize_int8_options_add_calibration_data(
    migraphx_quantize_int8_options_t quantize_int8_options, migraphx_program_parameters_t data);

migraphx_status migraphx_quantize_int8(migraphx_program_t prog,
                                       migraphx_target_t target,
                                       migraphx_quantize_int8_options_t options);

#ifdef __cplusplus
}
#endif

#endif
