/// <reference path="playground.ts"/>

// handbook

// Type
var boolType : boolean = false;
var numberType : number = 2;
var stringType : string = "HEllo";

var list: number[] = [2,3,5];
var list2 : Array<number> = [3,5,6];

enum Color {Red = 2, Green, Yellow};
var red : Color = Color.Red;

var whatever: any = 4;
whatever = "string";

// Interface

// optional property
interface SquareConfig {
  color?: string;
  width?: number;
}

// function
interface SearchFunc {
  (source: string, subString: string): boolean;
}

// array
interface StringArray {
  [index: number]: string;
}

// class
interface ClockInterface {
    currentTime: Date;
    setTime(d: Date);
}

// static class (need to search)

// extend interface
interface Shape {
    color: string;
}

interface PenStroke {
    penWidth: number;
}

interface Square extends Shape, PenStroke {
    sideLength: number;
}

// Classes 

class Greeter {
    greeting: string;
    constructor(message: string) {
        this.greeting = message;
    }
    greet() {
        return "Hello, " + this.greeting;
    }
}

var greeter = new Greeter("world");

// Use `extends` for inheritance
// 
// `private` property
// 
//  public/private 可以写在constructor中表示创建property。
class Animal {
    constructor(private name: string) { }
    move(meters: number) {
        alert(this.name + " moved " + meters + "m.");
    }
} 

// Accessors
var passcode = "secret passcode";

class Employee {
    private _fullName: string;

    get fullName(): string {
        return this._fullName;
    }
    
    set fullName(newName: string) {
        if (passcode && passcode == "secret passcode") {
            this._fullName = newName;
        }
        else {
            alert("Error: Unauthorized update of employee!");
        }
    }
}

var employee = new Employee();
employee.fullName = "Bob Smith";
if (employee.fullName) {
    alert(employee.fullName);
}

// static property
class Grid {
    static origin = {x: 0, y: 0};
    calculateDistanceFromOrigin(point: {x: number; y: number;}) {
        var xDist = (point.x - Grid.origin.x);
        var yDist = (point.y - Grid.origin.y);
        return Math.sqrt(xDist * xDist + yDist * yDist) / this.scale;
    }
    constructor (public scale: number) { }
}

// modules
// <reference /> must at first line
module Validation {
    export interface StringValidator {
        isAcceptable(s: string): boolean;
    }
}






