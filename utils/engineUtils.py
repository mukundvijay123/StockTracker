import utils
import queue as q
from datetime import datetime

tasksTypes = ["ADD", "DEL", "UPDATE"]
statusTypes = ["PENDING", "ERROR", "COMPLETED"]



class AddTask:
    def __init__(self,ticker,status,time,force=False):
        self.task="ADD"
        self.ticker=ticker
        self.status=status
        self.time=time
        self.force=force

    def add(self):
        try:
            if(utils.add_ticker(self.ticker)):
                utils.makeData(self.ticker)
                utils.UpdateDfDma(self.ticker,"Close",[50,10])
                print("Ticker added succesfully")
        except:
            print("Error while adding ticker")
             #put in error queue
    
    def __str__(self):
        print(f"task:{self.task}")
        print(f"ticker:{self.ticker}")
        print(f"status:{self.status}")
        print(f"timeOfOrigin:{self.time}")
        print(f"force:{self.force}")

        return ""


class delTask:
    def __init__(self,ticker,status,time):
        self.task="DEL"
        self.ticker=ticker
        self.status=status
        self.time=time

    def remove(self):
        try:
            utils.delete_ticker(self.ticker)
            utils.deleteData(self.ticker)
            print(f"{self.ticker} deleted from list of tickers")
        except:
            print(f"error while deleting{self.ticker}")
            # add to the error queue

    def __str__(self):
        print(f"task:{self.task}")
        print(f"ticker:{self.ticker}")
        print(f"status:{self.status}")
        print(f"timeOfOrigin:{self.time}")
        return ""


class updateTask:
    def __init__(self,ticker,status,time):
        self.task="UPDATE"
        self.ticker=ticker
        self.status=status
        self.time=time

    def update (self):
        try:
            utils.UpdateData(self.ticker)
            utils.UpdateDerived(self.ticker)
            utils.UpdateDfDma(self.ticker,"Close",[50,10])
            print(f"{self.ticker}  updated successfully")
        except Exception as e:
            print(e)
            print(f" error while updating {self.ticker}")
            #add to error queue

    def __str__(self):
        print(f"task:{self.task}")
        print(f"ticker:{self.ticker}")
        print(f"status:{self.status}")
        print(f"timeOfOrigin:{self.time}")
        return ""


class TaskQueue:
    def __init__(self):
        self.queue=[]
        self.length=0
        self.lastTaskPerform=None
    

    def push(self,task):
        self.length+=1
        self.queue.append(task)
    
    def pop(self):
        if(self.length>=0):
            self.length-=1
            return self.queue.pop(0)

    def readTop(self):
        if self.length >=0:
            return self.queue[0] 
        
    

def canUpdateorAdd(lastAdd:datetime,lastUpdaate:datetime):
    lastApiRequest=lastAdd if lastAdd>lastUpdaate else lastUpdaate
    if((datetime.now()-lastApiRequest).total_seconds()>120):
        return True
    else:
        return False

