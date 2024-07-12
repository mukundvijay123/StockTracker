import pandas as pd 
from datetime import datetime,date

def strToDate(dateString):
    return datetime.strptime(dateString, '%Y-%m-%d %H:%M:%S%z').date()


def DfDateCaster(dataframe,dateCol='Date'):
    return dataframe[dateCol].apply(strToDate)
