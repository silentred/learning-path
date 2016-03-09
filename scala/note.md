## install
brew install scala

## hello world
SCALA_HOME=/usr/local/Celler/scala/...
PATH=$PATH:$SCALA_HOME/bin

HelloWorld.scala

```scala
object HelloWorld {
  def main(args: Array[String]): Unit = {
    println("Hello, world!")
  }
}
```
scalac HelloWorld.scala
scala HelloWorld

## hello world with IDEA
install scala plugin

new project

cmd+;
import scala sdk: /usr/local/Celler/scala/.../idea
注意这里是idea文件夹结尾的，看这篇文章。否则会报错，重复的文件。(发现 libexc文件夹也可以, 没发现区别)
http://ark.svbtle.com/my-days-of-scala-week-1


## Date Type

Unit
Nothing
Any
AnyRef

## Variable
var 变量
val 常量

## Access Modifier
private, protected, public

```scala
class Outer {
   class Inner {
      private def f() { println("f") }
      class InnerMost {
         f() // OK
      }
   }
   (new Inner).f() // Error: f is not accessible
}

package p {
   class Super {
      protected def f() { println("f") }
   }
   class Sub extends Super {
      f()
   }
   class Other {
     (new Super).f() // Error: f is not accessible
   }
}

package society {
   package professional {
      class Executive {
         private[professional] var workDetails = null // 在 professional 包范围内可访问
         private[society] var friends = null
         private[this] var secrets = null

         def help(another : Executive) {
            println(another.workDetails)
            println(another.secrets) //ERROR。只能在another对象中访问
         }
      }
   }
}
```

## Function

```scala
def functionName ([list of parameters]) : [return type] = {
   //function body
   return [expr]
}
```
没有＝和函数体，表示abstract

## Closure

```scala
val method = (i:Int) => i * 3
```

## Array

```scala
var z : Array[String] = new Array[String](3)
var z = new Array[String](3)
z(0) = "Zara"; z(1) = "Nuha"; z(4/2) = "Ayan"


```

## Collection
strict
lazy

mutable
immutable

```scala
// Define List of integers.
val x = List(1,2,3,4)
val fruit: List[String] = List("apples", "oranges", "pears")
val fruit = "apples" :: ("oranges" :: ("pears" :: Nil))


// Define a set.
var x = Set(1,3,5,7)
var s : Set[Int] = Set(1,3,5,7)

// Define a map.
val x = Map("one" -> 1, "two" -> 2, "three" -> 3)

// Create a tuple of two elements.
val x = (10, "Scala")

// Define an option
val x:Option[Int] = Some(5)
```
Option[T] can be Some[T] or None





