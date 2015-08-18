## Methods

### 实例方法 (Instance Methods)
实例方法是属于某个特定类、结构体或者枚举类型实例的方法。

```swift
class Counter {
    var count = 0
    func increment() {
        ++count
    }
    func incrementBy(amount: Int) {
        count += amount
    }
    func reset() {
        count = 0
    }
}

let counter = Counter()
// the initial counter value is 0
counter.increment()
// the counter's value is now 1
counter.incrementBy(5)
// the counter's value is now 6
counter.reset()
// the counter's value is now 0
```
### Local and External Parameter Names for Methods

```swift
class Counter {
    var count: Int = 0
    func incrementBy(amount: Int, numberOfTimes: Int) {
        count += amount * numberOfTimes
    }
}

let counter = Counter()
counter.incrementBy(5, numberOfTimes: 3)
```
方法的第一个参数`amount`默认只会被解析为local parameter name, 没有外部参数名. 第二个参数`numberOfTimes`默认被解析为local and external parameter name。所以默认情况下为`incrementBy(_, numberOfTimes)`。

### Modifying External Parameter Name Behavior for Methods

`#`作为prefix, 表示external name == local name.
`_`作为prefix, 表示没有external name.

## self 属性(The self Property)

`self`在没有歧义时可以省略.

structure, enumeration 都是value type, 默认是不能从内部func中修改其property的。
`mutating`关键词修饰`func`可以解决这个问题。方法结束时，会新建一个实例，重新绑定到self。
注意这里property不能为常量，因为常量不可修改。

```swift
struct Point {
    var x = 0.0, y = 0.0
    mutating func moveByX(deltaX: Double, y deltaY: Double) {
        x += deltaX
        y += deltaY
    }
}
var somePoint = Point(x: 1.0, y: 1.0)
somePoint.moveByX(2.0, y: 3.0)
println("The point is now at (\(somePoint.x), \(somePoint.y))")
// prints "The point is now at (3.0, 4.0)"
```

### 在变异方法中给self赋值(Assigning to self Within a Mutating Method)

```swift
struct Point {
  var x = 0.0, y = 0.0
  mutating func moveByX(deltaX: Double, y deltaY: Double) {
    self = Point(x: x + deltaX, y: y + deltaY)
  }
}
```
新版的变异方法moveByX(_:y:)创建了一个新的结构（它的 x 和 y 的值都被设定为目标值）。调用这个版本的方法和调用上个版本的最终结果是一样的。

```swift
enum TriStateSwitch {
  case Off, Low, High
  mutating func next() {
    switch self {
    case Off:
      self = Low
    case Low:
      self = High
    case High:
      self = Off
    }
  }
}
var ovenLight = TriStateSwitch.Low
ovenLight.next()
// ovenLight 现在等于 .High
ovenLight.next()
// ovenLight 现在等于 .Off
```

## 类型方法 (Type Methods)

structure, enumeration 在func 之前加`static` keyword. Class 用关键词`class`加在func之前， 子类可以override这个方法。

```swift
class SomeClass {
  class func someTypeMethod() {
    // type method implementation goes here
  }
}
SomeClass.someTypeMethod()
```

