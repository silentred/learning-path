JAVA_HOME=/usr/java/jdk1.7.0_51 
CATALINA_HOME=/usr/local/tomcat7
export JAVA_HOME
export CATALINA_HOME


###############################################

start_tomcat=$CATALINA_HOME/bin/startup.sh   
stop_tomcat=$CATALINA_HOME/bin/shutdown.sh

start() {   
        echo -n "Starting tomcat: "
        ${start_tomcat}
        echo "tomcat start ok."
}
stop() {
        echo -n "Shutting down tomcat: "
        ${stop_tomcat}
        echo "tomcat stop ok."
}

case "$1" in
  start)
        start
        ;;
  stop)
        stop
        ;;
  restart)
        stop
        sleep 3
        start
        ;;
  *)
        echo "Usage: $0 {start|stop|restart}"
esac

exit 0