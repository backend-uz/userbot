from pyrogram import filters, Client, enums, errors
from pyrogram import enums
from pyrogram.types import Story, InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
import re, json, os, shutil
from text_db import * #hello_eng, hello_rus, hello_uzb, storylink_uzb_error, storylink_eng_error, storylink_rus_error
from db import add_user, add_task, Session, User, Tasks
import os, re, time

session = Session()

api_id = 2703583
api_hash = "2d4d9b6687e180b29daafe9b6d473fff"
bot_token = "6721412346:AAFtbDjFzEIYQFXKrK0adPASy5abTEXOYyQ"

bot = Client("bot", api_id, api_hash)

@bot.on_message(filters.command("start"))
async def start(client:Client, message:Message):
    chat_id=message.from_user.id
    fname = message.from_user.first_name
    lname = message.from_user.last_name
    username = message.from_user.username
    existing_user = session.query(User).filter_by(chat_id=chat_id).first()
    if existing_user:
        existing_user.lang = "rus"
        session.commit()
    else:
        add_user(fname=fname, lname=lname, chat_id=chat_id, username=username)
        
    buttons = [
        [
            InlineKeyboardButton("🇺🇸 English", callback_data="eng"),
            InlineKeyboardButton("🇺🇿 O'zbekcha", callback_data="uzb"),
            InlineKeyboardButton("🇷🇺 Русский", callback_data="rus"),
        ]
    ]
    text = """Please, select your lanuage using the buttons below!
    
Iltimos Quyidagi tugmala yordamida tilingizni tanlang!

Выберите язык, используя кнопки ниже!"""
    await message.reply(text=text, reply_markup=InlineKeyboardMarkup(buttons))


@bot.on_callback_query()
async def button_handler(client: Client, callback_query):
    chat_id = callback_query.from_user.id
    selected_lang = callback_query.data
    user = session.query(User).filter_by(chat_id=chat_id).first()
    user.lang = selected_lang
    session.commit()
    if selected_lang == 'uzb':
        await client.edit_message_text(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.id,
            text=hello_uzb,
        )
    elif selected_lang == 'eng':
        await client.edit_message_text(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.id,
            text=hello_eng,
        )
    elif selected_lang == 'rus':
        await client.edit_message_text(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.id,
            text=hello_rus,
        )
   
@bot.on_message(filters.chat(1380674728) & filters.private)
async def incoming_media_handle(client:Client, message:Message):
    msg_id = message.id
    caption = message.caption
    replied = message.reply_to_message.text
    waiter = replied.split('-')[0]
    split_caption = caption.split('\n')
    owner = split_caption[0]
    post = split_caption[1]
    exp = split_caption[2]
    capt = str(split_caption[3])
    edit = str(split_caption[4])
    
    user = session.query(User).filter_by(chat_id=waiter).first()
    if user.lang == 'uzb':
        if capt == 'False':
            capt = 'Izoh mavjud emas'
        if edit == 'None':
            edit = 'tahrirlanmagan'
        text = f"**Ismi:** {owner}\n**🕗 Joylangan vaqt:** {post}\n**🗑 O'chish vaqti:** {exp}\n**✍️ Tahrir:** {edit}\n**📝 Izoh:** {capt}\n"
    
    if user.lang == 'eng':
        if capt == 'False':
            capt = 'Caption is empty'
        if edit == 'None':
            edit = 'Not edited'
        text = f"**Belong to:** {owner}\n**🕗 Posted time:** {post}\n**🗑 Expired time:** {exp}\n**✍️ Edit:** {edit}\n**📝 Caption:** {capt}\n"
        
    if user.lang == 'rus':
        if capt == 'False':
            capt = 'Комментарий пуст'
        if edit == 'None':
            edit = 'не редактировалось'
        text = f"**Имя:** {owner}\n**🕗 Время публикации:** {post}\n**🗑 Время закрытия:** {exp}\n**✍️ Редактировать:** {edit}\n**📝 Комментарий:** {capt}\n"
    
    await client.copy_message(chat_id=waiter, caption=text, from_chat_id=1380674728, message_id=msg_id, parse_mode=enums.ParseMode.MARKDOWN)

    

@bot.on_message(filters.story &filters.private)
async def story_handler(client: Client, message:Message):
    from_id = message.from_user.id
    newmsg_id = await client.forward_messages(chat_id=1380674728, from_chat_id=from_id, message_ids=message.id)
    await newmsg_id.reply(text=from_id, quote=True)
    
@bot.on_message(filters.private & filters.text)
async def id_or_username(client, message):
    erroruzb = "Bu foydalanuvchida hikoyalar topilmadi. ☹️"
    errorrus = "У этого пользователя нет истории. ☹️"
    erroreng = "No stories found for this user. ☹️"
    if "@" in message.text or message.text.isdigit():
        chat_id = message.from_user.id
        msg = message.text
        user = session.query(User).filter_by(chat_id=chat_id).first()
        
        try:
            if message.text.isdigit():
                usr = await client.get_users([msg])
            else:
                usr = await client.get_users([msg])

            if usr[0].is_stories_unavailable == False:
                await client.send_message(1380674728, text=f'{chat_id}-{msg}')
        
        except errors.UsernameInvalid:
            if user.lang == 'uzb':
                await message.reply_text(erroruzb)
            elif user.lang == 'eng':
                await message.reply_text(erroreng)
            elif user.lang == 'rus':
                await message.reply_text(errorrus)
                
        except errors.UsernameNotOccupied:
            if user.lang == 'uzb':
                await message.reply_text(erroruzb)
            elif user.lang == 'eng':
                await message.reply_text(erroreng)
            elif user.lang == 'rus':
                await message.reply_text(errorrus)
        except errors.PeerIdInvalid:
            if user.lang == 'uzb':
                await message.reply_text(erroruzb)
            elif user.lang == 'eng':
                await message.reply_text(erroreng)
            elif user.lang == 'rus':
                await message.reply_text(errorrus)
    else:
        if user.lang == 'uzb':
                await message.reply_text(erroruzb)
        elif user.lang == 'eng':
            await message.reply_text(erroreng)
        elif user.lang == 'rus':
            await message.reply_text(errorrus)
    


@bot.on_message(filters.private & filters.text)
async def story_link(client, message):
    chat_id = message.from_user.id
    msg = message.text
    await client.send_message(1380674728, text=f'{chat_id}-{msg}')
    
    # with open('task_id.txt', 'r') as file:
    #     data_id = file.read()
      
    # task = session.query(Tasks).filter_by(id=data_id).first()
    # user = session.query(User).filter_by(chat_id=chat_id).first()
    # if task:
    #     caption = task.caption
    #     post = task.postedtime
    #     exp = task.exptime
    #     edit = task.edit
    #     if user.lang == 'uzb':
    #         if caption == None:
    #             caption = 'Izoh mavjud emas'
    #         if edit == False:
    #             edit = 'tahrirlanmagan'
    #         text = f"**🕗 Joylangan vaqt:** {post}\n**🗑 O'chish vaqti:** {exp}\n**✍️ Tahrir:** {edit}\n**📝 Izoh:** {caption}\n"
    #     elif user.lang == 'eng':
    #         text = f"**🕗 Joylangan vaqt:** {post}\n**🗑 O'chish vaqti:** {exp}\n**✍️ Tahrir:** {edit}\n**📝 Izoh:** {caption}\n"
    #     elif user.lang == 'rus':
    #         text = f"**🕗 Joylangan vaqt:** {post}\n**🗑 O'chish vaqti:** {exp}\n**✍️ Tahrir:** {edit}\n**📝 Izoh:** {caption}\n"
    #     await message.reply_document(document=task.filepath, caption=text, parse_mode=enums.ParseMode.MARKDOWN)
        # time.sleep(5)
        # shutil.rmtree('1472154968')
