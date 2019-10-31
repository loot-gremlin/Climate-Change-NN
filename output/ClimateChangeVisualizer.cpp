#include <iostream>
#include <string>
#include <fstream>
#include <map>
#include <cassert>
using namespace std;

typedef map<pair<int,string>,string> cityMap;

int main(int argc, char* argv[])
{
  cityMap cities;
  fstream fstr;
  fstr.open("cities.txt");
  int count=1;
  string temp;
  while(fstr>>temp){
    std::string state=temp;
        fstr>>temp;
        for(int i=0;i<temp.size();i++){
            if(temp[i]=='_')
                temp[i]=' ';
        }
        cities[make_pair(count,state)]=temp;
        count++;
  }

  std::cout<<"Input a state (abbreviation)"<<std::endl;
  int option=0;
  std::cin>>temp;
  for(cityMap::const_iterator itr=cities.begin();itr!=cities.end();itr++)
  {
    if(itr->first.second==temp){
      cout<<itr->first.first<<". "<<itr->second<<", "<<itr->first.second<<endl;
    }
  }
  std::cout<<"Input the city number:"<<std::endl;
  std::cin>>option;
  assert(cities.find(make_pair(option,temp))!=cities.end());
  std::cout<<"input future date: DD/MM/YYYY"<<std::endl;
  string date;
  int days;
  cin>>date;
  assert(date.length()==10);
  assert(stoi(date.substr(0,2))<=31);
  assert(stoi(date.substr(3,2))<=12);
  assert(stoi(date.substr(6,4))>=2010);
  days=(stoi(date.substr(0,2))-1)*30+(stoi(date.substr(3,2))-1)+(stoi(date.substr(6,4))-2010)*365;
  string city=cities.find(make_pair(option,temp))->second;
  for(int i=0;i<city.size();i++){
    if(city[i]==' ')
      city[i]='_';
    }
  string commandString="python3 middleman.py ";
  commandString+= to_string(days);
  commandString+=" "+temp+ " "+city;
  system(commandString.c_str());
}
