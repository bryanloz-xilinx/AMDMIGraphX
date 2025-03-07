# This script generates onnx files for MIGraphX onnx operator tests.
# To generate an individual onnx file, you can use the following
# command: python -c "import gen_onnx; gen_onnx.{test_name}_test()"
import numpy as np
import onnx
from onnx import helper
from onnx import TensorProto


def onnx_test(op_test):
    def run_test():
        op_info = op_test()
        if len(op_info) > 3:
            graph_def = helper.make_graph(op_info[0],
                                          op_test.__name__,
                                          op_info[1],
                                          op_info[2],
                                          initializer=op_info[3])
        else:
            graph_def = helper.make_graph(op_info[0], op_test.__name__,
                                          op_info[1], op_info[2])
        model_def = helper.make_model(graph_def,
                                      producer_name=op_test.__name__)
        onnx.save(model_def, '{}.onnx'.format(op_test.__name__))

    return run_test


@onnx_test
def acos_test():
    x = helper.make_tensor_value_info('x', TensorProto.FLOAT, [10])
    y = helper.make_tensor_value_info('y', TensorProto.FLOAT, [10])

    node = onnx.helper.make_node(
        'Acos',
        inputs=['x'],
        outputs=['y'],
    )

    return ([node], [x], [y])


@onnx_test
def acosh_test():
    x = helper.make_tensor_value_info('x', TensorProto.FLOAT, [10])
    y = helper.make_tensor_value_info('y', TensorProto.FLOAT, [10])

    node = onnx.helper.make_node(
        'Acosh',
        inputs=['x'],
        outputs=['y'],
    )

    return ([node], [x], [y])


@onnx_test
def add_bcast_test():
    x = helper.make_tensor_value_info('0', TensorProto.FLOAT, [2, 3, 4, 5])
    y = helper.make_tensor_value_info('1', TensorProto.FLOAT, [3, 4])
    z = helper.make_tensor_value_info('2', TensorProto.FLOAT, [2, 3, 4, 5])

    node = onnx.helper.make_node('Add',
                                 inputs=['0', '1'],
                                 broadcast=1,
                                 axis=1,
                                 outputs=['2'])

    return ([node], [x, y], [z])


@onnx_test
def add_fp16_test():
    x = helper.make_tensor_value_info('0', TensorProto.FLOAT16, [1])
    y = helper.make_tensor_value_info('1', TensorProto.FLOAT16, [1])
    z = helper.make_tensor_value_info('2', TensorProto.FLOAT16, [1])

    node = onnx.helper.make_node(
        'Add',
        inputs=['0', '1'],
        outputs=['2'],
    )

    return (
        [node],
        [x, y],
        [z],
        # '0' -> 1.5, '1' -> 2.5
        [
            onnx.helper.make_tensor('0', TensorProto.FLOAT16, [1], [15872]),
            onnx.helper.make_tensor('1', TensorProto.FLOAT16, [1], [16640])
        ])


@onnx_test
def add_scalar_test():
    x = helper.make_tensor_value_info('0', TensorProto.UINT8, [2, 3, 4, 5])
    y = helper.make_tensor_value_info('1', TensorProto.UINT8, [])
    z = helper.make_tensor_value_info('2', TensorProto.UINT8, [2, 3, 4, 5])

    node = onnx.helper.make_node('Add', inputs=['0', '1'], outputs=['2'])

    return ([node], [x, y], [z])


@onnx_test
def argmax_test():
    x = helper.make_tensor_value_info('x', TensorProto.FLOAT, [3, 4, 5, 6])
    y = helper.make_tensor_value_info('y', TensorProto.FLOAT, [3, 4, 6])

    node = onnx.helper.make_node('ArgMax',
                                 inputs=['x'],
                                 outputs=['y'],
                                 axis=2,
                                 keepdims=0)

    return ([node], [x], [y])


@onnx_test
def argmin_test():
    x = helper.make_tensor_value_info('x', TensorProto.FLOAT, [3, 4, 5, 6])
    y = helper.make_tensor_value_info('y', TensorProto.FLOAT, [3, 4, 5])

    node = onnx.helper.make_node('ArgMin',
                                 inputs=['x'],
                                 outputs=['y'],
                                 axis=3,
                                 keepdims=0)

    return ([node], [x], [y])


@onnx_test
def asin_test():
    x = helper.make_tensor_value_info('x', TensorProto.FLOAT, [10])
    y = helper.make_tensor_value_info('y', TensorProto.FLOAT, [10])

    node = onnx.helper.make_node(
        'Asin',
        inputs=['x'],
        outputs=['y'],
    )

    return ([node], [x], [y])


@onnx_test
def asinh_test():
    x = helper.make_tensor_value_info('x', TensorProto.FLOAT, [10])
    y = helper.make_tensor_value_info('y', TensorProto.FLOAT, [10])

    node = onnx.helper.make_node(
        'Asinh',
        inputs=['x'],
        outputs=['y'],
    )

    return ([node], [x], [y])


@onnx_test
def atan_test():
    x = helper.make_tensor_value_info('x', TensorProto.FLOAT, [10])
    y = helper.make_tensor_value_info('y', TensorProto.FLOAT, [10])

    node = onnx.helper.make_node(
        'Atan',
        inputs=['x'],
        outputs=['y'],
    )

    return ([node], [x], [y])


@onnx_test
def atanh_test():
    x = helper.make_tensor_value_info('x', TensorProto.FLOAT, [10])
    y = helper.make_tensor_value_info('y', TensorProto.FLOAT, [10])

    node = onnx.helper.make_node(
        'Atanh',
        inputs=['x'],
        outputs=['y'],
    )

    return ([node], [x], [y])


@onnx_test
def averagepool_1d_test():
    x = helper.make_tensor_value_info('0', TensorProto.FLOAT, [1, 3, 5])
    out = helper.make_tensor_value_info('1', TensorProto.FLOAT, [1, 3, 3])

    node = onnx.helper.make_node('AveragePool',
                                 inputs=['0'],
                                 outputs=['1'],
                                 kernel_shape=[3])

    return ([node], [x], [out])


@onnx_test
def averagepool_3d_test():
    x = helper.make_tensor_value_info('0', TensorProto.FLOAT, [1, 3, 5, 5, 5])
    out = helper.make_tensor_value_info('1', TensorProto.FLOAT,
                                        [1, 3, 3, 3, 3])

    node = onnx.helper.make_node('AveragePool',
                                 inputs=['0'],
                                 outputs=['1'],
                                 kernel_shape=[3, 3, 3])

    return ([node], [x], [out])


@onnx_test
def averagepool_notset_test():
    x = helper.make_tensor_value_info('x', TensorProto.FLOAT, [1, 1, 5, 5])
    y = helper.make_tensor_value_info('y', TensorProto.FLOAT, [1, 1, 1, 1])

    node = onnx.helper.make_node('AveragePool',
                                 inputs=['x'],
                                 outputs=['y'],
                                 kernel_shape=[6, 6],
                                 strides=[2, 2],
                                 pads=[0, 0, 1, 1],
                                 auto_pad='NOTSET')

    return ([node], [x], [y])


@onnx_test
def averagepool_nt_cip_test():
    x = helper.make_tensor_value_info('x', TensorProto.FLOAT, [1, 1, 5, 5])
    y = helper.make_tensor_value_info('y', TensorProto.FLOAT, [1, 1, 1, 1])

    node = onnx.helper.make_node('AveragePool',
                                 inputs=['x'],
                                 outputs=['y'],
                                 kernel_shape=[6, 6],
                                 strides=[2, 2],
                                 pads=[0, 0, 1, 1],
                                 auto_pad='NOTSET',
                                 count_include_pad=1)

    return ([node], [x], [y])


@onnx_test
def averagepool_same_lower_test():
    x = helper.make_tensor_value_info('x', TensorProto.FLOAT, [1, 1, 5, 5])
    y = helper.make_tensor_value_info('y', TensorProto.FLOAT, [1, 1, 5, 5])

    node = onnx.helper.make_node('AveragePool',
                                 inputs=['x'],
                                 outputs=['y'],
                                 kernel_shape=[2, 2],
                                 auto_pad='SAME_LOWER')

    return ([node], [x], [y])


@onnx_test
def averagepool_sl_cip_test():
    x = helper.make_tensor_value_info('x', TensorProto.FLOAT, [1, 1, 5, 5])
    y = helper.make_tensor_value_info('y', TensorProto.FLOAT, [1, 1, 5, 5])

    node = onnx.helper.make_node('AveragePool',
                                 inputs=['x'],
                                 outputs=['y'],
                                 kernel_shape=[2, 2],
                                 auto_pad='SAME_LOWER',
                                 count_include_pad=1)

    return ([node], [x], [y])


@onnx_test
def averagepool_same_upper_test():
    x = helper.make_tensor_value_info('x', TensorProto.FLOAT, [1, 1, 5, 5])
    y = helper.make_tensor_value_info('y', TensorProto.FLOAT, [1, 1, 5, 5])

    node = onnx.helper.make_node('AveragePool',
                                 inputs=['x'],
                                 outputs=['y'],
                                 kernel_shape=[2, 2],
                                 auto_pad='SAME_UPPER')

    return ([node], [x], [y])


@onnx_test
def batchnorm_1d_test():
    x = helper.make_tensor_value_info('0', TensorProto.FLOAT, [1, 3, 5])
    scale = helper.make_tensor_value_info('1', TensorProto.FLOAT, [3])
    bias = helper.make_tensor_value_info('2', TensorProto.FLOAT, [3])
    mean = helper.make_tensor_value_info('3', TensorProto.FLOAT, [3])
    var = helper.make_tensor_value_info('4', TensorProto.FLOAT, [3])
    out = helper.make_tensor_value_info('5', TensorProto.FLOAT, [1, 3, 5])

    node = onnx.helper.make_node('BatchNormalization',
                                 inputs=['0', '1', '2', '3', '4'],
                                 outputs=['5'],
                                 epsilon=1e-6,
                                 momentum=0.9)

    return ([node], [x, scale, bias, mean, var], [out])


@onnx_test
def batchnorm_3d_test():
    x = helper.make_tensor_value_info('0', TensorProto.FLOAT, [1, 3, 5, 5, 5])
    scale = helper.make_tensor_value_info('1', TensorProto.FLOAT, [3])
    bias = helper.make_tensor_value_info('2', TensorProto.FLOAT, [3])
    mean = helper.make_tensor_value_info('3', TensorProto.FLOAT, [3])
    var = helper.make_tensor_value_info('4', TensorProto.FLOAT, [3])
    out = helper.make_tensor_value_info('5', TensorProto.FLOAT,
                                        [1, 3, 5, 5, 5])

    node = onnx.helper.make_node('BatchNormalization',
                                 inputs=['0', '1', '2', '3', '4'],
                                 outputs=['5'],
                                 epsilon=1e-6,
                                 momentum=0.9)

    return ([node], [x, scale, bias, mean, var], [out])


@onnx_test
def cast_test():
    x = helper.make_tensor_value_info('x', TensorProto.FLOAT16, [10])
    y = helper.make_tensor_value_info('y', TensorProto.FLOAT, [10])

    node = onnx.helper.make_node('Cast', inputs=['x'], outputs=['y'], to=1)

    return ([node], [x], [y])


@onnx_test
def ceil_test():
    x = helper.make_tensor_value_info('x', TensorProto.FLOAT, [10])
    y = helper.make_tensor_value_info('y', TensorProto.FLOAT, [10])

    node = onnx.helper.make_node(
        'Ceil',
        inputs=['x'],
        outputs=['y'],
    )

    return ([node], [x], [y])


@onnx_test
def clip_test():
    x = helper.make_tensor_value_info('0', TensorProto.FLOAT, [3])
    y = helper.make_tensor_value_info('1', TensorProto.FLOAT, [3])

    node = onnx.helper.make_node('Clip',
                                 inputs=['0'],
                                 outputs=['1'],
                                 max=6.0,
                                 min=0.0)

    return ([node], [x], [y])


@onnx_test
def clip_test_op11():
    x = helper.make_tensor_value_info('0', TensorProto.FLOAT, [3])
    y = helper.make_tensor_value_info('1', TensorProto.FLOAT, [3])

    min_val = helper.make_tensor('min', TensorProto.FLOAT, [], [0.0])
    max_val = helper.make_tensor('max', TensorProto.FLOAT, [], [6.0])

    node = onnx.helper.make_node('Clip',
                                 inputs=['0', 'min', 'max'],
                                 outputs=['1'])

    return ([node], [x], [y], [min_val, max_val])


@onnx_test
def clip_test_op11_max_only():
    x = helper.make_tensor_value_info('0', TensorProto.FLOAT, [3])
    y = helper.make_tensor_value_info('1', TensorProto.FLOAT, [3])

    max_val = helper.make_tensor('max', TensorProto.FLOAT, [], [0.0])

    node = onnx.helper.make_node('Clip',
                                 inputs=['0', '', 'max'],
                                 outputs=['1'])

    return ([node], [x], [y], [max_val])


@onnx_test
def clip_test_op11_min_only():
    x = helper.make_tensor_value_info('0', TensorProto.FLOAT, [3])
    y = helper.make_tensor_value_info('1', TensorProto.FLOAT, [3])

    min_val = helper.make_tensor('min', TensorProto.FLOAT, [], [0.0])

    node = onnx.helper.make_node('Clip', inputs=['0', 'min'], outputs=['1'])

    return ([node], [x], [y], [min_val])


@onnx_test
def clip_test_op11_no_args():
    x = helper.make_tensor_value_info('0', TensorProto.FLOAT, [3])
    y = helper.make_tensor_value_info('1', TensorProto.FLOAT, [3])

    node = onnx.helper.make_node('Clip', inputs=['0'], outputs=['1'])

    return ([node], [x], [y])


@onnx_test
def clip_test_op11_no_args1():
    x = helper.make_tensor_value_info('0', TensorProto.FLOAT, [3])
    y = helper.make_tensor_value_info('1', TensorProto.FLOAT, [3])

    node = onnx.helper.make_node('Clip', inputs=['0', '', ''], outputs=['1'])

    return ([node], [x], [y])


@onnx_test
def concat_test():
    x = helper.make_tensor_value_info('0', TensorProto.FLOAT, [2, 4, 3])
    y = helper.make_tensor_value_info('1', TensorProto.FLOAT, [7, 4, 3])
    z = helper.make_tensor_value_info('2', TensorProto.FLOAT, [9, 4, 3])

    node = onnx.helper.make_node(
        'Concat',
        inputs=['0', '1'],
        axis=0,
        outputs=['2'],
    )

    return ([node], [x, y], [z])


@onnx_test
def constant_test():
    x = np.array([0, 1, 2])
    y = helper.make_tensor_value_info('0', TensorProto.FLOAT, [3])

    node = onnx.helper.make_node(
        'Constant',
        inputs=[],
        outputs=['0'],
        value=onnx.helper.make_tensor(
            name='const_tensor',
            data_type=TensorProto.FLOAT,
            dims=x.shape,
            vals=x.flatten().astype(float),
        ),
    )

    return ([node], [], [y])


@onnx_test
def constant_fill_test():
    value = helper.make_tensor_value_info('value', TensorProto.FLOAT, [2, 3])

    node = onnx.helper.make_node(
        'ConstantFill',
        inputs=[],
        outputs=['value'],
        dtype=1,
        value=1.0,
        shape=[2, 3],
        input_as_shape=0,
    )

    return ([node], [], [value])


@onnx_test
def constant_fill_input_as_shape_test():
    np_shape = np.array([2, 3])
    value = helper.make_tensor_value_info('value', TensorProto.FLOAT, [2, 3])

    ts_shape = helper.make_tensor(name='shape_tensor',
                                  data_type=TensorProto.INT32,
                                  dims=np_shape.shape,
                                  vals=np_shape.flatten().astype(int))

    const_shape_node = onnx.helper.make_node(
        'Constant',
        inputs=[],
        outputs=['shape'],
        value=ts_shape,
    )

    node = onnx.helper.make_node(
        'ConstantFill',
        inputs=['shape'],
        outputs=['value'],
        dtype=1,
        value=1.0,
        input_as_shape=1,
    )

    return ([const_shape_node, node], [], [value])


@onnx_test
def constant_scalar_test():
    x = np.array([1])
    y = helper.make_tensor_value_info('0', TensorProto.FLOAT, [1])

    node = onnx.helper.make_node(
        'Constant',
        inputs=[],
        outputs=['0'],
        value=onnx.helper.make_tensor(
            name='const_tensor',
            data_type=TensorProto.INT32,
            dims=x.shape,
            vals=x.flatten().astype(int),
        ),
    )

    return ([node], [], [y])


@onnx_test
def const_of_shape_empty_input_test():
    tensor_val = onnx.helper.make_tensor('value', onnx.TensorProto.INT64, [1],
                                         [10])
    empty_val = np.array([]).astype(np.int64)
    empty_ts = helper.make_tensor(name='empty_tensor',
                                  data_type=TensorProto.INT32,
                                  dims=empty_val.shape,
                                  vals=empty_val.flatten().astype(int))
    shape_const = helper.make_node(
        'Constant',
        inputs=[],
        outputs=['shape'],
        value=empty_ts,
    )
    y = helper.make_tensor_value_info('y', TensorProto.FLOAT, [2, 3, 4])

    node = onnx.helper.make_node(
        'ConstantOfShape',
        inputs=['shape'],
        outputs=['y'],
        value=tensor_val,
    )

    return ([shape_const, node], [], [y])


@onnx_test
def const_of_shape_float_test():
    tensor_val = onnx.helper.make_tensor('value', onnx.TensorProto.FLOAT, [1],
                                         [10])

    shape_val = np.array([2, 3, 4]).astype(np.int64)
    shape_ts = helper.make_tensor(name='shape_tensor',
                                  data_type=TensorProto.INT32,
                                  dims=shape_val.shape,
                                  vals=shape_val.flatten().astype(int))

    shape_const = helper.make_node(
        'Constant',
        inputs=[],
        outputs=['shape'],
        value=shape_ts,
    )
    y = helper.make_tensor_value_info('y', TensorProto.FLOAT, [2, 3, 4])

    node = onnx.helper.make_node('ConstantOfShape',
                                 inputs=['shape'],
                                 outputs=['y'],
                                 value=tensor_val)

    return ([shape_const, node], [], [y])


@onnx_test
def const_of_shape_int64_test():
    tensor_val = onnx.helper.make_tensor('value', onnx.TensorProto.INT64, [1],
                                         [10])
    shape_val = np.array([2, 3, 4]).astype(np.int64)
    shape_ts = helper.make_tensor(name='shape_tensor',
                                  data_type=TensorProto.INT32,
                                  dims=shape_val.shape,
                                  vals=shape_val.flatten().astype(int))
    shape_const = helper.make_node(
        'Constant',
        inputs=[],
        outputs=['shape'],
        value=shape_ts,
    )
    y = helper.make_tensor_value_info('y', TensorProto.FLOAT, [2, 3, 4])

    node = onnx.helper.make_node('ConstantOfShape',
                                 inputs=['shape'],
                                 outputs=['y'],
                                 value=tensor_val)

    return ([shape_const, node], [], [y])


@onnx_test
def const_of_shape_no_value_attr_test():
    shape_val = np.array([2, 3, 4]).astype(np.int64)
    shape_ts = helper.make_tensor(name='shape_tensor',
                                  data_type=TensorProto.INT32,
                                  dims=shape_val.shape,
                                  vals=shape_val.flatten().astype(int))
    shape_const = helper.make_node(
        'Constant',
        inputs=[],
        outputs=['shape'],
        value=shape_ts,
    )
    y = helper.make_tensor_value_info('y', TensorProto.FLOAT, [2, 3, 4])

    node = onnx.helper.make_node(
        'ConstantOfShape',
        inputs=['shape'],
        outputs=['y'],
    )

    return ([shape_const, node], [], [y])


@onnx_test
def conv_1d_test():
    x = helper.make_tensor_value_info('0', TensorProto.FLOAT, [1, 3, 5])
    y = helper.make_tensor_value_info('1', TensorProto.FLOAT, [1, 3, 3])
    out = helper.make_tensor_value_info('2', TensorProto.FLOAT, [1, 1, 3])

    node = onnx.helper.make_node('Conv', inputs=['0', '1'], outputs=['2'])

    return ([node], [x, y], [out])


@onnx_test
def conv_3d_test():
    x = helper.make_tensor_value_info('0', TensorProto.FLOAT, [1, 3, 5, 5, 5])
    y = helper.make_tensor_value_info('1', TensorProto.FLOAT, [1, 3, 3, 3, 3])
    out = helper.make_tensor_value_info('2', TensorProto.FLOAT,
                                        [1, 1, 3, 3, 3])

    node = onnx.helper.make_node('Conv', inputs=['0', '1'], outputs=['2'])

    return ([node], [x, y], [out])


@onnx_test
def conv_attr_fail_test():
    x = helper.make_tensor_value_info('0', TensorProto.FLOAT, [1, 3, 5])
    y = helper.make_tensor_value_info('1', TensorProto.FLOAT, [1, 3, 3])
    out = helper.make_tensor_value_info('2', TensorProto.FLOAT, [1, 1, 3])

    node = onnx.helper.make_node('Conv',
                                 inputs=['0', '1'],
                                 strides=[1, 1],
                                 outputs=['2'])

    return ([node], [x, y], [out])


@onnx_test
def conv_autopad_fail_test():
    x = helper.make_tensor_value_info('0', TensorProto.FLOAT, [1, 3, 32, 32])
    y = helper.make_tensor_value_info('1', TensorProto.FLOAT, [1, 3, 1, 1])
    out = helper.make_tensor_value_info('2', TensorProto.FLOAT, [1, 1, 34, 34])

    node = onnx.helper.make_node('Conv',
                                 inputs=['0', '1'],
                                 outputs=['2'],
                                 dilations=[1, 1],
                                 strides=[1, 1],
                                 auto_pad='SAME',
                                 pads=[0, 0, 1, 1, 0, 0, 1, 1])

    return ([node], [x, y], [out])


@onnx_test
def conv_autopad_same_test():
    x = helper.make_tensor_value_info('0', TensorProto.FLOAT, [1, 3, 32, 32])
    y = helper.make_tensor_value_info('1', TensorProto.FLOAT, [1, 3, 3, 3])
    out = helper.make_tensor_value_info('2', TensorProto.FLOAT, [1, 1, 32, 32])

    node = onnx.helper.make_node('Conv',
                                 inputs=['0', '1'],
                                 outputs=['2'],
                                 dilations=[1, 1],
                                 strides=[1, 1],
                                 auto_pad='SAME')

    return ([node], [x, y], [out])


@onnx_test
def conv_bias_test():
    x = helper.make_tensor_value_info('0', TensorProto.FLOAT, [1, 3, 32, 32])
    y = helper.make_tensor_value_info('1', TensorProto.FLOAT, [1, 3, 5, 5])
    z = helper.make_tensor_value_info('2', TensorProto.FLOAT, [1])
    out = helper.make_tensor_value_info('3', TensorProto.FLOAT, [1, 2, 28, 28])

    node = onnx.helper.make_node('Conv',
                                 inputs=['0', '1', '2'],
                                 outputs=['3'],
                                 dilations=[1, 1],
                                 strides=[1, 1])

    return ([node], [x, y, z], [out])


@onnx_test
def conv_bn_relu_maxpool_test():
    x = helper.make_tensor_value_info('0', TensorProto.FLOAT, [1, 3, 32, 32])
    y = helper.make_tensor_value_info('1', TensorProto.FLOAT, [1, 3, 5, 5])
    z = helper.make_tensor_value_info('2', TensorProto.FLOAT, [1])
    m = helper.make_tensor_value_info('3', TensorProto.FLOAT, [1])
    n = helper.make_tensor_value_info('4', TensorProto.FLOAT, [1])
    k = helper.make_tensor_value_info('5', TensorProto.FLOAT, [1])
    l = helper.make_tensor_value_info('6', TensorProto.FLOAT, [1])
    out = helper.make_tensor_value_info('10', TensorProto.FLOAT,
                                        [1, 1, 14, 14])

    node0 = onnx.helper.make_node('Conv',
                                  inputs=['0', '1', '2'],
                                  outputs=['7'],
                                  dilations=[1, 1],
                                  strides=[1, 1],
                                  pads=[0, 0, 0, 0])

    node1 = onnx.helper.make_node('BatchNormalization',
                                  inputs=['7', '3', '4', '5', '6'],
                                  outputs=['8'],
                                  epsilon=9.99999974737875e-06,
                                  momentum=0.899999976158142)

    node2 = onnx.helper.make_node('Relu', inputs=['8'], outputs=['9'])
    node3 = onnx.helper.make_node('MaxPool',
                                  inputs=['9'],
                                  outputs=['10'],
                                  pads=[0, 0, 0, 0],
                                  strides=[2, 2],
                                  kernel_shape=[2, 2])

    return ([node0, node1, node2, node3], [x, y, z, m, n, k, l], [out])


@onnx_test
def conv_relu_maxpool_test():
    x = helper.make_tensor_value_info('0', TensorProto.FLOAT, [1, 3, 32, 32])
    y = helper.make_tensor_value_info('1', TensorProto.FLOAT, [1, 3, 5, 5])
    z = helper.make_tensor_value_info('2', TensorProto.FLOAT, [1])
    out = helper.make_tensor_value_info('5', TensorProto.FLOAT, [1, 1, 14, 14])

    node1 = onnx.helper.make_node('Conv',
                                  inputs=['0', '1', '2'],
                                  outputs=['3'],
                                  dilations=[1, 1],
                                  strides=[1, 1],
                                  pads=[0, 0, 0, 0])

    node2 = onnx.helper.make_node('Relu', inputs=['3'], outputs=['4'])

    node3 = onnx.helper.make_node('MaxPool',
                                  inputs=['4'],
                                  outputs=['5'],
                                  pads=[0, 0, 0, 0],
                                  strides=[2, 2],
                                  kernel_shape=[2, 2])

    return ([node1, node2, node3], [x, y, z], [out])


@onnx_test
def conv_relu_maxpool_x2_test():
    x = helper.make_tensor_value_info('0', TensorProto.FLOAT, [1, 3, 32, 32])
    y = helper.make_tensor_value_info('1', TensorProto.FLOAT, [5, 3, 5, 5])
    z = helper.make_tensor_value_info('2', TensorProto.FLOAT, [5])
    m = helper.make_tensor_value_info('3', TensorProto.FLOAT, [1, 5, 5, 5])
    n = helper.make_tensor_value_info('4', TensorProto.FLOAT, [1])
    out = helper.make_tensor_value_info('10', TensorProto.FLOAT, [1, 1, 5, 5])

    node1 = onnx.helper.make_node('Conv',
                                  inputs=['0', '1', '2'],
                                  outputs=['5'],
                                  dilations=[1, 1],
                                  strides=[1, 1],
                                  pads=[0, 0, 0, 0])

    node2 = onnx.helper.make_node('Relu', inputs=['5'], outputs=['6'])

    node3 = onnx.helper.make_node('MaxPool',
                                  inputs=['6'],
                                  outputs=['7'],
                                  pads=[0, 0, 0, 0],
                                  strides=[2, 2],
                                  kernel_shape=[2, 2])

    node4 = onnx.helper.make_node('Conv',
                                  inputs=['7', '3', '4'],
                                  outputs=['8'],
                                  dilations=[1, 1],
                                  strides=[1, 1],
                                  pads=[0, 0, 0, 0])

    node5 = onnx.helper.make_node('Relu', inputs=['8'], outputs=['9'])

    node6 = onnx.helper.make_node('MaxPool',
                                  inputs=['9'],
                                  outputs=['10'],
                                  pads=[0, 0, 0, 0],
                                  strides=[2, 2],
                                  kernel_shape=[2, 2])

    return ([node1, node2, node3, node4, node5, node6], [x, y, z, m, n], [out])


@onnx_test
def convinteger_bias_test():
    x = helper.make_tensor_value_info('0', TensorProto.INT8, [1, 3, 32, 32])
    y = helper.make_tensor_value_info('1', TensorProto.INT8, [1, 3, 5, 5])
    z = helper.make_tensor_value_info('2', TensorProto.INT32, [1])
    out = helper.make_tensor_value_info('3', TensorProto.INT32, [1, 2, 28, 28])

    node = onnx.helper.make_node('ConvInteger',
                                 inputs=['0', '1', '2'],
                                 outputs=['3'],
                                 dilations=[1, 1],
                                 strides=[1, 1])

    return ([node], [x, y, z], [out])


@onnx_test
def cos_test():
    x = helper.make_tensor_value_info('x', TensorProto.FLOAT, [10])
    y = helper.make_tensor_value_info('y', TensorProto.FLOAT, [10])

    node = onnx.helper.make_node(
        'Cos',
        inputs=['x'],
        outputs=['y'],
    )

    return ([node], [x], [y])


@onnx_test
def cosh_test():
    x = helper.make_tensor_value_info('x', TensorProto.FLOAT, [1])
    y = helper.make_tensor_value_info('y', TensorProto.FLOAT, [1])

    node = onnx.helper.make_node(
        'Cosh',
        inputs=['x'],
        outputs=['y'],
    )

    return ([node], [x], [y])


@onnx_test
def deconv_test():
    x = helper.make_tensor_value_info('x', TensorProto.FLOAT, [1, 1, 3, 3])
    w = helper.make_tensor_value_info('w', TensorProto.FLOAT, [1, 1, 3, 3])
    y = helper.make_tensor_value_info('y', TensorProto.FLOAT, [1, 1, 5, 5])

    node = onnx.helper.make_node('ConvTranspose',
                                 name='conv1',
                                 inputs=['x', 'w'],
                                 outputs=['y'])

    return ([node], [x, w], [y])


@onnx_test
def deconv_bias_test():
    x = helper.make_tensor_value_info('x', TensorProto.FLOAT, [1, 1, 3, 3])
    w = helper.make_tensor_value_info('w', TensorProto.FLOAT, [1, 1, 3, 3])
    b = helper.make_tensor_value_info('b', TensorProto.FLOAT, [1])
    y = helper.make_tensor_value_info('y', TensorProto.FLOAT, [1, 1, 5, 5])

    node = onnx.helper.make_node('ConvTranspose',
                                 name='conv1',
                                 inputs=['x', 'w', 'b'],
                                 outputs=['y'])

    return ([node], [x, w, b], [y])


@onnx_test
def deconv_input_pads_strides_test():
    x = helper.make_tensor_value_info('x', TensorProto.FLOAT, [1, 1, 3, 3])
    w = helper.make_tensor_value_info('w', TensorProto.FLOAT, [1, 2, 3, 3])
    y = helper.make_tensor_value_info('y', TensorProto.FLOAT, [1, 2, 7, 5])

    node = onnx.helper.make_node('ConvTranspose',
                                 inputs=['x', 'w'],
                                 outputs=['y'],
                                 strides=[3, 2],
                                 pads=[1, 1, 1, 1])

    return ([node], [x, w], [y])


@onnx_test
def deconv_input_pads_asymm_test():
    x = helper.make_tensor_value_info('x', TensorProto.FLOAT, [1, 1, 3, 3])
    w = helper.make_tensor_value_info('w', TensorProto.FLOAT, [1, 2, 3, 3])
    y = helper.make_tensor_value_info('y', TensorProto.FLOAT, [1, 2, 8, 6])

    node = onnx.helper.make_node('ConvTranspose',
                                 inputs=['x', 'w'],
                                 outputs=['y'],
                                 strides=[3, 2],
                                 pads=[0, 0, 1, 1])

    return ([node], [x, w], [y])


@onnx_test
def deconv_input_pads_asymm_1d_test():
    x = helper.make_tensor_value_info('x', TensorProto.FLOAT, [1, 1, 3])
    w = helper.make_tensor_value_info('w', TensorProto.FLOAT, [1, 2, 3])
    y = helper.make_tensor_value_info('y', TensorProto.FLOAT, [1, 2, 6])

    node = onnx.helper.make_node('ConvTranspose',
                                 inputs=['x', 'w'],
                                 outputs=['y'],
                                 strides=[2],
                                 pads=[0, 1],
                                 dilations=[1])

    return ([node], [x, w], [y])


@onnx_test
def deconv_output_padding_test():
    x = helper.make_tensor_value_info('x', TensorProto.FLOAT, [1, 1, 3, 3])
    w = helper.make_tensor_value_info('w', TensorProto.FLOAT, [1, 2, 3, 3])
    y = helper.make_tensor_value_info('y', TensorProto.FLOAT, [1, 2, 10, 8])

    node = onnx.helper.make_node('ConvTranspose',
                                 inputs=['x', 'w'],
                                 outputs=['y'],
                                 strides=[3, 2],
                                 output_padding=[1, 1])

    return ([node], [x, w], [y])


@onnx_test
def deconv_output_padding_3d_test():
    x = helper.make_tensor_value_info('x', TensorProto.FLOAT, [1, 1, 3, 3, 3])
    w = helper.make_tensor_value_info('w', TensorProto.FLOAT, [1, 2, 3, 3, 3])
    y = helper.make_tensor_value_info('y', TensorProto.FLOAT, [1, 2, 10, 8, 8])

    node = onnx.helper.make_node('ConvTranspose',
                                 inputs=['x', 'w'],
                                 outputs=['y'],
                                 strides=[3, 2, 2],
                                 output_padding=[1, 1, 1])

    return ([node], [x, w], [y])


@onnx_test
def deconv_output_shape_test():
    x = helper.make_tensor_value_info('x', TensorProto.FLOAT, [1, 1, 3, 3])
    w = helper.make_tensor_value_info('w', TensorProto.FLOAT, [1, 2, 3, 3])
    y = helper.make_tensor_value_info('y', TensorProto.FLOAT, [1, 2, 10, 8])

    node = onnx.helper.make_node('ConvTranspose',
                                 inputs=['x', 'w'],
                                 outputs=['y'],
                                 strides=[3, 2],
                                 output_shape=[10, 8])

    return ([node], [x, w], [y])


@onnx_test
def deconv_output_shape_3d_test():
    x = helper.make_tensor_value_info('x', TensorProto.FLOAT, [1, 1, 3, 3, 3])
    w = helper.make_tensor_value_info('w', TensorProto.FLOAT, [1, 2, 3, 3, 3])
    y = helper.make_tensor_value_info('y', TensorProto.FLOAT, [1, 2, 10, 8, 8])

    node = onnx.helper.make_node('ConvTranspose',
                                 inputs=['x', 'w'],
                                 outputs=['y'],
                                 strides=[3, 2, 2],
                                 output_shape=[10, 8, 8])

    return ([node], [x, w], [y])


@onnx_test
def deconv_stride_test():
    x = helper.make_tensor_value_info('x', TensorProto.FLOAT, [1, 1, 3, 3])
    w = helper.make_tensor_value_info('w', TensorProto.FLOAT, [1, 2, 3, 3])
    y = helper.make_tensor_value_info('y', TensorProto.FLOAT, [1, 2, 7, 3])

    node = onnx.helper.make_node('ConvTranspose',
                                 inputs=['x', 'w'],
                                 outputs=['y'],
                                 strides=[3, 2])

    return ([node], [x, w], [y])


@onnx_test
def depthtospace_test():

    x = helper.make_tensor_value_info('x', TensorProto.FLOAT, [2, 8, 5, 5])
    y = helper.make_tensor_value_info('y', TensorProto.FLOAT, [2, 2, 10, 10])

    node = onnx.helper.make_node('DepthToSpace',
                                 inputs=['x'],
                                 outputs=['y'],
                                 blocksize=2,
                                 mode='DCR')

    return ([node], [x], [y])


@onnx_test
def depthtospace_simple_test():

    x = helper.make_tensor_value_info('x', TensorProto.FLOAT, [1, 8, 2, 3])
    y = helper.make_tensor_value_info('y', TensorProto.FLOAT, [1, 2, 4, 6])

    node = onnx.helper.make_node('DepthToSpace',
                                 inputs=['x'],
                                 outputs=['y'],
                                 blocksize=2,
                                 mode='DCR')

    return ([node], [x], [y])


@onnx_test
def depthtospace_crd_test():

    x = helper.make_tensor_value_info('x', TensorProto.FLOAT, [2, 8, 5, 5])
    y = helper.make_tensor_value_info('y', TensorProto.FLOAT, [2, 2, 10, 10])

    node = onnx.helper.make_node('DepthToSpace',
                                 inputs=['x'],
                                 outputs=['y'],
                                 blocksize=2,
                                 mode='CRD')

    return ([node], [x], [y])


@onnx_test
def spacetodepth_test():

    x = helper.make_tensor_value_info('x', TensorProto.float, [2, 2, 10, 10])
    y = helper.make_tensor_value_info('y', TensorProto.float, [2, 8, 5, 5])

    node = onnx.helper.make_node('spacetodepth',
                                 inputs=['x'],
                                 outputs=['y'],
                                 blocksize=2)

    return ([node], [x], [y])


@onnx_test
def spacetodepth_simple_test():

    x = helper.make_tensor_value_info('x', TensorProto.FLOAT, [1, 2, 4, 6])
    y = helper.make_tensor_value_info('y', TensorProto.FLOAT, [1, 8, 2, 3])

    node = onnx.helper.make_node('SpaceToDepth',
                                 inputs=['x'],
                                 outputs=['y'],
                                 blocksize=2)

    return ([node], [x], [y])


@onnx_test
def spacetodepth_invalid_blocksize_test():

    x = helper.make_tensor_value_info('x', TensorProto.FLOAT, [1, 2, 4, 6])
    y = helper.make_tensor_value_info('y', TensorProto.FLOAT, [1, 8, 2, 3])

    node = onnx.helper.make_node('SpaceToDepth',
                                 inputs=['x'],
                                 outputs=['y'],
                                 blocksize=0.3)

    return ([node], [x], [y])


@onnx_test
def spacetodepth_nondivisibility_test():

    x = helper.make_tensor_value_info('x', TensorProto.FLOAT, [1, 2, 5, 5])
    y = helper.make_tensor_value_info('y', TensorProto.FLOAT, [1, 8, 2, 2])

    node = onnx.helper.make_node('SpaceToDepth',
                                 inputs=['x'],
                                 outputs=['y'],
                                 blocksize=2)

    return ([node], [x], [y])


@onnx_test
def dequantizelinear_test():
    arg0 = helper.make_tensor_value_info('0', TensorProto.INT8, [5])
    arg1 = helper.make_tensor_value_info('1', TensorProto.FLOAT, [1])
    arg_out = helper.make_tensor_value_info('out', TensorProto.FLOAT, [5])

    node = onnx.helper.make_node(
        'DequantizeLinear',
        inputs=['0', '1'],
        outputs=['out'],
    )

    return ([node], [arg0, arg1], [arg_out])


@onnx_test
def dequantizelinear_zero_point_test():
    arg0 = helper.make_tensor_value_info('0', TensorProto.INT8, [5])
    arg1 = helper.make_tensor_value_info('1', TensorProto.FLOAT, [1])
    arg2 = helper.make_tensor_value_info('2', TensorProto.INT8, [1])
    arg_out = helper.make_tensor_value_info('out', TensorProto.FLOAT, [5])

    node = onnx.helper.make_node(
        'DequantizeLinear',
        inputs=['0', '1', '2'],
        outputs=['out'],
    )

    return ([node], [arg0, arg1, arg2], [arg_out])


def make_dequantizelinear_axis_graph(axis):
    arg0 = helper.make_tensor_value_info('0', TensorProto.INT8, [1, 1, 5, 1])
    arg1 = helper.make_tensor_value_info('1', TensorProto.FLOAT, [5])
    arg2 = helper.make_tensor_value_info('2', TensorProto.INT8, [5])
    arg_out = helper.make_tensor_value_info('out', TensorProto.FLOAT,
                                            [1, 1, 5, 1])

    node = onnx.helper.make_node('DequantizeLinear',
                                 inputs=['0', '1', '2'],
                                 outputs=['out'],
                                 axis=axis)

    return ([node], [arg0, arg1, arg2], [arg_out])


@onnx_test
def dequantizelinear_axis_test():
    return make_dequantizelinear_axis_graph(2)


@onnx_test
def dequantizelinear_neg_axis_test():
    return make_dequantizelinear_axis_graph(-2)


@onnx_test
def dropout_test():
    x = helper.make_tensor_value_info('0', TensorProto.FLOAT, [1, 3, 2, 2])
    y = helper.make_tensor_value_info('1', TensorProto.FLOAT, [1, 3, 2, 2])

    node = onnx.helper.make_node(
        'Dropout',
        inputs=['0'],
        outputs=['1'],
    )

    return ([node], [x], [y])


@onnx_test
def elu_test():
    x = helper.make_tensor_value_info('0', TensorProto.FLOAT, [3])
    y = helper.make_tensor_value_info('1', TensorProto.FLOAT, [3])

    node = onnx.helper.make_node('Elu',
                                 inputs=['0'],
                                 outputs=['1'],
                                 alpha=0.01)

    return ([node], [x], [y])


@onnx_test
def embedding_bag_test():

    index_val = np.array([1, 0, 2])
    offset_val = np.array([0])

    index_tensor = helper.make_tensor(name='index_val',
                                      data_type=TensorProto.INT32,
                                      dims=index_val.shape,
                                      vals=index_val.astype(np.int32))

    index = onnx.helper.make_node('Constant',
                                  inputs=[],
                                  outputs=['index'],
                                  value=index_tensor)

    offset_tensor = helper.make_tensor(name='offset_val',
                                       data_type=TensorProto.INT32,
                                       dims=offset_val.reshape(()).shape,
                                       vals=offset_val.astype(np.int32))

    offset = onnx.helper.make_node('Constant',
                                   inputs=[],
                                   outputs=['offset'],
                                   value=offset_tensor)

    weight = helper.make_tensor_value_info('weight', TensorProto.FLOAT, [4, 2])

    y1 = helper.make_tensor_value_info('y1', TensorProto.FLOAT, [1, 2])
    y2 = helper.make_tensor_value_info('y2', TensorProto.FLOAT, [1, 2])
    y3 = helper.make_tensor_value_info('y3', TensorProto.FLOAT, [1, 2])

    node1 = onnx.helper.make_node('ATen',
                                  inputs=['weight', 'index', 'offset'],
                                  outputs=['y1'],
                                  mode=0,
                                  operator='embedding_bag')

    node2 = onnx.helper.make_node('ATen',
                                  inputs=['weight', 'index', 'offset'],
                                  outputs=['y2'],
                                  mode=1,
                                  operator='embedding_bag')

    node3 = onnx.helper.make_node('ATen',
                                  inputs=['weight', 'index', 'offset'],
                                  outputs=['y3'],
                                  mode=2,
                                  operator='embedding_bag')

    return ([index, offset, node1, node2, node3], [weight], [y1, y2, y3])


@onnx_test
def embedding_bag_offset_test():

    index_val = np.array([1, 0])
    offset_val = np.array([0, 1])

    index_tensor = helper.make_tensor(name='index_val',
                                      data_type=TensorProto.INT32,
                                      dims=index_val.shape,
                                      vals=index_val.astype(np.int32))

    index = onnx.helper.make_node('Constant',
                                  inputs=[],
                                  outputs=['index'],
                                  value=index_tensor)

    offset_tensor = helper.make_tensor(name='offset_val',
                                       data_type=TensorProto.INT32,
                                       dims=offset_val.shape,
                                       vals=offset_val.astype(np.int32))

    offset = onnx.helper.make_node('Constant',
                                   inputs=[],
                                   outputs=['offset'],
                                   value=offset_tensor)

    weight = helper.make_tensor_value_info('weight', TensorProto.FLOAT, [2, 3])

    y = helper.make_tensor_value_info('y', TensorProto.FLOAT, [2, 3])

    node = onnx.helper.make_node('ATen',
                                 inputs=['weight', 'index', 'offset'],
                                 outputs=['y'],
                                 mode=0,
                                 operator='embedding_bag')

    return ([index, offset, node], [weight], [y])


@onnx_test
def equal_test():
    ax1 = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0])
    x1 = helper.make_tensor("x1",
                            data_type=TensorProto.FLOAT,
                            dims=(2, 3),
                            vals=ax1.astype(np.float32))

    x2 = helper.make_tensor_value_info('x2', TensorProto.FLOAT, [2, 3])
    y = helper.make_tensor_value_info('y', TensorProto.FLOAT, [2, 3])

    node = onnx.helper.make_node(
        'Equal',
        inputs=['x1', 'x2'],
        outputs=['y'],
    )

    return ([node], [x2], [y], [x1])


@onnx_test
def equal_bool_test():

    x1 = helper.make_tensor_value_info('x1', TensorProto.FLOAT, [2, 3])
    x2 = helper.make_tensor_value_info('x2', TensorProto.BOOL, [2, 3])
    y = helper.make_tensor_value_info('y', TensorProto.FLOAT, [2, 3])

    node1 = onnx.helper.make_node('Cast', inputs=['x1'], outputs=['bx1'], to=9)

    node2 = onnx.helper.make_node(
        'Equal',
        inputs=['bx1', 'x2'],
        outputs=['y'],
    )

    return ([node1, node2], [x1, x2], [y])


@onnx_test
def erf_test():
    x = helper.make_tensor_value_info('x', TensorProto.FLOAT, [10, 15])
    y = helper.make_tensor_value_info('y', TensorProto.FLOAT, [10, 15])

    node = onnx.helper.make_node(
        'Erf',
        inputs=['x'],
        outputs=['y'],
    )

    return ([node], [x], [y])


@onnx_test
def exp_test():
    x = helper.make_tensor_value_info('x', TensorProto.FLOAT, [10])
    y = helper.make_tensor_value_info('y', TensorProto.FLOAT, [10])

    node = onnx.helper.make_node(
        'Exp',
        inputs=['x'],
        outputs=['y'],
    )

    return ([node], [x], [y])


@onnx_test
def expand_test():
    shape_val = np.array([2, 3, 4, 5]).astype(np.int64)
    shape_ts = helper.make_tensor(name='shape_tensor',
                                  data_type=TensorProto.INT32,
                                  dims=shape_val.shape,
                                  vals=shape_val.flatten().astype(int))
    shape_const = helper.make_node(
        'Constant',
        inputs=[],
        outputs=['shape'],
        value=shape_ts,
    )
    x = helper.make_tensor_value_info('x', TensorProto.FLOAT, [3, 1, 1])
    y = helper.make_tensor_value_info('y', TensorProto.FLOAT, [2, 3, 4, 5])

    node = onnx.helper.make_node('Expand',
                                 inputs=['x', 'shape'],
                                 outputs=['y'])

    return ([shape_const, node], [x], [y])


@onnx_test
def flatten_test():
    x = helper.make_tensor_value_info('0', TensorProto.FLOAT, [2, 3, 4, 5])
    y = helper.make_tensor_value_info('2', TensorProto.FLOAT, [6, 20])
    y2 = helper.make_tensor_value_info('3', TensorProto.FLOAT, [2, 60])

    node = onnx.helper.make_node('Flatten',
                                 inputs=['0'],
                                 axis=2,
                                 outputs=['2'])

    node2 = onnx.helper.make_node('Flatten', inputs=['0'], outputs=['3'])

    return ([node, node2], [x], [y, y2])


@onnx_test
def flatten_nonstd_test():
    x = helper.make_tensor_value_info('0', TensorProto.FLOAT, [2, 3, 5, 4])
    y = helper.make_tensor_value_info('2', TensorProto.FLOAT, [6, 20])
    y2 = helper.make_tensor_value_info('3', TensorProto.FLOAT, [2, 60])

    trans = helper.make_node(
        'Transpose',
        inputs=['0'],
        outputs=['tx'],
        perm=[0, 1, 3, 2],
    )

    node = onnx.helper.make_node('Flatten',
                                 inputs=['tx'],
                                 axis=2,
                                 outputs=['2'])

    node2 = onnx.helper.make_node('Flatten', inputs=['tx'], outputs=['3'])

    return ([trans, node, node2], [x], [y, y2])


@onnx_test
def floor_test():
    x = helper.make_tensor_value_info('x', TensorProto.FLOAT, [10])
    y = helper.make_tensor_value_info('y', TensorProto.FLOAT, [10])

    node = onnx.helper.make_node(
        'Floor',
        inputs=['x'],
        outputs=['y'],
    )

    return ([node], [x], [y])


@onnx_test
def gather_test():
    x = helper.make_tensor_value_info('data', TensorProto.FLOAT, [3, 4, 5, 6])
    i = helper.make_tensor_value_info('indices', TensorProto.INT32,
                                      [2, 3, 4, 5])
    y = helper.make_tensor_value_info('y', TensorProto.FLOAT, [2, 3, 4, 5])

    node = onnx.helper.make_node(
        'Gather',
        inputs=['data', 'indices'],
        outputs=['y'],
        axis=1,
    )

    return ([node], [x, i], [y])


@onnx_test
def gather_elements_axis0_test():
    x = helper.make_tensor_value_info('data', TensorProto.FLOAT, [3, 4])
    i = helper.make_tensor_value_info('indices', TensorProto.INT32, [2, 3])
    y = helper.make_tensor_value_info('y', TensorProto.FLOAT, [2, 3])

    node = onnx.helper.make_node(
        'GatherElements',
        inputs=['data', 'indices'],
        outputs=['y'],
        axis=0,
    )

    return ([node], [x, i], [y])


@onnx_test
def gather_elements_axis1_test():
    x = helper.make_tensor_value_info('data', TensorProto.FLOAT, [3, 4])
    i = helper.make_tensor_value_info('indices', TensorProto.INT32, [2, 3])
    y = helper.make_tensor_value_info('y', TensorProto.FLOAT, [2, 3])

    node = onnx.helper.make_node(
        'GatherElements',
        inputs=['data', 'indices'],
        outputs=['y'],
        axis=1,
    )

    return ([node], [x, i], [y])


@onnx_test
def gemm_test():
    x = helper.make_tensor_value_info('0', TensorProto.FLOAT, [5, 7])
    y = helper.make_tensor_value_info('1', TensorProto.FLOAT, [11, 5])
    z = helper.make_tensor_value_info('2', TensorProto.FLOAT, [])
    a = helper.make_tensor_value_info('3', TensorProto.FLOAT, [7, 11])

    node = onnx.helper.make_node('Gemm',
                                 inputs=['0', '1', '2'],
                                 outputs=['3'],
                                 alpha=2.0,
                                 beta=2.0,
                                 transA=1,
                                 transB=1)

    return ([node], [x, y, z], [a])


@onnx_test
def gemm_ex_test():
    m1 = helper.make_tensor_value_info('1', TensorProto.FLOAT, [1, 1, 8, 6])
    m2 = helper.make_tensor_value_info('2', TensorProto.FLOAT, [1, 1, 8, 7])
    m3 = helper.make_tensor_value_info('3', TensorProto.FLOAT, [1, 1, 6, 7])
    y = helper.make_tensor_value_info('y', TensorProto.FLOAT, [1, 1, 6, 7])

    node = onnx.helper.make_node('Gemm',
                                 inputs=['1', '2', '3'],
                                 outputs=['y'],
                                 alpha=0.5,
                                 beta=0.8,
                                 transA=1)

    return ([node], [m1, m2, m3], [y])


@onnx_test
def gemm_ex_brcst_test():
    m1 = helper.make_tensor_value_info('1', TensorProto.FLOAT, [1, 1, 5, 6])
    m2 = helper.make_tensor_value_info('2', TensorProto.FLOAT, [1, 1, 5, 7])
    m3 = helper.make_tensor_value_info('3', TensorProto.FLOAT, [1, 1, 6, 1])
    y = helper.make_tensor_value_info('y', TensorProto.FLOAT, [1, 1, 6, 7])

    node = onnx.helper.make_node('Gemm',
                                 inputs=['1', '2', '3'],
                                 outputs=['y'],
                                 alpha=0.5,
                                 beta=0.8,
                                 transA=1)

    return ([node], [m1, m2, m3], [y])


@onnx_test
def gemm_half_test():
    m1 = helper.make_tensor_value_info('1', TensorProto.FLOAT16, [1, 1, 8, 6])
    m2 = helper.make_tensor_value_info('2', TensorProto.FLOAT16, [1, 1, 8, 7])
    m3 = helper.make_tensor_value_info('3', TensorProto.FLOAT16, [1, 1, 6, 1])
    y = helper.make_tensor_value_info('y', TensorProto.FLOAT16, [1, 1, 6, 7])

    node = onnx.helper.make_node('Gemm',
                                 inputs=['1', '2', '3'],
                                 outputs=['y'],
                                 alpha=0.5,
                                 beta=0.8,
                                 transA=1)

    return ([node], [m1, m2, m3], [y])


@onnx_test
def globalavgpool_test():
    x = helper.make_tensor_value_info('0', TensorProto.FLOAT, [1, 3, 16, 16])
    y = helper.make_tensor_value_info('1', TensorProto.FLOAT, [1, 3, 1, 1])

    node = onnx.helper.make_node(
        'GlobalAveragePool',
        inputs=['0'],
        outputs=['1'],
    )

    return ([node], [x], [y])


@onnx_test
def globalmaxpool_test():
    x = helper.make_tensor_value_info('0', TensorProto.FLOAT, [1, 3, 16, 16])
    y = helper.make_tensor_value_info('1', TensorProto.FLOAT, [1, 3, 1, 1])

    node = onnx.helper.make_node(
        'GlobalMaxPool',
        inputs=['0'],
        outputs=['1'],
    )

    return ([node], [x], [y])


@onnx_test
def greater_test():
    ax1 = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0])
    x1 = helper.make_tensor("x1",
                            data_type=TensorProto.FLOAT,
                            dims=(2, 3),
                            vals=ax1.astype(np.float32))

    x2 = helper.make_tensor_value_info('x2', TensorProto.FLOAT, [2, 3])
    y = helper.make_tensor_value_info('y', TensorProto.FLOAT, [2, 3])

    node = onnx.helper.make_node(
        'Greater',
        inputs=['x1', 'x2'],
        outputs=['y'],
    )

    return ([node], [x2], [y], [x1])


@onnx_test
def greater_bool_test():

    x1 = helper.make_tensor_value_info('x1', TensorProto.FLOAT, [2, 3])
    x2 = helper.make_tensor_value_info('x2', TensorProto.BOOL, [2, 3])
    y = helper.make_tensor_value_info('y', TensorProto.FLOAT, [2, 3])

    node1 = onnx.helper.make_node('Cast', inputs=['x1'], outputs=['bx1'], to=9)

    node2 = onnx.helper.make_node(
        'Greater',
        inputs=['bx1', 'x2'],
        outputs=['y'],
    )

    return ([node1, node2], [x1, x2], [y])


@onnx_test
def greaterorequal_test():

    x1 = helper.make_tensor_value_info('x1', TensorProto.FLOAT, [3])
    x2 = helper.make_tensor_value_info('x2', TensorProto.FLOAT, [3])
    y = helper.make_tensor_value_info('y', TensorProto.FLOAT, [3])

    node = onnx.helper.make_node(
        'GreaterOrEqual',
        inputs=['x1', 'x2'],
        outputs=['y'],
    )

    return ([node], [x1, x2], [y])


@onnx_test
def group_conv_test():
    x = helper.make_tensor_value_info('0', TensorProto.FLOAT, [1, 4, 16, 16])
    y = helper.make_tensor_value_info('1', TensorProto.FLOAT, [4, 1, 3, 3])
    z = helper.make_tensor_value_info('2', TensorProto.FLOAT, [1, 4, 14, 14])

    node = onnx.helper.make_node(
        'Conv',
        inputs=['0', '1'],
        group=4,
        outputs=['2'],
    )

    return ([node], [x, y], [z])


@onnx_test
def hardsigmoid_default_test():
    x = helper.make_tensor_value_info('x', TensorProto.FLOAT, [1, 3, 4, 5])
    y = helper.make_tensor_value_info('y', TensorProto.FLOAT, [1, 3, 4, 5])

    node = onnx.helper.make_node('HardSigmoid', inputs=['x'], outputs=['y'])

    return ([node], [x], [y])


@onnx_test
def hardsigmoid_double_test():
    x = helper.make_tensor_value_info('x', TensorProto.DOUBLE, [1, 3, 4, 5])
    y = helper.make_tensor_value_info('y', TensorProto.DOUBLE, [1, 3, 4, 5])

    node = onnx.helper.make_node('HardSigmoid',
                                 inputs=['x'],
                                 outputs=['y'],
                                 alpha=0.3,
                                 beta=0.7)

    return ([node], [x], [y])


@onnx_test
def hardsigmoid_half_test():
    x = helper.make_tensor_value_info('x', TensorProto.FLOAT16, [1, 3, 4, 5])
    y = helper.make_tensor_value_info('y', TensorProto.FLOAT16, [1, 3, 4, 5])

    node = onnx.helper.make_node('HardSigmoid', inputs=['x'], outputs=['y'])

    return ([node], [x], [y])


@onnx_test
def hardsigmoid_verify_test():
    x = helper.make_tensor_value_info('x', TensorProto.FLOAT, [2, 5])
    y = helper.make_tensor_value_info('y', TensorProto.FLOAT, [2, 5])

    node = onnx.helper.make_node('HardSigmoid', inputs=['x'], outputs=['y'])

    return ([node], [x], [y])


@onnx_test
def if_else_test():
    x = onnx.helper.make_tensor_value_info('x', onnx.TensorProto.FLOAT, [2, 3])
    y = onnx.helper.make_tensor_value_info('y', onnx.TensorProto.FLOAT, [2, 3])

    then_out = onnx.helper.make_tensor_value_info('then_out',
                                                  onnx.TensorProto.FLOAT,
                                                  [2, 3])
    else_out = onnx.helper.make_tensor_value_info('else_out',
                                                  onnx.TensorProto.FLOAT,
                                                  [2, 3])

    xt = np.ones((2, 3)).astype(np.float)
    xt_tensor = helper.make_tensor(name='xt',
                                   data_type=TensorProto.FLOAT,
                                   dims=xt.shape,
                                   vals=xt.flatten().astype(np.float32))

    yt = np.random.randn(2, 3).astype(np.float)
    yt_tensor = helper.make_tensor(name='yt',
                                   data_type=TensorProto.FLOAT,
                                   dims=yt.shape,
                                   vals=yt.flatten().astype(np.float32))

    then_add_node = onnx.helper.make_node('Add',
                                          inputs=['x', 'xt'],
                                          outputs=['then_out'])

    else_mul_node = onnx.helper.make_node('Mul',
                                          inputs=['y', 'yt'],
                                          outputs=['else_out'])

    then_body = onnx.helper.make_graph([then_add_node], 'then_body', [],
                                       [then_out])

    else_body = onnx.helper.make_graph([else_mul_node], 'else_body', [],
                                       [else_out])

    cond = np.array([0]).astype(np.bool)
    cond_tensor = helper.make_tensor(name="cond",
                                     data_type=TensorProto.BOOL,
                                     dims=cond.shape,
                                     vals=cond.astype(bool))
    res = onnx.helper.make_tensor_value_info('res', TensorProto.FLOAT, [])

    node = onnx.helper.make_node('If',
                                 inputs=['cond'],
                                 outputs=['res'],
                                 then_branch=then_body,
                                 else_branch=else_body)

    return ([node], [x, y], [res], [cond_tensor, xt_tensor, yt_tensor])


@onnx_test
def if_literal_test():
    then_out = onnx.helper.make_tensor_value_info('then_out',
                                                  onnx.TensorProto.FLOAT, [5])
    else_out = onnx.helper.make_tensor_value_info('else_out',
                                                  onnx.TensorProto.FLOAT, [5])

    x = np.array([1, 2, 3, 4, 5]).astype(np.float32)
    y = np.array([5, 4, 3, 2, 1]).astype(np.float32)
    z = np.array([]).astype(np.float32)

    then_const_node = onnx.helper.make_node(
        'Constant',
        inputs=[],
        outputs=['then_out'],
        value=onnx.numpy_helper.from_array(x))

    else_const_node = onnx.helper.make_node(
        'Constant',
        inputs=[],
        outputs=['else_out'],
        value=onnx.numpy_helper.from_array(y))

    empty_const_node = onnx.helper.make_node(
        'Constant',
        inputs=[],
        outputs=['empty_out'],
        value=onnx.numpy_helper.from_array(z))

    then_body = onnx.helper.make_graph([then_const_node, empty_const_node],
                                       'then_body', [], [then_out])

    else_body = onnx.helper.make_graph([else_const_node, empty_const_node],
                                       'else_body', [], [else_out])

    cond_input = onnx.helper.make_tensor_value_info('cond',
                                                    onnx.TensorProto.BOOL, [])
    ret = onnx.helper.make_tensor_value_info('ret', TensorProto.FLOAT, [])

    node = onnx.helper.make_node('If',
                                 inputs=['cond'],
                                 outputs=['ret'],
                                 then_branch=then_body,
                                 else_branch=else_body)

    return ([node], [cond_input], [ret])


@onnx_test
def if_param_excp_test():
    then_out = onnx.helper.make_tensor_value_info('then_out',
                                                  onnx.TensorProto.FLOAT,
                                                  [2, 3])
    else_out = onnx.helper.make_tensor_value_info('else_out',
                                                  onnx.TensorProto.FLOAT,
                                                  [2, 3])

    x = onnx.helper.make_tensor_value_info('x', onnx.TensorProto.FLOAT, [2, 3])
    y = onnx.helper.make_tensor_value_info('y', onnx.TensorProto.FLOAT, [2, 4])

    yt = np.random.randn(2, 4).astype(np.float)
    xt = np.random.randn(2, 3).astype(np.float)

    xt_tensor = helper.make_tensor(name='xt',
                                   data_type=TensorProto.FLOAT,
                                   dims=xt.shape,
                                   vals=xt.flatten().astype(np.float32))

    yt_tensor = helper.make_tensor(name='yt',
                                   data_type=TensorProto.FLOAT,
                                   dims=yt.shape,
                                   vals=yt.flatten().astype(np.float32))

    then_add_node = onnx.helper.make_node('Add',
                                          inputs=['x', 'xt'],
                                          outputs=['then_out'])

    else_mul_node = onnx.helper.make_node('Mul',
                                          inputs=['y', 'yt'],
                                          outputs=['else_out'])

    then_body = onnx.helper.make_graph([then_add_node], 'then_body', [],
                                       [then_out], [xt_tensor])

    else_body = onnx.helper.make_graph([else_mul_node], 'else_body', [],
                                       [else_out], [yt_tensor])

    cond_input = onnx.helper.make_tensor_value_info('cond',
                                                    onnx.TensorProto.BOOL, [])
    ret = onnx.helper.make_tensor_value_info('ret', TensorProto.FLOAT, [])

    node = onnx.helper.make_node('If',
                                 inputs=['cond'],
                                 outputs=['ret'],
                                 then_branch=then_body,
                                 else_branch=else_body)

    return ([node], [cond_input, x, y], [ret])


@onnx_test
def if_param_excp1_test():
    then_out = onnx.helper.make_tensor_value_info('sub_out',
                                                  onnx.TensorProto.FLOAT,
                                                  [2, 3])

    x = onnx.helper.make_tensor_value_info('x', onnx.TensorProto.FLOAT, [2, 3])

    xt = np.random.randn(2, 3).astype(np.float)

    xt_tensor = helper.make_tensor(name='xt',
                                   data_type=TensorProto.FLOAT,
                                   dims=xt.shape,
                                   vals=xt.flatten().astype(np.float32))

    then_add_node = onnx.helper.make_node('Add',
                                          inputs=['x', 'xt'],
                                          outputs=['sub_out'])

    sub_body = onnx.helper.make_graph([then_add_node], 'sub_body', [],
                                      [then_out], [xt_tensor])

    cond_input = onnx.helper.make_tensor_value_info('cond',
                                                    onnx.TensorProto.BOOL, [2])
    ret = onnx.helper.make_tensor_value_info('ret', TensorProto.FLOAT, [])

    node = onnx.helper.make_node('If',
                                 inputs=['cond'],
                                 outputs=['ret'],
                                 then_branch=sub_body,
                                 else_branch=sub_body)

    return ([node], [cond_input, x], [ret])


@onnx_test
def if_param_test():
    then_out = onnx.helper.make_tensor_value_info('then_out',
                                                  onnx.TensorProto.FLOAT,
                                                  [2, 3])
    else_out = onnx.helper.make_tensor_value_info('else_out',
                                                  onnx.TensorProto.FLOAT,
                                                  [2, 3])

    x = onnx.helper.make_tensor_value_info('x', onnx.TensorProto.FLOAT, [2, 3])
    y = onnx.helper.make_tensor_value_info('y', onnx.TensorProto.FLOAT, [2, 3])

    yt = np.random.randn(2, 3).astype(np.float)
    xt = np.random.randn(2, 3).astype(np.float)

    xt_tensor = helper.make_tensor(name='xt',
                                   data_type=TensorProto.FLOAT,
                                   dims=xt.shape,
                                   vals=xt.flatten().astype(np.float32))

    yt_tensor = helper.make_tensor(name='yt',
                                   data_type=TensorProto.FLOAT,
                                   dims=yt.shape,
                                   vals=yt.flatten().astype(np.float32))

    then_add_node = onnx.helper.make_node('Add',
                                          inputs=['x', 'xt'],
                                          outputs=['then_out'])

    else_mul_node = onnx.helper.make_node('Mul',
                                          inputs=['y', 'yt'],
                                          outputs=['else_out'])

    then_body = onnx.helper.make_graph([then_add_node], 'then_body', [],
                                       [then_out], [xt_tensor])

    else_body = onnx.helper.make_graph([else_mul_node], 'else_body', [],
                                       [else_out], [yt_tensor])

    cond_input = onnx.helper.make_tensor_value_info('cond',
                                                    onnx.TensorProto.BOOL, [])
    ret = onnx.helper.make_tensor_value_info('ret', TensorProto.FLOAT, [])

    node = onnx.helper.make_node('If',
                                 inputs=['cond'],
                                 outputs=['ret'],
                                 then_branch=then_body,
                                 else_branch=else_body)

    return ([node], [cond_input, x, y], [ret])


@onnx_test
def if_pl_test():
    out_x = onnx.helper.make_tensor_value_info('out_x', onnx.TensorProto.FLOAT,
                                               [2, 3])
    out_l_x = onnx.helper.make_tensor_value_info('out_l_x',
                                                 onnx.TensorProto.FLOAT,
                                                 [2, 3])
    out_y = onnx.helper.make_tensor_value_info('out_y', onnx.TensorProto.FLOAT,
                                               [3, 3])
    out_l_y = onnx.helper.make_tensor_value_info('out_l_y',
                                                 onnx.TensorProto.FLOAT,
                                                 [3, 3])

    x = onnx.helper.make_tensor_value_info('x', onnx.TensorProto.FLOAT, [2, 3])
    y = onnx.helper.make_tensor_value_info('y', onnx.TensorProto.FLOAT, [3, 3])

    xt = np.array([[1, 2, 3], [4, 5, 6]]).astype(np.float32)
    yt = np.array([[8, 7, 6], [5, 4, 3], [2, 1, 0]]).astype(np.float32)

    xt_tensor = helper.make_tensor(name='xt',
                                   data_type=TensorProto.FLOAT,
                                   dims=xt.shape,
                                   vals=xt.flatten().astype(np.float32))

    yt_tensor = helper.make_tensor(name='yt',
                                   data_type=TensorProto.FLOAT,
                                   dims=yt.shape,
                                   vals=yt.flatten().astype(np.float32))

    then_add_node = onnx.helper.make_node('Add',
                                          inputs=['x', 'xt'],
                                          outputs=['out_x'])

    else_mul_node = onnx.helper.make_node('Mul',
                                          inputs=['y', 'yt'],
                                          outputs=['out_y'])

    then_const_node = onnx.helper.make_node(
        'Constant',
        inputs=[],
        outputs=['out_l_y'],
        value=onnx.numpy_helper.from_array(yt))

    else_const_node = onnx.helper.make_node(
        'Constant',
        inputs=[],
        outputs=['out_l_x'],
        value=onnx.numpy_helper.from_array(xt))

    then_body = onnx.helper.make_graph([then_add_node, then_const_node],
                                       'then_body', [], [out_x, out_l_y])

    else_body = onnx.helper.make_graph([else_mul_node, else_const_node],
                                       'else_body', [], [out_l_x, out_y])

    cond_input = onnx.helper.make_tensor_value_info('cond',
                                                    onnx.TensorProto.BOOL, [])
    ret = onnx.helper.make_tensor_value_info('ret', TensorProto.FLOAT, [])

    node = onnx.helper.make_node('If',
                                 inputs=['cond'],
                                 outputs=['ret'],
                                 then_branch=then_body,
                                 else_branch=else_body)

    return ([node], [cond_input, x, y], [ret], [xt_tensor, yt_tensor])


@onnx_test
def if_then_test():
    x = onnx.helper.make_tensor_value_info('x', onnx.TensorProto.FLOAT, [2, 3])
    y = onnx.helper.make_tensor_value_info('y', onnx.TensorProto.FLOAT, [2, 3])

    then_out = onnx.helper.make_tensor_value_info('then_out',
                                                  onnx.TensorProto.FLOAT,
                                                  [2, 3])
    else_out = onnx.helper.make_tensor_value_info('else_out',
                                                  onnx.TensorProto.FLOAT,
                                                  [2, 3])

    xt = np.ones((2, 3)).astype(np.float)
    xt_tensor = helper.make_tensor(name='xt',
                                   data_type=TensorProto.FLOAT,
                                   dims=xt.shape,
                                   vals=xt.flatten().astype(np.float32))

    yt = np.random.randn(2, 3).astype(np.float)
    yt_tensor = helper.make_tensor(name='yt',
                                   data_type=TensorProto.FLOAT,
                                   dims=yt.shape,
                                   vals=yt.flatten().astype(np.float32))

    then_add_node = onnx.helper.make_node('Add',
                                          inputs=['x', 'xt'],
                                          outputs=['then_out'])

    else_mul_node = onnx.helper.make_node('Mul',
                                          inputs=['y', 'yt'],
                                          outputs=['else_out'])

    then_body = onnx.helper.make_graph([then_add_node], 'then_body', [],
                                       [then_out])

    else_body = onnx.helper.make_graph([else_mul_node], 'else_body', [],
                                       [else_out])

    cond = np.array([1]).astype(np.bool)
    cond_tensor = helper.make_tensor(name="cond",
                                     data_type=TensorProto.BOOL,
                                     dims=cond.shape,
                                     vals=cond.astype(bool))
    res = onnx.helper.make_tensor_value_info('res', TensorProto.FLOAT, [])

    node = onnx.helper.make_node('If',
                                 inputs=['cond'],
                                 outputs=['res'],
                                 then_branch=then_body,
                                 else_branch=else_body)

    return ([node], [x, y], [res], [cond_tensor, xt_tensor, yt_tensor])


@onnx_test
def if_tuple_test():
    x = onnx.helper.make_tensor_value_info('x', onnx.TensorProto.FLOAT, [1, 4])
    y = onnx.helper.make_tensor_value_info('y', onnx.TensorProto.FLOAT, [3, 4])
    cond_input = onnx.helper.make_tensor_value_info('cond',
                                                    onnx.TensorProto.BOOL, [])

    then_out0 = onnx.helper.make_tensor_value_info('then_out0',
                                                   onnx.TensorProto.FLOAT,
                                                   [1, 4])
    then_out1 = onnx.helper.make_tensor_value_info('then_out1',
                                                   onnx.TensorProto.FLOAT,
                                                   [3, 4])
    else_out0 = onnx.helper.make_tensor_value_info('else_out0',
                                                   onnx.TensorProto.FLOAT,
                                                   [1, 4])
    else_out1 = onnx.helper.make_tensor_value_info('else_out1',
                                                   onnx.TensorProto.FLOAT,
                                                   [3, 4])

    one = np.ones([1]).astype(np.float)
    one_tensor = helper.make_tensor(name='one',
                                    data_type=TensorProto.FLOAT,
                                    dims=one.shape,
                                    vals=one.flatten().astype(np.float32))

    two = np.array([2]).astype(np.float)
    two_tensor = helper.make_tensor(name='two',
                                    data_type=TensorProto.FLOAT,
                                    dims=two.shape,
                                    vals=two.flatten().astype(np.float32))

    three = np.array([3]).astype(np.float)
    three_tensor = helper.make_tensor(name='three',
                                      data_type=TensorProto.FLOAT,
                                      dims=three.shape,
                                      vals=three.flatten().astype(np.float32))

    then_add_node = onnx.helper.make_node('Add',
                                          inputs=['x', 'one'],
                                          outputs=['then_out0'])
    then_mul_node = onnx.helper.make_node('Mul',
                                          inputs=['y', 'two'],
                                          outputs=['then_out1'])

    else_mul_node = onnx.helper.make_node('Mul',
                                          inputs=['x', 'three'],
                                          outputs=['else_out0'])
    else_add_node = onnx.helper.make_node('Add',
                                          inputs=['y', 'three'],
                                          outputs=['else_out1'])

    then_body = onnx.helper.make_graph([then_add_node, then_mul_node],
                                       'then_body', [], [then_out0, then_out1])

    else_body = onnx.helper.make_graph([else_mul_node, else_add_node],
                                       'else_body', [], [else_out0, else_out1])

    res0 = onnx.helper.make_tensor_value_info('res0', TensorProto.FLOAT, [])
    res1 = onnx.helper.make_tensor_value_info('res1', TensorProto.FLOAT, [])

    node = onnx.helper.make_node('If',
                                 inputs=['cond'],
                                 outputs=['res0', 'res1'],
                                 then_branch=then_body,
                                 else_branch=else_body)

    return ([node], [cond_input, x,
                     y], [res0, res1], [one_tensor, two_tensor, three_tensor])


@onnx_test
def imagescaler_test():
    x = helper.make_tensor_value_info('0', TensorProto.FLOAT, [1, 3, 16, 16])
    y = helper.make_tensor_value_info('1', TensorProto.FLOAT, [1, 3, 16, 16])

    node = onnx.helper.make_node('ImageScaler',
                                 inputs=['0'],
                                 outputs=['1'],
                                 bias=[0.01, 0.02, 0.03],
                                 scale=0.5)

    return ([node], [x], [y])


@onnx_test
def imagescaler_half_test():
    x = helper.make_tensor_value_info('0', TensorProto.FLOAT16, [1, 3, 16, 16])
    y = helper.make_tensor_value_info('1', TensorProto.FLOAT16, [1, 3, 16, 16])

    node = onnx.helper.make_node('ImageScaler',
                                 inputs=['0'],
                                 outputs=['1'],
                                 bias=[0.01, 0.02, 0.03],
                                 scale=0.5)

    return ([node], [x], [y])


@onnx_test
def implicit_add_bcast_test():
    x = helper.make_tensor_value_info('0', TensorProto.FLOAT, [2, 3, 4, 5])
    y = helper.make_tensor_value_info('1', TensorProto.FLOAT, [3, 4, 1])
    z = helper.make_tensor_value_info('2', TensorProto.FLOAT, [2, 3, 4, 5])

    node = onnx.helper.make_node(
        'Add',
        inputs=['0', '1'],
        outputs=['2'],
    )

    return ([node], [x, y], [z])


@onnx_test
def implicit_pow_bcast_test():
    arg0 = helper.make_tensor_value_info('0', TensorProto.FLOAT, [2, 3, 4, 5])
    arg1 = helper.make_tensor_value_info('1', TensorProto.FLOAT, [3, 4, 1])
    arg_out = helper.make_tensor_value_info('out', TensorProto.FLOAT,
                                            [2, 3, 4, 5])

    node = onnx.helper.make_node(
        'Pow',
        inputs=['0', '1'],
        outputs=['out'],
    )

    return ([node], [arg0, arg1], [arg_out])


@onnx_test
def implicit_sub_bcast_test():
    arg0 = helper.make_tensor_value_info('0', TensorProto.UINT64, [2, 3, 4, 5])
    arg1 = helper.make_tensor_value_info('1', TensorProto.UINT64, [4, 5])
    arg_out = helper.make_tensor_value_info('out', TensorProto.UINT64,
                                            [2, 3, 4, 5])

    node = onnx.helper.make_node(
        'Sub',
        inputs=['0', '1'],
        outputs=['out'],
    )

    return ([node], [arg0, arg1], [arg_out])


@onnx_test
def initializer_not_an_input():
    values = np.array([[1, 2, 3, 4], [5, 6, 7, 8]])
    w = helper.make_tensor(name='w',
                           data_type=TensorProto.FLOAT,
                           dims=values.shape,
                           vals=values.flatten().astype(np.float))

    x = helper.make_tensor_value_info('x', TensorProto.FLOAT, [5, 2])
    y = helper.make_tensor_value_info('y', TensorProto.FLOAT, [5, 4])

    node = onnx.helper.make_node(
        'Gemm',
        inputs=['x', 'w'],
        outputs=['y'],
    )

    return ([node], [x], [y], [w])


@onnx_test
def instance_norm_test():
    x = helper.make_tensor_value_info('0', TensorProto.FLOAT, [1, 2, 3, 3])
    scale = helper.make_tensor_value_info('1', TensorProto.FLOAT, [2])
    bias = helper.make_tensor_value_info('2', TensorProto.FLOAT, [2])
    y = helper.make_tensor_value_info('3', TensorProto.FLOAT, [1, 2, 3, 3])

    node = onnx.helper.make_node('InstanceNormalization',
                                 inputs=['0', '1', '2'],
                                 outputs=['3'])

    return ([node], [x, scale, bias], [y])


@onnx_test
def instance_norm_val_test():
    x = np.array([[[[0, 1, 2], [3, 4, 5], [6, 7, 8]],
                   [[0, 1, 2], [3, 4, 5], [6, 7, 8]]]])
    scale = np.array([1, 2])
    bias = np.array([0, 1])

    x_tensor = helper.make_tensor(name='x_tensor',
                                  data_type=TensorProto.FLOAT,
                                  dims=x.shape,
                                  vals=x.flatten().astype(np.float))
    scale_tensor = helper.make_tensor(name='scale_tensor',
                                      data_type=TensorProto.FLOAT,
                                      dims=scale.shape,
                                      vals=scale.flatten().astype(np.float))
    bias_tensor = helper.make_tensor(name='bias_tensor',
                                     data_type=TensorProto.FLOAT,
                                     dims=bias.shape,
                                     vals=bias.flatten().astype(np.float))

    y = helper.make_tensor_value_info('y', TensorProto.FLOAT, [1, 2, 3, 3])

    node = onnx.helper.make_node(
        'InstanceNormalization',
        inputs=['x_tensor', 'scale_tensor', 'bias_tensor'],
        outputs=['y'])

    return ([node], [], [y], [x_tensor, scale_tensor, bias_tensor])


@onnx_test
def instance_norm_val_3d_test():
    x = np.array([[[[[0, 1], [2, 3]], [[4, 5], [6, 7]]],
                   [[[0, 1], [2, 3]], [[4, 5], [6, 7]]]]])
    scale = np.array([1, 2])
    bias = np.array([0, 1])

    x_tensor = helper.make_tensor(name='x_tensor',
                                  data_type=TensorProto.FLOAT,
                                  dims=x.shape,
                                  vals=x.flatten().astype(np.float))
    scale_tensor = helper.make_tensor(name='scale_tensor',
                                      data_type=TensorProto.FLOAT,
                                      dims=scale.shape,
                                      vals=scale.flatten().astype(np.float))
    bias_tensor = helper.make_tensor(name='bias_tensor',
                                     data_type=TensorProto.FLOAT,
                                     dims=bias.shape,
                                     vals=bias.flatten().astype(np.float))

    y = helper.make_tensor_value_info('y', TensorProto.FLOAT, [1, 2, 2, 2, 2])

    node = onnx.helper.make_node(
        'InstanceNormalization',
        inputs=['x_tensor', 'scale_tensor', 'bias_tensor'],
        outputs=['y'])

    return ([node], [], [y], [x_tensor, scale_tensor, bias_tensor])


@onnx_test
def layernorm_test():
    x = helper.make_tensor_value_info('0', TensorProto.FLOAT, [1, 1, 5])
    y = helper.make_tensor_value_info('1', TensorProto.FLOAT, [1, 1, 5])
    scale = helper.make_tensor_value_info('scale', TensorProto.FLOAT, [5])
    bias = helper.make_tensor_value_info('bias', TensorProto.FLOAT, [5])
    axes = [2]
    pow_2 = np.array([[[2, 2, 2, 2, 2]]])
    epsilon = np.array([1e-12])

    pow_tensor = helper.make_tensor(name='pow',
                                    data_type=TensorProto.FLOAT,
                                    dims=pow_2.shape,
                                    vals=pow_2.flatten().astype(np.float))

    epsilon_tensor = helper.make_tensor(name='epsilon',
                                        data_type=TensorProto.FLOAT,
                                        dims=epsilon.shape,
                                        vals=epsilon.flatten().astype(
                                            np.float))

    mean = onnx.helper.make_node('ReduceMean',
                                 inputs=['0'],
                                 outputs=['mean_out'],
                                 axes=axes)

    sub_mean = onnx.helper.make_node('Sub',
                                     inputs=['0', 'mean_out'],
                                     outputs=['sub_out'])

    sub_pow = onnx.helper.make_node('Pow',
                                    inputs=['sub_out', 'pow'],
                                    outputs=['pow_out'])

    var = onnx.helper.make_node('ReduceMean',
                                inputs=['pow_out'],
                                outputs=['var_out'],
                                axes=axes)

    add = onnx.helper.make_node('Add',
                                inputs=['var_out', 'epsilon'],
                                outputs=['add_out'])

    sqrt = onnx.helper.make_node('Sqrt',
                                 inputs=['add_out'],
                                 outputs=['sqrt_out'])

    div = onnx.helper.make_node('Div',
                                inputs=['sub_out', 'sqrt_out'],
                                outputs=['div_out'])

    mul = onnx.helper.make_node('Mul',
                                inputs=['scale', 'div_out'],
                                outputs=['mul_out'])

    bias_add = onnx.helper.make_node('Add',
                                     inputs=['mul_out', 'bias'],
                                     outputs=['1'])

    return ([mean, sub_mean, sub_pow, var, add, sqrt, div, mul,
             bias_add], [x, scale, bias], [y], [pow_tensor, epsilon_tensor])


@onnx_test
def leaky_relu_test():
    x = helper.make_tensor_value_info('0', TensorProto.FLOAT, [3])
    y = helper.make_tensor_value_info('1', TensorProto.FLOAT, [3])

    node = onnx.helper.make_node('LeakyRelu',
                                 inputs=['0'],
                                 outputs=['1'],
                                 alpha=0.01)

    return ([node], [x], [y])


@onnx_test
def less_test():
    ax1 = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0])
    x1 = helper.make_tensor("x1",
                            data_type=TensorProto.FLOAT,
                            dims=(2, 3),
                            vals=ax1.astype(np.float32))

    x2 = helper.make_tensor_value_info('x2', TensorProto.FLOAT, [2, 3])
    y = helper.make_tensor_value_info('y', TensorProto.FLOAT, [2, 3])

    node = onnx.helper.make_node(
        'Less',
        inputs=['x1', 'x2'],
        outputs=['y'],
    )

    return ([node], [x2], [y], [x1])


@onnx_test
def less_bool_test():

    x1 = helper.make_tensor_value_info('x1', TensorProto.FLOAT, [2, 3])
    x2 = helper.make_tensor_value_info('x2', TensorProto.BOOL, [2, 3])
    y = helper.make_tensor_value_info('y', TensorProto.FLOAT, [2, 3])

    node1 = onnx.helper.make_node('Cast', inputs=['x1'], outputs=['bx1'], to=9)

    node2 = onnx.helper.make_node(
        'Less',
        inputs=['bx1', 'x2'],
        outputs=['y'],
    )

    return ([node1, node2], [x1, x2], [y])


@onnx_test
def lessorequal_test():

    x1 = helper.make_tensor_value_info('x1', TensorProto.FLOAT, [3])
    x2 = helper.make_tensor_value_info('x2', TensorProto.FLOAT, [3])
    y = helper.make_tensor_value_info('y', TensorProto.FLOAT, [3])

    node = onnx.helper.make_node(
        'LessOrEqual',
        inputs=['x1', 'x2'],
        outputs=['y'],
    )

    return ([node], [x1, x2], [y])


@onnx_test
def log_test():
    x = helper.make_tensor_value_info('x', TensorProto.FLOAT, [10])
    y = helper.make_tensor_value_info('y', TensorProto.FLOAT, [10])

    node = onnx.helper.make_node(
        'Log',
        inputs=['x'],
        outputs=['y'],
    )

    return ([node], [x], [y])


@onnx_test
def logical_and_bcast_test():
    x = helper.make_tensor_value_info('0', TensorProto.BOOL, [2, 3, 4, 5])
    y = helper.make_tensor_value_info('1', TensorProto.BOOL, [4, 5])
    z = helper.make_tensor_value_info('2', TensorProto.BOOL, [2, 3, 4, 5])

    node = onnx.helper.make_node('And', inputs=['0', '1'], outputs=['2'])

    return ([node], [x, y], [z])


@onnx_test
def logical_or_test():
    x = helper.make_tensor_value_info('0', TensorProto.BOOL, [2, 3, 4, 5])
    y = helper.make_tensor_value_info('1', TensorProto.BOOL, [2, 3, 4, 5])
    z = helper.make_tensor_value_info('2', TensorProto.BOOL, [2, 3, 4, 5])

    node = onnx.helper.make_node('Or', inputs=['0', '1'], outputs=['2'])

    return ([node], [x, y], [z])


@onnx_test
def logical_xor_bcast_test():
    x = helper.make_tensor_value_info('0', TensorProto.BOOL, [2, 3, 4, 5])
    y = helper.make_tensor_value_info('1', TensorProto.BOOL, [4, 1])
    z = helper.make_tensor_value_info('2', TensorProto.BOOL, [2, 3, 4, 5])

    node = onnx.helper.make_node('Xor', inputs=['0', '1'], outputs=['2'])

    return ([node], [x, y], [z])


@onnx_test
def logsoftmax_test():
    x = helper.make_tensor_value_info('x', TensorProto.FLOAT, [3, 4, 5, 6])
    y = helper.make_tensor_value_info('y', TensorProto.FLOAT, [3, 4, 5, 6])

    node = onnx.helper.make_node('LogSoftmax',
                                 inputs=['x'],
                                 outputs=['y'],
                                 axis=1)

    return ([node], [x], [y])


@onnx_test
def logsoftmax_nonstd_input_test():
    x = helper.make_tensor_value_info('0', TensorProto.FLOAT, [6, 9])
    y = helper.make_tensor_value_info('2', TensorProto.FLOAT, [3, 4])

    node0 = onnx.helper.make_node('Slice',
                                  inputs=['0'],
                                  axes=[0, 1],
                                  starts=[1, 0],
                                  ends=[4, 4],
                                  outputs=['1'])

    node1 = onnx.helper.make_node('LogSoftmax',
                                  inputs=['1'],
                                  outputs=['2'],
                                  axis=-1)

    return ([node0, node1], [x], [y])


@onnx_test
def loop_default_test():
    body = helper.make_graph([
        helper.make_node("Add", ["a", "b_in"], ["my_local"]),
        helper.make_node("Sub", ["a", "b_in"], ["a_sub_b_in"]),
        helper.make_node("Greater", ["my_local", "a_sub_b_in"],
                         ["keep_going"]),
        helper.make_node("Add", ["a_sub_b_in", "a_sub_b_in"],
                         ["user_defined_vals"]),
    ], "body", [
        helper.make_tensor_value_info('iteration_num', TensorProto.INT64, []),
        helper.make_tensor_value_info('keep_going_inp', TensorProto.BOOL, []),
        helper.make_tensor_value_info('b_in', TensorProto.FLOAT, [])
    ], [
        helper.make_tensor_value_info('keep_going', TensorProto.BOOL, []),
        helper.make_tensor_value_info('a_sub_b_in', TensorProto.FLOAT, []),
        helper.make_tensor_value_info('my_local', TensorProto.FLOAT, []),
        helper.make_tensor_value_info('user_defined_vals', TensorProto.FLOAT,
                                      []),
    ])

    node = helper.make_node(
        "Loop",
        inputs=["", "", "b"],
        outputs=["b_loop", "my_local_loop", "user_defined_vals_loop"],
        body=body)

    a = helper.make_tensor_value_info('a', TensorProto.FLOAT, [])
    b = helper.make_tensor_value_info('b', TensorProto.FLOAT, [])

    b_loop = helper.make_tensor_value_info('b_loop', TensorProto.FLOAT, [])
    uout = helper.make_tensor_value_info('user_defined_vals_loop',
                                         TensorProto.FLOAT, [2, 1])

    return ([node], [a, b], [b_loop, uout])


@onnx_test
def loop_test():
    body = helper.make_graph([
        helper.make_node("Add", ["a", "b_in"], ["my_local"]),
        helper.make_node("Sub", ["a", "b_in"], ["a_sub_b_in"]),
        helper.make_node("Greater", ["my_local", "a_sub_b_in"],
                         ["keep_going"]),
        helper.make_node("Add", ["a_sub_b_in", "a_sub_b_in"],
                         ["user_defined_vals"]),
    ], "body", [
        helper.make_tensor_value_info('iteration_num', TensorProto.INT64, [1]),
        helper.make_tensor_value_info('keep_going_inp', TensorProto.BOOL, [1]),
        helper.make_tensor_value_info('b_in', TensorProto.FLOAT, [1])
    ], [
        helper.make_tensor_value_info('keep_going', TensorProto.BOOL, [1]),
        helper.make_tensor_value_info('a_sub_b_in', TensorProto.FLOAT, [1]),
        helper.make_tensor_value_info('my_local', TensorProto.FLOAT, [1]),
        helper.make_tensor_value_info('user_defined_vals', TensorProto.FLOAT,
                                      [1]),
    ])

    node = helper.make_node(
        "Loop",
        inputs=["max_trip_count", "keep_going_cond", "b"],
        outputs=["b_loop", "my_local_loop", "user_defined_vals_loop"],
        body=body)

    a = helper.make_tensor_value_info('a', TensorProto.FLOAT, [1])
    b = helper.make_tensor_value_info('b', TensorProto.FLOAT, [1])
    cond = helper.make_tensor_value_info('keep_going_cond', TensorProto.BOOL,
                                         [1])
    iter = helper.make_tensor_value_info('max_trip_count', TensorProto.INT64,
                                         [1])

    b_loop = helper.make_tensor_value_info('b_loop', TensorProto.FLOAT, [1])
    uout = helper.make_tensor_value_info('user_defined_vals_loop',
                                         TensorProto.FLOAT, [2, 1])

    return ([node], [iter, cond, a, b], [b_loop, uout])


@onnx_test
def lrn_test():
    x = helper.make_tensor_value_info('0', TensorProto.FLOAT, [1, 28, 24, 24])
    y = helper.make_tensor_value_info('1', TensorProto.FLOAT, [1, 28, 24, 24])

    node = onnx.helper.make_node('LRN',
                                 inputs=['0'],
                                 size=5,
                                 alpha=0.0001,
                                 beta=0.75,
                                 bias=1.0,
                                 outputs=['1'])

    return ([node], [x], [y])


@onnx_test
def matmul_bmbm_test():
    m1 = helper.make_tensor_value_info('1', TensorProto.FLOAT, [3, 6, 7])
    m2 = helper.make_tensor_value_info('2', TensorProto.FLOAT, [5, 2, 1, 7, 8])
    y = helper.make_tensor_value_info('y', TensorProto.FLOAT, [5, 2, 3, 6, 8])

    node = onnx.helper.make_node(
        'MatMul',
        inputs=['1', '2'],
        outputs=['y'],
    )

    return ([node], [m1, m2], [y])


@onnx_test
def matmul_bmv_test():
    m1 = helper.make_tensor_value_info('1', TensorProto.FLOAT, [3, 6, 7])
    m2 = helper.make_tensor_value_info('2', TensorProto.FLOAT, [7])
    y = helper.make_tensor_value_info('y', TensorProto.FLOAT, [3, 6])

    node = onnx.helper.make_node(
        'MatMul',
        inputs=['1', '2'],
        outputs=['y'],
    )

    return ([node], [m1, m2], [y])


@onnx_test
def matmul_mv_test():
    m1 = helper.make_tensor_value_info('1', TensorProto.FLOAT, [6, 7])
    m2 = helper.make_tensor_value_info('2', TensorProto.FLOAT, [7])
    y = helper.make_tensor_value_info('y', TensorProto.FLOAT, [6])

    node = onnx.helper.make_node(
        'MatMul',
        inputs=['1', '2'],
        outputs=['y'],
    )

    return ([node], [m1, m2], [y])


@onnx_test
def matmul_vbm_test():
    m1 = helper.make_tensor_value_info('1', TensorProto.FLOAT, [7])
    m2 = helper.make_tensor_value_info('2', TensorProto.FLOAT, [5, 7, 8])
    y = helper.make_tensor_value_info('y', TensorProto.FLOAT, [5, 8])

    node = onnx.helper.make_node(
        'MatMul',
        inputs=['1', '2'],
        outputs=['y'],
    )

    return ([node], [m1, m2], [y])


@onnx_test
def matmul_vm_test():
    m1 = helper.make_tensor_value_info('1', TensorProto.FLOAT, [7])
    m2 = helper.make_tensor_value_info('2', TensorProto.FLOAT, [7, 8])
    y = helper.make_tensor_value_info('y', TensorProto.FLOAT, [8])

    node = onnx.helper.make_node(
        'MatMul',
        inputs=['1', '2'],
        outputs=['y'],
    )

    return ([node], [m1, m2], [y])


@onnx_test
def matmul_vv_test():
    m1 = helper.make_tensor_value_info('1', TensorProto.FLOAT, [7])
    m2 = helper.make_tensor_value_info('2', TensorProto.FLOAT, [7])
    y = helper.make_tensor_value_info('y', TensorProto.FLOAT, [1])

    node = onnx.helper.make_node(
        'MatMul',
        inputs=['1', '2'],
        outputs=['y'],
    )

    return ([node], [m1, m2], [y])


@onnx_test
def matmulinteger_test():
    m1 = helper.make_tensor_value_info('1', TensorProto.INT8, [3, 6, 16])
    m2 = helper.make_tensor_value_info('2', TensorProto.INT8, [3, 16, 8])
    y = helper.make_tensor_value_info('y', TensorProto.INT32, [3, 6, 8])

    node = onnx.helper.make_node(
        'MatMulInteger',
        inputs=['1', '2'],
        outputs=['y'],
    )

    return ([node], [m1, m2], [y])


@onnx_test
def max_test():
    a = helper.make_tensor_value_info('0', TensorProto.FLOAT, [3])
    b = helper.make_tensor_value_info('1', TensorProto.FLOAT, [3])
    c = helper.make_tensor_value_info('2', TensorProto.FLOAT, [3])
    y = helper.make_tensor_value_info('2', TensorProto.FLOAT, [3])

    node = onnx.helper.make_node(
        'Max',
        inputs=['0', '1', '2'],
        outputs=['3'],
    )

    return ([node], [a, b, c], [y])


@onnx_test
def maxpool_notset_test():
    x = helper.make_tensor_value_info('x', TensorProto.FLOAT, [1, 1, 5, 5])
    y = helper.make_tensor_value_info('y', TensorProto.FLOAT, [1, 1, 1, 1])

    node = onnx.helper.make_node('MaxPool',
                                 inputs=['x'],
                                 outputs=['y'],
                                 kernel_shape=[6, 6],
                                 strides=[2, 2],
                                 pads=[0, 0, 1, 1],
                                 auto_pad='NOTSET')

    return ([node], [x], [y])


@onnx_test
def maxpool_same_upper_test():
    x = helper.make_tensor_value_info('x', TensorProto.FLOAT, [1, 1, 5, 5])
    y = helper.make_tensor_value_info('y', TensorProto.FLOAT, [1, 1, 5, 5])

    node = onnx.helper.make_node('MaxPool',
                                 inputs=['x'],
                                 outputs=['y'],
                                 kernel_shape=[2, 2],
                                 auto_pad='SAME_UPPER')

    return ([node], [x], [y])


@onnx_test
def min_test():
    a = helper.make_tensor_value_info('0', TensorProto.FLOAT, [3])
    b = helper.make_tensor_value_info('1', TensorProto.FLOAT, [3])
    c = helper.make_tensor_value_info('2', TensorProto.FLOAT, [3])
    y = helper.make_tensor_value_info('2', TensorProto.FLOAT, [3])

    node = onnx.helper.make_node(
        'Min',
        inputs=['0', '1', '2'],
        outputs=['3'],
    )

    return ([node], [a, b, c], [y])


@onnx_test
def multinomial_test():
    sample_size = 10
    seed = 0.0
    input = helper.make_tensor_value_info("input", TensorProto.FLOAT, [1, 10])
    output = helper.make_tensor_value_info("output", TensorProto.INT32,
                                           [1, 10])

    node = onnx.helper.make_node('Multinomial',
                                 inputs=['input'],
                                 sample_size=sample_size,
                                 seed=seed,
                                 outputs=['output'])

    return ([node], [input], [output])


@onnx_test
def multinomial_generated_seed_test():
    sample_size = 10
    input = helper.make_tensor_value_info("input", TensorProto.FLOAT, [1, 10])
    output = helper.make_tensor_value_info("output", TensorProto.INT32,
                                           [1, 10])

    node = onnx.helper.make_node('Multinomial',
                                 inputs=['input'],
                                 sample_size=sample_size,
                                 outputs=['output'])

    return ([node], [input], [output])


@onnx_test
def multinomial_dtype_error_test():
    sample_size = 10
    dtype = 0
    input = helper.make_tensor_value_info("input", TensorProto.FLOAT, [1, 10])
    output = helper.make_tensor_value_info("output", TensorProto.INT64,
                                           [1, 10])

    node = onnx.helper.make_node('Multinomial',
                                 inputs=['input'],
                                 sample_size=sample_size,
                                 dtype=dtype,
                                 outputs=['output'])

    return ([node], [input], [output])


@onnx_test
def multinomial_int64_test():
    sample_size = 10
    dtype = 7
    seed = 1.0
    input = helper.make_tensor_value_info("input", TensorProto.FLOAT, [1, 10])
    output = helper.make_tensor_value_info("output", TensorProto.INT64,
                                           [1, 10])

    node = onnx.helper.make_node('Multinomial',
                                 inputs=['input'],
                                 sample_size=sample_size,
                                 dtype=dtype,
                                 seed=seed,
                                 outputs=['output'])

    return ([node], [input], [output])


@onnx_test
def neg_test():
    x = helper.make_tensor_value_info('0', TensorProto.INT64, [2, 3])
    y = helper.make_tensor_value_info('1', TensorProto.INT64, [2, 3])

    node = onnx.helper.make_node('Neg', inputs=['0'], outputs=['1'])

    return ([node], [x], [y])


@onnx_test
def nms_test():
    b = helper.make_tensor_value_info('boxes', TensorProto.FLOAT, [1, 6, 4])
    s = helper.make_tensor_value_info('scores', TensorProto.FLOAT, [1, 1, 6])
    mo = helper.make_tensor_value_info('max_output_boxes_per_class',
                                       TensorProto.INT64, [1])
    iou = helper.make_tensor_value_info('iou_threshold', TensorProto.FLOAT,
                                        [1])
    st = helper.make_tensor_value_info('score_threshold', TensorProto.FLOAT,
                                       [1])
    out = helper.make_tensor_value_info('selected_indices', TensorProto.INT64,
                                        [6, 3])

    node = onnx.helper.make_node('NonMaxSuppression',
                                 inputs=[
                                     'boxes', 'scores',
                                     'max_output_boxes_per_class',
                                     'iou_threshold', 'score_threshold'
                                 ],
                                 outputs=['selected_indices'],
                                 center_point_box=1)

    return ([node], [b, s, mo, iou, st], [out])


@onnx_test
def not_test():
    x = helper.make_tensor_value_info('0', TensorProto.INT32, [4])
    y = helper.make_tensor_value_info('1', TensorProto.INT32, [4])

    node = onnx.helper.make_node('Not', inputs=['0'], outputs=['1'])

    return ([node], [x], [y])


@onnx_test
def not_bool_test():
    x = helper.make_tensor_value_info('0', TensorProto.BOOL, [4])
    y = helper.make_tensor_value_info('1', TensorProto.BOOL, [4])

    node = onnx.helper.make_node('Not', inputs=['0'], outputs=['1'])

    return ([node], [x], [y])


@onnx_test
def no_pad_test():
    x = helper.make_tensor_value_info('0', TensorProto.FLOAT, [2, 2])
    y = helper.make_tensor_value_info('1', TensorProto.FLOAT, [2, 2])

    node = onnx.helper.make_node('Pad',
                                 inputs=['0'],
                                 pads=[0, 0, 0, 0],
                                 outputs=['1'])

    return ([node], [x], [y])


@onnx_test
def nonzero_dynamic_test():
    x = helper.make_tensor_value_info('data', TensorProto.BOOL, [2, 2])
    y = helper.make_tensor_value_info('indices', TensorProto.INT64, [2, 3])

    node = onnx.helper.make_node('NonZero',
                                 inputs=['data'],
                                 outputs=['indices'])

    return ([node], [x], [y])


@onnx_test
def nonzero_test():
    data1 = np.array([[1., 0.], [1., 1.]])
    data = helper.make_tensor(name='data',
                              data_type=TensorProto.FLOAT,
                              dims=data1.shape,
                              vals=data1.flatten().astype(np.float))
    y = helper.make_tensor_value_info('indices', TensorProto.INT64, [2, 3])

    node = onnx.helper.make_node('NonZero',
                                 inputs=['data'],
                                 outputs=['indices'])

    return ([node], [], [y], [data])


@onnx_test
def nonzero_int_test():
    data1 = np.array([[1, 1, 0], [1, 0, 1]])
    data = helper.make_tensor(name='data',
                              data_type=TensorProto.INT16,
                              dims=data1.shape,
                              vals=data1.flatten().astype(np.int16))
    y = helper.make_tensor_value_info('indices', TensorProto.INT64, [2, 4])

    node = onnx.helper.make_node('NonZero',
                                 inputs=['data'],
                                 outputs=['indices'])

    return ([node], [], [y], [data])


@onnx_test
def onehot_test():
    axis_value = 0
    depth = np.array([3])
    indices = helper.make_tensor_value_info("indices", TensorProto.INT32,
                                            [5, 2])
    values = helper.make_tensor_value_info("values", TensorProto.FLOAT16, [2])
    y = helper.make_tensor_value_info('y', TensorProto.FLOAT16, [3, 5, 2])

    depth_tensor = helper.make_tensor(name="depth",
                                      data_type=TensorProto.INT32,
                                      dims=None,
                                      vals=depth.astype(int))

    node = onnx.helper.make_node('OneHot',
                                 inputs=['indices', 'depth', 'values'],
                                 outputs=['y'],
                                 axis=axis_value)

    return ([node], [indices, values], [y], [depth_tensor])


@onnx_test
def pad_test():
    x = helper.make_tensor_value_info('0', TensorProto.FLOAT, [2, 2])
    y = helper.make_tensor_value_info('1', TensorProto.FLOAT, [4, 4])

    node = onnx.helper.make_node('Pad',
                                 inputs=['0'],
                                 pads=[1, 1, 1, 1],
                                 outputs=['1'])

    return ([node], [x], [y])


@onnx_test
def pad_3arg_test():
    values = np.array([1])
    val_tensor = helper.make_tensor(name='val',
                                    data_type=TensorProto.FLOAT,
                                    dims=values.reshape(()).shape,
                                    vals=values.astype(float))
    arg_val = onnx.helper.make_node('Constant',
                                    inputs=[],
                                    outputs=['arg_val'],
                                    value=val_tensor)

    sizes = np.array([1, 1, 2, 2])
    pad_tensor = helper.make_tensor(name='pad_size',
                                    data_type=TensorProto.INT32,
                                    dims=sizes.shape,
                                    vals=sizes.astype(int))
    arg_pad = onnx.helper.make_node('Constant',
                                    inputs=[],
                                    outputs=['arg_pad'],
                                    value=pad_tensor)

    x = helper.make_tensor_value_info('0', TensorProto.FLOAT, [2, 2])
    y = helper.make_tensor_value_info('1', TensorProto.FLOAT, [5, 5])

    node = onnx.helper.make_node('Pad',
                                 inputs=['0', 'arg_pad', 'arg_val'],
                                 outputs=['1'])

    return ([arg_val, arg_pad, node], [x], [y])


@onnx_test
def pad_reflect_test():
    x = helper.make_tensor_value_info('0', TensorProto.FLOAT, [2, 2])
    y = helper.make_tensor_value_info('1', TensorProto.FLOAT, [2, 5])

    sizes = np.array([0, 2, 0, 1])
    pad_tensor = helper.make_tensor(name='pad_size',
                                    data_type=TensorProto.INT32,
                                    dims=sizes.shape,
                                    vals=sizes.astype(int))
    arg_pad = onnx.helper.make_node('Constant',
                                    inputs=[],
                                    outputs=['arg_pad'],
                                    value=pad_tensor)

    node = onnx.helper.make_node('Pad',
                                 mode='reflect',
                                 inputs=['0', 'arg_pad'],
                                 outputs=['1'])

    return ([arg_pad, node], [x], [y])


@onnx_test
def pad_reflect_multiaxis_test():
    x = helper.make_tensor_value_info('0', TensorProto.FLOAT, [2, 3])
    y = helper.make_tensor_value_info('1', TensorProto.FLOAT, [4, 5])

    sizes = np.array([0, 2, 2, 0])
    pad_tensor = helper.make_tensor(name='pad_size',
                                    data_type=TensorProto.INT32,
                                    dims=sizes.shape,
                                    vals=sizes.astype(int))
    arg_pad = onnx.helper.make_node('Constant',
                                    inputs=[],
                                    outputs=['arg_pad'],
                                    value=pad_tensor)

    node = onnx.helper.make_node('Pad',
                                 mode='reflect',
                                 inputs=['0', 'arg_pad'],
                                 outputs=['1'])

    return ([arg_pad, node], [x], [y])


@onnx_test
def pow_test():
    arg0 = helper.make_tensor_value_info('0', TensorProto.FLOAT, [2, 3, 4, 5])
    arg1 = helper.make_tensor_value_info('1', TensorProto.FLOAT, [2, 3, 4, 5])
    arg_out = helper.make_tensor_value_info('out', TensorProto.FLOAT,
                                            [2, 3, 4, 5])

    node = onnx.helper.make_node(
        'Pow',
        inputs=['0', '1'],
        outputs=['out'],
    )

    return ([node], [arg0, arg1], [arg_out])


@onnx_test
def pow_fp32_i64_test():
    arg0 = helper.make_tensor_value_info('0', TensorProto.FLOAT, [2, 3, 4, 5])
    arg1 = helper.make_tensor_value_info('1', TensorProto.INT64, [2, 3, 4, 5])
    arg_out = helper.make_tensor_value_info('out', TensorProto.FLOAT,
                                            [2, 3, 4, 5])

    node = onnx.helper.make_node(
        'Pow',
        inputs=['0', '1'],
        outputs=['out'],
    )

    return ([node], [arg0, arg1], [arg_out])


@onnx_test
def pow_i64_fp32_test():
    arg0 = helper.make_tensor_value_info('0', TensorProto.INT64, [2, 3, 4, 5])
    arg1 = helper.make_tensor_value_info('1', TensorProto.FLOAT, [2, 3, 4, 5])
    arg_out = helper.make_tensor_value_info('out', TensorProto.INT64,
                                            [2, 3, 4, 5])

    node = onnx.helper.make_node(
        'Pow',
        inputs=['0', '1'],
        outputs=['out'],
    )

    return ([node], [arg0, arg1], [arg_out])


@onnx_test
def prefix_scan_sum_test():
    x = helper.make_tensor_value_info('x', TensorProto.FLOAT, [2, 2, 2])
    y = helper.make_tensor_value_info('y', TensorProto.FLOAT, [2, 2, 2])
    axis_val = np.array([0])
    axis_tensor = helper.make_tensor(name="axis",
                                     data_type=TensorProto.INT32,
                                     dims=axis_val.shape,
                                     vals=axis_val.astype(int))
    node = onnx.helper.make_node('CumSum',
                                 inputs=['x', 'axis'],
                                 outputs=['y'],
                                 exclusive=1,
                                 reverse=1)
    return ([node], [x], [y], [axis_tensor])


@onnx_test
def prelu_brcst_test():
    arg0 = helper.make_tensor_value_info('0', TensorProto.FLOAT, [2, 3, 4, 5])
    arg1 = helper.make_tensor_value_info('1', TensorProto.FLOAT, [4, 5])
    arg_out = helper.make_tensor_value_info('out', TensorProto.FLOAT,
                                            [2, 3, 4, 5])

    node = onnx.helper.make_node(
        'PRelu',
        inputs=['0', '1'],
        outputs=['out'],
    )

    return ([node], [arg0, arg1], [arg_out])


@onnx_test
def quantizelinear_test():
    arg0 = helper.make_tensor_value_info('0', TensorProto.FLOAT, [5])
    arg1 = helper.make_tensor_value_info('1', TensorProto.FLOAT, [1])
    arg_out = helper.make_tensor_value_info('out', TensorProto.INT8, [5])

    node = onnx.helper.make_node(
        'QuantizeLinear',
        inputs=['0', '1'],
        outputs=['out'],
    )

    return ([node], [arg0, arg1], [arg_out])


@onnx_test
def quantizelinear_int32_test():
    arg0 = helper.make_tensor_value_info('0', TensorProto.INT32, [5])
    arg1 = helper.make_tensor_value_info('1', TensorProto.FLOAT, [1])
    arg_out = helper.make_tensor_value_info('out', TensorProto.INT8, [5])

    node = onnx.helper.make_node(
        'QuantizeLinear',
        inputs=['0', '1'],
        outputs=['out'],
    )

    return ([node], [arg0, arg1], [arg_out])


@onnx_test
def quantizelinear_zero_point_test():
    arg0 = helper.make_tensor_value_info('0', TensorProto.FLOAT, [5])
    arg1 = helper.make_tensor_value_info('1', TensorProto.FLOAT, [1])
    arg2 = helper.make_tensor_value_info('2', TensorProto.INT8, [1])
    arg_out = helper.make_tensor_value_info('out', TensorProto.INT8, [5])

    node = onnx.helper.make_node(
        'QuantizeLinear',
        inputs=['0', '1', '2'],
        outputs=['out'],
    )

    return ([node], [arg0, arg1, arg2], [arg_out])


def make_quantizelinear_axis_graph(axis):
    arg0 = helper.make_tensor_value_info('0', TensorProto.FLOAT, [1, 1, 5, 1])
    arg1 = helper.make_tensor_value_info('1', TensorProto.FLOAT, [5])
    arg2 = helper.make_tensor_value_info('2', TensorProto.INT8, [5])
    arg_out = helper.make_tensor_value_info('out', TensorProto.INT8,
                                            [1, 1, 5, 1])

    node = onnx.helper.make_node('QuantizeLinear',
                                 inputs=['0', '1', '2'],
                                 outputs=['out'],
                                 axis=axis)

    return ([node], [arg0, arg1, arg2], [arg_out])


@onnx_test
def quantizelinear_axis_test():
    return make_quantizelinear_axis_graph(2)


@onnx_test
def quantizelinear_neg_axis_test():
    return make_quantizelinear_axis_graph(-2)


@onnx_test
def randomnormal_test():
    dtype = 11
    mean = 10.0
    scale = 1.5
    seed = 0.0
    shape = [2, 3, 4]
    output = helper.make_tensor_value_info('output', TensorProto.DOUBLE,
                                           [2, 3, 4])

    node = onnx.helper.make_node('RandomNormal',
                                 inputs=[],
                                 outputs=['output'],
                                 dtype=dtype,
                                 mean=mean,
                                 scale=scale,
                                 seed=seed,
                                 shape=shape)

    return ([node], [], [output])


@onnx_test
def randomnormal_dtype_error_test():
    dtype = 6
    shape = [2, 3, 4]
    output = helper.make_tensor_value_info('output', TensorProto.INT32,
                                           [2, 3, 4])

    node = onnx.helper.make_node('RandomNormal',
                                 inputs=[],
                                 outputs=['output'],
                                 dtype=dtype,
                                 shape=shape)

    return ([node], [], [output])


@onnx_test
def randomnormal_generated_seed_test():
    sample_size = 10
    input = helper.make_tensor_value_info("input", TensorProto.FLOAT, [1, 10])
    output = helper.make_tensor_value_info("output", TensorProto.INT32,
                                           [1, 10])

    node = onnx.helper.make_node('RandomNormal',
                                 inputs=['input'],
                                 sample_size=sample_size,
                                 outputs=['output'])

    return ([node], [input], [output])


@onnx_test
def randomnormal_shape_error_test():
    dtype = 1
    output = helper.make_tensor_value_info('output', TensorProto.FLOAT,
                                           [2, 3, 4])

    node = onnx.helper.make_node('RandomNormal',
                                 inputs=[],
                                 outputs=['output'],
                                 dtype=dtype)

    return ([node], [], [output])


@onnx_test
def randomnormallike_test():
    dtype = 10
    mean = 10.0
    scale = 1.5
    seed = 0.0
    input = helper.make_tensor_value_info('input', TensorProto.FLOAT16,
                                          [2, 3, 4])
    output = helper.make_tensor_value_info('output', TensorProto.FLOAT16,
                                           [2, 3, 4])

    node = onnx.helper.make_node('RandomNormalLike',
                                 inputs=['input'],
                                 outputs=['output'],
                                 dtype=dtype,
                                 mean=mean,
                                 scale=scale,
                                 seed=seed)

    return ([node], [input], [output])


@onnx_test
def randomnormallike_type_error_test():
    seed = 0
    input = helper.make_tensor_value_info('input', TensorProto.INT32,
                                          [2, 3, 4])
    output = helper.make_tensor_value_info('output', TensorProto.FLOAT,
                                           [2, 3, 4])

    node = onnx.helper.make_node('RandomNormalLike',
                                 inputs=['input'],
                                 outputs=['output'],
                                 seed=seed)

    return ([node], [input], [output])


@onnx_test
def randomuniform_test():
    dtype = 11
    high = 1.0
    low = 0.0
    seed = 0.0
    shape = [2, 3, 4]
    output = helper.make_tensor_value_info('output', TensorProto.DOUBLE,
                                           [2, 3, 4])

    node = onnx.helper.make_node('RandomUniform',
                                 inputs=[],
                                 outputs=['output'],
                                 dtype=dtype,
                                 high=high,
                                 low=low,
                                 seed=seed,
                                 shape=shape)

    return ([node], [], [output])


@onnx_test
def randomuniform_dtype_error_test():
    dtype = 6
    shape = [2, 3, 4]
    output = helper.make_tensor_value_info('output', TensorProto.INT32,
                                           [2, 3, 4])

    node = onnx.helper.make_node('RandomUniform',
                                 inputs=[],
                                 outputs=['output'],
                                 dtype=dtype,
                                 shape=shape)

    return ([node], [], [output])


@onnx_test
def randomuniform_generated_seed_test():
    sample_size = 10
    input = helper.make_tensor_value_info("input", TensorProto.FLOAT, [1, 10])
    output = helper.make_tensor_value_info("output", TensorProto.INT32,
                                           [1, 10])

    node = onnx.helper.make_node('RandomUniform',
                                 inputs=['input'],
                                 sample_size=sample_size,
                                 outputs=['output'])

    return ([node], [input], [output])


@onnx_test
def randomuniform_shape_error_test():
    dtype = 1
    output = helper.make_tensor_value_info('output', TensorProto.FLOAT,
                                           [2, 3, 4])

    node = onnx.helper.make_node('RandomUniform',
                                 inputs=[],
                                 outputs=['output'],
                                 dtype=dtype)

    return ([node], [], [output])


@onnx_test
def randomuniformlike_test():
    dtype = 10
    high = 10.0
    low = 1.0
    seed = 0.0
    input = helper.make_tensor_value_info('input', TensorProto.FLOAT16,
                                          [2, 3, 4])
    output = helper.make_tensor_value_info('output', TensorProto.FLOAT16,
                                           [2, 3, 4])

    node = onnx.helper.make_node('RandomUniformLike',
                                 inputs=['input'],
                                 outputs=['output'],
                                 dtype=dtype,
                                 high=high,
                                 low=low,
                                 seed=seed)

    return ([node], [input], [output])


@onnx_test
def randomuniformlike_type_error_test():
    seed = 0
    input = helper.make_tensor_value_info('input', TensorProto.INT32,
                                          [2, 3, 4])
    output = helper.make_tensor_value_info('output', TensorProto.FLOAT,
                                           [2, 3, 4])

    node = onnx.helper.make_node('RandomUniformLike',
                                 inputs=['input'],
                                 outputs=['output'],
                                 seed=seed)

    return ([node], [input], [output])


@onnx_test
def range_test():

    start_val = np.array([10])
    limit_val = np.array([6])
    delta_val = np.array([-3])

    start_tensor = helper.make_tensor(name='start_val',
                                      data_type=TensorProto.INT64,
                                      dims=start_val.reshape(()).shape,
                                      vals=start_val.astype(np.int64))
    start = onnx.helper.make_node('Constant',
                                  inputs=[],
                                  outputs=['start'],
                                  value=start_tensor)

    limit_tensor = helper.make_tensor(name='limit_val',
                                      data_type=TensorProto.INT64,
                                      dims=limit_val.reshape(()).shape,
                                      vals=limit_val.astype(np.int64))
    limit = onnx.helper.make_node('Constant',
                                  inputs=[],
                                  outputs=['limit'],
                                  value=limit_tensor)

    delta_tensor = helper.make_tensor(name='delta_val',
                                      data_type=TensorProto.INT64,
                                      dims=delta_val.reshape(()).shape,
                                      vals=delta_val.astype(np.int64))
    delta = onnx.helper.make_node('Constant',
                                  inputs=[],
                                  outputs=['delta'],
                                  value=delta_tensor)

    node = onnx.helper.make_node('Range',
                                 inputs=['start', 'limit', 'delta'],
                                 outputs=['1'])

    y = helper.make_tensor_value_info('1', TensorProto.FLOAT, [3])

    return ([start, limit, delta, node], [], [y])


@onnx_test
def range_float_test():

    start_val = np.array([2])
    limit_val = np.array([11])
    delta_val = np.array([2])

    start_tensor = helper.make_tensor(name='start_val',
                                      data_type=TensorProto.FLOAT,
                                      dims=start_val.reshape(()).shape,
                                      vals=start_val.astype(np.float))
    start = onnx.helper.make_node('Constant',
                                  inputs=[],
                                  outputs=['start'],
                                  value=start_tensor)

    limit_tensor = helper.make_tensor(name='limit_val',
                                      data_type=TensorProto.FLOAT,
                                      dims=limit_val.reshape(()).shape,
                                      vals=limit_val.astype(np.float))
    limit = onnx.helper.make_node('Constant',
                                  inputs=[],
                                  outputs=['limit'],
                                  value=limit_tensor)

    delta_tensor = helper.make_tensor(name='delta_val',
                                      data_type=TensorProto.FLOAT,
                                      dims=delta_val.reshape(()).shape,
                                      vals=delta_val.astype(np.float))
    delta = onnx.helper.make_node('Constant',
                                  inputs=[],
                                  outputs=['delta'],
                                  value=delta_tensor)

    node = onnx.helper.make_node('Range',
                                 inputs=['start', 'limit', 'delta'],
                                 outputs=['1'])

    y = helper.make_tensor_value_info('1', TensorProto.FLOAT, [3])

    return ([start, limit, delta, node], [], [y])


@onnx_test
def recip_test():
    x = helper.make_tensor_value_info('x', TensorProto.FLOAT, [3])
    y = helper.make_tensor_value_info('y', TensorProto.FLOAT, [3])

    node = onnx.helper.make_node(
        'Reciprocal',
        inputs=['x'],
        outputs=['y'],
    )

    return ([node], [x], [y])


@onnx_test
def reducel1_test():
    x = helper.make_tensor_value_info('x', TensorProto.FLOAT, [3, 4, 5, 6])
    y = helper.make_tensor_value_info('y', TensorProto.FLOAT, [3, 4, 6])
    axes = [-2]

    node = onnx.helper.make_node('ReduceL1',
                                 inputs=['x'],
                                 outputs=['y'],
                                 axes=axes,
                                 keepdims=0)

    return ([node], [x], [y])


@onnx_test
def reducel2_test():
    x = helper.make_tensor_value_info('x', TensorProto.FLOAT, [3, 4, 5, 6])
    y = helper.make_tensor_value_info('y', TensorProto.FLOAT, [3, 4, 5])
    axes = [-1]

    node = onnx.helper.make_node('ReduceL2',
                                 inputs=['x'],
                                 outputs=['y'],
                                 axes=axes,
                                 keepdims=0)

    return ([node], [x], [y])


@onnx_test
def reduce_log_sum_test():
    x = helper.make_tensor_value_info('x', TensorProto.FLOAT, [3, 4, 5, 6])
    y = helper.make_tensor_value_info('y', TensorProto.FLOAT, [3, 1, 5, 6])
    axes = [-3]

    node = onnx.helper.make_node('ReduceLogSum',
                                 inputs=['x'],
                                 outputs=['y'],
                                 axes=axes,
                                 keepdims=1)

    return ([node], [x], [y])


@onnx_test
def reduce_log_sum_exp_test():
    x = helper.make_tensor_value_info('x', TensorProto.FLOAT, [3, 4, 5, 6])
    y = helper.make_tensor_value_info('y', TensorProto.FLOAT, [4, 5, 6])
    axes = [-4]

    node = onnx.helper.make_node('ReduceLogSumExp',
                                 inputs=['x'],
                                 outputs=['y'],
                                 axes=axes,
                                 keepdims=1)

    return ([node], [x], [y])


@onnx_test
def reducemax_test():
    x = helper.make_tensor_value_info('x', TensorProto.FLOAT, [3, 4, 5, 6])
    y = helper.make_tensor_value_info('y', TensorProto.FLOAT, [3, 4, 6])
    axes = [2]

    node = onnx.helper.make_node('ReduceMax',
                                 inputs=['x'],
                                 outputs=['y'],
                                 axes=axes,
                                 keepdims=0)

    return ([node], [x], [y])


@onnx_test
def reducemean_test():
    x = helper.make_tensor_value_info('x', TensorProto.FLOAT, [3, 4, 5, 6])
    y = helper.make_tensor_value_info('y', TensorProto.FLOAT, [3, 4])
    axes = [2, 3]

    node = onnx.helper.make_node('ReduceMean',
                                 inputs=['x'],
                                 outputs=['y'],
                                 axes=axes,
                                 keepdims=0)

    return ([node], [x], [y])


@onnx_test
def reducemean_keepdims_test():
    x = helper.make_tensor_value_info('x', TensorProto.FLOAT, [3, 4, 5, 6])
    y = helper.make_tensor_value_info('y', TensorProto.FLOAT, [3, 4, 1, 6])
    axes = [2]

    node = onnx.helper.make_node('ReduceMean',
                                 inputs=['x'],
                                 outputs=['y'],
                                 axes=axes,
                                 keepdims=1)

    return ([node], [x], [y])


@onnx_test
def reducemin_test():
    x = helper.make_tensor_value_info('x', TensorProto.FLOAT, [3, 4, 5, 6])
    y = helper.make_tensor_value_info('y', TensorProto.FLOAT, [3, 1, 5, 1])
    axes = [1, 3]

    node = onnx.helper.make_node('ReduceMin',
                                 inputs=['x'],
                                 outputs=['y'],
                                 axes=axes,
                                 keepdims=1)

    return ([node], [x], [y])


@onnx_test
def reduceprod_test():
    x = helper.make_tensor_value_info('x', TensorProto.FLOAT, [3, 4, 5, 6])
    y = helper.make_tensor_value_info('y', TensorProto.FLOAT, [3, 4, 1, 6])
    axes = [2]

    node = onnx.helper.make_node('ReduceProd',
                                 inputs=['x'],
                                 outputs=['y'],
                                 axes=axes,
                                 keepdims=1)

    return ([node], [x], [y])


@onnx_test
def reducesum_test():
    x = helper.make_tensor_value_info('x', TensorProto.FLOAT, [3, 4, 5, 6])
    y = helper.make_tensor_value_info('y', TensorProto.FLOAT, [3, 4, 1, 6])
    axes = [2]

    node = onnx.helper.make_node('ReduceSum',
                                 inputs=['x'],
                                 outputs=['y'],
                                 axes=axes,
                                 keepdims=0)

    return ([node], [x], [y])


@onnx_test
def reducesum_empty_axes_test():
    x = helper.make_tensor_value_info('x', TensorProto.FLOAT, [3, 4, 5, 6])
    y = helper.make_tensor_value_info('y', TensorProto.FLOAT, [3, 4, 1, 6])
    axes = np.array([], dtype=np.int64)
    axes_tensor = helper.make_tensor(name="axes",
                                     data_type=TensorProto.INT64,
                                     dims=axes.shape,
                                     vals=axes.astype(np.int64))

    node = onnx.helper.make_node('ReduceSum',
                                 inputs=['x', 'axes'],
                                 outputs=['y'],
                                 keepdims=0,
                                 noop_with_empty_axes=False)

    return ([node], [x], [y], [axes_tensor])


@onnx_test
def reducesum_noop_test():
    x = helper.make_tensor_value_info('x', TensorProto.FLOAT, [3, 4, 5, 6])
    y = helper.make_tensor_value_info('y', TensorProto.FLOAT, [3, 4, 1, 6])
    axes = np.array([], dtype=np.int64)
    axes_tensor = helper.make_tensor(name="axes",
                                     data_type=TensorProto.INT64,
                                     dims=axes.shape,
                                     vals=axes.astype(np.int64))

    node = onnx.helper.make_node('ReduceSum',
                                 inputs=['x', 'axes'],
                                 outputs=['y'],
                                 keepdims=0,
                                 noop_with_empty_axes=True)

    return ([node], [x], [y], [axes_tensor])


@onnx_test
def reducesum_keepdims_test():
    x = helper.make_tensor_value_info('x', TensorProto.FLOAT, [3, 4, 5, 6])
    y = helper.make_tensor_value_info('y', TensorProto.FLOAT, [3, 4, 1, 1])
    axes = [2, 3]

    node = onnx.helper.make_node('ReduceSum',
                                 inputs=['x'],
                                 outputs=['y'],
                                 axes=axes,
                                 keepdims=1)

    return ([node], [x], [y])


@onnx_test
def reducesum_multiaxis_test():
    x = helper.make_tensor_value_info('x', TensorProto.FLOAT, [3, 4, 5, 6])
    y = helper.make_tensor_value_info('y', TensorProto.FLOAT, [3, 4, 1, 1])
    axes = [2, 3]

    node = onnx.helper.make_node('ReduceSum',
                                 inputs=['x'],
                                 outputs=['y'],
                                 axes=axes,
                                 keepdims=0)

    return ([node], [x], [y])


@onnx_test
def reducesum_square_test():
    x = helper.make_tensor_value_info('x', TensorProto.FLOAT, [3, 4, 5, 6])
    y = helper.make_tensor_value_info('y', TensorProto.FLOAT, [3, 4, 6])
    axes = [-2]

    node = onnx.helper.make_node('ReduceSumSquare',
                                 inputs=['x'],
                                 outputs=['y'],
                                 axes=axes,
                                 keepdims=0)

    return ([node], [x], [y])


@onnx_test
def reshape_test():
    x = helper.make_tensor_value_info('0', TensorProto.FLOAT, [4, 2, 3])
    x_shape = helper.make_tensor_value_info('1', TensorProto.INT64, [2])
    x_shape_list = [3, 8]
    y = helper.make_tensor_value_info('2', TensorProto.FLOAT, [3, 8])
    y2 = helper.make_tensor_value_info('3', TensorProto.FLOAT, [3, 8])

    node = onnx.helper.make_node('Reshape', inputs=['0', '1'], outputs=['2'])

    node2 = onnx.helper.make_node('Reshape',
                                  inputs=['0'],
                                  shape=x_shape_list,
                                  outputs=['3'])

    return ([node, node2], [x, x_shape], [y, y2],
            [helper.make_tensor('1', TensorProto.INT64, [2], [3, 8])])


@onnx_test
def reshape_non_standard_test():
    x = helper.make_tensor_value_info('x', TensorProto.FLOAT, [2, 3, 4])
    y = helper.make_tensor_value_info('y', TensorProto.FLOAT, [4, 3, 2])

    trans = helper.make_node(
        'Transpose',
        inputs=['x'],
        outputs=['trans_x'],
        perm=[0, 2, 1],
    )

    res = onnx.helper.make_node('Reshape',
                                inputs=['trans_x'],
                                outputs=['y'],
                                shape=[4, 3, 2])

    return ([trans, res], [x], [y])


@onnx_test
def resize_downsample_f_test():
    scales = np.array([1.0, 1.0, 0.6, 0.6], dtype=np.float32)
    scale_tensor = helper.make_tensor(name='scales',
                                      data_type=TensorProto.FLOAT,
                                      dims=scales.shape,
                                      vals=scales.flatten().astype(np.float32))

    X = helper.make_tensor_value_info('X', TensorProto.FLOAT, [1, 1, 2, 4])
    Y = helper.make_tensor_value_info('Y', TensorProto.FLOAT, [])

    node = onnx.helper.make_node(
        'Resize',
        inputs=['X', '', 'scales'],
        outputs=['Y'],
        coordinate_transformation_mode='align_corners',
        mode='nearest',
        nearest_mode='floor')

    return ([node], [X], [Y], [scale_tensor])


@onnx_test
def resize_downsample_c_test():
    scales = np.array([1.0, 1.0, 0.6, 0.6], dtype=np.float32)
    scale_tensor = helper.make_tensor(name='scales',
                                      data_type=TensorProto.FLOAT,
                                      dims=scales.shape,
                                      vals=scales.flatten().astype(np.float32))

    X = helper.make_tensor_value_info('X', TensorProto.FLOAT, [1, 1, 2, 4])
    Y = helper.make_tensor_value_info('Y', TensorProto.FLOAT, [1, 1, 1, 2])

    node = onnx.helper.make_node('Resize',
                                 inputs=['X', '', 'scales'],
                                 outputs=['Y'],
                                 coordinate_transformation_mode='asymmetric',
                                 mode='nearest',
                                 nearest_mode='ceil')

    return ([node], [X], [Y], [scale_tensor])


@onnx_test
def resize_downsample_linear_test():
    scales = np.array([1.0, 1.0, 0.6, 0.5], dtype=np.float32)
    scale_tensor = helper.make_tensor(name='scales',
                                      data_type=TensorProto.FLOAT,
                                      dims=scales.shape,
                                      vals=scales.flatten().astype(np.float32))

    X = helper.make_tensor_value_info('X', TensorProto.FLOAT, [1, 1, 2, 4])
    Y = helper.make_tensor_value_info('Y', TensorProto.FLOAT, [])

    node = onnx.helper.make_node('Resize',
                                 inputs=['X', '', 'scales'],
                                 outputs=['Y'],
                                 mode='linear')

    return ([node], [X], [Y], [scale_tensor])


@onnx_test
def resize_nonstd_input_test():
    scales = np.array([1.0, 1.0, 0.6, 0.6], dtype=np.float32)
    scale_tensor = helper.make_tensor(name='scales',
                                      data_type=TensorProto.FLOAT,
                                      dims=scales.shape,
                                      vals=scales.flatten().astype(np.float32))

    X = helper.make_tensor_value_info('X', TensorProto.FLOAT, [1, 1, 4, 2])
    Y = helper.make_tensor_value_info('Y', TensorProto.FLOAT, [1, 1, 1, 2])

    trn = onnx.helper.make_node('Transpose',
                                inputs=['X'],
                                outputs=['TX'],
                                perm=[0, 1, 3, 2])

    node = onnx.helper.make_node('Resize',
                                 inputs=['TX', '', 'scales'],
                                 outputs=['Y'],
                                 coordinate_transformation_mode='asymmetric',
                                 mode='nearest',
                                 nearest_mode='ceil')

    return ([trn, node], [X], [Y], [scale_tensor])


@onnx_test
def resize_outsize_test():
    out_lens = np.array([1, 1, 4, 6], dtype=np.int64)
    out_lens_tensor = helper.make_tensor(name='out_lens',
                                         data_type=TensorProto.INT64,
                                         dims=out_lens.shape,
                                         vals=out_lens.flatten().astype(
                                             np.int64))

    X = helper.make_tensor_value_info('X', TensorProto.FLOAT, [1, 1, 2, 2])
    Y = helper.make_tensor_value_info('Y', TensorProto.FLOAT, [1, 1, 4, 6])

    node = onnx.helper.make_node(
        'Resize',
        inputs=['X', '', '', 'out_lens'],
        outputs=['Y'],
        coordinate_transformation_mode='tf_half_pixel_for_nn',
        mode='nearest',
        nearest_mode='round_prefer_floor')

    return ([node], [X], [Y], [out_lens_tensor])


@onnx_test
def resize_upsample_linear_ac_test():
    scales = np.array([1.0, 1.0, 2.0, 2.0], dtype=np.float32)
    scales_tensor = helper.make_tensor(name='scales',
                                       data_type=TensorProto.FLOAT,
                                       dims=scales.shape,
                                       vals=scales.flatten().astype(
                                           np.float32))
    X = helper.make_tensor_value_info('X', TensorProto.FLOAT, [1, 1, 2, 2])
    Y = helper.make_tensor_value_info('Y', TensorProto.FLOAT, [])

    node = onnx.helper.make_node(
        'Resize',
        inputs=['X', '', 'scales'],
        outputs=['Y'],
        mode='linear',
        coordinate_transformation_mode='align_corners')

    return ([node], [X], [Y], [scales_tensor])


@onnx_test
def resize_upsample_linear_test():
    scales = np.array([1.0, 1.0, 2.0, 2.0], dtype=np.float32)
    scales_tensor = helper.make_tensor(name='scales',
                                       data_type=TensorProto.FLOAT,
                                       dims=scales.shape,
                                       vals=scales.flatten().astype(
                                           np.float32))
    X = helper.make_tensor_value_info('X', TensorProto.FLOAT, [1, 1, 2, 2])
    Y = helper.make_tensor_value_info('Y', TensorProto.FLOAT, [])

    node = onnx.helper.make_node('Resize',
                                 inputs=['X', '', 'scales'],
                                 outputs=['Y'],
                                 mode='linear')

    return ([node], [X], [Y], [scales_tensor])


@onnx_test
def resize_upsample_pf_test():
    scales = np.array([1.0, 1.0, 2.0, 3.0], dtype=np.float32)
    scale_tensor = helper.make_tensor(name='scales',
                                      data_type=TensorProto.FLOAT,
                                      dims=scales.shape,
                                      vals=scales.flatten().astype(np.float32))

    X = helper.make_tensor_value_info('X', TensorProto.FLOAT, [1, 1, 2, 2])
    Y = helper.make_tensor_value_info('Y', TensorProto.FLOAT, [1, 1, 4, 6])

    node = onnx.helper.make_node('Resize',
                                 inputs=['X', '', 'scales'],
                                 outputs=['Y'],
                                 mode='nearest')

    return ([node], [X], [Y], [scale_tensor])


@onnx_test
def resize_upsample_pc_test():
    scales = np.array([1.0, 1.0, 2.0, 1.5], dtype=np.float32)
    scale_tensor = helper.make_tensor(name='scales',
                                      data_type=TensorProto.FLOAT,
                                      dims=scales.shape,
                                      vals=scales.flatten().astype(np.float32))

    X = helper.make_tensor_value_info('X', TensorProto.FLOAT, [1, 1, 2, 4])
    Y = helper.make_tensor_value_info('Y', TensorProto.FLOAT, [1, 1, 4, 6])

    node = onnx.helper.make_node(
        'Resize',
        inputs=['X', '', 'scales'],
        outputs=['Y'],
        coordinate_transformation_mode='pytorch_half_pixel',
        mode='nearest',
        exclude_outside=0,
        nearest_mode='round_prefer_ceil')

    return ([node], [X], [Y], [scale_tensor])


@onnx_test
def roialign_default_test():
    x = helper.make_tensor_value_info('x', TensorProto.FLOAT, [10, 4, 7, 8])
    roi = helper.make_tensor_value_info('rois', TensorProto.FLOAT, [8, 4])
    bi = helper.make_tensor_value_info('batch_ind', TensorProto.INT64, [8])
    y = helper.make_tensor_value_info('y', TensorProto.FLOAT, [8, 4, 1, 1])

    node = onnx.helper.make_node('RoiAlign',
                                 inputs=['x', 'rois', 'batch_ind'],
                                 outputs=['y'])

    return ([node], [x, roi, bi], [y])


@onnx_test
def roialign_test():
    x = helper.make_tensor_value_info('x', TensorProto.FLOAT, [10, 5, 4, 7])
    roi = helper.make_tensor_value_info('rois', TensorProto.FLOAT, [8, 4])
    bi = helper.make_tensor_value_info('batch_ind', TensorProto.INT64, [8])
    y = helper.make_tensor_value_info('y', TensorProto.FLOAT, [8, 4, 5, 5])

    node = onnx.helper.make_node(
        'RoiAlign',
        inputs=['x', 'rois', 'batch_ind'],
        outputs=['y'],
        spatial_scale=2.0,
        output_height=5,
        output_width=5,
        sampling_ratio=3,
        mode="avg",
        coordinate_transformation_mode="output_half_pixel")

    return ([node], [x, roi, bi], [y])


@onnx_test
def scatter_test():
    x = helper.make_tensor_value_info('data', TensorProto.FLOAT, [3, 4, 5, 6])
    i = helper.make_tensor_value_info('indices', TensorProto.INT32,
                                      [2, 3, 4, 5])
    u = helper.make_tensor_value_info('update', TensorProto.FLOAT,
                                      [2, 3, 4, 5])
    y = helper.make_tensor_value_info('y', TensorProto.FLOAT, [3, 4, 5, 6])

    node = onnx.helper.make_node(
        'Scatter',
        inputs=['data', 'indices', 'update'],
        outputs=['y'],
        axis=-2,
    )

    return ([node], [x, i, u], [y])


@onnx_test
def selu_test():
    x = helper.make_tensor_value_info('x', TensorProto.DOUBLE, [2, 3])
    y = helper.make_tensor_value_info('y', TensorProto.DOUBLE, [2, 3])

    node = onnx.helper.make_node('Selu',
                                 inputs=['x'],
                                 outputs=['y'],
                                 alpha=0.3,
                                 gamma=0.5)

    return ([node], [x], [y])


@onnx_test
def shape_test():
    x = helper.make_tensor_value_info('x', TensorProto.FLOAT, [3, 4, 5, 6])
    y = helper.make_tensor_value_info('y', TensorProto.INT64, [4])

    node = onnx.helper.make_node(
        'Shape',
        inputs=['x'],
        outputs=['y'],
    )

    return ([node], [x], [y])


@onnx_test
def shape_gather_test():
    values = np.array([1])
    # value = helper.make_tensor_value_info('value', TensorProto.INT32, [1])
    x = helper.make_tensor_value_info('x', TensorProto.FLOAT, [7, 3, 10])
    z = helper.make_tensor_value_info('z', TensorProto.FLOAT, [1])

    value_tensor = helper.make_tensor(name='const_tensor',
                                      data_type=TensorProto.INT32,
                                      dims=values.shape,
                                      vals=values.flatten().astype(int))

    node_const = onnx.helper.make_node(
        'Constant',
        inputs=[],
        outputs=['value'],
        value=value_tensor,
    )

    node_shape = onnx.helper.make_node(
        'Shape',
        inputs=['x'],
        outputs=['y'],
    )

    node_gather = helper.make_node(
        'Gather',
        inputs=['y', 'value'],
        outputs=['z'],
        axis=0,
    )

    return ([node_const, node_shape, node_gather], [x], [z])


@onnx_test
def sign_test():
    x = helper.make_tensor_value_info('x', TensorProto.DOUBLE, [10, 5])
    y = helper.make_tensor_value_info('y', TensorProto.DOUBLE, [10, 5])

    node = onnx.helper.make_node(
        'Sign',
        inputs=['x'],
        outputs=['y'],
    )

    return ([node], [x], [y])


@onnx_test
def sin_test():
    x = helper.make_tensor_value_info('x', TensorProto.FLOAT, [10])
    y = helper.make_tensor_value_info('y', TensorProto.FLOAT, [10])

    node = onnx.helper.make_node(
        'Sin',
        inputs=['x'],
        outputs=['y'],
    )

    return ([node], [x], [y])


@onnx_test
def sinh_test():
    x = helper.make_tensor_value_info('x', TensorProto.FLOAT, [10])
    y = helper.make_tensor_value_info('y', TensorProto.FLOAT, [10])

    node = onnx.helper.make_node(
        'Sinh',
        inputs=['x'],
        outputs=['y'],
    )

    return ([node], [x], [y])


@onnx_test
def slice_test():
    x = helper.make_tensor_value_info('0', TensorProto.FLOAT, [3, 2])
    y = helper.make_tensor_value_info('1', TensorProto.FLOAT, [1, 2])

    node = onnx.helper.make_node('Slice',
                                 inputs=['0'],
                                 axes=[0, 1],
                                 starts=[1, 0],
                                 ends=[2, 2],
                                 outputs=['1'])

    return ([node], [x], [y])


@onnx_test
def slice_3arg_test():
    x = helper.make_tensor_value_info('0', TensorProto.FLOAT, [5, 5])
    y = helper.make_tensor_value_info('1', TensorProto.FLOAT, [2, 5])
    start = np.array([0, 0])
    start_tensor = helper.make_tensor(name="start",
                                      data_type=TensorProto.INT32,
                                      dims=start.shape,
                                      vals=start.astype(int))

    arg_start = helper.make_node("Constant",
                                 inputs=[],
                                 outputs=['arg_start'],
                                 value=start_tensor)

    end = np.array([2, 5])
    end_tensor = helper.make_tensor(name="end",
                                    data_type=TensorProto.INT32,
                                    dims=end.shape,
                                    vals=end.astype(int))
    arg_end = helper.make_node("Constant",
                               inputs=[],
                               outputs=['arg_end'],
                               value=end_tensor)

    node = onnx.helper.make_node('Slice',
                                 inputs=['0', 'arg_start', 'arg_end'],
                                 outputs=['1'])

    return ([arg_start, arg_end, node], [x], [y])


@onnx_test
def slice_5arg_test():
    step = np.array([1, 1])
    step_tensor = helper.make_tensor(name="step",
                                     data_type=TensorProto.INT32,
                                     dims=step.shape,
                                     vals=step.astype(int))
    arg_step = helper.make_node("Constant",
                                inputs=[],
                                outputs=['arg_step'],
                                value=step_tensor)

    axis = np.array([-1, -2])
    axis_tensor = helper.make_tensor(name="axis",
                                     data_type=TensorProto.INT32,
                                     dims=axis.shape,
                                     vals=axis.astype(int))
    arg_axis = helper.make_node("Constant",
                                inputs=[],
                                outputs=['arg_axis'],
                                value=axis_tensor)

    end = np.array([-1, -1])
    end_tensor = helper.make_tensor(name="end",
                                    data_type=TensorProto.INT32,
                                    dims=end.shape,
                                    vals=end.astype(int))
    arg_end = helper.make_node("Constant",
                               inputs=[],
                               outputs=['arg_end'],
                               value=end_tensor)

    start = np.array([-5, -3])
    start_tensor = helper.make_tensor(name="start",
                                      data_type=TensorProto.INT32,
                                      dims=start.shape,
                                      vals=start.astype(int))
    arg_start = helper.make_node("Constant",
                                 inputs=[],
                                 outputs=['arg_start'],
                                 value=start_tensor)

    x = helper.make_tensor_value_info('0', TensorProto.FLOAT, [5, 5])
    y = helper.make_tensor_value_info('1', TensorProto.FLOAT, [4, 2])

    node = onnx.helper.make_node(
        'Slice',
        inputs=['0', 'arg_start', 'arg_end', 'arg_axis', 'arg_step'],
        outputs=['1'])

    return ([arg_step, arg_axis, arg_end, arg_start, node], [x], [y])


@onnx_test
def slice_5arg_reverse_test():
    step = np.array([-1, 1])
    step_tensor = helper.make_tensor(name="step",
                                     data_type=TensorProto.INT32,
                                     dims=step.shape,
                                     vals=step.astype(int))
    arg_step = helper.make_node("Constant",
                                inputs=[],
                                outputs=['arg_step'],
                                value=step_tensor)

    axis = np.array([-1, -2])
    axis_tensor = helper.make_tensor(name="axis",
                                     data_type=TensorProto.INT32,
                                     dims=axis.shape,
                                     vals=axis.astype(int))
    arg_axis = helper.make_node("Constant",
                                inputs=[],
                                outputs=['arg_axis'],
                                value=axis_tensor)

    end = np.array([-5, -1])
    end_tensor = helper.make_tensor(name="end",
                                    data_type=TensorProto.INT32,
                                    dims=end.shape,
                                    vals=end.astype(int))
    arg_end = helper.make_node("Constant",
                               inputs=[],
                               outputs=['arg_end'],
                               value=end_tensor)

    start = np.array([-1, -3])
    start_tensor = helper.make_tensor(name="start",
                                      data_type=TensorProto.INT32,
                                      dims=start.shape,
                                      vals=start.astype(int))
    arg_start = helper.make_node("Constant",
                                 inputs=[],
                                 outputs=['arg_start'],
                                 value=start_tensor)

    x = helper.make_tensor_value_info('0', TensorProto.FLOAT, [5, 5])
    y = helper.make_tensor_value_info('1', TensorProto.FLOAT, [4, 2])

    node = onnx.helper.make_node(
        'Slice',
        inputs=['0', 'arg_start', 'arg_end', 'arg_axis', 'arg_step'],
        outputs=['1'])

    return ([arg_step, arg_axis, arg_end, arg_start, node], [x], [y])


@onnx_test
def slice_5arg_step_test():
    step = np.array([-2, 2])
    step_tensor = helper.make_tensor(name="step",
                                     data_type=TensorProto.INT32,
                                     dims=step.shape,
                                     vals=step.astype(int))
    arg_step = helper.make_node("Constant",
                                inputs=[],
                                outputs=['arg_step'],
                                value=step_tensor)

    axis = np.array([-1, -2])
    axis_tensor = helper.make_tensor(name="axis",
                                     data_type=TensorProto.INT32,
                                     dims=axis.shape,
                                     vals=axis.astype(int))
    arg_axis = helper.make_node("Constant",
                                inputs=[],
                                outputs=['arg_axis'],
                                value=axis_tensor)

    end = np.array([-5, -1])
    end_tensor = helper.make_tensor(name="end",
                                    data_type=TensorProto.INT32,
                                    dims=end.shape,
                                    vals=end.astype(int))
    arg_end = helper.make_node("Constant",
                               inputs=[],
                               outputs=['arg_end'],
                               value=end_tensor)

    start = np.array([-1, -3])
    start_tensor = helper.make_tensor(name="start",
                                      data_type=TensorProto.INT32,
                                      dims=start.shape,
                                      vals=start.astype(int))
    arg_start = helper.make_node("Constant",
                                 inputs=[],
                                 outputs=['arg_start'],
                                 value=start_tensor)

    x = helper.make_tensor_value_info('0', TensorProto.FLOAT, [5, 5])
    y = helper.make_tensor_value_info('1', TensorProto.FLOAT, [4, 2])

    node = onnx.helper.make_node(
        'Slice',
        inputs=['0', 'arg_start', 'arg_end', 'arg_axis', 'arg_step'],
        outputs=['1'])

    return ([arg_step, arg_axis, arg_end, arg_start, node], [x], [y])


@onnx_test
def slice_max_end_test():
    x = helper.make_tensor_value_info('0', TensorProto.FLOAT, [10, 20])
    y = helper.make_tensor_value_info('1', TensorProto.FLOAT, [9, 17])

    node = onnx.helper.make_node('Slice',
                                 inputs=['0'],
                                 axes=[0, 1],
                                 starts=[1, 2],
                                 ends=[3000000000, -1],
                                 outputs=['1'])

    return ([node], [x], [y])


@onnx_test
def softmax_test():
    x = helper.make_tensor_value_info('0', TensorProto.FLOAT, [1, 3])
    y = helper.make_tensor_value_info('1', TensorProto.FLOAT, [1, 3])

    node = onnx.helper.make_node('Softmax', inputs=['0'], outputs=['1'])

    return ([node], [x], [y])


@onnx_test
def softmax_nonstd_input_test():
    x = helper.make_tensor_value_info('0', TensorProto.FLOAT, [6, 8])
    y = helper.make_tensor_value_info('2', TensorProto.FLOAT, [3, 4])

    node0 = onnx.helper.make_node('Slice',
                                  inputs=['0'],
                                  axes=[0, 1],
                                  starts=[1, 0],
                                  ends=[4, 4],
                                  outputs=['1'])

    node1 = onnx.helper.make_node('Softmax', inputs=['1'], outputs=['2'])

    return ([node0, node1], [x], [y])


@onnx_test
def softsign_test():
    x = helper.make_tensor_value_info('x', TensorProto.FLOAT, [5])
    y = helper.make_tensor_value_info('y', TensorProto.FLOAT, [5])

    node = onnx.helper.make_node('Softsign', inputs=['x'], outputs=['y'])

    return ([node], [x], [y])


def softplus_test():
    x = helper.make_tensor_value_info('x', TensorProto.FLOAT, [5])
    y = helper.make_tensor_value_info('y', TensorProto.FLOAT, [5])

    node = onnx.helper.make_node('Softplus', inputs=['x'], outputs=['y'])

    return ([node], [x], [y])


@onnx_test
def softsign_nd_test():
    x = helper.make_tensor_value_info('x', TensorProto.FLOAT16, [3, 4, 5])
    y = helper.make_tensor_value_info('y', TensorProto.FLOAT16, [3, 4, 5])

    node = onnx.helper.make_node('Softsign', inputs=['x'], outputs=['y'])

    return ([node], [x], [y])


def softplus_nd_test():
    x = helper.make_tensor_value_info('x', TensorProto.FLOAT16, [3, 4, 5])
    y = helper.make_tensor_value_info('y', TensorProto.FLOAT16, [3, 4, 5])

    node = onnx.helper.make_node('Softplus', inputs=['x'], outputs=['y'])

    return ([node], [x], [y])


@onnx_test
def split_minus_axis_test():
    x = helper.make_tensor_value_info('x', TensorProto.FLOAT, [10, 15])
    y1 = helper.make_tensor_value_info('y1', TensorProto.FLOAT, [10, 5])
    y2 = helper.make_tensor_value_info('y2', TensorProto.FLOAT, [10, 5])
    y3 = helper.make_tensor_value_info('y3', TensorProto.FLOAT, [10, 5])

    node = onnx.helper.make_node(
        'Split',
        inputs=['x'],
        outputs=['y1', 'y2', 'y3'],
        axis=-1,
    )

    return ([node], [x], [y1, y2, y3])


@onnx_test
def split_test():
    x = helper.make_tensor_value_info('x', TensorProto.FLOAT, [10, 15])
    y1 = helper.make_tensor_value_info('y1', TensorProto.FLOAT, [10, 7])
    y2 = helper.make_tensor_value_info('y2', TensorProto.FLOAT, [10, 4])
    y3 = helper.make_tensor_value_info('y3', TensorProto.FLOAT, [10, 4])

    node = onnx.helper.make_node('Split',
                                 inputs=['x'],
                                 outputs=['y1', 'y2', 'y3'],
                                 axis=1,
                                 split=[7, 4, 4])

    return ([node], [x], [y1, y2, y3])


@onnx_test
def split_test_default():
    x = helper.make_tensor_value_info('x', TensorProto.FLOAT, [10, 15])
    y1 = helper.make_tensor_value_info('y1', TensorProto.FLOAT, [5, 15])
    y2 = helper.make_tensor_value_info('y2', TensorProto.FLOAT, [5, 15])

    node = onnx.helper.make_node(
        'Split',
        inputs=['x'],
        outputs=['y1', 'y2'],
    )

    return ([node], [x], [y1, y2])


@onnx_test
def sqrt_test():
    x = helper.make_tensor_value_info('x', TensorProto.FLOAT, [10, 15])
    y = helper.make_tensor_value_info('y', TensorProto.FLOAT, [10, 15])

    node = onnx.helper.make_node(
        'Sqrt',
        inputs=['x'],
        outputs=['y'],
    )

    return ([node], [x], [y])


@onnx_test
def squeeze_axes_input_test():
    x = helper.make_tensor_value_info('x', TensorProto.FLOAT, [3, 1, 5, 1])
    y = helper.make_tensor_value_info('y', TensorProto.FLOAT, [3, 5])
    axes = np.array([1, 3], dtype=np.int64)
    axes_tensor = helper.make_tensor(name="axes",
                                     data_type=TensorProto.INT64,
                                     dims=axes.shape,
                                     vals=axes.astype(np.int64))

    node = onnx.helper.make_node('Squeeze',
                                 inputs=['x', 'axes'],
                                 outputs=['y'])

    return ([node], [x], [y], [axes_tensor])


@onnx_test
def squeeze_empty_axes_test():
    x = helper.make_tensor_value_info('x', TensorProto.FLOAT, [3, 1, 5, 1])
    y = helper.make_tensor_value_info('y', TensorProto.FLOAT, [3, 5])
    axes = np.array([], dtype=np.int64)
    axes_tensor = helper.make_tensor(name="axes",
                                     data_type=TensorProto.INT64,
                                     dims=axes.shape,
                                     vals=axes.astype(np.int64))

    node = onnx.helper.make_node('Squeeze',
                                 inputs=['x', 'axes'],
                                 outputs=['y'])

    return ([node], [x], [y], [axes_tensor])


@onnx_test
def squeeze_unsqueeze_test():
    x = helper.make_tensor_value_info('0', TensorProto.FLOAT,
                                      [1, 3, 1, 1, 2, 1])
    y = helper.make_tensor_value_info('2', TensorProto.FLOAT,
                                      [1, 1, 3, 1, 2, 1])

    node = onnx.helper.make_node('Squeeze',
                                 inputs=['0'],
                                 axes=[0, 2, 3, 5],
                                 outputs=['1'])

    node2 = onnx.helper.make_node('Unsqueeze',
                                  inputs=['1'],
                                  axes=[0, 1, 3, 5],
                                  outputs=['2'])

    return ([node, node2], [x], [y])


@onnx_test
def sub_bcast_test():
    arg0 = helper.make_tensor_value_info('0', TensorProto.FLOAT, [2, 3, 4, 5])
    arg1 = helper.make_tensor_value_info('1', TensorProto.FLOAT, [3, 4])
    arg_out = helper.make_tensor_value_info('out', TensorProto.FLOAT,
                                            [2, 3, 4, 5])

    node = onnx.helper.make_node(
        'Sub',
        inputs=['0', '1'],
        outputs=['out'],
        broadcast=1,
        axis=1,
    )

    return ([node], [arg0, arg1], [arg_out])


@onnx_test
def sub_scalar_test():
    values = np.array([1])
    arg_node = helper.make_tensor_value_info('0', TensorProto.FLOAT,
                                             [2, 3, 4, 5])
    arg_out = helper.make_tensor_value_info('out', TensorProto.FLOAT,
                                            [2, 3, 4, 5])

    values_tensor = helper.make_tensor(name='const',
                                       data_type=TensorProto.FLOAT,
                                       dims=values.reshape(()).shape,
                                       vals=values.flatten().astype(float))

    arg_const = onnx.helper.make_node(
        'Constant',
        inputs=[],
        outputs=['arg_const'],
        value=values_tensor,
    )

    node = onnx.helper.make_node(
        'Sub',
        inputs=['0', 'arg_const'],
        outputs=['out'],
    )

    return ([arg_const, node], [arg_node], [arg_out])


@onnx_test
def sum_int_test():
    a = helper.make_tensor_value_info('0', TensorProto.INT16, [3])
    b = helper.make_tensor_value_info('1', TensorProto.UINT16, [3])
    c = helper.make_tensor_value_info('2', TensorProto.UINT32, [3])
    y = helper.make_tensor_value_info('3', TensorProto.UINT32, [3])

    cnode1 = onnx.helper.make_node('Cast', inputs=['0'], outputs=['c0'], to=12)

    cnode2 = onnx.helper.make_node('Cast', inputs=['1'], outputs=['c1'], to=12)

    node = onnx.helper.make_node(
        'Sum',
        inputs=['c0', 'c1', '2'],
        outputs=['3'],
    )

    return ([cnode1, cnode2, node], [a, b, c], [y])


@onnx_test
def sum_test():
    a = helper.make_tensor_value_info('0', TensorProto.FLOAT, [3])
    b = helper.make_tensor_value_info('1', TensorProto.FLOAT, [3])
    c = helper.make_tensor_value_info('2', TensorProto.FLOAT, [3])
    y = helper.make_tensor_value_info('3', TensorProto.FLOAT, [3])

    node = onnx.helper.make_node(
        'Sum',
        inputs=['0', '1', '2'],
        outputs=['3'],
    )

    return ([node], [a, b, c], [y])


@onnx_test
def sum_type_test():
    valb = np.array([1, 0])
    t_bool = helper.make_tensor(name="bool",
                                data_type=TensorProto.BOOL,
                                dims=valb.shape,
                                vals=valb.astype(np.bool))

    val = np.array([1, 1])
    t_int8 = helper.make_tensor(name="int8",
                                data_type=TensorProto.INT8,
                                dims=val.shape,
                                vals=val.astype(np.int8))

    t_uint8 = helper.make_tensor(name="uint8",
                                 data_type=TensorProto.UINT8,
                                 dims=val.shape,
                                 vals=val.astype(np.uint8))

    t_uint16 = helper.make_tensor(name="uint16",
                                  data_type=TensorProto.UINT16,
                                  dims=val.shape,
                                  vals=val.astype(np.uint16))

    t_uint32 = helper.make_tensor(name="uint32",
                                  data_type=TensorProto.UINT32,
                                  dims=val.shape,
                                  vals=val.astype(np.uint32))

    t_uint64 = helper.make_tensor(name="uint64",
                                  data_type=TensorProto.UINT64,
                                  dims=val.shape,
                                  vals=val.astype(np.uint64))

    t_double = helper.make_tensor(name="double",
                                  data_type=TensorProto.DOUBLE,
                                  dims=val.shape,
                                  vals=val.astype(np.float64))

    valr = np.array([1.5, 2.0])
    t_raw = helper.make_tensor(name="raw",
                               data_type=TensorProto.DOUBLE,
                               dims=valr.shape,
                               vals=valr.tobytes(),
                               raw=True)

    n_bool = onnx.helper.make_node('Cast',
                                   inputs=['bool'],
                                   outputs=['o_bool'],
                                   to=11)

    n_int8 = onnx.helper.make_node('Cast',
                                   inputs=['int8'],
                                   outputs=['o_int8'],
                                   to=11)

    n_uint8 = onnx.helper.make_node('Cast',
                                    inputs=['uint8'],
                                    outputs=['o_uint8'],
                                    to=11)

    n_uint16 = onnx.helper.make_node('Cast',
                                     inputs=['uint16'],
                                     outputs=['o_uint16'],
                                     to=11)

    n_uint32 = onnx.helper.make_node('Cast',
                                     inputs=['uint32'],
                                     outputs=['o_uint32'],
                                     to=11)

    n_uint64 = onnx.helper.make_node('Cast',
                                     inputs=['uint64'],
                                     outputs=['o_uint64'],
                                     to=11)

    node = onnx.helper.make_node(
        'Sum',
        inputs=[
            'o_bool', 'o_int8', 'o_uint8', 'o_uint16', 'o_uint32', 'o_uint64',
            'double', 'raw'
        ],
        outputs=['out'],
    )

    y = helper.make_tensor_value_info('out', TensorProto.DOUBLE, [2])

    return ([n_bool, n_int8, n_uint8, n_uint16, n_uint32, n_uint64,
             node], [], [y], [
                 t_bool, t_int8, t_uint8, t_uint16, t_uint32, t_uint64,
                 t_double, t_raw
             ])


@onnx_test
def tan_test():
    x = helper.make_tensor_value_info('x', TensorProto.FLOAT, [10])
    y = helper.make_tensor_value_info('y', TensorProto.FLOAT, [10])

    node = onnx.helper.make_node(
        'Tan',
        inputs=['x'],
        outputs=['y'],
    )

    return ([node], [x], [y])


@onnx_test
def tanh_test():
    x = helper.make_tensor_value_info('x', TensorProto.FLOAT, [1])
    y = helper.make_tensor_value_info('y', TensorProto.FLOAT, [1])

    node = onnx.helper.make_node(
        'Tanh',
        inputs=['x'],
        outputs=['y'],
    )

    return ([node], [x], [y])


@onnx_test
def thresholdedrelu_default_test():
    x = helper.make_tensor_value_info('x', TensorProto.FLOAT, [2, 2, 3])
    y = helper.make_tensor_value_info('y', TensorProto.FLOAT, [2, 2, 3])

    node = onnx.helper.make_node('ThresholdedRelu',
                                 inputs=['x'],
                                 outputs=['y'])

    return ([node], [x], [y])


@onnx_test
def thresholdedrelu_test():
    x = helper.make_tensor_value_info('x', TensorProto.FLOAT, [2, 2, 3])
    y = helper.make_tensor_value_info('y', TensorProto.FLOAT, [2, 2, 3])
    alpha = 3.0

    node = onnx.helper.make_node('ThresholdedRelu',
                                 inputs=['x'],
                                 outputs=['y'],
                                 alpha=alpha)

    return ([node], [x], [y])


@onnx_test
def thresholdedrelu_int_test():
    x = helper.make_tensor_value_info('x', TensorProto.INT32, [2, 2, 3])
    y = helper.make_tensor_value_info('y', TensorProto.INT32, [2, 2, 3])
    alpha = 3.0

    node = onnx.helper.make_node('ThresholdedRelu',
                                 inputs=['x'],
                                 outputs=['y'],
                                 alpha=alpha)

    return ([node], [x], [y])


@onnx_test
def tile_test():
    x = helper.make_tensor_value_info('x', TensorProto.FLOAT, [2, 2])
    y = helper.make_tensor_value_info('y', TensorProto.INT64, [2])
    z = helper.make_tensor_value_info('z', TensorProto.FLOAT, [2, 4])

    node = onnx.helper.make_node('Tile', inputs=['x', 'y'], outputs=['z'])

    return ([node], [x, y], [z],
            [helper.make_tensor('y', TensorProto.INT64, [2], [1, 2])])


@onnx_test
def tile_test_3x2():
    x = helper.make_tensor_value_info('x', TensorProto.FLOAT, [2, 2])
    y = helper.make_tensor_value_info('y', TensorProto.INT64, [2])
    z = helper.make_tensor_value_info('z', TensorProto.FLOAT, [6, 4])

    node = onnx.helper.make_node('Tile', inputs=['x', 'y'], outputs=['z'])

    return ([node], [x, y], [z],
            [helper.make_tensor('y', TensorProto.INT64, [2], [3, 2])])


@onnx_test
def topk_attrk_test():
    x = helper.make_tensor_value_info('data', TensorProto.FLOAT, [2, 5, 3, 2])
    val = helper.make_tensor_value_info('val', TensorProto.FLOAT, [2, 2, 3, 2])
    ind = helper.make_tensor_value_info('indices', TensorProto.INT64,
                                        [2, 2, 3, 2])

    node = onnx.helper.make_node('TopK',
                                 inputs=['data'],
                                 outputs=['val', 'indices'],
                                 k=2)
    return ([node], [x], [val, ind])


@onnx_test
def topk_neg_axis_test():
    k = np.array([3])
    x = helper.make_tensor_value_info('data', TensorProto.FLOAT, [3, 4, 5, 6])
    val = helper.make_tensor_value_info('val', TensorProto.FLOAT, [3, 3, 5, 6])
    ind = helper.make_tensor_value_info('indices', TensorProto.INT64,
                                        [3, 3, 5, 6])

    k_tensor = helper.make_tensor(name='k',
                                  data_type=TensorProto.INT64,
                                  dims=k.shape,
                                  vals=k.astype(np.int64))

    node = onnx.helper.make_node('TopK',
                                 inputs=['data', 'k'],
                                 outputs=['val', 'indices'],
                                 axis=-2,
                                 sorted=0)
    return ([node], [x], [val, ind], [k_tensor])


@onnx_test
def topk_test():
    k = np.array([4])
    x = helper.make_tensor_value_info('data', TensorProto.FLOAT, [2, 5, 3, 2])
    val = helper.make_tensor_value_info('val', TensorProto.FLOAT, [2, 4, 3, 2])
    ind = helper.make_tensor_value_info('indices', TensorProto.INT64,
                                        [2, 4, 3, 2])

    k_tensor = helper.make_tensor(name='k',
                                  data_type=TensorProto.INT64,
                                  dims=k.shape,
                                  vals=k.astype(np.int64))

    node = onnx.helper.make_node('TopK',
                                 inputs=['data', 'k'],
                                 outputs=['val', 'indices'],
                                 largest=0,
                                 axis=1)
    return ([node], [x], [val, ind], [k_tensor])


def transpose_default_perm_test():
    x = helper.make_tensor_value_info('0', TensorProto.FLOAT, [1, 5, 2, 3])
    y = helper.make_tensor_value_info('1', TensorProto.FLOAT, [3, 2, 5, 1])

    node = onnx.helper.make_node(
        'Transpose',
        inputs=['0'],
        outputs=['1'],
    )

    return ([node], [x], [y])


@onnx_test
def transpose_invalid_perm_test():
    x = helper.make_tensor_value_info('0', TensorProto.FLOAT, [1, 2, 4, 3])
    y = helper.make_tensor_value_info('1', TensorProto.FLOAT, [1, 3, 2, 2])

    node = onnx.helper.make_node(
        'Transpose',
        perm=[0, 2, 1],
        inputs=['0'],
        outputs=['1'],
    )

    return ([node], [x], [y])


@onnx_test
def transpose_test():
    x = helper.make_tensor_value_info('0', TensorProto.FLOAT, [1, 2, 2, 3])
    y = helper.make_tensor_value_info('1', TensorProto.FLOAT, [1, 3, 2, 2])

    node = onnx.helper.make_node(
        'Transpose',
        perm=[0, 3, 1, 2],
        inputs=['0'],
        outputs=['1'],
    )

    return ([node], [x], [y])


@onnx_test
def transpose_gather_test():
    x = helper.make_tensor_value_info('data', TensorProto.FLOAT, [3, 5, 4, 6])
    i = helper.make_tensor_value_info('indices', TensorProto.INT32,
                                      [2, 4, 3, 5])
    y = helper.make_tensor_value_info('y', TensorProto.FLOAT,
                                      [3, 2, 3, 4, 5, 4, 5, 6])

    td = onnx.helper.make_node(
        'Transpose',
        inputs=['data'],
        outputs=['tdata'],
        perm=[0, 2, 1, 3],
    )

    ti = onnx.helper.make_node('Transpose',
                               inputs=['indices'],
                               outputs=['tindices'],
                               perm=[0, 2, 1, 3])

    node = onnx.helper.make_node(
        'Gather',
        inputs=['tdata', 'tindices'],
        outputs=['y'],
        axis=1,
    )

    return ([td, ti, node], [x, i], [y])


@onnx_test
def undefined_test():
    x = helper.make_tensor_value_info('0', TensorProto.FLOAT, [2, 3, 4, 5])
    y = helper.make_tensor_value_info('1', TensorProto.FLOAT, [2, 3, 4, 5])

    node = onnx.helper.make_node('Identity', inputs=[''], outputs=['1'])

    return ([node], [x], [y])


@onnx_test
def unknown_test():
    x = helper.make_tensor_value_info('0', TensorProto.FLOAT, [2, 3, 4, 5])
    y = helper.make_tensor_value_info('1', TensorProto.FLOAT, [3, 4])

    helper.make_tensor_value_info('2', TensorProto.FLOAT, [2, 3, 4, 5])

    a = helper.make_tensor_value_info('3', TensorProto.FLOAT, [2, 3, 4, 5])

    node = onnx.helper.make_node('Unknown', inputs=['0', '1'], outputs=['2'])

    node2 = onnx.helper.make_node('Unknown', inputs=['2'], outputs=['3'])

    return ([node, node2], [x, y], [a])


@onnx_test
def unknown_aten_test():
    x = helper.make_tensor_value_info('0', TensorProto.FLOAT, [2, 3, 4, 5])
    y = helper.make_tensor_value_info('1', TensorProto.FLOAT, [3, 4])

    helper.make_tensor_value_info('2', TensorProto.FLOAT, [2, 3, 4, 5])

    a = helper.make_tensor_value_info('3', TensorProto.FLOAT, [2, 3, 4, 5])

    node = onnx.helper.make_node('ATen',
                                 inputs=['0', '1'],
                                 outputs=['2'],
                                 operator='unknown')

    return ([node], [x, y], [a])


@onnx_test
def upsample_test():
    scales = np.array([1.0, 1.0, 2.0, 3.0], dtype=np.float32)
    scale_tensor = helper.make_tensor(name='scales',
                                      data_type=TensorProto.FLOAT,
                                      dims=scales.shape,
                                      vals=scales.flatten().astype(np.float32))

    X = helper.make_tensor_value_info('X', TensorProto.FLOAT, [1, 1, 2, 2])
    Y = helper.make_tensor_value_info('Y', TensorProto.FLOAT, [1, 1, 4, 6])

    node = onnx.helper.make_node(
        'Upsample',
        inputs=['X', 'scales'],
        outputs=['Y'],
        mode='nearest',
    )

    return ([node], [X], [Y], [scale_tensor])


@onnx_test
def variable_batch_test():
    x = helper.make_tensor_value_info('0', TensorProto.FLOAT,
                                      [None, 3, 16, 16])
    y = helper.make_tensor_value_info('1', TensorProto.FLOAT,
                                      [None, 3, 16, 16])

    node = onnx.helper.make_node('Identity', inputs=['0'], outputs=['1'])

    return ([node], [x], [y])


@onnx_test
def variable_batch_leq_zero_test():
    x = helper.make_tensor_value_info('0', TensorProto.FLOAT, [0, 3, 16, 16])
    y = helper.make_tensor_value_info('1', TensorProto.FLOAT, [-1, 3, 16, 16])

    z = helper.make_tensor_value_info('2', TensorProto.FLOAT, [-1, 3, 16, 16])
    node = onnx.helper.make_node('Add', inputs=['0', '1'], outputs=['2'])

    return ([node], [x, y], [z])


@onnx_test
def where_test():
    c = helper.make_tensor_value_info('c', TensorProto.BOOL, [2])
    x = helper.make_tensor_value_info('x', TensorProto.FLOAT, [2, 2, 2])
    y = helper.make_tensor_value_info('y', TensorProto.FLOAT, [2, 1, 2, 2])

    z = helper.make_tensor_value_info('z', TensorProto.FLOAT, [2, 2, 2, 2])
    node = onnx.helper.make_node('Where',
                                 inputs=['c', 'x', 'y'],
                                 outputs=['z'])

    return ([node], [c, x, y], [z])
