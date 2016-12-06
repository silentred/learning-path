void print_string();
void print_time();

class Person {
    public:
        std::string name;
        int age;

        Person(std::string name, int age);
        ~Person();
        void sayHello();
};