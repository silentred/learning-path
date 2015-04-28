#源码解析

## autoload.php 用的是composer的autoload
有一个地方需要提醒，Laravel中的两个helper.php在venders中的laravle框架目录下的composer.json中包含了，所以在加载autolaod.php之后就能使用helper中的函数了

## app.php 启动整个项目

### 首先看下Application这个类
`class Application extends Container implements ApplicationContract, HttpKernelInterface`
Container中方法很多，实现了ArrayAccess，主要方法都是是用于绑定对象的（利于重用）。
ApplicationContract 需要实现注册service provider。
HttpKernelInterface 就一个handle方法，接受一个Request, 返回一个Response。

#### Application的构造方法
- registerBaseBindings()
把app对象自身绑定到instance属性数组。

- registerBaseServiceProviders()
注册两个service provider, 一个是EventServiceProvider，注册一个单例Dispatcher，名字为'events'（TODO）,另一个是RoutingServiceProvider(), 包含了Router， RouterGenerator, Redirector, ResponseFactory, 构造ResponseFactory接受两个参数，一个是ViewFactory,一个是Redirecer

- registerCoreContainerAliases(), 把一系列key和对应的类名，接口名加入alias属性数组
`'app'                  => ['Illuminate\Foundation\Application', 'Illuminate\Contracts\Container\Container', 'Illuminate\Contracts\Foundation\Application']`
'app'是key， 数组中的三个是别名（猜测：估计是每当用$app->make('Illuminate\Foundation\Application'),都会返回$app['app']）

### 构造完App后开始创建重要的instance
1. 在app容器中共享一个App\Http\Kernel单例。
看一下这个类，继承了一个`Illuminate\Foundation\Http\Kernel`，实现了bootstrap, handle, terminate, getApplication这四个方法，可以想象，当收到request时候，流程就是前三个依次执行，非常简化。
`protected $bootstrappers`数组，包含了bootstrap的一系列启动项目。
他的__construct接受两个参数，一个Application，一个Router。需要再看一下`$app->singleton`是如何初始化他的，莫非已经包含了IoC的功能？（**TODO**）
这里先假设这两个参数已经被正确传入了。接着，立即把`protected $routeMiddleware`中的给router的middleware方法调用。middleware方法只是把key和Class名称加入到router的middleware属性数组中。


2. 在app容器中共享一个App\Console\Kernel单例。
继承自`Illuminate\Foundation\Console\Kernal`。他的构造方法接受一个$app，一个Dispatcher $event。并且设置了一个scheduler，用于每隔一个时间段执行任务。`protected $command`s属性和`protected function schedule`方法都是用来重写的。

3. 在app容器中共享一个App\Exceptions\Handler单例。
继承自`Illuminate\Foundation\Exceptions\Handler`。他的构造方法接受一格`Psr\Log\LoggerInterface`。

至此，app算是构造完成。接下来就要调用他的方法了。

### 调用Application

> $kernel = $app->make('Illuminate\Contracts\Http\Kernel');

> $response = $kernel->handle(
	$request = Illuminate\Http\Request::capture()
);

> $response->send();

> $kernel->terminate($request, $response);

这里的代码非常明确，首先make一个Kernal，之前已经将其绑定为singleton了。然后kernal handle一个request, 得到一个response, response调用send方法，最后kernal terminate。这里只是一个高纬度的概括，具体其中实现的方法，还需要进一步深入。

看到这里，我的感觉是，整个项目最重要的部分就是$app这个容器，或者说Container这个类，绑定的是什么(Closure)，有哪些绑定方法，各个方法的作用是什么，make 和 build有什么区别，alias的作用是什么，等。了解了这些，对写框架会有帮助。
Event的作用，


---

#源码解析（二）
##包装请求
`Illuminate\Http\Request::capture()`根据SymfonyRequest的createFromGlobals得到的request，复制其中内容$_GET, $_POST, $_COOKIE, $_FILEs, $_SERVER到laravel到request类，包装完成。
请求包含的属性可以看一下，其中有一个是sessionStore。

## $app->handle($request)
            try
    		{
    			$response = $this->sendRequestThroughRouter($request);
    		}
    		catch (Exception $e)
    		{
    			$this->reportException($e);
    
    			$response = $this->renderException($request, $e);
    		}
    
    		$this->app['events']->fire('kernel.handled', [$request, $response]);

传给router，或者exeption handler给出response