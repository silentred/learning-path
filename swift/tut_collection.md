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
```
