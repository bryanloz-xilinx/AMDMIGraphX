#include <migraphx/gpu/multinomial.hpp>
#include <migraphx/gpu/device/multinomial.hpp>
#include <migraphx/gpu/context.hpp>
#include <migraphx/tune_axis.hpp>

namespace migraphx {
inline namespace MIGRAPHX_INLINE_NS {
namespace gpu {

shape hip_multinomial::compute_shape(std::vector<shape> inputs) const
{
    inputs.pop_back();
    return op.compute_shape(inputs);
}

argument
hip_multinomial::compute(context& ctx, const shape&, const std::vector<argument>& args) const
{
    device::multinomial(ctx.get_stream().get(), args.back(), args.front(), args[1]);
    return args.back();
}

} // namespace gpu
} // namespace MIGRAPHX_INLINE_NS
} // namespace migraphx
