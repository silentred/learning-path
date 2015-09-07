# Subscripts

下标脚本 可以定义在类（Class）、结构体（structure）和枚举（enumeration）这些目标中，可以认为是访问集合（collection），列表（list）或序列（sequence的快捷方式，使用下标脚本的索引设置和获取值，不需要再调用实例的特定的赋值和访问方法。举例来说，用下标脚本访问一个数组(Array)实例中的元素可以这样写 someArray[index] ，访问字典(Dictionary)实例中的元素可以这样写 someDictionary[key]。

使用关键词`subscript`, 参数可以多个。

```swift
// 
// 用下标访问时出发的代码段，读和写。和php中的__set(), __get()类似。
subscript(index: Int) -> Int {
    get {
      // 返回与入参匹配的Int类型的值
    }

    set(newValue) {
      // 执行赋值操作
    }
}

// 只读，可以省略get, set关键词，直接写读的代码段
struct TimesTable {
    let multiplier: Int
    subscript(index: Int) -> Int {
      return multiplier * index
    }
}
let threeTimesTable = TimesTable(multiplier: 3)
print("3的6倍是\(threeTimesTable[6])")
```

## Subscript Usage

```swift
var numberOfLegs = ["spider": 8, "ant": 6, "cat": 4]
numberOfLegs["bird"] = 2


struct Matrix {
    let rows: Int, columns: Int
    var grid: [Double]
    init(rows: Int, columns: Int) {
      self.rows = rows
      self.columns = columns
      grid = Array(count: rows * columns, repeatedValue: 0.0)
    }
    func indexIsValidForRow(row: Int, column: Int) -> Bool {
        return row >= 0 && row < rows && column >= 0 && column < columns
    }
    subscript(row: Int, column: Int) -> Double {
        get {
            assert(indexIsValidForRow(row, column: column), "Index out of range")
            return grid[(row * columns) + column]
        }
        set {
            assert(indexIsValidForRow(row, column: column), "Index out of range")
            grid[(row * columns) + column] = newValue
        }
    }
}

var matrix = Matrix(rows: 2, columns: 2)
matrix[0, 1] = 1.5
matrix[1, 0] = 3.2

```










