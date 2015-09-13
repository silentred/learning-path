## Optional Chaining

```swift
if let firstRoomName = john.residence?[0].name {
    print("The first room name is \(firstRoomName).")
} else {
    print("Unable to retrieve the first room name.")
}

if (john.residence?.address = someAddress) != nil

if john.residence?.printNumberOfRooms() != nil

if let johnsStreet = john.residence?.address?.street

```

##  Error Handling

`func canThrowErrors() throws -> String`, `throw` keyword.

```swift
enum VendingMachineError: ErrorType {
    case InvalidSelection
    case InsufficientFunds(required: Double)
    case OutOfStock
}

do {    
    try vend(itemNamed: "Candy Bar")    
    // Enjoy delicious snack    
} catch VendingMachineError.InvalidSelectio {
    print("Invalid Selection")
} catch VendingMachineError.OutOfStock {
    print("Out of Stock.")
} catch VendingMachineError.InsufficientFunds(let   amountRequired) {
    print("Insufficient funds. Please insert an additional $\(amountRequired).")
}
```

`try!`确定不会抛错误，如果抛出，则runtime error.

`defer{ //do something }` 在作用域延迟操作，和Go中的一样。

## Type Casting

`is` 检查是否为某一类。 `as?`, `as!`向下转型。

`AnyObject`为任意类。 `Any`为任意类型。

## Nested Type


## Extensions

## Protocol

协议中的通常用var来声明属性，在类型声明后加上`{ set get }`来表示属性是可读可写的，只读属性则用{ get }来表示。

在协议中定义类属性(type property)时，总是使用`static`关键字作为前缀。

有时需要在方法中改变它的实例。例如，值类型(结构体，枚举)的实例方法中，将`mutating`关键字作为函数的前缀，写在func之前，表示可以在该方法中修改它所属的实例及其实例属性的值。
> 用类实现协议中的mutating方法时，不用写mutating关键字;用结构体，枚举实现协议中的mutating方法时，必须写mutating关键字。

你可以在遵循该协议的类中实现构造器，并指定其为类的指定构造器(designated initializer)或者便利构造器(convenience initializer)。 在这两种情况下，你都必须给构造器实现标上"required"修饰符：

使用`required` 修饰符可以保证： 所有的遵循该协议的子类，同样能为构造器规定提供一个显式的实现或继承实现。
> 如果类已经被标记为final， 那么不需要在协议构造器的实现中使用required修饰符。因为final类不能有子类。

你可以在协议的继承列表中,通过添加`class`关键字,限制协议只能适配到类（class）类型。（结构体或枚举不能遵循该协议）。该class关键字必须是第一个出现在协议的继承列表中，其后，才是其他继承协议。

```swift
protocol SomeClassOnlyProtocol: class, SomeInheritedProtocol {
    // class-only protocol definition goes here
}
```

有时候需要同时遵循多个协议。你可以将多个协议采用`protocol<SomeProtocol， AnotherProtocol>`这样的格式进行组合，称为协议合成(protocol composition)。你可以在<>中罗列任意多个你想要遵循的协议，以逗号分隔。

```swift
func wishHappyBirthday(celebrator: protocol<Named, Aged>) {
    print("Happy birthday \(celebrator.name) - you're \(celebrator.age)!")
}
```

> 可选协议只能在含有`@objc`前缀的协议中生效。且@objc的协议只能被类遵循
这个前缀表示协议将暴露给Objective-C代码，详情参见Using Swift with Cocoa and Objective-C。即使你不打算和Objective-C有什么交互，如果你想要指明协议包含可选属性，那么还是要加上@obj前缀


## Generics

### Type Constraints

```swift
func someFunction<T: SomeClass, U: SomeProtocol>(someT: T, someU: U) {
    // 这里是函数主体
}
```

### `where` keyword

