在 file -> project preference 中可以设置 android sdk的位置

默认的sdk安装在 android-studio 同目录下，名为 android-sdk

ANT_HOME
ANDROID_HOME
JAVA_HOME

PATH = %JAVA_HOME%\bin; \
	%ANT_HOME%\bin; \
	%ANDROID_HOME%\platform-tools; \
	%ANDROID_HOME%\tools; \

如果Android studio 显示 no debugable application, 点击
Tools->Android->Enable ADB Integration
