#include "climatechangevisualizer.h"
#include <fstream>
#include <iostream>
#include <QApplication>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    std::ifstream input;
    input.open("cities.txt");
    std::string temp;
    //std::vector<City> cities;
    std::map<std::pair<std::string,std::string>,int> cities;
    int count=1;
    while(input>>temp){
        std::string state=temp;
        input>>temp;
        for(int i=0;i<temp.size();i++){
            if(temp[i]=='_')
                temp[i]=' ';
        }
        cities[std::make_pair(state,temp)]=count;
        count++;
    }
    ClimateChangeVisualizer w;
    w.loadData(cities);
    w.show();

    return a.exec();
}
