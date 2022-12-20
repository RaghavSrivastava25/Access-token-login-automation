#!/usr/bin/env python
# coding: utf-8

# In[1]:


pip install selenium


# In[2]:


pip install urllib3


# In[3]:


pip install pyotp


# In[4]:


import pyotp
totp = pyotp.TOTP('W3HMHYHFJ4AXXIHRTOHHAJXZJPJARON6')
token = totp.now()


# In[5]:


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
import urllib.parse as urlparse
from selenium.webdriver.chrome.options import Options

class ZerodhaAccessToken:
    def __init__(self):
        self.apiKey = 'XXXXX'
        self.apiSecret = 'XXXXX'
        self.accountUserName ='XXXXX'
        self.accountPassword = 'XXXXX'
        self.securityPin = 'XXXXX'

    def getaccesstoken(self):
        try:
            login_url = "https://kite.trade/connect/login?v=3&api_key={apiKey}".format(apiKey=self.apiKey)

            chrome_driver_path = "chrome_driver_path\\your_machine\\chromedriver.exe"
            options = Options()
           
            driver = webdriver.Chrome(chrome_driver_path, chrome_options=options)

           
            driver.get(login_url)

           
            wait = WebDriverWait(driver, 30)

            
            wait.until(EC.presence_of_element_located((By.XPATH, '//input[@type="text"]')))                .send_keys(self.accountUserName)

           
            wait.until(EC.presence_of_element_located((By.XPATH, '//input[@type="password"]')))                .send_keys(self.accountPassword)

           
            wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@type="submit"]')))                .submit()

            
            wait.until(EC.presence_of_element_located((By.XPATH, '//input[@type="password"]'))).click()
            time.sleep(5)
            driver.find_element_by_xpath('//input[@type="password"]').send_keys(self.securityPin)
            driver.find_element_by_xpath('//input[@type="password"]').send_keys(token)
            driver.find_element_by_xpath("//button[@type = 'submit']").click()
            

          
            wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@type="submit"]'))).submit()


        
            wait.until(EC.url_contains('status=success'))

           
            tokenurl = driver.current_url
            parsed = urlparse.urlparse(tokenurl)
            driver.close()
            return urlparse.parse_qs(parsed.query)['request_token'][0]
        except Exception as ex:
            print(ex)



_ztoken = ZerodhaAccessToken()
actual_token = _ztoken.getaccesstoken()
print(actual_token)

