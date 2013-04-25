# -*- coding:gbk -*-
# auther : pdm
# email : ppppdm@gmail.com
import threading

task_lock = threading.Lock()


class taskUnit():
    def __init__(self, mac, args):
        self.mac = mac
        self.args = args
    
    def printUnit(self):
        print('mac :', self.mac)
        print('args:', self.args)

myTaskList = list()


def insertTaskList(tasks):
    task_lock.acquire()
    myTaskList.extend(tasks)
    task_lock.release()

def insertOneTask(task):
    task_lock.acquire()
    myTaskList.append(task)
    task_lock.release()

def getTask(mac):
    t = None
    task_lock.acquire()
    for i in range(len(myTaskList)):
        task = myTaskList[i]
        if task.mac == mac:
            t = myTaskList.pop(i)
            break
    task_lock.release()
    return t


# for test
if __name__=='__main__':
    a = taskUnit('123', {'x':1, 'y':2})
    b = taskUnit('123', {'x':3, 'y':4})
    c = taskUnit('456', {'x':2, 'y':5})
    
    insertTaskList((a, b, c))
    
    for i in myTaskList:
        i.printUnit()
    
    print()
    
    getTask('123').printUnit()
    getTask('456').printUnit()
    getTask('456').printUnit() 
