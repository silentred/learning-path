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

## debug

如果Android studio 显示 no debugable application, 点击
Tools->Android->Enable ADB Integration

## root
`adb shell` 进入android shell
`su` 进入root权限
`cd /data/data/com.example.jason.myapplication`进入项目文件夹
