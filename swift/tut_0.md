# Swift Tutorial

### 基础
- var: 变量
- let: 常量
- 类型可以显示或隐式声明

```swift
let implicitInteger = 70
let implicitDouble = 70.0
let explicitDouble: Double = 70
```

- 变量永远不会隐式转换，如有需要必须显示转换，转换方式类似 `String(implicitInteger)`
- 变量拼接字符串有一种方便的方法`\(var)`

```swift
let apples = 3
let oranges = 5
let appleSummary = "I have \(apples) apples."
let fruitSummary = "I have \(apples + oranges) pieces of fruit."
```

- 声明数组有三种方式

```swift
var newArray = Array<String>()
var newArray = [String]()
var shoppingList = ["catfish", "water", "tulips", "blue paint"]
shoppingList[1] = "bottle of water"
```

- 声明字典也是类似的
- 如果数组，字典的类型可以被推断，那么可以用`var = []`或者`var = [:]`设置为空

```swift
var dict = Dictionary<Int, String>()
var dict = [Int:String]()
var occupations = [
    1: "Captain",
    2: "Mechanic",
]
occupations[1] = "Public Relations"
```

- 元组可以用index(从0开始)或者name访问

```
var tup = (a:1,b:3,c:4)
println(tup.c)
println(tup.2)
var tuple = (1,4,5)
println(tuple.0)
```

### 控制流

包含 for-in, for, if, while, switch, do-while

```
let individualScores = [75, 43, 103, 87, 12]
var teamScore = 0
for score in individualScores {
    if score > 50 {
        teamScore += 3
    } else {
        teamScore += 1
    }
}
println(teamScore)
```
- if条件必须为Boolean
- 用if和let用来判断可选值(Optional)是否为nil。逻辑为：如果optional为nil，则if
语句条件为false，如果不为nil，if条件为true，并把trueValue赋值给let定义的变量

```
var optionalString: String? = "Hello"
println(optionalString == nil)

var optionalName: String? = "John Appleseed"
var greeting = "Hello!"
if let name = optionalName {
    greeting = "Hello, \(name)"
}
```
- switch中case的几种用法：“或”判断多个值，where语句，default等。
- switch自动break，如果想让case“漏过”，用 fallthrough

```
let vegetable = "red pepper"
switch vegetable {
case "celery":
    let vegetableComment = "Add some raisins and make ants on a log."
case "cucumber", "watercress":
    let vegetableComment = "That would make a good tea sandwich."
case let x where x.hasSuffix("pepper"):
    let vegetableComment = "Is it a spicy \(x)?"
default:
    let vegetableComment = "Everything tastes good in soup."
}
```

- for in 循环的使用，可以用_表示舍弃

```
let interestingNumbers = [
    "Prime": [2, 3, 5, 7, 11, 13],
    "Fibonacci": [1, 1, 2, 3, 5, 8],
    "Square": [1, 4, 9, 16, 25],
]
var largest = 0
for (kind, numbers) in interestingNumbers {
    for number in numbers {
        if number > largest {
            largest = number
        }
    }
}
println(largest)
```
- 区间表示：`0...4`前闭后闭，`0..<4`前闭后开; 例如 `for x in 0...4`

### 函数于闭包
- 用func关键词定义函数，`->`后加返回类型，例如

```
func greet(name: String, day: String) -> String {
    return "Hello \(name), today is \(day)."
}
greet("Bob", "Tuesday")
```

- 函数可以嵌套，函数内部可以定义函数
- 函数可以返回函数,返回函数的写法如下

```
func makeIncrementer() -> (Int -> Int) {
    func addOne(number: Int) -> Int {
        return 1 + number
    }
    return addOne
}
var increment = makeIncrementer()
increment(7)
```

- 函数可作为参数传入

```
func hasAnyMatches(list: [Int], condition: Int -> Bool) -> Bool {
    for item in list {
        if condition(item) {
            return true
        }
    }
    return false
}
func lessThanTen(number: Int) -> Bool {
    return number < 10
}
var numbers = [20, 19, 7, 12]
hasAnyMatches(numbers, lessThanTen)
```

- 函数的简写方式，`{}`中，用`in`分隔参数返回值 和 函数体

```
var newArray = array.map({
    (number: Int) -> Int in let result = 3 * number return result
})
```

- 当闭包的参数类型是已知的，可以省略参数类型

```
let mappedNumbers = numbers.map({ number in 3 * number })
```

- 可以用数字表示参数
- 闭包可以写在函数调用的括号外边，表示第二个传入参数，如下

```
let sortedNumbers = sorted(numbers) { $0 > $1 }
```

### 类和对象

- `class Name {}`创建class

```
class Shape {
    var numberOfSides = 0
    func simpleDescription() -> String {
        return "A shape with \(numberOfSides) sides."
    }
}
```
- 类名后加括号创建对象

```
var shape = Shape()
shape.numberOfSides = 7
var shapeDescription = shape.simpleDescription()
```

- `init`构造函数，`deinit`析构函数， self是关键词

```
class NamedShape {
    var numberOfSides: Int = 0
    var name: String

    init(name: String) {
        self.name = name
    }

    func simpleDescription() -> String {
        return "A shape with \(numberOfSides) sides."
    }
}
var shape = NamedShape(name:"Circle")
shape.simpleDescription()
shape.name
```

- 子类，分号后加父类名，super表示父类引用，override表示重写父类方法,override多写或少写
都会被编译器检测到

```
class Square: NamedShape {
    var sideLength: Double

    init(sideLength: Double, name: String) {
        self.sideLength = sideLength
        super.init(name: name)
        numberOfSides = 4
    }

    func area() ->  Double {
        return sideLength * sideLength
    }

    override func simpleDescription() -> String {
        return "A square with sides of length \(sideLength)."
    }
}
let test = Square(sideLength: 5.2, name: "my test square")
test.area()
test.simpleDescription()
```

- 为property定义getter和setter, 这里的`perimeter`的setter用了隐式的newVlaue参数，
也可以显式的在`set`后面加上参数

```
class EquilateralTriangle: NamedShape {
    var sideLength: Double = 0.0

    init(sideLength: Double, name: String) {
        self.sideLength = sideLength
        super.init(name: name)
        numberOfSides = 3
    }

    var perimeter: Double {
        get {
            return 3.0 * sideLength
        }
        set {
            sideLength = newValue / 3.0
        }
    }

    override func simpleDescription() -> String {
        return "An equilateral triangle with sides of length \(sideLength)."
    }
}
var triangle = EquilateralTriangle(sideLength: 3.1, name: "a triangle")
println(triangle.perimeter)
triangle.perimeter = 9.9
println(triangle.sideLength)
```
