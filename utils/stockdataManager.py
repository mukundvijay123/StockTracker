import pandas as pd
import yfinance as yf
from utils import profileManager as pm
import os
from datetime import timedelta,datetime
import shutil

class stockData():
    def __init__ (self,success,dataFrame,timePeriod):
        self.success=success
        self.dataFrame=dataFrame
        self.time=timePeriod



#function to create stockdata for the first time
def makeData(ticker,time="1y",exchange=True):
    stock=yf.Ticker(ticker)
    try:
        history=stock.history(period=time)
        if history.empty==True:
            return
        history.reset_index(inplace=True)
        history['Date'] = history['Date'].dt.strftime('%d-%m-%Y')
        profile_dict=pm.get_profile()

        #creating exchange data CSV
        exchange_file_path = os.path.join(profile_dict["ExchangeData"], f"{ticker[:-3]}.csv")

        #creating derived data 
        derived_file_path=os.path.join(profile_dict["DerivedData"],f"{ticker[:-3]}.csv")
        derived_df=history[['Date','Close']]
        
        #Conveting to CSV
        if exchange : history.to_csv(exchange_file_path,index=False) 
        derived_df.to_csv(derived_file_path,index=False)
    except:
        pass # Add to error Queue
        
'''
Currently there is an errror in this function ,if the dataframe is fully updated  and then the update funtion is called then the last row is copied twice.
To fix it if the last date is equal to the first date in the df then dont update.
'''
def UpdateData(ticker,lastUpdate=None):
    profile_dict=pm.get_profile()
    file_path = os.path.join(profile_dict["ExchangeData"], f"{ticker[:-3]}.csv")
    current_his = pd.read_csv(file_path)
    current_his['Date'] = pd.to_datetime(current_his['Date'], format='%d-%m-%Y')


    last_date=current_his.iloc[-1]['Date'].date() #Last date in the data current_his dataFrame
    today_date = datetime.now().date()
    delta_days = (today_date - last_date).days #difference in days
    stock = yf.Ticker(ticker)

    try:
        new_data = stock.history(start=last_date + timedelta(days=1), end=today_date)
    except:
        pass #Add to error queue
    #Currently there is an errror in this function ,if the dataframe is fully updated  and then the update funtion is called then the last row is copied twice.
    new_data.reset_index(inplace=True)
    new_data['Date']=new_data['Date'].dt.strftime('%d-%m-%Y') #converting datatime objects in new_data datframe to strings
    current_his['Date'] = current_his['Date'].dt.strftime('%d-%m-%Y') #converting datatime objects in current_his datframe to strings
    
    updated_his = pd.concat([current_his, new_data], ignore_index=True)#Concatenating both dataframes
    updated_his.to_csv(file_path, index=False)


def UpdateDerived(ticker):
    profile_dict=pm.get_profile()
    exchange_file_path = os.path.join(profile_dict["ExchangeData"], f"{ticker[:-3]}.csv")
    derived_file_path=os.path.join(profile_dict["DerivedData"],f"{ticker[:-3]}.csv")

    current_his = pd.read_csv(exchange_file_path)
    derived_his= pd.read_csv(derived_file_path)

    new_entries = current_his[~current_his["Date"].isin(derived_his.iloc[:, 0])]
    new_entries=new_entries[['Date','Close']]
    updated_derived_his = pd.concat([derived_his, new_entries], ignore_index=True)
    
    updated_derived_his.to_csv(derived_file_path, index=False)


def deleteData(ticker):
    profile_dict =pm.get_profile()
    exchange_file_path = os.path.join(profile_dict["ExchangeData"], f"{ticker[:-3]}.csv")
    derived_file_path=os.path.join(profile_dict["DerivedData"],f"{ticker[:-3]}.csv")

    try:
        if os.path.isfile(exchange_file_path):
            shutil.move(exchange_file_path,profile_dict["TempData"])
        if  os.path.isfile(derived_file_path):
            os.remove(derived_file_path)
    except Exception as e:
        pass




        






