## 策略模式 Stragety 
StragetyContext, StragetyInterface, StragetyA, B, C
客户的只要知道一个Context, Context持有具体的Stragety

## 面向接口
高层模块，依赖抽象； 底层模块 实现抽象； 像Laravel, database 的 数据库driver 可以随意切换，这就是接口的力量。

## 装饰模式 Decorator
特点是 Decorator 自身持有 Decorator, 一层一层不断包装自己的过程。

## 代理模式 Proxy
A -> Proxy -> C
A想送礼物给C，A不能直接持有C的实例，就需要代理。A, Proxy 实现同一个送礼物的借口，c实例传给proxy， proxy持有a实例，proxy把c传入a，在接口中调用a的方法。

## 工厂模式 Factory

## 原型模式 prototype
clone()

## 模版模式 template
定义一个骨架，把一些具体的操作延迟到子类中。就是总结不变到代码，逻辑，放到父类中。

## 外观模式 Facade
为子系统的多组接口提供一个一致的interface. 为了完成一个功能，子系统中要调用多个类多个方法， 把这些方法放入Facade中，这样其他系统只要知道这个Facade就能完成功能了，而不需要知道每个子系统的类和方法。

## Builder

## 观察者 Observer
多个观察者订阅一个主题，主题更新时，会自动通知观察者，更新状态

## 状态模式 State
用于把很长的if条件，分解到各个State中，从而简化条件语句的写法。

## 适配器模式 Adaptor

## 备忘录模式 Memento

## 组合模式 Composite
将对象组合为树状结构来表示 “部分－整体”的层次结构。单个对象 和 组合对象 具有相同的接口。

## 迭代器模式 Iterator

## 单例模式 Singleton

## 桥接模式 

## 命令模式 Command

## 责任链模式 responsibility chain

## 中介者模式 Mediator

## 享元模式 Flyweight
Factory中用map存储对象，共享给其他类使用

## 解释器模式 Interpreter

## 访问者模式 Visitor











