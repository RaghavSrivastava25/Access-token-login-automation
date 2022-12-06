#!/usr/bin/env python
# coding: utf-8

# In[1]:


import csv
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
import os

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

creds = ServiceAccountCredentials.from_json_keyfile_name(
    r'C:\Users\User\Downloads\csv-gsheet-370805-00981fb846fd.json', scope)

client = gspread.authorize(creds)

with open(r'C:\Users\User\Desktop\MySpreadsheet - Sheet1.csv') as csvfile:
    reader = csv.reader(csvfile)
    sheet = client.create('https://docs.google.com/spreadsheets/d/1o1Fe7pfvNlS_cqLtRFjfkzwBBQgcdZkMfNvVAU-MH30/edit?usp=sharing')
    worksheet = sheet.get_worksheet(0)
    for row in reader:
        worksheet.append_rows([row])      


# In[2]:


import pandas as pd
df = pd.read_csv(r'C:\Users\User\Desktop\MySpreadsheet - Sheet1.csv')


# In[3]:


df


# In[4]:


sheets_service = build('sheets', 'v4', credentials=creds)
with open(r'C:\Users\User\Desktop\MySpreadsheet - Sheet1.csv') as csvfile:
    data = list(csv.reader(csvfile))

body = {'values': data}

os.environ['SPREADSHEET_ID'] = '1o1Fe7pfvNlS_cqLtRFjfkzwBBQgcdZkMfNvVAU-MH30'

spreadsheet_id = os.environ['SPREADSHEET_ID']

result = sheets_service.spreadsheets().values().update(
    spreadsheetId=spreadsheet_id,
    range='A1',
    valueInputOption='RAW',
    body=body
).execute()


# In[ ]:




