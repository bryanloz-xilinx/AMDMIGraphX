/*=============================================================================
    Copyright (c) 2017 Paul Fultz II
    types.hpp
    Distributed under the Boost Software License, Version 1.0. (See accompanying
    file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
==============================================================================*/

#ifndef MIGRAPHX_GUARD_RTGLIB_GPU_DEVICE_TYPES_HPP
#define MIGRAPHX_GUARD_RTGLIB_GPU_DEVICE_TYPES_HPP

#include <hip/hip_runtime.h>
#include <migraphx/half.hpp>
#include <migraphx/config.hpp>
#include <migraphx/tensor_view.hpp>

namespace migraphx {
inline namespace MIGRAPHX_INLINE_NS {
namespace gpu {
namespace device {

using index_int = std::uint32_t;

#define MIGRAPHX_DEVICE_CONSTEXPR constexpr __device__ __host__ // NOLINT

template <class T, index_int N>
using vec = T __attribute__((ext_vector_type(N)));

template <index_int N, class T>
__device__ __host__ T* as_pointer(vec<T, N>* x)
{
    return reinterpret_cast<T*>(x);
}

template <index_int N, class T>
__device__ __host__ vec<T, N>* as_vec(T* x)
{
    return reinterpret_cast<vec<T, N>*>(x);
}

template <index_int N, class T>
tensor_view<vec<T, N>> as_vec(tensor_view<T> x)
{
    return {x.get_shape(), as_vec<N>(x.data())};
}

template <index_int N, class... Ts>
auto pack_vec(Ts... xs)
{
    return [=](auto f, index_int n) { return f(as_vec<N>(xs)[n]...); };
}

using gpu_half = __fp16;

namespace detail {
template <class T>
struct device_type
{
    using type = T;
};

template <class T, index_int N>
struct device_type<vec<T, N>>
{
    using type = vec<typename device_type<T>::type, N>;
};

template <>
struct device_type<half>
{
    using type = gpu_half;
};

template <class T>
struct host_type
{
    using type = T;
};

template <>
struct host_type<gpu_half>
{
    using type = half;
};

} // namespace detail

template <class T>
using host_type = typename detail::host_type<T>::type;

template <class T>
using device_type = typename detail::device_type<T>::type;

template <class T>
host_type<T> host_cast(T x)
{
    return reinterpret_cast<const host_type<T>&>(x);
}

template <class T>
host_type<T>* host_cast(T* x)
{
    return reinterpret_cast<host_type<T>*>(x);
}

template <class T>
__device__ __host__ device_type<T> device_cast(const T& x)
{
    return reinterpret_cast<const device_type<T>&>(x);
}

template <class T>
__device__ __host__ device_type<T>* device_cast(T* x)
{
    return reinterpret_cast<device_type<T>*>(x);
}

template <class T>
__device__ __host__ tensor_view<device_type<T>> device_cast(tensor_view<T> x)
{
    return {x.get_shape(), reinterpret_cast<device_type<T>*>(x.data())};
}

template <class T>
__device__ __host__ T to_hip_type(T x)
{
    return x;
}

// Hip doens't support __fp16
inline __device__ __host__ float to_hip_type(gpu_half x) { return x; }

#define MIGRAPHX_DETAIL_EXTEND_TRAIT_FOR(trait, T) \
    template <class X>                             \
    struct trait : std::trait<X>                   \
    {                                              \
    };                                             \
                                                   \
    template <>                                    \
    struct trait<T> : std::true_type               \
    {                                              \
    };

MIGRAPHX_DETAIL_EXTEND_TRAIT_FOR(is_floating_point, __fp16)
MIGRAPHX_DETAIL_EXTEND_TRAIT_FOR(is_signed, __fp16)
MIGRAPHX_DETAIL_EXTEND_TRAIT_FOR(is_arithmetic, __fp16)

} // namespace device
} // namespace gpu
} // namespace MIGRAPHX_INLINE_NS
} // namespace migraphx

#endif
