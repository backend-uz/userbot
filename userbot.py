from pyrogram import filters, Client, enums, errors
from pyrogram.types import Story, Message
import re, json, os, shutil, random
from time import sleep

log = Client("log", api_id='2703583', api_hash='2d4d9b6687e180b29daafe9b6d473fff')


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
  sleep(5)
  shutil.rmtree(f'./{waiter}')
  
  
  #---text for sending user
  # info_text =f"🕗 **Joylangan vaqt:** {posted_time}\n🗑 **Tugash vaqti:** {expired_time}\n✍️ **Tahrir:** {edited}\n📝 **Izoh:** {caption} "
  # rndm = generatded_random()
  # if '.VIDEO' in str(story_type):
  #   await message.story.download(f'./{user_id}/StoryNinja_bot-{rndm}.mp4')
  # elif '.PHOTO' in str(story_type):
  #   await message.story.download(f'./{user_id}/StoryNinja_bot-{rndm}.jpg')
  # for f in os.listdir(f'./{user_id}'):
  #   await message.reply_document(os.path.join(f'./{user_id}', f), caption=info_text, parse_mode=enums.ParseMode.MARKDOWN, quote=True)
  # shutil.rmtree(f'./{user_id}')
    
    
    
# link bilan yuklash
@log.on_message(filters.text & filters.private & ~filters.chat(1380674728) & ~filters.reply)
async def story_link_handler(client:Client, message:Message):
  txt = message.text.split('-')
  waiter = txt[0]
  target = txt[1]
  print(target)
  match = re.match(r'https://t\.me/(\S+?)/s/(\d+)', target)
  username = match.group(1)
  story_id = match.group(2)
  stories = await client.get_stories(username, [int(story_id)])
  if stories == []:
    return {"link_error"}
  else:
    for story in stories:
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

      sleep(5)
      shutil.rmtree(f'{waiter}')

# @log.on_message(filters.chat(6721412346) & filters.text)
# async def check_username_exists(client:Client, message:Message):
#     async for story in client.get_chat_stories(id):
#           media_type = story.media.value
#           posted_time = story.date
#           expired_time = story.expire_date
#           edited = story.edited
#           caption = story.caption
#           posted_time = str(posted_time).replace("-", ".").replace(" ", " - ")[:-3]
#           expired_time = str(expired_time).replace("-", ".").replace(" ", " - ")[:-3]
#           if media_type == 'video':
#             rndm = generatded_random()
#             file_path = await story.download(f'./{chat_id}/StoryNinja_bot-{rndm}.mp4')
  
  
# async def forbot(chat_id, id):
  

async def onlydash(_, __, text):
  if '-' in text:
    return True
  else:
    return False

my_filter = filters.create(onlydash)

#---with user ID or username
@log.on_message(my_filter, ~filters.chat(1380674728) & filters.chat(6721412346) & filters.text)
async def check_username_exists(client:Client, message:Message):
    txt = message.text.split('-')
    waiter = txt[0]
    target = txt[1]

    try:
        async for story in client.get_chat_stories(target):
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
        shutil.rmtree(f'./{waiter}')
          
    except errors.UsernameInvalid:
      print('username xato')
    except errors.UsernameNotOccupied:
      print('username xato')
    except errors.PeerIdInvalid:
      print('id xato')