#!/usr/bin/env python
# coding: utf-8

# In[3]:


from telethon.sync import TelegramClient
from telethon.sessions.memory import MemorySession

api_id = 22740769
api_hash = 'f15137d044ff341e187c61195d915796'
# Create the MemorySession
session = MemorySession()

# Create the TelegramClient
client = TelegramClient(session, api_id, api_hash)

# Start the client
await client.start()

# Get the user's ID
user_id = 5782610197

# Send the user a message
await client.send_message(user_id, 'Error!')


# In[ ]:




