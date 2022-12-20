#!/usr/bin/env python
# coding: utf-8

# In[10]:


""" Regular Library"""
import pandas as pd
from datetime import datetime, date, timedelta
import datetime as dt
from time import sleep
from pathlib import Path
import os
import sys
# import re
# import requests
""" Selenium related Library"""
from selenium import webdriver
from getpass import getpass
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
import logging
""" Stop showing selenium related warnings and Suggestions"""
import urllib.parse as urlparse
from selenium.webdriver.remote.remote_connection import LOGGER
LOGGER.setLevel(logging.WARNING)
""" Download Chrome Driver every time library or mudules"""
import undetected_chromedriver as uc
from webdriver_manager.chrome import ChromeDriverManager
""" Scheduling Time for sending Image on Telegram"""
import schedule
import time
""" For Negleting Warnings during connecting Webdrive"""
import warnings
""" Kite Zerodha Developer Library"""
from kiteconnect import KiteConnect
""" Kite TOTP getting library"""
import pyotp
""" Telegram bot Library"""
#import telepot
""" Image Genrating Library Pilow"""
from PIL import ImageFont, ImageDraw, Image
""" WebSocket Library"""
from kiteconnect import KiteTicker
""" Threading use for Multitasking"""
import threading
import multiprocessing
import requests
from urllib.parse import urljoin
import json
#from XTSConnect.Connect import XTSConnect


# In[9]:


pip install XTSConnect


# In[ ]:


import selenium
selenium.__version__


# In[11]:


### Credentials of zerodha historial
# shikha tanwar 
zerodha_api_key = "XXXXX"
zerodha_api_secrets = "XXXXX"
zerodha_user_id = "XXXXX"
zerodha_password = "XXXXX"
zerodha_totp_key = "XXXXX"
zerodha_pin = "XXXXX"

path=Path(r'C:\B120_orders\zerodha')
#exit_file_path = Path(r"C:\B120_orders\Helper\logfile")


# In[14]:


"""  These three lines of code for Hide Warning messages,
        Which is showes by Request method and kite  """
logging.getLogger("urllib3").setLevel(logging.WARNING)             # Hide Request related warnings
logging.getLogger("urllib3").propagate = False                     # Hide Request related warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)     # Hide Kite related warnings

kite = KiteConnect(api_key=zerodha_api_key)

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    driver = webdriver.Chrome(ChromeDriverManager().install())
    # driver = webdriver.Chrome(Webdriver_chrome)
    url = kite.login_url()
    driver.get(url)
    #print("login Url: ", url)

    # Login Into Zerodha Account
    user_id = WebDriverWait(driver, 5).until(lambda x: x.find_element("xpath", "//*[@id='userid']")).send_keys(zerodha_user_id)
    password = WebDriverWait(driver, 5).until(lambda x: x.find_element("xpath", "//*[@id='password']")).send_keys(zerodha_password)
    submit = WebDriverWait(driver, 5).until(lambda x: x.find_element("xpath", "//*[@id='container']/div/div/div/form/div[4]/button")).submit()
    auth_key = pyotp.TOTP(zerodha_totp_key)
    #print(auth_key.now())
    totp = WebDriverWait(driver, 5).until(lambda x: x.find_element("xpath", "//*[@label='External TOTP']")).send_keys(auth_key.now())
    #pin = WebDriverWait(driver, 5).until(lambda x: x.find_element_by_xpath("//*[@id='pin']")).send_keys(zerodha_pin)
    submit_btn = WebDriverWait(driver, 5).until(lambda x: x.find_element("xpath", "//*[@id='container']/div/div/div[2]/form/div[3]/button")).submit()

    # Request Token 
    sleep(2)
    Current_url = driver.current_url
    driver.close()
    #print(Current_url)
    initial_token = Current_url.split('request_token=')[1]
    request_token = initial_token.split('&')[0]
    #print("request_token: ", request_token)

    # Access Token 
    data = kite.generate_session(request_token, api_secret=zerodha_api_secrets)
    kite.set_access_token(data["access_token"])
    acc_tkn = data['access_token']
    df=pd.DataFrame()
    df['access_token']=[acc_tkn]
    df.to_csv(path/'zerodha_access_token.csv',index=False)
    
    print("Access Tocken Recived")

    """ Data Fetching and Filtering Code Starts From Here, 
        Where we are fetching NFO instruments data through Kite API and, 
        after fetching data Filtering Instruments Data, That is starting from the "filtering" Varibale"""
    #len_instrumnets = len(instrument)
    try:
        fu_instruments = kite.instruments(exchange="NFO")
    except:
        sleep(15)
        fu_instruments = kite.instruments(exchange="NFO")

    """ Option and Future Token having Instrument file Dataframe"""
    Dataset = pd.DataFrame.from_dict(fu_instruments) 
    
    Dataset.to_csv(path/'instruments_file.csv',index=False)
    print("Instrument File Done")
   


# In[ ]:





# In[15]:


access_token=(pd.read_csv(r"C:\B120_orders\zerodha\zerodha_access_token.csv"))['access_token'].iloc[0]


# In[ ]:


kite = KiteConnect(api_key='XXXXX') 
kite.set_access_token(access_token)
print("Kite Connection Established")


# In[ ]:


def myround(x, base):
    return base * round(x/base)

# NIfty 50 & Bank NIfty Current Time According PRICE and making ATM Strike 
Nifty50_atm_strike = myround((kite.ltp(['NSE:NIFTY 50']))['NSE:NIFTY 50']['last_price'], 50)
BANKNIFTY_atm_strike = myround(kite.ltp(['NSE:NIFTY BANK'])['NSE:NIFTY BANK']['last_price'], 100)

# Nifty 50 -  5 Strike (Instrument Token) List for CE & PE
nifty_above_50 = instrument_file[(instrument_file.exchange == "NFO") & (instrument_file.name == "NIFTY") & (instrument_file.strike >= Nifty50_atm_strike)].sort_values('strike', ascending=True)
nifty_min_expiry = nifty_above_50.expiry.min()
nifty_above_50 = nifty_above_50[nifty_above_50.expiry == nifty_min_expiry].head(52)
nifty_above_50_CE_PE_token = list(nifty_above_50["instrument_token"])
nifty_above_50_trading_symbol_list = list(nifty_above_50["tradingsymbol"])

nifty_below_50 = instrument_file[(instrument_file.exchange == "NFO") & (instrument_file.name == "NIFTY") & (instrument_file.strike < Nifty50_atm_strike)].sort_values('strike', ascending=False)
nifty_below_50 = nifty_below_50[nifty_below_50.expiry == nifty_min_expiry].head(48)
nifty_below_50_CE_PE_token = list(nifty_below_50["instrument_token"])
nifty_below_50_trading_symbol_list = list(nifty_below_50["tradingsymbol"])

# Bank Nifty - 5 Strike (Instrument Token) List for CE & PE
banknifty_above_50 = instrument_file[(instrument_file.exchange == "NFO") & (instrument_file.name == "BANKNIFTY") & (instrument_file.strike >= BANKNIFTY_atm_strike)].sort_values('strike', ascending=True)
banknifty_min_expiry = banknifty_above_50.expiry.min()
banknifty_above_50 = banknifty_above_50[banknifty_above_50.expiry == banknifty_min_expiry].head(52)
banknifty_above_50_CE_PE_token = list(banknifty_above_50["instrument_token"])
banknifty_above_50_trading_symbol_list = list(banknifty_above_50["tradingsymbol"])

banknifty_below_50 = instrument_file[(instrument_file.exchange == "NFO") & (instrument_file.name == "BANKNIFTY") & (instrument_file.strike < BANKNIFTY_atm_strike)].sort_values('strike', ascending=False)
banknifty_below_50 = banknifty_below_50[banknifty_below_50.expiry == banknifty_min_expiry].head(48)
banknifty_below_50_CE_PE_token = list(banknifty_below_50["instrument_token"])
banknifty_below_50_trading_symbol_list = list(banknifty_below_50["tradingsymbol"])


# All trading Symbol List (Banknifty and nifty)
trading_symbols = (nifty_above_50_trading_symbol_list + nifty_below_50_trading_symbol_list + banknifty_above_50_trading_symbol_list+ banknifty_below_50_trading_symbol_list)


# In[ ]:


kws = KiteTicker('XXXXX', access_token)

# All Tokens list (Banknifty and nifty)
tokens = (nifty_above_50_CE_PE_token + nifty_below_50_CE_PE_token + banknifty_above_50_CE_PE_token + banknifty_below_50_CE_PE_token)

def on_ticks(ws, ticks):
    logging.debug("Ticks: {}".format(ticks))
        
def on_connect(ws, response):
    ws.subscribe(tokens)    
    ws.set_mode(ws.MODE_FULL, tokens)
        
kws.on_ticks = on_ticks
kws.on_connect = on_connect
kws.connect(threaded=True)

while True:
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    if current_time <= "17:20:00":
        def on_ticks(ws, ticks):
            feed_data(ticks)
            
        def feed_data(ticks):
            mergefile = []
            for i in ticks:
                df = pd.DataFrame()
                instrument_data = instrument_file[instrument_file.instrument_token == i['instrument_token']]
                df['Instrument'] = [instrument_data['name'].iloc[0]]
                df['Tadingsymbol'] = [instrument_data['tradingsymbol'].iloc[0]]
                df['Exchange_token'] = [instrument_data['exchange_token'].iloc[0]]
                df['Instrument_token'] = [i['instrument_token']]
                df['Strike'] = [int(instrument_data['strike'].iloc[0])]
                df['Option_type'] = [instrument_data['instrument_type'].iloc[0]]
                ltp = i['last_price']
                
                current_time = datetime.strptime(datetime.now().strftime("%H:%M:%S"), '%H:%M:%S').time()
                df['Time']=[current_time]
                df['ltp'] = [ltp]
                mergefile.append(df)
            dataset = pd.concat(mergefile)
            dataset.to_csv(BN_live_data_path, index=False, header=True)
            time.sleep(1)
        kws.on_ticks=on_ticks
    else:
        break
    


# In[ ]:





# In[ ]:




