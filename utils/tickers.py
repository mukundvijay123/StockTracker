import yfinance as yf
import json 
import utils.profileManager as pm
import os



def add_ticker(ticker_symb, forceAdd=False):
    profile_dict = pm.get_profile()
    ticker_path = profile_dict["Tickers"]

    # Create the file if it does not exist
    if not os.path.exists(ticker_path):
        with open(ticker_path, 'w') as ticker_fp:
            json.dump({"tickersList": []}, ticker_fp)
    
    ticker = yf.Ticker(ticker_symb)
    try:
        if  forceAdd or ticker.info:
            with open(ticker_path, "r+") as ticker_fp:
                tickers_dict = json.load(ticker_fp)
                if ticker_symb not in tickers_dict["tickersList"]:
                    tickers_dict["tickersList"].append(ticker_symb)
                    ticker_fp.seek(0)
                    ticker_fp.truncate()
                    json.dump(tickers_dict, ticker_fp)
                    return True
                else:
                    print(f"{ticker_symb} is already in the tickers list.")
                    return True
    except Exception as e:
        print(f"Error adding ticker {ticker_symb}: {e}")
        return False

def delete_ticker(ticker_symb):
    profile_dict = pm.get_profile()
    ticker_path = profile_dict["Tickers"]

    if os.path.exists(ticker_path):
        with open(ticker_path, "r+") as ticker_fp:
            tickers_dict = json.load(ticker_fp)
            if ticker_symb in tickers_dict["tickersList"]:
                tickers_dict["tickersList"].remove(ticker_symb)
                ticker_fp.seek(0)
                ticker_fp.truncate()
                json.dump(tickers_dict, ticker_fp)
                print(f"{ticker_symb} has been removed from the tickers list.")
            else:
                print(f"{ticker_symb} is not in the tickers list.")
    else:
        print(f"Ticker file does not exist at {ticker_path}")

def get_tickers():
    profile_dict = pm.get_profile()
    ticker_path = profile_dict["Tickers"]

    if os.path.exists(ticker_path):
        with open(ticker_path, "r") as ticker_fp:
            tickers_dict = json.load(ticker_fp)
            return tickers_dict.get("tickersList", [])
    else:
        print(f"Ticker file does not exist at {ticker_path}")
        return []
