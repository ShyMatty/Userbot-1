from telethon import events; 
import os; 
import time; 
from userbot.system import register
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import MessageEntityMentionName

@register(pattern=".storm")
async def who(event):
    if event.fwd_from:
        return
    a = 0
    while a < 101: #puoi cambiarlo
        a+=1
        await event.respond("Sei bell*:" + str(a))
        time.sleep(0.2) #puoi cambiarlo
