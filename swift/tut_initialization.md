## Initialization

类和结构体在实例创建时，必须为所有存储型属性设置合适的初始值。存储型属性的值不能处于一个未知的状态。
你可以在构造器中为存储型属性赋初值，也可以在定义属性时为其设置默认值。

> 当你为存储型属性设置默认值或者在构造器中为其赋值时，它们的值是被直接设置的，不会触发任何属性观测器（property observers）。

多个构造函数

```swift
struct Celsius {
    var temperatureInCelsius: Double = 0.0
    init(fromFahrenheit fahrenheit: Double) {
        temperatureInCelsius = (fahrenheit - 32.0) / 1.8
    }
    init(fromKelvin kelvin: Double) {
        temperatureInCelsius = kelvin - 273.15
    }
}
let boilingPointOfWater = Celsius(fromFahrenheit: 212.0)
// boilingPointOfWater.temperatureInCelsius 是 100.0
let freezingPointOfWater = Celsius(fromKelvin: 273.15)
// freezingPointOfWater.temperatureInCelsius 是 0.0”
```

注意，如果不通过外部参数名字传值，你是没法调用这个构造器的。只要构造器定义了某个外部参数名，你就必须使用它，忽略它将导致编译错误：

如果你不希望为构造器的某个参数提供外部名字，你可以使用下划线(_)来显示描述它的外部名，以此重写上面所说的默认行为。

### Optional Property Types
default value is nil

### Assigning Constant Properties During Initialization
不能再子类中设定const

### Designated Initializers and Convenience Initializers
Desinated: vertical
Convenience: horizental


skip for now... toooo god damn complicated







