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




