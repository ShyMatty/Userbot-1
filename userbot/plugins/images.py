"""Download & Upload Images on Telegram\n
Syntax: `.img <Name>` or `.img (replied message)`
"""

from userbot.googol_images import googleimagesdownload
import os
import shutil
from re import findall
from userbot import ALIVE_NAME, bot
from userbot.system import dev_cmd

@bot.on(dev_cmd(pattern="img ?(.*)"))
async def img_sampler(event):
    await event.edit("**Processing...**")
    reply = await event.get_reply_message()
    if event.pattern_match.group(1):
        query = event.pattern_match.group(1)
    elif reply:
        query = reply.message
    else:
    	await event.edit(f"**Inserisci un testo da ricercare come img.**")
    	return
        
    lim = findall(r"lim=\d+", query)
    # lim = event.pattern_match.group(1)
    try:
        lim = lim[0]
        lim = lim.replace("lim=", "")
        query = query.replace("lim=" + lim[0], "")
    except IndexError:
        lim = 4
    response = googleimagesdownload()

    # creating list of arguments
    arguments = {
        "keywords": query,
        "limit": lim,
        "format": "jpg",
        "no_directory": "no_directory"
    }

    # passing the arguments to the function
    paths = response.download(arguments)
    lst = paths[0][query]
    await event.client.send_file(await event.client.get_input_entity(event.chat_id), lst)
    shutil.rmtree(os.path.dirname(os.path.abspath(lst[0])))
    await event.delete()
