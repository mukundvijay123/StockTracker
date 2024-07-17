'''
Structure for redis json strings
{objType:ADD/DEL/UPDATE,
ticker: ticker_name
}
'''


import os 
import json
import redis
import utils
import threading
from datetime import datetime,timedelta
from utils import TaskQueue,updateTask,delTask,AddTask,canUpdateorAdd

redisPort=6379

#Engine Logic
addq=TaskQueue()
delq=TaskQueue()
updtq=TaskQueue()

#setting initial timestamps
addq.lastTaskPerform=datetime(2000,1,1,1,1,1)
delq.lastTaskPerform=datetime(2000,1,1,1,1,1)
updtq.lastTaskPerform=datetime(2000,1,1,1,1,1)


#Distributor thread
def distributor(addq:TaskQueue,delq:TaskQueue,updtq:TaskQueue):
    redisClient=redis.Redis("localhost",redisPort)

    while True:
        if(redisClient.llen("InputQueue")>0):
            temp=redisClient.lpop("InputQueue")
            obj=json.loads(temp)
            if(obj["objType"]=="ADD"):
                addq.push(AddTask(obj["ticker"],"PENDING",datetime.now()))
            elif(obj["objType"]=="DEL"):
                delq.push(delTask(obj["ticker"],"PENDING",datetime.now()))
            elif(obj["objType"]=="UPDATE"):
                updtq.push(updateTask(obj["ticker"],"PENDING",datetime.now()))


#Engine function
#canUpdateorAdd() used to avoid being rate limited by yahoo finance.Between any two add or update taskks a buffer time is maintained .The buffer time value is stored in engineUtils which is present within the utils folder.
def engine(addq:TaskQueue,delq:TaskQueue,updtq:TaskQueue):
    
    while True:
        
        if(addq.length>0 and canUpdateorAdd(addq.lastTaskPerform,updtq.lastTaskPerform)):
            temp=addq.pop()
            temp.add()
            addq.lastTaskPerform=datetime.now()
            print(temp)
        
        if(delq.length>0):
            temp=delq.pop()
            temp.remove()
            delq.lastTaskPerform=datetime.now()
            print(temp)

        if(updtq.length>0 and canUpdateorAdd(addq.lastTaskPerform,updtq.lastTaskPerform)):
            temp=updtq.pop()
            temp.update()
            updtq.lastTaskPerform=datetime.now()
            print(temp)

#def dailyUpdates(updtq:TaskQueue):



if __name__=="__main__":
    
    disThread=threading.Thread(target=distributor,args=(addq,delq,updtq))
    disThread.start()
    
    
    EngineThread=threading.Thread(target=engine,args=(addq,delq,updtq))
    EngineThread.start()
    
    disThread.join()
    EngineThread.join()


    




