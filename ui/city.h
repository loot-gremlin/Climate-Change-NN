#ifndef CITY_H
#define CITY_H
#include <string>

class City
{
public:
    City(): cityName(), state() {}
    City( std::string c, std::string s){cityName=c;state=s;}
    std::string cityName;
    std::string state;
};

#endif // CITY_H
