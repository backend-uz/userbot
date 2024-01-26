from pyrogram import filters, Client, enums, errors
from pyrogram import enums
from pyrogram.types import Story, InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from text_db import *
from db import add_user, Session, User
import os, re

session = Session()

api_id = 28864563
api_hash = "279e21383d2073b78c9428200f5d067a"
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


@bot.on_message(filters.private & filters.chat(6868556623) & filters.text)
async def error_handler(client: Client, message:Message):
    waiter = message.reply_to_message.text.split('-')[0]
    text = message.text
    user = session.query(User).filter_by(chat_id=waiter).first()

    if text == 'tg_error':
        if user.lang == 'uzb':
            await client.send_message(chat_id=waiter, text="Telegram xatoligi sabab yuklashning imkoni bo'lmadi 😞")
        if user.lang == 'eng':
            await client.send_message(chat_id=waiter, text="Failed to upload due to Telegram error 😞")
        if user.lang == 'rus':
            await client.send_message(chat_id=waiter, text="Не удалось загрузить из-за ошибки Telegram 😞")

    elif text == 'link_error':
        if user.lang == 'uzb':
            await client.send_message(chat_id=waiter, text="Siz yuborgan link xato 😕")
        if user.lang == 'eng':
            await client.send_message(chat_id=waiter, text="The link you sent is wrong 😕")
        if user.lang == 'rus':
            await client.send_message(chat_id=waiter, text="Ссылка, которую вы отправили, неверная 😕")


@bot.on_message(filters.chat(6868556623) & filters.private)
async def incoming_media_handle(client:Client, message:Message):
    msg_id = message.id
    caption = message.caption
    replied = message.reply_to_message.text
    waiter = replied.split('-')[0]
    split_caption = caption.split('\n')
    owner = split_caption[0]
    post = split_caption[1]
    exp = split_caption[2]
    edit = str(split_caption[3])
    capt = str(split_caption[4])
    
    user = session.query(User).filter_by(chat_id=waiter).first()
    if user.lang == 'uzb':
        if capt == 'None':
            capt = 'Izoh mavjud emas'
        if edit == 'False':
            edit = 'tahrirlanmagan'
        text = f"**Ismi:** {owner}\n**🕗 Joylangan vaqt:** {post}\n**🗑 O'chish vaqti:** {exp}\n**✍️ Tahrir:** {edit}\n**📝 Izoh:** {capt}\n"
    
    if user.lang == 'eng':
        if capt == 'NOne':
            capt = 'Caption is empty'
        if edit == 'False':
            edit = 'Not edited'
        text = f"**Belong to:** {owner}\n**🕗 Posted time:** {post}\n**🗑 Expired time:** {exp}\n**✍️ Edit:** {edit}\n**📝 Caption:** {capt}\n"
        
    if user.lang == 'rus':
        if capt == 'None':
            capt = 'Комментарий пуст'
        if edit == 'False':
            edit = 'не редактировалось'
        text = f"**Имя:** {owner}\n**🕗 Время публикации:** {post}\n**🗑 Время закрытия:** {exp}\n**✍️ Редактировать:** {edit}\n**📝 Комментарий:** {capt}\n"
    
    await client.copy_message(chat_id=waiter, caption=text, from_chat_id=6868556623, message_id=msg_id, parse_mode=enums.ParseMode.MARKDOWN)

    

@bot.on_message(filters.story &filters.private)
async def story_handler(client: Client, message:Message):
    from_id = message.from_user.id
    user = session.query(User).filter_by(chat_id=from_id).first()
    if user.lang == 'uzb':
        await message.reply_text("Iltimos kuting! Yuklanmoqda 📥")
    elif user.lang == 'eng':
        await message.reply_text("Please wait! Downloading 📥")
    elif user.lang == 'rus':
        await message.reply_text("Пожалуйста, подождите! Загрузка 📥")
    newmsg_id = await client.forward_messages(chat_id=6868556623, from_chat_id=from_id, message_ids=message.id)
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
                if user.lang == 'uzb':
                    await message.reply_text("Iltimos kuting! Yuklanmoqda 📥")
                elif user.lang == 'eng':
                    await message.reply_text("Please wait! Downloading 📥")
                elif user.lang == 'rus':
                    await message.reply_text("Пожалуйста, подождите! Загрузка 📥")
                await client.send_message(6868556623, text=f'{chat_id}-{msg}')
                
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
    waiter = message.from_user.id
    msg = message.text
    await client.send_message(chat_id=6868556623, text=f'{waiter}-{msg}')
