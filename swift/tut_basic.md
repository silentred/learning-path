## Basic

- 一行声明多个变量
`var x = 0.0, y = 0.0, z = 0.0`

`var red, green, blue: Double`

- 整型有几种  8, 16, 32, and 64 bit forms, 且有常量
`let minValue = UInt8.min`

- 数字的多种写法
```
let decimalInteger = 17
let binaryInteger = 0b10001       // 17 in binary notation
let octalInteger = 0o21           // 17 in octal notation
let hexadecimalInteger = 0x11     // 17 in hexadecimal notation

let decimalDouble = 12.1875
let exponentDouble = 1.21875e1
let hexadecimalDouble = 0xC.3p0

let paddedDouble = 000123.456
let oneMillion = 1_000_000
let justOverOneMillion = 1_000_000.000_000_1
```

- 类型别名
`typealias AudioSample = UInt16`

- Tuple, 元组
```
let http404Error = (404, "Not Found")
// http404Error is of type (Int, String), and equals (404, "Not Found")
```
- Tuple的解包
```
let (statusCode, statusMessage) = http404Error
println("The status code is \(statusCode)")
// prints "The status code is 404"
println("The status message is \(statusMessage)")
// prints "The status message is Not Found"
```

- 用数字index可以直接访问tuple中的元素；如果给元素命名的话，可以用这个命名来访问。
```
println("The status code is \(http404Error.0)")

let http200Status = (statusCode: 200, description: "OK")
println("The status code is \(http200Status.statusCode)")
```

- 可选值, String的toInt()方法可能失败，此时返回nil，所以这里的convertedNumber被认为是
`Int?`类型
```
let possibleNumber = "123"
let convertedNumber = possibleNumber.toInt()
```

- 定义一个可选值，默认值为nil
```
var surveyAnswer: String?
```

- 如果确定可选值不为nil，可以用`!`来取得他的 `underlying value`。如果为nil，并使用了!，
会产生runtime error。
```
if convertedNumber != nil {
    println("convertedNumber has an integer value of \(convertedNumber!).")
}
```

- optional binding：用if,while可以把值传给一个var或者let且condition为true，
如果为nil则condition为false。多个binding可以在一个if语句中，用逗号分隔。
```
if let actualNumber = possibleNumber.toInt() {
    println("\'\(possibleNumber)\' has an integer value of \(actualNumber)")
} else {
    println("\'\(possibleNumber)\' could not be converted to an integer")
}

if let constantName = someOptional, anotherConstantName = someOtherOptional {
    statements
}
```

- Implicitly Unwrapped Optionals， 隐式解包的可选值。声明时候用`!`，
这样赋值必须确保给的值不为nil，在使用这个可选值的真值的时候可以不加`!`，
其余用法和一般的可选值一样。
```
let assumedString: String! = "An implicitly unwrapped optional string."
let implicitString: String = assumedString // no need for an exclamation mark
```

- 断言，assert
```
let age = -3
assert(age >= 0, "A person's age cannot be less than zero")
```

- Nil Coalescing Operator
```
a ?? b
a != nil ? a! : b
```

- range 范围
`1...4`, `1..<4`
