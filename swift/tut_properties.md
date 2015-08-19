## Properties

### Stored Properties

Simple properties are just variable or constant (using var or let to define).
Constant can be assigned during the initialization, however cannot be changed thereafter.

```swift
struct FixedLengthRange {
    var firstValue: Int
    let length: Int
}
var rangeOfThreeItems = FixedLengthRange(firstValue: 0, length: 3)
// the range represents integer values 0, 1, and 2
rangeOfThreeItems.firstValue = 6
// the range now represents integer values 6, 7, and 8

```

> If you create an instance of a structure and assign that instance to a constant, you cannot modify the instance’s properties, even if they were declared as variable properties.

赋予常量的Structure实例，没办法修改其属性。因为Structure是value type, 所以他的任何值都不可修改。
Class则不同，因为是reference type, 所以可以修改他的var properties.

### Lazy Stored Properties

> A lazy stored property is a property whose initial value is not calculated until the first time it is used. You indicate a lazy stored property by writing the lazy modifier before its declaration. 

直到第一次使用才计算属性的值。在定义时用`lazy`标识符。

> You must always declare a lazy property as a variable (with the var keyword), because its initial value might not be retrieved until after instance initialization completes. Constant properties must always have a value before initialization completes, and therefore cannot be declared as lazy.

变量最好都定义为 `lazy property` , 因为他的值一般都是在实例初始化完成后才从外部取得的。 而常量必须在初始化完成之前有一个值，因为一旦初始化后，就无法改变其值了，所以常量无法被定义为`lazy`.

```swift
class DataImporter {
    /*
    DataImporter is a class to import data from an external file.
    The class is assumed to take a non-trivial amount of time to initialize.
    */
    var fileName = "data.txt"
    // the DataImporter class would provide data importing functionality here
}
 
class DataManager {
    lazy var importer = DataImporter()
    var data = [String]()
    // the DataManager class would provide data management functionality here
}

// 不会立即创建DataImporter, 因为是lazy。因为这个importer可能不去使用， manager也能完成任务；
let manager = DataManager()
manager.data.append("Some data")
manager.data.append("Some more data")
// the DataImporter instance for the importer property has not yet been created

// 直到第一次取importer时，才会去创建实例。
println(manager.importer.fileName)
// the DataImporter instance for the importer property has now been created
// prints "data.txt"
```

### Stored Properties and Instance Variables
different with OC. the property's name, type, memory management characteristics is defined in one single location as part of the type's definition.

## Computed Properties

>computed properties, which do not actually store a value. Instead, they provide a getter and an optional setter to retrieve and set other properties and values indirectly.

不存值，而是一个getter和可选的setter，setter用于设置其他属性的值。

```swift
struct Point {
    var x = 0.0, y = 0.0
}
struct Size {
    var width = 0.0, height = 0.0
}
struct Rect {
    var origin = Point()
    var size = Size()
    var center: Point {
        get {
            let centerX = origin.x + (size.width / 2)
            let centerY = origin.y + (size.height / 2)
            return Point(x: centerX, y: centerY)
        }
        // 如果没有提供 `newCenter`, 默认使用 `newVlaue`
        set(newCenter) {
            origin.x = newCenter.x - (size.width / 2)
            origin.y = newCenter.y - (size.height / 2)
        }
    }
}
var square = Rect(origin: Point(x: 0.0, y: 0.0),
    size: Size(width: 10.0, height: 10.0))
let initialSquareCenter = square.center
square.center = Point(x: 15.0, y: 15.0)
println("square.origin is now at (\(square.origin.x), \(square.origin.y))")
// prints "square.origin is now at (10.0, 10.0)"
```


### Shorthand Setter Declaration

> If a computed property’s setter does not define a name for the new value to be set, a default name of newValue is used.

如果setter没有提供一个参数名，默认为`newValue`

### Read-Only Computed Properties

just dont define a setter. And you could remove the `get` keyword like:

```swift
struct Cuboid {
    var width = 0.0, height = 0.0, depth = 0.0
    var volume: Double {
        return width * height * depth
    }
}
let fourByFiveByTwo = Cuboid(width: 4.0, height: 5.0, depth: 2.0)
println("the volume of fourByFiveByTwo is \(fourByFiveByTwo.volume)")
// prints "the volume of fourByFiveByTwo is 40.0"
```

## Property Observers

>Property observers observe and respond to changes in a property’s value. Property observers are called every time a property’s value is set, even if the new value is the same as the property’s current value.

每次属性值改变都会触发观察者。lazy stored property 无法设置观察者。两个新关键词：

- `willSet` is called just before the value is stored.
- `didSet` is called immediately after the new value is stored.

> If you implement a willSet observer, it is passed the new property value as a constant parameter. You can specify a name for this parameter as part of your willSet implementation. If you choose not to write the parameter name and parentheses within your implementation, the parameter will still be made available with a default parameter name of newValue.

参数为 将要设置的 newValue

> Similarly, if you implement a didSet observer, it will be passed a constant parameter containing the old property value. You can name the parameter if you wish, or use the default parameter name of oldValue.

参数为 oldValue

```swift
class StepCounter {
    var totalSteps: Int = 0 {
        willSet(newTotalSteps) {
            println("About to set totalSteps to \(newTotalSteps)")
        }
        didSet {
            if totalSteps > oldValue  {
                println("Added \(totalSteps - oldValue) steps")
            }
        }
    }
}
let stepCounter = StepCounter()
stepCounter.totalSteps = 200
// About to set totalSteps to 200
// Added 200 steps
stepCounter.totalSteps = 360
// About to set totalSteps to 360
// Added 160 steps
stepCounter.totalSteps = 896
// About to set totalSteps to 896
// Added 536 steps
```

### Global and Local Variables
全局和局部变量都有 sotred value, computed value. 
全局变量的computed value不需要`lazy`keyword.


## Type Properties

类型属性用于定义特定类型所有实例共享的数据，比如所有实例都能用的一个常量（就像 C 语言中的静态常量），或者所有实例都能访问的一个变量（就像 C 语言中的`静态变量`）。

值类型的存储型类型属性可以是变量或常量，计算型类型属性跟实例的计算属性一样只能定义成变量属性。

注意：
跟实例的存储属性不同，必须给存储型类型属性指定默认值，因为类型本身无法在初始化过程中使用构造器给类型属性赋值。

### 类型属性语法

在 C 或 Objective-C 中，与某个类型关联的静态常量和静态变量，是作为全局（global）静态变量定义的。但是在 Swift 编程语言中，类型属性是作为类型定义的一部分写在类型最外层的花括号内，因此它的作用范围也就在类型支持的范围内。

使用关键字static来定义类型属性。在为类（class）定义计算型类型属性时，可以使用关键字class来支持子类对父类的实现进行重写。

```swift
struct SomeStructure {
    static var storedTypeProperty = "Some value."
    static var computedTypeProperty: Int {
        return 1
    }
}
enum SomeEnumeration {
    static var storedTypeProperty = "Some value."
    static var computedTypeProperty: Int {
        return 6
    }
}
class SomeClass {
    static var storedTypeProperty = "Some value."
    static var computedTypeProperty: Int {
        return 27
    }
    class var overrideableComputedTypeProperty: Int {
        return 107
    }
}

print(SomeStructure.storedTypeProperty)
// 输出 "Some value."
SomeStructure.storedTypeProperty = "Another value."
print(SomeStructure.storedTypeProperty)
// 输出 "Another value.”
print(SomeEnumeration.computedTypeProperty)
// 输出 "6"
print(SomeClass.computedTypeProperty)
// 输出 "27"
```



