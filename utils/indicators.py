import pandas as pd

def dma(stockDataframe,length,index):
    if(index>=length-1):
        SumPrice=float(0)
        for i in range(index -length,index):
           
            SumPrice=SumPrice+float(stockDataframe['Close'][i+1])
        
        return SumPrice/length
    else:
        return float(0)

def dmaCalc(stockDataframe,length):
    return stockDataframe.apply(lambda row : dma(stockDataframe,length,row.name),axis=1)
