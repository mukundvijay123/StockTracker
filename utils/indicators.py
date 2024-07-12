import pandas as pd
from utils import profileManager as pm
import os

#Function for doing small updates
#Column->column to derive dma from
#days-> window for DMA
def calcDma(df,column:str,days:int):
    return df[column].rolling(window=days).mean()


#Change this function to only add dma if dma doenst exit already
#days ->List of rolling window values
def UpdateDfDma(ticker:str,column:str,days:list):
    profile_dict=pm.get_profile()
    derived_file_path=os.path.join(profile_dict["DerivedData"],f"{ticker[:-3]}.csv")
    derived_his= pd.read_csv(derived_file_path)
    for day in days:
        derived_his[str(day)+"DMA"]=calcDma(derived_his,column,day)

    derived_his.to_csv(derived_file_path,index=False)

    
