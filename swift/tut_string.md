## Strings and Characters

- 初始化空字符串
```
var emptyString = ""               // empty string literal
var anotherEmptyString = String()  // initializer syntax
```

- isEmpty属性
```
if emptyString.isEmpty {
    println("Nothing to see here")
}
```

- String是Character的集合，可以用for-in来遍历

- 声明字符; 字符数组可以转换为字符串

```
let exclamationMark: Character = "!"

let catCharacters: [Character] = ["C", "a", "t", "!", "🐱"]
let catString = String(catCharacters)
println(catString)
```

- 字符串用`+`连接，字符串用`append()`添加字符

```
let exclamationMark: Character = "!"
welcome.append(exclamationMark) // welcome now equals "hello there!"
```

- String Interpolation. 字符串插入

```
let multiplier = 3
let message = "\(multiplier) times 2.5 is \(Double(multiplier) * 2.5)"
// message is "3 times 2.5 is 7.5"
```

- 特殊字符的表示

>The escaped special characters \0 (null character), \\ (backslash), \t (horizontal tab), \n (line feed), \r (carriage return), \" (double quote) and \' (single quote)

>An arbitrary Unicode scalar, written as \u{n}, where n is a 1–8 digit hexadecimal number with a value equal to a valid Unicode code point

```swift
let wiseWords = "\"Imagination is more important than knowledge\" - Einstein"
// "Imagination is more important than knowledge" - Einstein
let dollarSign = "\u{24}"        // $,  Unicode scalar U+0024
let blackHeart = "\u{2665}"      // ♥,  Unicode scalar U+2665
let sparklingHeart = "\u{1F496}" // 💖, Unicode scalar U+1F496
```

- Extended Grapheme Clusters; An extended grapheme cluster is a sequence of one or more Unicode scalars that (when combined) produce a single human-readable character. 增强字符集是一个或多个Unicode标量组合而成的人类可读的字符。下面例子是一个可读字符的两种表示方法，一个只有一个标量，一个有两个组成。在swift中都可被认为是字符类型。

```
let eAcute: Character = "\u{E9}"                         // é
let combinedEAcute: Character = "\u{65}\u{301}"          // e followed by ́
// eAcute is é, combinedEAcute is é
```

- 字符计数. 由于swift使用了Extended Grapheme Clusters作为字符识别的单位，意味着对字符串添加
内容不一定会增加count()的返回长度,例如下面：

```
var word = "cafe"
println("the number of characters in \(word) is \(count(word))")
// prints "the number of characters in cafe is 4"

word += "\u{301}"    // COMBINING ACUTE ACCENT, U+0301

println("the number of characters in \(word) is \(count(word))")
// prints "the number of characters in café is 4"
```

注意，由于在swift中一个字符所占内存不固定，所以`count(_:)`方法必须遍历字符串中所有字符来判断
extended grapheme cluster的边界.
`count(_:)`和`NSString`的length属性的值不一定一致。length属性是基于UTF16代表的16-bit代码单位。
为表明区别，在swift中访问NSString的length属性时，使用utf16Count。

- String indexes; `startIndex`, `endIndex`属性.
上一个index内容，下一个index内容，`predecessor()`, `successor()`.
 `advance(start:n:)` 从index向后数n的index
 `indicies(_:)` 创建一个index的Range

```
let greeting = "Guten Tag"
println(greeting.startIndex) // 0
println(greeting.endIndex)  // 9
greeting[greeting.startIndex] // G

greeting[greeting.startIndex.successor()]  // u
greeting[greeting.endIndex.predecessor()]  // g
let index = advance(greeting.startIndex, 7)
greeting[index]  // a
greeting.endIndex.successor() // fatal error: can not increment endIndex

for index in indices(greeting) {
    print("\(greeting[index]) ")
}
// prints "G u t e n   T a g"
```

- Inserting and Removing. `insert(_:atIndex:)`, `splice(_:atIndex:)`,
`removeAtIndex(_:)`, `removeRange(_:)`

```
var welcome = "hello"
welcome.insert("!", atIndex: welcome.endIndex)
// welcome now equals "hello!"

welcome.splice(" there", atIndex: welcome.endIndex.predecessor())
// welcome now equals "hello there!"

welcome.removeAtIndex(welcome.endIndex.predecessor())
// welcome now equals "hello there"

let range = advance(welcome.endIndex, -6)..<welcome.endIndex
welcome.removeRange(range)
// welcome now equals "hello"
```

- 字符串比较，用`==`, `!=`,并且比较的是extended grapheme cluster。字符比较也一样，所以即便两个字符串或者字符的
unicode scalar不同，结果也能是true。下面举了正反两个例子，外表相似不一定相同，重要的是extended grapheme cluster中是否相等。

>For example, LATIN SMALL LETTER E WITH ACUTE (U+00E9) is canonically equivalent to LATIN SMALL LETTER E (U+0065) followed by COMBINING ACUTE ACCENT (U+0301). Both of these extended grapheme clusters are valid ways to represent the character é, and so they are considered to be canonically equivalent:

>Conversely, LATIN CAPITAL LETTER A (U+0041, or "A"), as used in English, is not equivalent to CYRILLIC CAPITAL LETTER A (U+0410, or "А"), as used in Russian. The characters are visually similar, but do not have the same linguistic meaning:


- 前缀后缀的查询 `hasPrefix(_:)` 和 `hasSuffix(_:)`
- 字符串的Unicode表示， string有三个属性`utf8`, `utf16`, `unicodeScalars`;需要细读
