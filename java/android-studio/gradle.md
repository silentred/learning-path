默认位置是在 %HOME%/.gradle 下, 在 setting -> gradle 中可以调整 gradle home

- Offline work : If you check this option, Gradle will use things from the cache itself for dependency resolution. In case the files are not there in the cache, then it will result in a build error.
- The Service Directory Path is the default Gradle Home directory. This is where the cache is maintained, etc.
- Gradle VM Options can be used to tweak some JVM Settings and/or provide some property files.

reference: http://rominirani.com/2014/08/19/gradle-tutorial-part-6-android-studio-gradle/
