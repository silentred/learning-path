## function

```
func sayHello(personName: String) -> String {
    let greeting = "Hello, " + personName + "!"
    return greeting
}
```

- 多个返回值，用tuple；返回的tuple的成员名称和函数定义中的返回值名称相同，参考下面的例子

```
func minMax(array: [Int]) -> (min: Int, max: Int) {
    var currentMin = array[0]
    var currentMax = array[0]
    for value in array[1..<array.count] {
        if value < currentMin {
            currentMin = value
        } else if value > currentMax {
            currentMax = value
        }
    }
    return (currentMin, currentMax)
}
et bounds = minMax([8, -6, 2, 109, 3, 71])
println("min is \(bounds.min) and max is \(bounds.max)")
// prints "min is -6 and max is 109"
```

- Optional Tuple Return Types, 在tuple后面加一个问号`?`，表示返回的是Optional。

```
func minMax(array: [Int]) -> (min: Int, max: Int)? {
    if array.isEmpty { return nil }
    var currentMin = array[0]
    var currentMax = array[0]
    for value in array[1..<array.count] {
        if value < currentMin {
            currentMin = value
        } else if value > currentMax {
            currentMax = value
        }
    }
    return (currentMin, currentMax)
}
```

- 参数名称

- 外部参数名。外部参数名可以省略，默认就是和内部参数名一致。也可以用`#localParameterName`，
显示表明外部参数名和内部参数名一致。

```
func someFunction(externalParameterName localParameterName: Int) {
    // function body goes here, and can use localParameterName
    // to refer to the argument value for that parameter
}

```

- 参数默认值，调用时必须写joiner的名称，例如 `joiner: '-' `

```
func join(s1: String, s2: String, joiner: String = " ") -> String {
    return s1 + joiner + s2
}
join("hello", "world", joiner: "-")
```

- 可变参数

```
func arithmeticMean(numbers: Double...) -> Double {
    var total: Double = 0
    for number in numbers {
        total += number
    }
    return total / Double(numbers.count)
}
arithmeticMean(1, 2, 3, 4, 5)
```

- 参数默认为常量，不可修改；在声明时加`var`可以定义为变量；

- In-Out Parameters; `inout`关键词，不能用于可变参数，不能var或let，不能传入字面量或者常量。
调用时需要在参数前加`&`; 文档解释为，参数值传入，修改后，值传出，替换原来的变量值。

```
func swapTwoInts(inout a: Int, inout b: Int) {
    let temporaryA = a
    a = b
    b = temporaryA
}
var someInt = 3
var anotherInt = 107
swapTwoInts(&someInt, &anotherInt)
println("someInt is now \(someInt), and anotherInt is now \(anotherInt)")
```

- 函数类型
例如 `(Int, Int)->Int` 表示接受两个int参数，返回一个int。如果不接受参数，不返回值，可以如下表示，
`()->()`, `Void`等价于空tuple，可以这样写 `Void -> Void`;

- 使用函数类型；函数可作为参数，可以作为返回值；

```
var mathFunction: (Int, Int) -> Int = addTwoInts
println("Result: \(mathFunction(2, 3))")
```

- 函数可以嵌套

```
func chooseStepFunction(backwards: Bool) -> (Int) -> Int {
    func stepForward(input: Int) -> Int { return input + 1 }
    func stepBackward(input: Int) -> Int { return input - 1 }
    return backwards ? stepBackward : stepForward
}
```
