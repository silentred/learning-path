// playground

class Student {
    fullname : string;
    constructor(public firstname, public middleinitial, public lastname) {
        this.fullname = firstname + " " + middleinitial + " " + lastname;
    }
}

interface Person {
    firstname: string;
    lastname: string;
}

class SuperStudent extends Student {
    title: string;
    level: number;

    shout() :string {
        return "hello world";
    }
}


var user = new Student("Jane", "M.", "User");
