# Control Flow

- for-in

```
for index in 1...5 {
    println("\(index) times 5 is \(index * 5)")
}

// Array , Dictionary, String都可以用for-in循环
for character in "Hello" {
    println(character)
}
```

- for

```
for initialization; condition; increment {
    statements
}

for var index = 0; index < 3; ++index {
    println("index is \(index)")
}

// for循环中的变量只存在于循环中；如果想得到index的最终值，需要把index定义在循环之外。
var index: Int
for index = 0; index < 3; ++index {
    println("index is \(index)")
}
// index is 0
// index is 1
// index is 2
println("The loop statements were executed \(index) times")
// prints "The loop statements were executed 3 times"
```


- while

- do-while

- if

- switch

```
switch some value to consider {
case value 1:
    respond to value 1
case value 2, value 3:
    respond to value 2 or 3
default:
    otherwise, do something else
}

//Explicit Fallthrough

// case可以判断interval（间隔）
switch count {
case 0:
    naturalCount = "no"
case 1...3:
    naturalCount = "a few"


```
Both the closed range operator (...) and half-open range operator (..<) functions are overloaded to return either an `IntervalType` or `Range`. An interval can determine whether it contains a particular element, such as when matching a switch statement case. A range is a collection of consecutive values, which can be iterated on in a for-in statement.

range operator（区间操作符）返回`IntervalType` 或 `Range`类型，switch中返回IntervalType；for-in中返回Range.

- 可以用switch比较tuple，`_`表示任意值，tuple中甚至可以包含interval
```
let somePoint = (1, 1)
switch somePoint {
case (0, 0):
    println("(0, 0) is at the origin")
case (_, 0):
    println("(\(somePoint.0), 0) is on the x-axis")
case (0, _):
    println("(0, \(somePoint.1)) is on the y-axis")
case (-2...2, -2...2):
    println("(\(somePoint.0), \(somePoint.1)) is inside the box")
default:
    println("(\(somePoint.0), \(somePoint.1)) is outside of the box")
}
```

- 值绑定

```
let anotherPoint = (2, 0)
switch anotherPoint {
case (let x, 0):
    println("on the x-axis with an x value of \(x)")
case (0, let y):
    println("on the y-axis with a y value of \(y)")
case let (x, y):
    println("somewhere else at (\(x), \(y))")
}
```

- Where

```
let yetAnotherPoint = (1, -1)
switch yetAnotherPoint {
case let (x, y) where x == y:
    println("(\(x), \(y)) is on the line x == y")
case let (x, y) where x == -y:
    println("(\(x), \(y)) is on the line x == -y")
case let (x, y):
    println("(\(x), \(y)) is just some arbitrary point")
}
```

- Control Transfer Statements
continue
break
fallthrough
return



































