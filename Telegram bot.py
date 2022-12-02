#!/usr/bin/env python
# coding: utf-8

# In[1]:


pip install telebot


# In[2]:


pip install telethon


# In[3]:


import telebot
from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerUser, InputPeerChannel
from telethon import TelegramClient, sync, events

api_id = '22740769'
api_hash = 'f15137d044ff341e187c61195d915796'
token = 'AAGkN8VQKA1T8TJEZVhiLjF7E1nGPWhTzhs'
message = "Error from the client side....."


phone = '+919818334567'

client = TelegramClient('session', api_id, api_hash)

client.connect()

if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, input('Enter the code: '))


try:
    receiver = InputPeerUser('user_id', 'user_hash')
    client.send_message(receiver, message, parse_mode='html')
except Exception as e:
    print(e);


client.disconnect()

