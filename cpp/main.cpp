// cpp std lib
#include <iostream>
#include <string>
#include <ctime>

// c std lib
#include <stdio.h>

// private lib
#include "main.h"

using namespace std;

int main() {
    // print_string();
    // print_time();
    test_class();

    bool sm;
    sm  = is_small_endian();

    cout << "is_small_endian: " << sm << endl;

    Person *p = new Person("jason", 27); 
    p->sayHello();
    delete p; // cannot delete a non-pointer

    printf("hello \n");

    return 0;
}

Person::Person(string name, int age)
:name(name),
age(age) 
{
    merried = true;
    cout << name << " constructing" << endl;
}

Person::~Person(){
    cout << name << " destructing" << endl;
} 

void Person::sayHello(){
    cout << "Hello " << name << " age is " << age <<endl;
    cout << "Merried: " << merried <<endl;
}

void test_class(){
    A *a;
    A base;
    B child;

    a = &base;
    a->foo();

    a = &child;
    a->foo();
    a->bar(); // B has no method of bar(), so it will call A::bar()  
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

bool is_small_endian(){
    int a = 0x5455;
    char *b = (char*)&a;

    if(b[0] == 0x55){
        return true;
    }

    return false;
}

void A::foo(){
    cout<<"A::foo() is called"<<endl;
}

void A::bar(){
    cout<<"A::bar() is called"<<endl;
}

void B::foo(){
    cout<<"B::foo() is called"<<endl;
}
