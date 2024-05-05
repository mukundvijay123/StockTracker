import pandas as pd
import yfinance as yf
import os
from utils import DfDateCaster
import utils.ArgsJsonManager as args




def FetchAndSave(Ticker,argsDict=args.getArgs()):
    stock = yf.Ticker(Ticker)
    try:
        hist = stock.history(period="12mo")
    except:
        #Write the error scheduler here
        pass
    if hist.empty !=True :
        hist.to_csv(os.path.join(argsDict['bufData'],Ticker[:-3]+".csv"))

    #Casting and resaving dates
    hist=pd.read_csv(os.path.join(argsDict['bufData'],Ticker[:-3]+".csv"))
    hist['Date']=DfDateCaster(hist)
    hist.to_csv(os.path.join(argsDict['ExchangeData'],Ticker[:-3]+".csv"))





def createSupplData(ticker,argsDict=args.getArgs()):
    tempDf=pd.read_csv(os.path.join(argsDict['ExchangeData'],ticker+".csv"))
    DfIndexes=tempDf.columns.values
    if 'Date' and 'Close' in DfIndexes:
        DerivedDf=pd.DataFrame()
        DerivedDf['Date']=tempDf['Date']
        DerivedDf['Close']=tempDf['Close']
        DerivedDf.to_csv(os.path.join(argsDict['DerivedDataPath'],ticker+".csv"))
    else:
        pass


#def updater
