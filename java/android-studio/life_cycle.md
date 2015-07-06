## 生命周期

打开FirstActivity
1. onCreate
2. onStart
3. onResume

点击打开SecondActivity
1. FirstActivity -- onPause
2. SecondActivity -- onCreate, onStart, onResume
3. FirstActivity -- onStop

点击back键
1. SecondActivity -- onPause
2. FirstActivity -- onRestart, onResume
3. SecondActivity -- onStop


`onSaveInstanceState()`在destroy之前执行？
其中保存在bundle的数据，可以在onCreate中取出？
例如 横竖屏转换

## 创建Activity
1. 类名
```java
Intent intent = new Intent(FirstActivity.this, SecondActivity.class);
startActivity(intent);
```

2. ComponentName
```java
Intent intent = new Intent(FirstActivity.this, SecondActivity.class);
ComponentName component = new ComponentName(FirstActivity.this, SecondActivity.class);
intent.setComponent(component)
startActivity(intent);
```

3. Intent-Filter 隐式
```java
//AndroidManifest.xml 文件中配置 activity => intent-filter => android:name
Intent intent = new Intent("com.example.jason.SecondActivity.START");
//intent.setAction(name)
startActivity(intent);
```

## Intent 传递数据
- 对象
```java
Bundle bundle = new Bundle();
bundle.putSerializable("obj", object);
intent.putExtra(bundle);
```
```java
//在SecondActivity中取数据
Object obj = getIntent().getSerializableExtra("obj");
```

- 图像(Bitmap)
```java
bundle.putParcelable("bitmap", bitmap);
```

- 大小限制

数据必须小于0.5MB，否则无法传递，后台报错. workaround:
把数据存文件，把文件地址传给activity. [参考链接](http://stackoverflow.com/questions/8552514/is-there-some-limits-in-android-bundle)


## 关于任务和栈
[官方文档](http://developer.android.com/guide/components/tasks-and-back-stack.html) 最好读一下。
