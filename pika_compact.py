#!/data/python3.9/bin/python3.9
# -*- coding: utf-8 -*-
# Created by wind on 2021/1/19

import subprocess
import requests
import time
import json


def cmdout(cmd):
    try:
        out_text = subprocess.check_output(cmd, shell=True).decode('utf-8')
    except subprocess.CalledProcessError as e:
        out_text = e.output.decode('utf-8')
    return out_text


def time_create():
    pday = int(time.strftime('%Y%m%d', time.localtime()))
    phour = time.localtime().tm_hour
    return pday, phour


def put_alert(url, message):
    ptime = time.strftime('%Y-%m-%d %H:%M:%S')
    headers = {'Content-Type': 'application/json;charset=utf-8'}
    botmessage = "------------------------------" + '\n' \
              + "           pika_compact_report"  + '\n' \
              + "------------------------------" + '\n' \
              + "报警: " + message + '\n' \
              + "报警时间: " + ptime + '\n' \
              + "------------------------------"
    try:
        body = {
            "msg_type": "text",
            "content": {
                "text": botmessage
            }
        }
        # print(body)
        requests.post(url, json.dumps(body), headers=headers)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    cmd1 = "du -s /pika | awk '{print $1}'"
    cmd2 = "redis-cli -h 172.28.8.51 -p 9221 compact"
    used = int(cmdout(cmd1).strip())
    ptime = time.strftime('%Y-%m-%d %H:%M:%S')

    if used/936969216 < 0.6:
        cmdout(cmd2)
        print("{} 172.28.8.51 pika compact success".format(ptime))
    else:
        put_alert('https://open.feishu.cn/open-apis/bot/v2/hook/xxxxxx', "pika51 /pika磁盘占用超过百分之六十，自动compact未执行")


# 1 1 * * * /usr/local/bin/pika_compact.py >> /usr/local/bin/pika_compact.log