# Collection Type

- 有三类arrays, sets, and dictionaries；

- Array类型`Array<SomeType>`, `[SomeType]`

- Array创建和初始化;count指定长度，repeatedValue指定初始值

```
var someInts = [Int]()
println("someInts is of type [Int] with \(someInts.count) items.")
someInts.append(3) // someInts now contains 1 value of type Int

someInts = []

var threeDoubles = [Double](count: 3, repeatedValue: 0.0)

var anotherThreeDoubles = [Double](count: 3, repeatedValue: 2.5)
// anotherThreeDoubles is inferred as [Double], and equals [2.5, 2.5, 2.5]

var sixDoubles = threeDoubles + anotherThreeDoubles
// sixDoubles is inferred as [Double], and equals [0.0, 0.0, 0.0, 2.5, 2.5, 2.5]

```

- 数组字面量

```
var shoppingList: [String] = ["Eggs", "Milk"]
```

- 数组的读和改; `count`属性，`isEmpty`属性，`append(_:)`方法，`+`可以用于append操作，
下标可以用于取值和赋值，可以给区间赋值，`insert(_:atIndex:)`用于插入元素到指定的index，
`removeAtIndex(_:)`删除位于指定的index的元素, `removeLast()`删除最后一个元素,

```
var firstItem = shoppingList[0]
shoppingList[0] = "Six eggs"

shoppingList[4...6] = ["Bananas", "Apples"]
shoppingList.insert("Maple Syrup", atIndex: 0)
let mapleSyrup = shoppingList.removeAtIndex(0)
```

- 遍历数组, for-in,

```
for item in shoppingList {
    println(item)
}

for (index, value) in enumerate(shoppingList) {
    println("Item \(index + 1): \(value)")
}
```

- 集合类型 `Set<SomeType>`

- 集合的创建和初始化, 字面量和Array相同

```
var letters = Set<Character>()
letters.insert("a")
// letters now contains 1 value of type Character
letters = []
// letters is now an empty set, but is still of type Set<Character>

var favoriteGenres: Set<String> = ["Rock", "Classical", "Hip hop"]
var favoriteGenres: Set = ["Rock", "Classical", "Hip hop"]
```

- `count`, `isEmpty`, `insert(_:)`, `remove(_:)`, `contains(_:)`
- 遍历Set

```
for genre in favoriteGenres {
    println("\(genre)")
}
for genre in sorted(favoriteGenres) {
    println("\(genre)")
}
```

- 集合操作：`union(_:)`并集, `subtract(_:)`相对补集,`intersect(_:)`交集，`exclusiveOr(_:)`

- 比较集合, `==`, `isSubsetOf(_:)`, `isSupersetOf(_:)`, `isStrictSubsetOf(_:)`,
`isStrictSupersetOf(_:)`strict表示比较的两个集合不能完全相等,
 `isDisjointWith(_:)`判断两集合是否有共同存在的值

 - 集合的类型必须能提供hash value，swift的基本类型，枚举类型都是hashable的。
 `Hashable`, `Equatable`. Hashable接口需要Type有一个Int类型的名为hashValue的属性。
 
 
- 字典 Dictionary
类型写作Dictionary<Key, Value> ， key必须是Hashable的。创建空的Dict：
```
var namesOfIntegers = [Int: String]()
namesOfIntegers[16] = "sixteen"
// namesOfIntegers now contains 1 key-value pair
namesOfIntegers = [:]
// namesOfIntegers is once again an empty dictionary of type [Int: String]
```

- Dict字面量： `[key 1: value 1, key 2: value 2, key 3: value 3]`

```
var airports: [String: String] = ["YYZ": "Toronto Pearson", "DUB": "Dublin"]
//也可以这样初始化
var airports = ["YYZ": "Toronto Pearson", "DUB": "Dublin"]
```

- 字典的存取

`airports.count`, `airports.isEmpty`
```
//设置新key/value, 修改value也是一样的语法
airports["LHR"] = "London"
// 修改也可以用 updateValue(_:forKey:) 这个方法，区别是该方法返回旧的值
if let oldValue = airports.updateValue("Dublin Airport", forKey: "DUB") {
    println("The old value for DUB was \(oldValue).")
}

// 直接取值，返回的是optional。如果key不存在，则返回nil。下面的unpack操作很实用
if let airportName = airports["DUB"] {
}

//删除key有两种方式：
airports["APL"] = nil // APL has now been removed from the dictionary
if let removedValue = airports.removeValueForKey("DUB") {
}
```

- 迭代

```
for (airportCode, airportName) in airports {
    println("\(airportCode): \(airportName)")
}

// 迭代keys属性，values属性
for airportCode in airports.keys {
    println("Airport code: \(airportCode)")
}
for airportName in airports.values {
    println("Airport name: \(airportName)")
}

// keys属性转为数组，需要查一下keys的类型
let airportCodes = [String](airports.keys)
```















 
 
 
 
