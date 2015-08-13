## Enumeration

- Definition

```
// has rawValue
enum CompassPoint : Int{
    case North = 1
    case South
    case East
    case West
}

// only has hashValue
enum Planet {
    case Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune
}

var directionToHead = CompassPoint.West

directionToHead = .South
switch directionToHead {
case .North:
    println("Lots of planets have a north")
}


```

- Associated Value

```

enum Barcode {
    case UPCA(Int, Int, Int, Int)
    case QRCode(String)
}

// associate a tuple of 4 Int with the enum value
var productBarcode = Barcode.UPCA(8, 85909, 51226, 3)

// extract value in the switch statement, using let or var
switch productBarcode {
case .UPCA(let numberSystem, let manufacturer, let product, let check):
    println("UPC-A: \(numberSystem), \(manufacturer), \(product), \(check).")
case .QRCode(let productCode):
    println("QR code: \(productCode).")
}

```
"Define an enumeration type called Barcode, which can take either a value of UPCA with an associated value of type (Int, Int, Int, Int), or a value of QRCode with an associated value of type String."


- Raw Value
this is prepopulated value. 

```
// has rawValue
enum CompassPoint : Int{
    case North = 1
    case South
    case East
    case West
}
let possiblePlanet = Planet(rawValue: 7)
// possiblePlanet is of type Planet? and equals Planet.Uranus
// NOTICE, return value is optional
```















