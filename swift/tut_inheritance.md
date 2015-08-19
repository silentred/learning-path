# Inheritance

## Base class

```swift
class Vehicle {
    var currentSpeed = 0.0
    var description: String {
        return "traveling at \(currentSpeed) miles per hour"
    }
    func makeNoise() {
        // 什么也不做-因为车辆不一定会有噪音
    }
}
let someVehicle = Vehicle()
println("Vehicle: \(someVehicle.description)")
// Vehicle: traveling at 0.0 miles per hour
```

## Subclassing

```swift
cclass Bicycle: Vehicle {
    var hasBasket = false
}
let bicycle = Bicycle()
bicycle.hasBasket = true
bicycle.currentSpeed = 15.0
println("Bicycle: \(bicycle.description)")
// Bicycle: traveling at 15.0 miles per hour
```

## Overriding

子类可以为继承来的实例方法（instance method），类方法（class method），实例属性（instance property），或下标脚本（subscript）提供自己定制的实现（implementation）。我们把这种行为叫重写（overriding）。

如果要重写某个特性，你需要在重写定义的前面加上`override`关键字。这么做，你就表明了你是想提供一个重写版本，而非错误地提供了一个相同的定义。意外的重写行为可能会导致不可预知的错误，任何缺少override关键字的重写都会在编译时被诊断为错误。

override关键字会提醒 Swift 编译器去检查该类的超类（或其中一个父类）是否有匹配重写版本的声明。这个检查可以确保你的重写定义是正确的。

### Accessing Superclass Methods, Properties, and Subscripts

你可以通过使用super前缀来访问超类版本的方法
- super.someMethod()
- super.someProperty, 在getter, setter中使用
- super[someIndex]来访问超类版本中的相同下标脚本

```swift
class Train: Vehicle {
    override func makeNoise() {
        println("Choo Choo")
    }
}

```

### Override Properties

> 你可以将一个继承来的只读属性重写为一个读写属性，只需要你在重写版本的属性里提供 getter 和 setter 即可。但是，你不可以将一个继承来的读写属性重写为一个只读属性。






