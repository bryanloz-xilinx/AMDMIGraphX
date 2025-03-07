#ifndef MIGRAPHX_GUARD_MIGRAPHLIB_STRINGUTILS_HPP
#define MIGRAPHX_GUARD_MIGRAPHLIB_STRINGUTILS_HPP

#include <algorithm>
#include <numeric>
#include <string>
#include <sstream>
#include <unordered_map>
#include <vector>
#include <migraphx/config.hpp>

namespace migraphx {
inline namespace MIGRAPHX_INLINE_NS {

#define MIGRAPHX_STRINGIZE_1(...) #__VA_ARGS__
#define MIGRAPHX_STRINGIZE(...) MIGRAPHX_STRINGIZE_1(__VA_ARGS__)

template <class F>
auto with_char(F f)
{
    return [=](unsigned char c) -> bool { return f(c); };
}

inline std::string
replace_string(std::string subject, const std::string& search, const std::string& replace)
{
    size_t pos = 0;
    while((pos = subject.find(search, pos)) != std::string::npos)
    {
        subject.replace(pos, search.length(), replace);
        pos += replace.length();
    }
    return subject;
}

inline bool ends_with(const std::string& value, const std::string& suffix)
{
    if(suffix.size() > value.size())
        return false;
    else
        return std::equal(suffix.rbegin(), suffix.rend(), value.rbegin());
}

template <class Strings>
inline std::string join_strings(Strings strings, const std::string& delim)
{
    auto it = strings.begin();
    if(it == strings.end())
        return "";

    auto nit = std::next(it);
    return std::accumulate(nit, strings.end(), *it, [&](std::string x, std::string y) {
        return std::move(x) + delim + std::move(y);
    });
}

inline std::vector<std::string> split_string(const std::string& s, char delim)
{
    std::vector<std::string> elems;
    std::stringstream ss(s + ' ');
    std::string item;
    while(std::getline(ss, item, delim))
    {
        elems.push_back(item);
    }
    return elems;
}

template <class F>
std::string trim(const std::string& s, F f)
{
    auto start = std::find_if_not(s.begin(), s.end(), f);
    auto last  = std::find_if_not(s.rbegin(), std::string::const_reverse_iterator(start), f).base();
    return {start, last};
}

inline std::string trim(const std::string& s)
{
    return trim(s, [](unsigned char c) { return std::isspace(c); });
}

template <class F>
inline std::string transform_string(std::string s, F f)
{
    std::transform(s.begin(), s.end(), s.begin(), f);
    return s;
}

inline std::string to_upper(std::string s) { return transform_string(std::move(s), ::toupper); }

inline std::string to_lower(std::string s) { return transform_string(std::move(s), ::tolower); }

inline bool starts_with(const std::string& value, const std::string& prefix)
{
    if(prefix.size() > value.size())
        return false;
    else
        return std::equal(prefix.begin(), prefix.end(), value.begin());
}

inline std::string remove_prefix(std::string s, const std::string& prefix)
{
    if(starts_with(s, prefix))
        return s.substr(prefix.length());
    else
        return s;
}

template <class F>
inline std::string
interpolate_string(const std::string& input, F f, std::string start = "${", std::string end = "}")
{
    std::string result = "";
    result.reserve(input.size());
    auto it = input.begin();
    while(it != input.end())
    {
        auto next_start = std::search(it, input.end(), start.begin(), start.end());
        auto next_end   = std::search(next_start, input.end(), end.begin(), end.end());
        result.append(it, next_start);
        if(next_start == input.end())
            break;
        auto r = f(next_start + start.size(), next_end);
        result.append(r.begin(), r.end());
        it = next_end + end.size();
    }
    return result;
}
inline std::string interpolate_string(const std::string& input,
                                      const std::unordered_map<std::string, std::string>& vars,
                                      std::string start = "${",
                                      std::string end   = "}")
{
    return interpolate_string(input,
                              [&](auto start_it, auto last_it) {
                                  auto key = trim({start_it, last_it});
                                  auto it  = vars.find(key);
                                  if(it == vars.end())
                                      throw std::runtime_error("Unknown key: " + key);
                                  return it->second;
                              },
                              std::move(start),
                              std::move(end));
}

template <class Iterator>
inline std::string to_string_range(Iterator start, Iterator last)
{
    std::stringstream ss;
    if(start != last)
    {
        ss << *start;
        std::for_each(std::next(start), last, [&](auto&& x) { ss << ", " << x; });
    }
    return ss.str();
}

template <class Range>
inline std::string to_string_range(const Range& r)
{
    return to_string_range(r.begin(), r.end());
}

template <class T>
inline std::string to_string_range(const std::initializer_list<T>& r)
{
    return to_string_range(r.begin(), r.end());
}

template <class T>
inline auto to_string(const T& x)
    -> decltype((std::declval<std::stringstream>() << x), std::string{})
{
    std::stringstream ss;
    ss << x;
    return ss.str();
}

} // namespace MIGRAPHX_INLINE_NS
} // namespace migraphx

#endif
