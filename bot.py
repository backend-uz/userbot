from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import ApplicationBuilder, ContextTypes, Updater, CommandHandler, CallbackContext
from text_db import * #hello_eng, hello_rus, hello_uzb, storylink_uzb_error, storylink_eng_error, storylink_rus_error
from userbot import handle_story_link
from db import add_user, Session, User
import os, re

session = Session()


def is_storylink(text):
  pattern = r"https://t\.me/\S+/s/\d+"
  if re.match(pattern, text):
      return True
  else:
    return False

async def story_link(update, context):
    bot = context.bot
    chat_id = update.effective_chat.id
    text = update.message.text
    message_id = update.message.message_id
    user = session.query(User).filter_by(chat_id=chat_id).first()
    if is_storylink(text) == True:
        call_userbot = await handle_story_link(text, chat_id)
        
        
    elif is_storylink(text) == False:
        if user.lang == 'uzb':
            await update.message.reply_text(storylink_uzb_error)
        elif user.lang == 'eng':
            await update.message.reply_text(storylink_eng_error)
        elif user.lang == 'rus':
            await update.message.reply_text(storylink_rus_error)


async def story(update, context):
    bot = context.bot
    chat_id = update.effective_chat.id
    message_id = update.message.message_id
    await bot.forward_message(chat_id=1380674728, from_chat_id=chat_id, message_id=message_id)
    # text = update.message.text
    # if '@' in text:
        

async def start(update, context) -> None:
    bot = context.bot
    chat_id = update.effective_chat.id
    firstname = update.effective_chat.first_name
    lastname = update.effective_chat.last_name
    username = update.effective_chat.username
    existing_user = session.query(User).filter_by(chat_id=chat_id).first()
    if existing_user:
        existing_user.lang = "NULL"
        session.commit()
    else:
        add_user(firstname, lastname, username, chat_id)
    btn1 = InlineKeyboardButton(text="🇺🇸 English", callback_data="eng")
    btn2 = InlineKeyboardButton(text="🇺🇿 O'zbekcha", callback_data="uzb")
    btn3 = InlineKeyboardButton(text="🇷🇺 Русский", callback_data="rus")
    text = """Please, select your lanuage using the buttons below!
    
Iltimos Quyidagi tugmala yordamida tilingizni tanlang!

Выберите язык, используя кнопки ниже"""
    keyboard = InlineKeyboardMarkup([[btn1], [btn2], [btn3]])
    await bot.send_message(chat_id, text, reply_markup=keyboard)

async def id_or_username(update, context):
    bot = context.bot
    chat_id = update.message_effective_chat.id
    text = update.message.text
    call = await handle_story_link(text)
    print(call)


async def change_lang(update, context):
    bot = context.bot
    query = update.callback_query
    chat_id = query.message.chat.id
    selected_lang = query.data
    user = session.query(User).filter_by(chat_id=chat_id).first()
    user.lang = selected_lang
    session.commit()
    if user.lang == 'uzb':
        text = hello_uzb
    elif user.lang == 'eng':
        text = hello_eng
    elif user.lang == 'rus':
        text = hello_rus
    await bot.edit_message_text(chat_id=chat_id, message_id=query.message.message_id, text=text)

async def username_id(update, context):
    chat_id = update.effective_chat.id
    msg = update.message.text
    call_userbot = handle_story_link(msg)
    print(call_userbot)
    