# SDK 文档

## conversion 设计

1. 存储

采用分表设计，名称格式为 affi_conversion_201701 。 
conversion_time 在1月内的转化记录都会进入这张表。

建表语句中有注释: 
```
CREATE TABLE `affi_conversion_%s` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `conversion_id` char(32) NOT NULL,
  `conversion_time` timestamp NOT NULL,
  `uid` bigint(20) unsigned NOT NULL,
  `app_id` char(25) NOT NULL,
  `customer_reference` char(10) NOT NULL,
  `conversion_status` char(15) NOT NULL,
  `conversion_value` decimal(10,2) NOT NULL COMMENT '用户给苹果的充值(美金)',
  `conversion_value_origin` decimal(10,4) NOT NULL DEFAULT '0.00' COMMENT '用户给苹果的充值(本地货币)',
  `publisher_commission` decimal(10,2) NOT NULL COMMENT '广告佣金(美金)',
  `apple_payed_us` tinyint(3) unsigned NOT NULL DEFAULT '0' COMMENT '苹果是否已经打款给我们',
  `apple_amount` double NOT NULL DEFAULT '0.00' COMMENT '苹果给我们打款的金额(当地货币)',
  `apple_amount_usd` double NOT NULL DEFAULT '0.00' COMMENT '苹果给我们打款的金额(美金), 汇率不同',
  `apple_currency` char(6) NOT NULL DEFAULT '' COMMENT '苹果给我们打款的货币名称, CNY, USD 等',
  `pay_user_amount` double NOT NULL DEFAULT '0.00' COMMENT '我们打给厂商的金额(美金), 每个厂商比例不同',
  `payed_user` tinyint(3) unsigned NOT NULL DEFAULT '0' COMMENT '我们是否已经打款给厂商',
  `app_payment_id` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '打款给厂商的支付ID',
  `pay_time` int(10) unsigned NOT NULL DEFAULT '0' COMMENT 'conversion 发生的 timestamp',
  `pay_time_day` tinyint(3) unsigned NOT NULL DEFAULT '0',
  `type` tinyint(3) unsigned NOT NULL DEFAULT '0' COMMENT '0: SDK, 1: Web',
  `at` char(32) NOT NULL DEFAULT '' COMMENT 'advertiser token',
  `in_app` tinyint(3) unsigned NOT NULL DEFAULT '1',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `affi_conversion_conversion_id_unique` (`conversion_id`),
  KEY `affi_conversion_uid_index` (`uid`),
  KEY `affi_conversion_app_id_index` (`app_id`),
  KEY `affi_conversion_day_index` (`pay_time_day`),
  KEY `affi_conversion_payment_flag` (`app_id`, `apple_payed_us`, `payed_user`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

还有一个 affi_conversion_raw 表，用于存放抓取到的原始的json格式的记录, 没有分表。

创建表的命令:

```
# game-website 目录下
php artisan affiliate:table --from=2017-03 --to=2017-06
```

2. 抓取

分为两种模式，cmd和web模式，cmd是以 termial 为UI的抓取模式；web是以 websocket 为数据展示接口的模式。

启动 web 模式的命令:

```
fetcher -appKey=yYit5mQdd1 -apiKey=SHba2kUI -go=4 -host=127.0.0.1:3306 -user=root -pwd=being2015 -db=fenda -log_dir=./log -web
```
监听7100端口。 -go=4 表示启动4个worker. 

接受job的接口为：
```
POST /job/fetch
request: 
{
    from_date: "2017-01-01 00:00:00",
    to_date: "2017-01-02 00:00:00",
}
参数以 web-form 形式传递，例如 a=b&c=d
```

查看状态的websocket接口为：
```
GET /status
message:
{"worker_num":4,"offset":0,"fetched_num":0,"saved_num":0,"stop_num":4}

每秒收到一次更新消息
```



启动cmd模式：
```
fetcher -appKey=yYit5mQdd1 -apiKey=SHba2kUI -from=2017-02-08T00:00:00 -to=2017-02-09T00:00:00 -go=4 -host=127.0.0.1:3306 -user=root -pwd=being2015 -db=fenda -log_dir=./log -web
```
这里多了 -from , -to, 表示本次抓取的时间范围。运行效果和top命令类似，能看到各个worker的运行状态。


抓取策略：

能从 form, to 中得到时间范围，把时间段分为 4 份， 分别包装为job, 交给每个worker。worker得到job后， 执行 worker.Start() 开始本次的抓取。 如果某个worker首先抓完，该worker状态会设为stop，这时调度器会判断一下，目前如果有running的worker，并且job的时间范围大于1小时，就会把这个running worker的job和空闲的worker平分一下，stopped worker再次进入 running 状态. 


## apple_payment 设计

1. 表结构：

```
Schema::create('affi_sdk_apple_payment', function (Blueprint $table) {
    $table->increments('id');
    $table->string('reference', 40); // 支付凭证的ID
    $table->string('payment_date', 32); // 苹果支付时间
    $table->string('currency', 6); // 当地货币名称
    $table->decimal('net_value', 10, 2); // 不含税当地货币
    $table->decimal('total_value', 10, 2); // 苹果支付我们的总额(当地货币)
    $table->string('paid_currency', 6); // 理论总是为 USD
    $table->decimal('paid_amount', 10, 2); // 苹果支付我们的总额(USD)
    $table->float('exchange_rate', 10, 4)->default(0); // 汇率 当地货币/美元, 例如 6.9/1
    $table->string('csv_file')->default(''); // csv 文件的URL
    $table->tinyInteger('imported',0, true)->default(0); // 是否已经导入， 0 未导入， 1 导入中， 2 已导入
    $table->timestamp('imported_at')->default(0); // 没有使用
    $table->timestamp('created_at')->default(DB::raw('CURRENT_TIMESTAMP'));
    $table->timestamp('updated_at')->default(DB::raw('CURRENT_TIMESTAMP'));
    $table->index(['reference']);
});
```

苹果有接口查询已经生成的支付文件，每天跑一次，插入新的支付凭证.

其中有一个字段在导入前必须填写，`paid_amount`, 在后台输入这个值后，才能得到苹果支付时的汇率，
exchange_rate 自动会补充完整。

2. 导入

conversion表，`apple_payed_us`, `apple_amount`, `apple_amount_usd`, `apple_currency` 这几个字段是从 苹果支付我们的明细中 查到对应的conversion，从而更新得到的。

步骤为：下载 csv 文件到本地，扫描文件每一行，找到对应的数据，更新 conversion 表中的某一行。

这里有可能会发生这种情况：
苹果的csv明细中包含了conversion表中没有的数据，说明conversion抓取时候漏了某几条数据。这几条数据会被记录下来，可以通过接口查询：

```
GET /import/warning
response:
{
    error_code:0,
    data: [
        {date:"2017-01-01 00:00:01", conv_id: "xxxx , filename"},
        ...
    ]
}
```

这个接口的数据可以直接在 后台的 "抓取转化工具" 中看到 warning.

## app

一张表，存放游戏的信息

```
Schema::create('affi_sdk_app', function (Blueprint $table) {
    $table->increments('id');
    $table->string('name', 100);  // 游戏名称
    $table->string('app_id', 50); // in app store
    $table->string('bundle_id', 50); //可以为空
    $table->float('ratio', 10, 5); // 分成比例，例如 0.6 ，表示 厂商得到 60%, 我们得到 40%
    $table->timestamp('created_at')->default(DB::raw('CURRENT_TIMESTAMP'));
    $table->timestamp('updated_at')->default(DB::raw('CURRENT_TIMESTAMP'));
});
```

## app_payment 设计

存放我们和游戏厂商结算的记录

```
Schema::create('affi_sdk_app_payment', function (Blueprint $table) {
    $table->bigIncrements('id');
    $table->integer('sdk_app_id', 0, true);
    $table->string('reference', 40); // ID, game-201701
    $table->timestamp('from_date')->default(DB::raw('CURRENT_TIMESTAMP')); // 计算日期范围 2016-10-01
    $table->timestamp('to_date')->default(DB::raw('CURRENT_TIMESTAMP')); // 2016-10-31
    $table->timestamp('payment_date')->default(DB::raw('CURRENT_TIMESTAMP')); // 我们实际支付厂商的日期 
    $table->string('currency', 6); // 为USD
    $table->decimal('net_value', 10, 2); // 不含税总额
    $table->decimal('total_value', 10, 2); // 我们支付厂商的 美金总额
    $table->double('apple_amount_usd')->default(0); // 苹果支付我们的 美金总额
    $table->string('dump_file', 60)->default(''); // 导出的 csv 文件; 包含每个conversion, 默认存放位置为 `public/app_csv/{this->reference}.csv`
    $table->tinyInteger('actual_paid')->default(0); // 实际是否支付了厂商
    $table->timestamp('created_at')->default(DB::raw('CURRENT_TIMESTAMP'));
    $table->timestamp('updated_at')->default(DB::raw('CURRENT_TIMESTAMP'));
});
```

生成记录的逻辑为： 
找到 apple 已支付我们的记录，把记录的 payed_user, pay_user_amount, app_payment_id 设置为对应的值。 app_amount_id 是为了把某个 app_payment 的转化记录导出到csv，给厂商结算的时候附带上作为明细.

## 整个项目包含的组件：

fetcher: 抓取conversion，导入 apple_payment; 项目在 be-service/apple-affiliate 中
game-website: php抓取脚本, 建表命令
game-manage: 生成 app_payment, 查询 conversion



