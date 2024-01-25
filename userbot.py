from pyrogram import filters, Client, enums, errors
from pyrogram.types import Story, Message
import re, json, os, shutil, random
from time import sleep

log = Client("log", api_id='28864563', api_hash='279e21383d2073b78c9428200f5d067a')


# medianing nomiga qo'shiladigan random 4 xonali beliglar.
# Saqlab olishda muammo bo'lmasligi uchun ishlatiladi
def generatded_random():
  characters = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz123456789"
  randomed = ""
  for _ in range(3):
    randomed += random.choice(characters)
  return randomed


# forward qilingan storyni yuklash
@log.on_message(filters.private & filters.reply)
async def forwarded_stories(client, message):
  waiter = message.text
  story_message_id = message.reply_to_message.id
  handle_story = await client.get_messages(6721412346, story_message_id)
  
  story = handle_story.story
  if story.media:
    owner_fname = story.from_user.first_name
    media_type = story.media.value
    posted_time = story.date
    expired_time = story.expire_date
    edited = story.edited
    caption = story.caption
    posted_time = str(posted_time).replace("-", ".").replace(" ", " - ")[:-3]
    expired_time = str(expired_time).replace("-", ".").replace(" ", " - ")[:-3]
    if media_type == 'video':
      rndm = generatded_random()
      file_path = await story.download(f'./{waiter}/StoryNinja_bot-{rndm}.mp4')
      await message.reply_document(file_path, caption=f"{owner_fname}\n{posted_time}\n{expired_time}\n{edited}\n{caption}")
      
    elif media_type == 'photo':
      rndm = generatded_random()
      file_path = await story.download(f'./{waiter}/StoryNinja_bot-{rndm}.jpg')
      await message.reply_document(file_path, caption=f"{owner_fname}\n{posted_time}\n{expired_time}\n{edited}\n{caption}")
    else:
      await message.reply_text('tg_error')
  sleep(5)
  shutil.rmtree(f'./{waiter}')
    
# link bilan yuklash
@log.on_message(filters.text & filters.private & ~filters.chat(6868556623) & ~filters.reply)
async def story_link_handler(client:Client, message:Message):
  txt = message.text.split('-')
  waiter = txt[0]
  target = txt[1]
  match = re.match(r'https://t\.me/(\S+?)/s/(\d+)', target)
  username = match.group(1)
  story_id = match.group(2)
  stories = await client.get_stories(username, [int(story_id)])
  if stories == []:
    await message.reply_text('link_error')
  else:
    for story in stories:
      if story.media:
        owner_fname = story.from_user.first_name
        media_type = story.media.value
        posted_time = story.date
        expired_time = story.expire_date
        edited = story.edited
        caption = story.caption
        posted_time = str(posted_time).replace("-", ".").replace(" ", " - ")[:-3]
        expired_time = str(expired_time).replace("-", ".").replace(" ", " - ")[:-3]
        rndm = generatded_random()
        if media_type == 'video':
          rndm = generatded_random()
          file_path = await story.download(f'./{waiter}/StoryNinja_bot-{rndm}.mp4')
          await message.reply_document(file_path, caption=f"{owner_fname}\n{posted_time}\n{expired_time}\n{edited}\n{caption}")
          
        elif media_type == 'photo':
          rndm = generatded_random()
          file_path = await story.download(f'./{waiter}/StoryNinja_bot-{rndm}.jpg')
          await message.reply_document(file_path, caption=f"{owner_fname}\n{posted_time}\n{expired_time}\n{edited}\n{caption}")
      else:
        await message.reply_text('tg_error')
      sleep(5)
      shutil.rmtree(f'{waiter}')


async def onlydash(_, __, text):
  if '-' in text:
    return True
  else:
    return False
my_filter = filters.create(onlydash)

#---with user ID or username
@log.on_message(my_filter, ~filters.chat(6868556623) & filters.chat(6721412346) & filters.text)
async def check_username_exists(client:Client, message:Message):
    txt = message.text.split('-')
    waiter = txt[0]
    target = txt[1]
    # error_tg = 0
    try:
        async for story in client.get_chat_stories(target):
          if story.media:
            media_type = story.media.value
            owner_fname = story.from_user.first_name
            posted_time = story.date
            expired_time = story.expire_date
            edited = story.edited
            caption = story.caption
            posted_time = str(posted_time).replace("-", ".").replace(" ", " - ")[:-3]
            expired_time = str(expired_time).replace("-", ".").replace(" ", " - ")[:-3]
            if media_type == 'video':
              rndm = generatded_random()
              file_path = await story.download(f'./{waiter}/StoryNinja_bot-{rndm}.mp4')
              await message.reply_document(file_path, caption=f"{owner_fname}\n{posted_time}\n{expired_time}\n{edited}\n{caption}")
              
            elif media_type == 'photo':
              rndm = generatded_random()
              file_path = await story.download(f'./{waiter}/StoryNinja_bot-{rndm}.jpg')
              await message.reply_document(file_path, caption=f"{owner_fname}\n{posted_time}\n{expired_time}\n{edited}\n{caption}")
          else:
            continue
          #   await message.reply_text('tg_error')
        shutil.rmtree(f'./{waiter}')
          
    except errors.UsernameInvalid:
      print('username xato')
    except errors.UsernameNotOccupied:
      print('username xato')
    except errors.PeerIdInvalid:
      print('id xato')
    