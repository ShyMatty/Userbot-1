"""Remove.BG Plugin
Syntax: .rmbg https://link.to/image.extension
Syntax: .rmbg as reply to a media"""

import asyncio
import io
import os
import requests

from datetime import datetime
from telethon import events
from userbot import bot
from userbot.system import progress, dev_cmd


@bot.on(dev_cmd("rmbg ?(.*)"))
async def _(event):
    HELP_STR = "**Rispondi `.rmbg` ad un img o insrisci un link e il comando**"
    if event.fwd_from:
        return
    if Var.REM_BG_API_KEY is None:
        await event.edit("**Serve API token da remove.bg per usare questo plugin.**")
        return False
    input_str = event.pattern_match.group(1)
    start = datetime.now()
    message_id = event.message.id
    if event.reply_to_msg_id:
        message_id = event.reply_to_msg_id
        reply_message = await event.get_reply_message()
        # check if media message
        await event.edit("**Scansione pic...**")
        try:
            downloaded_file_name = await bot.download_media(
                reply_message,
                Config.TMP_DOWNLOAD_DIRECTORY
            )
        except Exception as e:
            await event.edit(str(e))
            return
        else:
            await event.edit("Invio a ReMove.BG")
            output_file_name = ReTrieveFile(downloaded_file_name)
            os.remove(downloaded_file_name)
    elif input_str:
        await event.edit("Invio a ReMove.BG")
        output_file_name = ReTrieveURL(input_str)
    else:
        await event.edit(HELP_STR)
        return
    contentType = output_file_name.headers.get("content-type")
    if "image" in contentType:
        with io.BytesIO(output_file_name.content) as remove_bg_image:
            remove_bg_image.name = "BG_less.png"
            await bot.send_file(
                event.chat_id,
                remove_bg_image,
                force_document=True,
                supports_streaming=False,
                allow_cache=False,
                reply_to=message_id
            )
        end = datetime.now()
        ms = (end - start).seconds
        await event.edit("Ho rimosso lo sfondo in {} sec".format(ms))
    else:
        await event.edit("ReMove.BG API returned Errors. \n`{}".format(output_file_name.content.decode("UTF-8")))


# this method will call the API, and return in the appropriate format
# with the name provided.
def ReTrieveFile(input_file_name):
    headers = {
        "X-API-Key": Var.REM_BG_API_KEY,
    }
    files = {
        "image_file": (input_file_name, open(input_file_name, "rb")),
    }
    r = requests.post(
        "https://api.remove.bg/v1.0/removebg",
        headers=headers,
        files=files,
        allow_redirects=True,
        stream=True
    )
    return r


def ReTrieveURL(input_url):
    headers = {
        "X-API-Key": Var.REM_BG_API_KEY,
    }
    data = {
      "image_url": input_url
    }
    r = requests.post(
        "https://api.remove.bg/v1.0/removebg",
        headers=headers,
        data=data,
        allow_redirects=True,
        stream=True
    )
    return r
