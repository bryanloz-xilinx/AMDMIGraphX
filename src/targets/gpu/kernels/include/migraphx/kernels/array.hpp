#ifndef MIGRAPHX_GUARD_AMDMIGRAPHX_KERNELS_ARRAY_HPP
#define MIGRAPHX_GUARD_AMDMIGRAPHX_KERNELS_ARRAY_HPP

#include <migraphx/kernels/types.hpp>
#include <migraphx/kernels/type_traits.hpp>
#include <migraphx/kernels/integral_constant.hpp>
#include <migraphx/kernels/debug.hpp>

namespace migraphx {

// NOLINTNEXTLINE
#define MIGRAPHX_DEVICE_ARRAY_OP(op, binary_op)                                    \
    template <class U>                                                             \
    constexpr array& operator op(const array<U, N>& x)                             \
    {                                                                              \
        for(index_int i = 0; i < N; i++)                                           \
            d[i] op x[i];                                                          \
        return *this;                                                              \
    }                                                                              \
    template <class U, MIGRAPHX_REQUIRES(is_convertible<U, T>{})>                  \
    constexpr array& operator op(const U& x)                                       \
    {                                                                              \
        for(index_int i = 0; i < N; i++)                                           \
            d[i] op x;                                                             \
        return *this;                                                              \
    }                                                                              \
    template <class U>                                                             \
    friend constexpr auto operator binary_op(const array& x, const array<U, N>& y) \
    {                                                                              \
        array<decltype(T {} binary_op U{}), N> z{};                                \
        for(index_int i = 0; i < N; i++)                                           \
            z[i] = x[i] binary_op y[i];                                            \
        return z;                                                                  \
    }                                                                              \
    template <class U, MIGRAPHX_REQUIRES(is_convertible<U, T>{})>                  \
    friend constexpr auto operator binary_op(const array& x, const U& y)           \
    {                                                                              \
        array<decltype(T {} binary_op U{}), N> z{};                                \
        for(index_int i = 0; i < N; i++)                                           \
            z[i] = x[i] binary_op y;                                               \
        return z;                                                                  \
    }                                                                              \
    template <class U, MIGRAPHX_REQUIRES(is_convertible<U, T>{})>                  \
    friend constexpr auto operator binary_op(const U& x, const array& y)           \
    {                                                                              \
        array<decltype(T {} binary_op U{}), N> z{};                                \
        for(index_int i = 0; i < N; i++)                                           \
            z[i] = x binary_op y[i];                                               \
        return z;                                                                  \
    }

template <class T, index_int N>
struct array
{
    T d[N];
    constexpr T& operator[](index_int i)
    {
        MIGRAPHX_ASSERT(i < N);
        return d[i];
    }
    constexpr const T& operator[](index_int i) const
    {
        MIGRAPHX_ASSERT(i < N);
        return d[i];
    }

    constexpr T& front() { return d[0]; }
    constexpr const T& front() const { return d[0]; }

    constexpr T& back() { return d[N - 1]; }
    constexpr const T& back() const { return d[N - 1]; }

    constexpr T* data() { return d; }
    constexpr const T* data() const { return d; }

    constexpr index_constant<N> size() const { return {}; }

    constexpr T* begin() { return d; }
    constexpr const T* begin() const { return d; }

    constexpr T* end() { return d + size(); }
    constexpr const T* end() const { return d + size(); }

    constexpr T dot(const array& x) const
    {
        T result = 0;
        for(index_int i = 0; i < N; i++)
            result += x[i] * d[i];
        return result;
    }

    constexpr T product() const
    {
        T result = 1;
        for(index_int i = 0; i < N; i++)
            result *= d[i];
        return result;
    }

    constexpr T single(index_int width = 100) const
    {
        T result = 0;
        T a      = 1;
        for(index_int i = 0; i < N; i++)
        {
            result += d[N - i - 1] * a;
            a *= width;
        }
        return result;
    }

    MIGRAPHX_DEVICE_ARRAY_OP(+=, +)
    MIGRAPHX_DEVICE_ARRAY_OP(-=, -)
    MIGRAPHX_DEVICE_ARRAY_OP(*=, *)
    MIGRAPHX_DEVICE_ARRAY_OP(/=, /)
    MIGRAPHX_DEVICE_ARRAY_OP(%=, %)
    MIGRAPHX_DEVICE_ARRAY_OP(&=, &)
    MIGRAPHX_DEVICE_ARRAY_OP(|=, |)
    MIGRAPHX_DEVICE_ARRAY_OP(^=, ^)

    friend constexpr bool operator==(const array& x, const array& y)
    {
        for(index_int i = 0; i < N; i++)
        {
            if(x[i] != y[i])
                return false;
        }
        return true;
    }

    friend constexpr bool operator!=(const array& x, const array& y) { return !(x == y); }
    // This uses the product order rather than lexical order
    friend constexpr bool operator<(const array& x, const array& y)
    {
        for(index_int i = 0; i < N; i++)
        {
            if(not(x[i] < y[i]))
                return false;
        }
        return true;
    }
    friend constexpr bool operator>(const array& x, const array& y) { return y < x; }
    friend constexpr bool operator<=(const array& x, const array& y) { return (x < y) or (x == y); }
    friend constexpr bool operator>=(const array& x, const array& y) { return (y < x) or (x == y); }

    constexpr array carry(array result) const
    {
        uint32_t overflow = 0;
        for(std::ptrdiff_t i = result.size() - 1; i > 0; i--)
        {
            auto z = result[i] + overflow;
            // Reset overflow
            overflow = 0;
            // Compute overflow using while loop instead of mod
            while(z >= d[i])
            {
                z -= d[i];
                overflow += 1;
            }
            result[i] = z;
        }
        result[0] += overflow;
        return result;
    }

    template <class Stream>
    friend constexpr const Stream& operator<<(const Stream& ss, const array& a)
    {
        for(index_int i = 0; i < N; i++)
        {
            if(i > 0)
                ss << ", ";
            ss << a[i];
        }
        return ss;
    }
};

template <class T, T... Xs>
struct integral_const_array : array<T, sizeof...(Xs)>
{
    using base_array = array<T, sizeof...(Xs)>;
    MIGRAPHX_DEVICE_CONSTEXPR integral_const_array() : base_array({Xs...}) {}
};

template <class T, T... Xs, class F>
constexpr auto transform(integral_const_array<T, Xs...>, F f)
{
    return integral_const_array<T, f(Xs)...>{};
}

template <class T, T... Xs, class U, U... Ys, class F>
constexpr auto transform(integral_const_array<T, Xs...>, integral_const_array<U, Ys...>, F f)
{
    return integral_const_array<T, f(Xs, Ys)...>{};
}

template <index_int... Ns>
using index_ints = integral_const_array<index_int, Ns...>;

} // namespace migraphx

#endif
