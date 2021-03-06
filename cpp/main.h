void print_string();
void print_time();
bool is_small_endian();
void test_class();

class Person {
    public:
        std::string name;
        int age;

        Person(std::string name, int age);
        ~Person();
        void sayHello();

    private:
        bool merried;
};

class A {
    public:
        virtual void foo();
        void bar();
};

class B: public A {
    public:
        void foo();
};
  
class TestNull {
    private:
        void a();

    public:
        void f();
};