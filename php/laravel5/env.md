#Laravel5中环境变量的载入

## Bootstrap
在Kernel中可以发现第一个启动项就是关于ENV的

    protected $bootstrappers = [
    	'Illuminate\Foundation\Bootstrap\DetectEnvironment',
    	'Illuminate\Foundation\Bootstrap\LoadConfiguration',
    	'Illuminate\Foundation\Bootstrap\ConfigureLogging',
    	'Illuminate\Foundation\Bootstrap\HandleExceptions',
    	'Illuminate\Foundation\Bootstrap\RegisterFacades',
    	'Illuminate\Foundation\Bootstrap\RegisterProviders',
    	'Illuminate\Foundation\Bootstrap\BootProviders',
    ];

`Illuminate\Foundation\Bootstrap\DetectEnvironment` 在这个类中启动，进入查找，会发现

    try
    {
    	Dotenv::load($app->basePath(), $app->environmentFile());
    }
    catch (InvalidArgumentException $e)
    {
    	//
    }
    
    $app->detectEnvironment(function()
    {
    	return env('APP_ENV', 'production');
    });

具体的方法就是Dotenv的一个静态load方法，并且如果读取失败，会默认设置为'production'

这里可以看到load传入的两个参数是为了找到读取文件的位置，`$app->environmentFile()`返回的是文件名，是$app->environmentFile，默认是`.env`。在$app中有一个方法：

    public function loadEnvironmentFrom($file)
    {
    	$this->environmentFile = $file;
    
    	return $this;
    }

用这个方法可以修改载入env文件的名字。

## 解析ENV文件

Dotenv::load方法先判断文件is\_readable 和 is\_file，否则抛出异常。ini\_get， ini\_set设定auto\_detect\_line\_endings为1，然后再设会原来的值。

	file($filePath, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);

读出文件的每一行，然后foreach遍历，然后设置环境变量。可以发现，这里支持NestedVariable，就是说设置过的变量可以用$(VAR_EXISTS)在读取其值，类似shell。

设置变量存在于三个位置，putevn(), $\_ENV, $\_SERVER, 并且会判断是否key是否重复，如果重复就跳过。

读取时候也是从这三个位置, getenv(), $\_ENV, $\_SERVER。

## app中的几个关于Env的方法：


`public function environmentFile()`默认返回'.env'

`public function environment()`不带参数，返回当前env的值；如果带参数（array），则遍历比对判断，如果包含当前环境名称，则返回true

`public function isLocal()` $app['env']是否等于'local'

`public function afterLoadingEnvironment(Closure $callback)`

`public function detectEnvironment(Closure $callback)`

