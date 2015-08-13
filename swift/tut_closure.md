## Closure

- Closure Expression Syntax

```
{ (parameters) -> return type in
    statements
}


let names = ["Chris", "Alex", "Ewa", "Barry", "Daniella"]
reversed = sorted(names, { (s1: String, s2: String) -> Bool in return s1 > s2 })

```

- Inferring Type From Context

根据names的元素类型，可以推断出closure的参数类型，所以可简写; 
对于单行表达式，return也可以省略；

```
reversed = sorted(names, { s1, s2 in return s1 > s2 } )

// 省略return
reversed = sorted(names, { s1, s2 in s1 > s2 } )
```

- 简写参数; 参数用index表示，则可以省略in和in前面的参数声明了。

```
reversed = sorted(names, { $0 > $1 } )
```

- Operator Functions
String类型定义了`>`的字符特异的实现，为一个closure。所以可以这么用。
```
reversed = sorted(names, > )
```

- Trailing Closures

当closure为最后一个参数，并且表达式比较长时，可以如下写; 如果只有一个参数，且为closure，
则不用包含`()`, 例如下面Array.map的用法

```
reversed = sorted(names) { $0 > $1 }


let digitNames = [
    0: "Zero", 1: "One", 2: "Two",   3: "Three", 4: "Four",
    5: "Five", 6: "Six", 7: "Seven", 8: "Eight", 9: "Nine"
]
let numbers = [16, 58, 510]

let strings = numbers.map {
    (var number) -> String in
    var output = ""
    while number > 0 {
        output = digitNames[number % 10]! + output
        number /= 10
    }
    return output
}
```

- Capturing Values

- Closure是按引用传递的






