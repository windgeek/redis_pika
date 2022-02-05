#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by wind on 2021/7/13

import subprocess
import paramiko

def cmdout(cmd):
    # ip = str(cmdout("ifconfig | grep -C 1 eth0 | grep -v grep | grep inet | awk '{print $2}'")).strip()
    try:
        out_text = subprocess.check_output(cmd, shell=True).decode('utf-8')
    except subprocess.CalledProcessError as e:
        out_text = e.output.decode('utf-8')
    return out_text


def sshexec_tool(ip, cmd):
    ssh = paramiko.SSHClient()
    # 允许连接不在know_hosts文件中的主机
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # 建立连接
    # ssh.connect(ip, username="xxxxxx", port=22, password="xxxxxx")
    ssh.connect(ip, username="xxxxxx", port=22, password="xxxxxx=")
    # 使用这个连接执行命令
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd, get_pty=True)
    # 获取输出
    print(ssh_stdout.read())
    # 关闭连接
    ssh.close()


if __name__ == '__main__':
    with open("redis.conf") as f:
        for line in f:
            ip = line.strip().split(":")[0]
            redis_port = line.strip().split(":")[1]
            message = "{}:{} config change".format(ip, redis_port)
            password = '123'
            conf = "/data/redis/redis{}/redis.{}.conf".format(redis_port, redis_port)
            cmd = "sudo chmod 777 {}; sudo echo 'requirepass {}'>> {}; sudo echo 'masterauth {}'>> {}; sudo chmod 644 {}".format(conf, password, conf, password, conf, conf)
            print(cmd)
            print(message)
            sshexec_tool(ip, cmd)
