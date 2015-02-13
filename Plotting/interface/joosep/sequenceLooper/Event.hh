#pragma once
#include <boost/any.hpp>
#include <map>

class EventContainer
{
public:

    const int i;
    std::map<std::string, boost::any> data;

public:
    EventContainer(int _i) : i(_i)
    {
    };

    template <typename T>
    void addData(const std::string name, T d)
    {
        data[name] = boost::any(d);
    }

    template <typename T>
    T getData(const std::string name)
    {
        return boost::any_cast<T>(data[name]);
    }
};