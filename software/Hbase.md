# Hbase

### brew install hadoop
In Hadoop's config file:
  /usr/local/Cellar/hadoop/2.7.2/libexec/etc/hadoop/hadoop-env.sh,
  /usr/local/Cellar/hadoop/2.7.2/libexec/etc/hadoop/mapred-env.sh and
  /usr/local/Cellar/hadoop/2.7.2/libexec/etc/hadoop/yarn-env.sh
$JAVA_HOME has been set to be the output of:
  /usr/libexec/java_home


### brew install hbase
You must edit the configs in:
/usr/local/Cellar/hbase/1.1.2/libexec/conf
to reflect your environment.
For more details:
https://hbase.apache.org/book.html