import pandas as pd
import os
from utils import profileManager as pm



# 10DMA 50DMA crossover rule
'''
Given a dataframe this finds the dates a crossover has happened.
df is the dataframe containing the dates ,closing price,50DMA ,10DMA values
retCol is  the colum values to return in the list
dmaCols is a list with 2 columns and the crossover will return values of those dates in a list where dmaCols[0] crosses dmaCols[1]
'''

def isCrossOver(df:pd.DataFrame,dmaCols=["10DMA","50DMA"],retCol="Date"):
    if(len(dmaCols)!=2):
        raise Exception
    #temp1 an temp2 are bad variable names
    temp1=dmaCols[0]
    temp2=dmaCols[1]
    difference=df[temp2]-df[temp1]
    df["diff"]=difference
    df=df[[retCol,"diff"]].copy()
    cross_above = df[(df['diff'] > 0) & (df['diff'].shift(1) <= 0)]
    return list(cross_above[retCol])
    


def crossOverFilter(ticker,daysFromEnd=-7):
    profile_dict=pm.get_profile()
    derived_file_path=os.path.join(profile_dict["DerivedData"],f"{ticker[:-3]}.csv")
    if not  os.path.exists(derived_file_path):
        raise Exception("derived data file doesnt exist for given ticker ")
    
    derivedDf=pd.read_csv(derived_file_path)
    crossoverDates= isCrossOver(derivedDf[daysFromEnd:].copy())
    return crossoverDates




#Add more rules here
