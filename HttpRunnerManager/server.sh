#!/bin/bash                                                                                                                             

project_dir=/opt/
project_name=HttpRunnerManager
host=0.0.0.0
port=8000
log_path=$project_dir$project_name/logs/all.log
server(){
    echo "项目路径：$project_dir$project_name"
    if [ "$1" == '1' ]; then
        pid=`ps -ef|grep manage|grep $project_name|grep /usr/bin/python|awk '{print $2}'`
        if [ "$pid" == "" ]; then
            chmod -R 755 $project_dir$project_name > $log_path 2>&1
            nohup python $project_dir$project_name/manage.py runserver $host:$port > $log_path 2>&1 &
            sleep 1
            new_pid=`ps -ef|grep manage|grep $project_name|grep /usr/bin/python|awk '{print $2}'`
            echo "启动成功: $new_pid"
        else
            echo "项目已经启动：$pid"
        fi
        echo "访问地址: $host:$port"
    elif [ "$1" == '2' ]; then
        pid=`ps -ef|grep manage|grep $project_name|grep /usr/bin/python|awk '{print $2}'`
        if [ "$pid" != "" ]; then
            echo "关闭进程: $pid"
            kill -9 $pid
        fi
        echo "启动进程..."
        chmod -R 755 $project_dir$project_name > $log_path 2>&1
        nohup python $project_dir$project_name/manage.py runserver $host:$port >$log_path 2>&1 &
        sleep 1
        new_pid=`ps -ef|grep manage|grep $project_name|grep /usr/bin/python|awk '{print $2}'`
        echo "启动成功: $new_pid"
        echo "访问地址: $host:$port"
    elif [ "$1" == '3' ]; then
        pid=`ps -ef|grep manage|grep $project_name|grep /usr/bin/python|awk '{print $2}'`
        echo "关闭进程: $pid"
        kill -9 $pid
    else
        echo '请输入正确参数，1启动2重启3停止'
        exit 1
    fi
}
server $1

