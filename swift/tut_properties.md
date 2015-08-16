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






















