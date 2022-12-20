#!/usr/bin/env python
# coding: utf-8

# In[3]:


from telethon.sync import TelegramClient
from telethon.sessions.memory import MemorySession

api_id = 'XXXXX'
api_hash = 'XXXXX'
# Create the MemorySession
session = MemorySession()

# Create the TelegramClient
client = TelegramClient(session, api_id, api_hash)

# Start the client
await client.start()

# Get the user's ID
user_id = 'XXXXX'

# Send the user a message
await client.send_message(user_id, 'Error!')


# In[ ]:




