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
    T getData(const std::string &name)
    {
        if (data.find(name) == data.end()) {
            throw std::runtime_error("could not find " + name + " in event");
        }
        try {
            return boost::any_cast<T>(data[name]);
        } catch (...) {
            throw std::runtime_error("Could not cast " + name);
            return T();
        }
    }

    bool wasRun(const std::string &dep)
    {
        typename std::map<std::string, boost::any>::const_iterator it = data.find(dep);
        if (it == data.end())
        {
            return false;
        }
        return getData<bool>(dep);
    }

    void setWasRun(const std::string &dep, bool x) {
        data[dep] = x;
    }

    void setWasSuccess(const std::string &dep, bool x) {
        data[dep + "_success"] = x;
    }

    bool wasSuccess(const std::string &dep)
    {
        const std::string _dep = dep + "_success";
        typename std::map<std::string, boost::any>::const_iterator it = data.find(_dep);
        if (it == data.end())
        {
            return false;
        }
        return getData<bool>(_dep);
    }

    void print()
    {
    }
};