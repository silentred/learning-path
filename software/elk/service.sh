workDir=$(cd `dirname $0`; pwd)

logstashBin=logstash
filebeatBin=filebeat
elasticBin=elasticsearch
kibanaBin=kibana

elasticPid="$workDir/elastic.pid"
beatPid="$workDir/beat.pid"
logstashPid="$workDir/logstash.pid"
kibanaPid="$workDir/kibana.pid"

beatConfig="$workDir/filebeat.yml"
logstashConfig="$workDir/logstash.conf"

start() {
    nohup $elasticBin > /dev/null 2>&1 & 
    echo $! > $elasticPid
    nohup $filebeatBin -c $beatConfig > /dev/null 2>&1 &  
    echo $! > $beatPid
    nohup $logstashBin -c $logstashConfig > /dev/null 2>&1 & 
    echo $! > $logstashPid
    nohup $kibanaBin > /dev/null 2>&1 & 
    echo $! > $kibanaPid

}

stop() {
    stopByPid $kibanaPid $kibanaBin
    stopByPid $elasticPid $elasticBin
    stopByPid $logstashPid $logstashBin
    stopByPid $beatPid $filebeatBin
}

stopByPid() {
    FILE=$1
    BIN=$2
    if [ -f $FILE ]; then
        pid=`cat $FILE`
        rm -f $FILE

        if ["$pid"x != ""x]; then
            kill -9 $pid
        else
            echo "PID $pid is not running"
            return 1
        fi

    else 
        pid=`ps aux | grep $BIN | grep -v grep | awk '{print $2}' | head -1`

        echo "$FILE not exists, $BIN pid is $pid" && exit 1
    fi


}

case $1 in
start)
    if [ -f $beatPid]; then
        echo "already running"
        exit 1
    fi

    echo -n "starting..."
    start
    sleep 1
    echo "please check pid files"
    ;;
stop)
    echo -n "stoping..."
    stop
    if [[ $? -gt 0 ]]; then
         echo "failed"
    else
        echo "ok"
    fi
    ;;
*)
    echo "hello world"
;;
esac
