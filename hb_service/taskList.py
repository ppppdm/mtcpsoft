# -*- coding:gbk -*-
# auther : pdm
# email : ppppdm@gmail.com
import threading

task_lock = threading.Lock()


class taskUnit():
    def __init__(self, mac, args):
        self.mac = mac
        self.args = args

myTaskList = list()


def insertTask(tasks):
    task_lock.acquire()
    myTaskList.extend(tasks)
    task_lock.release()

def getTask(mac):
    t = None
    task_lock.acquire()
    for i in myTaskList:
        if i.mac == mac:
            t = i
            break
    task_lock.release()
    return t
