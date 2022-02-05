#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by wind on 2021/7/13

import subprocess

def cmdout(cmd):
    # ip = str(cmdout("ifconfig | grep -C 1 eth0 | grep -v grep | grep inet | awk '{print $2}'")).strip()
    try:
        out_text = subprocess.check_output(cmd, shell=True).decode('utf-8')
    except subprocess.CalledProcessError as e:
        out_text = e.output.decode('utf-8')
    return out_text


if __name__ == '__main__':
    with open("redis.conf") as f:
        for line in f:
            ip = line.strip().split(":")[0]
            port = line.strip().split(":")[1]
            # cmd = "cat ./cmd.txt | redis-cli -h {} -p {} -a password".format(ip, port)
            host = "{}:{} change".format(ip, port)
            # set master要先，不然认证后进不去了，因为是按行重新进的相当于
            cmd = "cat ./cmd.txt | redis-cli -h {} -p {}".format(ip, port)
            print(host)
            out_text= cmdout(cmd)
            print(out_text)

