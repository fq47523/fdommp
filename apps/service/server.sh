#!/bin/bash
ret=$1
process_name=$2
old_process_pid=`pgrep -o "$process_name"`

start_status_check(){
    local process_pid=`pgrep -o "$process_name"`
   
    if [[ $process_pid ]];then
        echo "{\"meters\":{\"new_pid\":\"$process_pid\",\"old_pid\":\"$old_process_pid\",\"status\":1}}"
    else
        echo "{\"meters\":{\"new_pid\":\"$process_pid\",\"old_pid\":\"$old_process_pid\",\"status\":2}}"

    fi

}


stop_status_check(){
    local process_pid=`pgrep -o "$process_name"`

    if [[ $process_pid ]];then
        echo "{\"meters\":{\"new_pid\":\"$process_pid\",\"status\":2}}"
    else
        echo "{\"meters\":{\"new_pid\":\"$process_pid\",\"status\":11}}"

    fi

}



zabbix_agentd(){
  if [ "$ret" = 'restarted' ];then
      /bin/systemctl restart  zabbix-agent
      start_status_check
  elif [ "$ret" = 'stopped' ];then
      /bin/systemctl stop  zabbix-agent
      stop_status_check
  elif [ "$ret" = 'started' ];then
      /bin/systemctl start  zabbix-agent
      start_status_check
  fi
}

nginx(){

  if [ "$ret" = 'restarted' ];then
      /sbin/service nginx restart
      start_status_check
  elif [ "$ret" = 'stopped' ];then
      /sbin/service nginx stop
      stop_status_check
  elif [ "$ret" = 'started' ];then
      /sbin/service nginx start
      start_status_check
  fi
}

mysql(){

  if [ "$ret" = 'restarted' ];then
      /sbin/service mysql restart
      start_status_check
  elif [ "$ret" = 'stopped' ];then
      /sbin/service mysql stop
      stop_status_check
  elif [ "$ret" = 'started' ];then
      /sbin/service mysql start
      start_status_check
  fi
}



$2


