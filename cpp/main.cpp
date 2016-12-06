#include <iostream>
#include <string>
#include <ctime>

#include "main.h"

using namespace std;

int main() {
    print_string();
    print_time();

    cout << "Hello World" << endl;

    Person *p = new Person("jason", 27); 
    p->sayHello();
    delete p;

    return 0;
}

Person::Person(string name, int age)
:name(name),
age(age) 
{
    cout << name << " constructing" << endl;
}

Person::~Person(){
    cout << name << " destructing" << endl;
} 

void Person::sayHello(){
    cout << "Hello " << name << " age is " << age <<endl;
}

void print_string(){
    string str1 = "Hello";
    string str2 = "World";
    string str3;
    int  len ;

    // copy str1 into str3
    str3 = str1;
    cout << "str3 : " << str3 << endl;

    // concatenates str1 and str2
    str3 = str1 + str2;
    cout << "str1 + str2 : " << str3 << endl;

    // total lenghth of str3 after concatenation
    len = str3.size();
    cout << "str3.size() :  " << len << endl;
}

void print_time(){
    time_t now;
    char *timeStr;

    now = time(0);
    timeStr = ctime(&now);
    cout << "now is " << now << " time string is " << timeStr << endl;
}