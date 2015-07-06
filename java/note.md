## 方法泛型

### 方法参数使用泛型

```java
public static < E > void printArray( E[] inputArray )
   {
      // Display array elements
         for ( E element : inputArray ){
            System.out.printf( "%s ", element );
         }
         System.out.println();
    }
```
传入的数组可以为任意类型。`<E>` 表示使用泛型。使用该方法时和普通方法没有差别。

### 方法绑定类型参数 (Bounded Type Parameters)
```java
// determines the largest of three Comparable objects
   public static <T extends Comparable<T>> T maximum(T x, T y, T z)
   {
      T max = x; // assume x is initially the largest
      if ( y.compareTo( max ) > 0 ){
         max = y; // y is the largest so far
      }
      if ( z.compareTo( max ) > 0 ){
         max = z; // z is the largest now
      }
      return max; // returns the largest object
   }
```
传入的x, y, z必须实现Comparable接口。`Comparable<T>`中的T的含义为
`the type of objects that this object may be compared to`

这种用法是对参数的一种范围限定。

## 类泛型

```java
public class Box<T> {

  private T t;

  public void add(T t) {
    this.t = t;
  }

  public T get() {
    return t;
  }

  public static void main(String[] args) {
     Box<Integer> integerBox = new Box<Integer>();
     Box<String> stringBox = new Box<String>();

     integerBox.add(new Integer(10));
     stringBox.add(new String("Hello World"));

     System.out.printf("Integer Value :%d\n\n", integerBox.get());
     System.out.printf("String Value :%s\n", stringBox.get());
  }
}
```
这种方式使得class中的属性可以为任意类型，不必在定义class就确定属性的类型，
属性的类型的确定被延迟到了使用class的时候。
