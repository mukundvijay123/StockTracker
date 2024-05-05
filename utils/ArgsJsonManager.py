import json
import os
from datetime import datetime



DerivedData=r"/home/mukund/data/stocks/data/stockdata"
ExchangeData=r"/home/mukund/data/stocks/data/stockdataSrc"
bufData=r"/home/mukund/data/stocks/data/bufData"
argsJson=r"/home/mukund/data/stocks/args.json"
errorJson=r"/home/mukund/data/stocks/error.json"


def ArgsJsonCreator(DerivedDataPath=DerivedData,ExchangeDataPath=ExchangeData):
    fp=open(argsJson,'w+')
    DetailsDict={}
    DetailsDict['ExchangeData']=ExchangeData
    DetailsDict['DerivedDataPath']=DerivedDataPath
    DetailsDict['bufData']=bufData
    json.dump(DetailsDict,fp)
    fp.close()


def TickerAdder(tickerName):
    fp=open(argsJson,"r+")
    DetailsDict=json.load(fp)
    if 'Tickers' in DetailsDict :
        if tickerName not in DetailsDict['Tickers']:
            DetailsDict['Tickers'].append(tickerName)
        else: 
            #Error codes here
            print("already in tickers list")
    else:
        DetailsDict['Tickers']=[]
        DetailsDict['Tickers'].append(tickerName)
    fp.seek(0)
    fp.truncate()
    json.dump(DetailsDict,fp,indent=4)
    fp.close()




def TickerDelete(tickerName):
    fp=open(argsJson,"r+")
    DetailsDict=json.load(fp)
    if 'Tickers' in DetailsDict :
        if tickerName  in DetailsDict['Tickers']:
            DetailsDict['Tickers'].remove(tickerName)
            fp.seek(0)
            fp.truncate()
            json.dump(DetailsDict,fp,indent=4)
        else:
            #Error codes here
            print("This ticker isnt in your list")
    else:
        DetailsDict['Tickers']=[]

    fp.close()



def checkIntegrity():
    fp=open(argsJson,"r")
    argsDict=json.load(fp)
    fp.close()
    if('ExchangeData' and 'DerivedDataPath' and 'Tickers' and 'bufData' in argsDict):
        return True

    else:
        fp=open(errorJson,"r+")
        ErrorDict=json.load(fp)
        ErrorDict[str(datetime.now())]="args.json integrity not maintained"
        fp.seek(0)
        fp.truncate()
        json.dump(ErrorDict,fp,indent=4)

        return False


def getArgs():
    fp=fp=open(argsJson,"r")
    argsDict=json.load(fp)
    fp.close()
    return argsDict





