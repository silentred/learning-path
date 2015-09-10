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

协议中的通常用var来声明属性，在类型声明后加上{ set get }来表示属性是可读可写的，只读属性则用{ get }来表示。



