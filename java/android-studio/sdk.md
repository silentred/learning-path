## SDK
在 file -> project preference 中可以设置 android sdk的位置

默认的sdk安装在 android-studio 同目录下，名为 android-sdk

- ANT_HOME
- ANDROID_HOME
- JAVA_HOME

```
PATH = %JAVA_HOME%\bin; \
	%ANT_HOME%\bin; \
	%ANDROID_HOME%\platform-tools; \
	%ANDROID_HOME%\tools; \
```

## debug应用

如果Android studio 显示 no debugable application, 点击
Tools->Android->Enable ADB Integration

## root权限
`adb shell` 进入android shell
`su` 进入root权限
`cd /data/data/com.example.jason.myapplication`进入项目文件夹

## 添加 external lib
Project Structure -> Dependencies -> + lib Dependency
这会在app目录下的build.gradle中加入
```
compile 'com.android.support:recyclerview-v7:22.2.0'
```


## support library
jar包的位置在 <sdk-dir>/extra/android/support 下
源码的位置在 <sdk-dir>/extra/android/m2repository 下

## 渲染错误 Missing styles
直接部署到device之后，就修复了

## Floating Action Button 背景色
加入属性：`app:backgroundTint="#FF0000"`
[参考链接](http://stackoverflow.com/questions/30576450/floatingactionbutton-example-with-support-library)
