## Class and Structure

### Difference
They Both： 有属性，方法，subscript, 初始化方法，Extension, 可实现Protocols
Class有额外的特点： 继承，运行时类型转换，Deinitializers，引用计数

### Definition Syntex & create an instance

```swift
struct Resolution {
    var width = 0
    var height = 0
}
class VideoMode {
    var resolution = Resolution()
    var interlaced = false
    var frameRate = 0.0
    var name: String?
}

let someResolution = Resolution()
let someVideoMode = VideoMode()
```
### Access to Properties

```
someVideoMode.resolution.width = 1280
println("The width of someVideoMode is now \(someVideoMode.resolution.width)")

// Structure 有默认的 memberwise initializer, 如下
let vga = Resolution(width: 640, height: 480)

```

### Structures and Enumerations Are Value Types

### Classes are Reference Types

### Identity Operators

- Identical to (===)
- Not identical to (!==)

用于比较两个class是否指向一个实例。structure是值传递，一般没有identical比较。

```swift
if tenEighty === alsoTenEighty {
    println("tenEighty and alsoTenEighty refer to the same VideoMode instance.")
}
```
这里注意下两个词的区别， Identical值同一个内存引用， Equal, equivalent指值相同。
“Identical to” means that two constants or variables of class type refer to exactly the same class instance.
“Equal to” means that two instances are considered “equal” or “equivalent” in value, for some appropriate meaning of “equal”, as defined by the type’s designer.


## Choosing Between Classes and Structures

### Choose Structure for any of following reason:

- Main purpose is to encapsulate some related values
- expect the encapsulated values to be copied rather than be referenced when they are passed
- any properties are themselves value types, which need to be copied rather referenced.
(这句话的意思是，Type A 内部有一个属性类型为 Type A, 此时最好用Structure 作为Type。但是貌似不合理，这样会形成死循环，必须有一个A为null。)
- do not need to inherit propertieds or methods from aother existing type

其他情况请用Class。

关于Copy，Swift在不得不copy的时候才会copy，所以不用担心性能问题。







