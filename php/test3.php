<?php
function checkUser()
{
    echo "============确定User身份=========== \n";
    global $SUDO;
    $user_id = posix_getuid();
    if ($user_id == 0){
        echo "This is root ! \n";
        $SUDO = '';
    } else {
        echo "This is non-root \n";
        $SUDO = 'sudo';
    }
}

function checkNginxConf(){
    echo "============测试nginx配置=========== \n";

    global $nginx_path, $SUDO;
    exec("{$SUDO} {$nginx_path} -t", $output, $return);
    foreach ($output as $value) {
        echo "$value \n";
    }

    if($return===0){
        echo 'nginx配置成功', "\n";
    }else{
        echo "nginx配置有误 \n";
        exit();
    }
}

function startNginx(){
    global $SUDO, $nginx_path;

    echo "============启动Nginx=========== \n";
    exec("{$SUDO} {$nginx_path}", $output, $return);
    if ($return===0) {
        echo "启动成功 \n";
    }else{
        echo "启动不成功 \n";
    }
}

function stopNginx(){
    global $SUDO, $nginx_path;
    echo "============关闭Nginx=========== \n";
    exec("{$SUDO} {$nginx_path} -s stop", $output, $return);
    foreach ($output as $value) {
        echo "$value \n";
    }
    if ($return===0) {
        echo "关闭成功 \n";
    }else{
        echo "关闭失败 \n";
    }

}

function isNginxRunning(){
    global $nginx_pid_path;
    if (is_file($nginx_pid_path) && $pid = file_get_contents($nginx_pid_path)) {
        echo "==========Nginx正在运行，pid= $pid=========== \n";
        return true;
    }
    return false;
}


function isFpmRunning()
{
    global $fpm_path, $fpm_pid_path;
    if (is_file($fpm_pid_path) && $pid = file_get_contents($fpm_pid_path)) {
        echo "==========PHP-FPM正在运行，pid= $pid=========== \n";
        return true;
    }
    return false;
}

function startFpm(){
    global $fpm_path, $fpm_pid_path, $SUDO;
    echo "===========启动PHP-FPM========== \n";
    exec("{$SUDO} {$fpm_path}", $output, $return);
    foreach ($output as $value) {
        echo "$value \n";
    }
    if ($return===0) {
        echo "启动成功 \n";
    }else{
        echo "启动失败，退出 \n";
        exit();
    }

}

function restartFpm(){
    global $fpm_path, $fpm_pid_path, $SUDO;
    if (is_file($fpm_pid_path) && $pid = file_get_contents($fpm_pid_path)) {
        echo "========PHP-FPM正在重启，pid= $pid========= \n";
        exec("{$SUDO} kill -USR2 {$pid}", $output, $return);
        foreach ($output as $value) {
            echo "$value \n";
        }
        if ($return===0) {
            echo "启动成功 \n";
        }else{
            echo "启动失败，退出 \n";
            exit();
        }
    }else{
        echo "启动失败，无法读取pid文件，退出 \n";
        exit();
    }
}

$SUDO = '';
$nginx_path = '/usr/sbin/nginx';
$nginx_pid_path = '/var/run/nginx.pid';

checkUser();
checkNginxConf();
if(isNginxRunning()){
    stopNginx();
    startNginx();
}else{
    startNginx();
}

$fpm_path = '/usr/sbin/php-fpm';
$fpm_pid_path = '/var/run/php-fpm/php-fpm.pid';
if (isFpmRunning()) {
    restartFpm();
}else{
    startFpm();
}
/*
Nginx has only a few command-line parameters. Unlike many other software systems, the configuration is done entirely via the configuration file (imagine that).

-c </path/to/config> Specify which configuration file Nginx should use instead of the default.

-g Set global directives. (version >=0.7.4)

-t Don't run, just test the configuration file. nginx checks configuration for correct syntax and then try to open files referred in configuration.

-s signal Send signal to a master process: stop, quit, reopen, reload. (version >= 0.7.53)

-v Print version.

-V Print nginx version, compiler version and configure parameters.

-p prefix Set prefix path (default: /usr/local/nginx/). (version >= 0.7.53)

-h,-? Print help.


[Service]
Type=notify
PIDFile=/var/run/php-fpm/php-fpm.pid
EnvironmentFile=/etc/sysconfig/php-fpm
ExecStart=/usr/sbin/php-fpm --nodaemonize
ExecReload=/bin/kill -USR2 $MAINPID
PrivateTmp=true

*/