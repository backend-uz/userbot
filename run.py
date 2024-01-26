import asyncio
from pyrogram.handlers import MessageHandler, CallbackQueryHandler
from pyrogram import Client, compose, filters
from pybot import start, id_or_username, button_handler, incoming_media_handle, story_handler, story_link, error_handler
from userbot import check_username_exists, forwarded_stories, story_link_handler
from pyrogram.types import Message
import re

async def main():
    apps = [
        bot := Client("bot"),
        log := Client("log")
    ]

    async def ignoredash(_, __, message:Message):
        if '-' in message.text:
            return False
        else:
            return True
    my_filter = filters.create(ignoredash)
    
    async def onlydash(_, __, message:Message):
        if '-' in message.text and 'https://t.me/' not in message.text:
            return True
        else:
            return False
    my_filter2 = filters.create(onlydash)

    async def is_storylink(_, __, message:Message):
        pattern = r"https://t\.me/[a-zA-Z0-9_]+/s/\d+"
        return re.match(pattern, message.text) 
    my_filter3 = filters.create(is_storylink)
    
    
    async def is_storylink_and_id(_,__, message:Message):
        pattern = r"\d+-https://t\.me/[a-zA-Z0-9_]+/s/\d+"
        return re.match(pattern, message.text)
    my_filter4 = filters.create(is_storylink_and_id)
    
    async def is_id_or_username(_,__, message:Message):
        text = message.text
        if text.isdigit() or text.startswith('@'):
            return True
    my_filter5 = filters.create(is_id_or_username)
        
    bot.add_handler(MessageHandler(start, filters.command("start") & filters.private))
    bot.add_handler(CallbackQueryHandler(button_handler))
    
    bot.add_handler(MessageHandler(id_or_username, (filters.text & my_filter5 & filters.private)))
    bot.add_handler(MessageHandler(story_handler, filters.story & filters.private))
    bot.add_handler(MessageHandler(incoming_media_handle, (~filters.text & filters.chat(6868556623) & filters.private) & (filters.document | filters.photo | filters.video)))
    
    
    log.add_handler(MessageHandler(forwarded_stories, (filters.private & filters.reply & my_filter & filters.text & ~filters.chat(6868556623))))
    log.add_handler(MessageHandler(check_username_exists, (filters.private & filters.text & my_filter2 & ~filters.chat(1380674728) & ~filters.reply)))
    bot.add_handler(MessageHandler(error_handler, filters.chat(6868556623) & filters.private & filters.text))
    bot.add_handler(MessageHandler(story_link, (filters.private & filters.text & my_filter3 & ~filters.chat(6868556623) & ~filters.reply)))
    log.add_handler(MessageHandler(story_link_handler, (filters.private & my_filter4 & filters.text & ~filters.chat(6868556623) & ~filters.reply)))

    await compose(apps)


asyncio.run(main())