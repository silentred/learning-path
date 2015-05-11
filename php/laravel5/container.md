
##关于bind方法：

- 这两种绑定相同，在$app->make()的时候，都返回一个新的实例
	
		$this->app->bind('App\DAO\UserDAO',function(){
		return new UserDAOImpl();
		});
		
		$this->app->bind('App\DAO\UserDAO','App\DAO\Impl\UserDAOImpl');

- bind还可以设置alias，如下，第一个参数传入数组，key为别名，value为接口名


		$this->app->bind(['dao.user' => 'App\DAO\UserDAO'],'App\DAO\Impl\UserDAOImpl');


- 第三个参数为true就是singleton的效果一样
 
		$this->app->bind(['dao.user' => 'App\DAO\UserDAO'],'App\DAO\Impl\UserDAOImpl', true);

- Controller的方法默认可以使用IoC

	 	public function showMoneyDashboard(MoneyRepository $money)

- 任意方法都可以使用IoC

例如有以下一个类

		class ThingDoer
		{
		    public function doThing($thing_key, ThingRepository $repository)
		    {
		        $thing = $repository->getThing($thing_key);
		        $thing->do();
		    }
		}
App::call()方法可以为某个类的某个方法使用IoC, 第二个数组参数是传入doThing方法参数

		App::call(
            [$thingDoer, 'doThing'],
            ['thing_key' => 'awesome-parameter-here']
        );


## Command Bus

本质是一个相关方法的调用集合

- 生成一个Command

		php artisan make:command FirstCommand

这时会在app\Commands下生产一个FirstCommand类，其中的handle方法就是具体执行的内容,handle方法支持IoC。

- 调用Command

在Controller中调用dispatch方法，如下。 默认的Controller拥有`trait DispatchesCommands` 所以拥有dispatch方法。下面的命令在controller中执行，就会执行FirstCommand::handle()中的内容

	$this->dispatch(new FirstCommand());

- 队列Command

		php artisan make:command PurchasePodcast --queued

这个`--queued`参数，会增加 `Illuminate\Contracts\Queue\ShouldBeQueued` 接口和`SerializesModels` trait 。 这个接口没有任何方法，只是一个标记（instanceof）。

- 管道命令（TODO）



##Event事件

- 生成事件类

在`EventServiceProvider`中的listen属性中添加事件名称和Handler的名称，例如：

	protected $listen = [
        'App\Events\FirstEvent' => [
            'App\Handlers\Events\FirstEventHandler',
        ],
	];

运行命令 `php artisan event:generate` 就能根据$listen中的内容生成对应文件，并且不会覆盖已经生成的文件。

- 处理事件

事件注册时在`EventServiceProvider`之中的boot完成的。 Hanlder中的handle方法接受一个FirstEvent参数，handle为处理方法。

- 触发事件

		\Event::fire(new FirstEvent()); 
		//or use the helper function
		event(new FirstEvent());

- 队列事件

加上`Illuminate\Contracts\Queue\ShouldBeQueued`标记即可，同时，使用`Illuminate\Queue\InteractsWithQueue` trait, 可以在处理事件之中使用 

	$this->release(30);
	$this->delete(); 

等方法把任务删除，重置等等。

- 订阅者

订阅者本质还是一个handler，必须实现subscribe($event)方法。

	class ThirdEventHandler {
	
		/**
		 * Create the event handler.
		 *
		 * @return void
		 */
		public function __construct()
		{
			//
		}
	
	    public function doSomething(){
	        echo " ThirdEventHalder !!!..";
	    }
	
	    public function doSomethingToo(){
	        echo "lalala, ThirdEventHalder again!!!..";
	    }
	
	    /**
	     * 注册监听器给订阅者。
	     *
	     * @param  Illuminate\Events\Dispatcher  $events
	     * @return array
	     */
	    public function subscribe($events)
	    {
	        $events->listen('App\Events\FirstEvent', 'App\Handlers\Events\ThirdEventHandler@doSomething');
	
	        $events->listen('App\Events\FirstEvent', 'App\Handlers\Events\ThirdEventHandler@doSomethingToo');
	    }
	
	}

如何订阅呢？

	$subscriber = new App\Handlers\Events\ThirdEventHandler();
	Event::subscribe($subscriber);
	// or rely on IoC
	Event::subscribe('App\Handlers\Events\ThirdEventHandler');

搞定了。

一个Event可以对应多个Handler,Handler的执行顺序和绑定顺序一致。
一个Subscriber可以绑定多个事件