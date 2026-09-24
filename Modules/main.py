import os, re, sys, json, pytz, requests, asyncio, logging, subprocess
from pyrogram import Client, filters
from pyrogram.types.messages_and_media import Message
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto, CallbackQuery, ForceReply
import helper
from DbNew import *
from config import *
from Tools.msg import *
from Tools.buttons import *
from Tools.yt_playlist import *
from Commands.welcome import *
from Commands.txt_call import *
from Commands.yt_upl import *
from Commands.OwnerCMD import *
from datetime import datetime, timedelta, timezone


class ISTFormatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        # Convert UTC timestamp to IST
        ist_time = datetime.fromtimestamp(record.created, timezone.utc) + timedelta(hours=5, minutes=30)
        return ist_time.strftime("%I:%M:%S %p  %d-%m-%y")

# Use custom formatter
formatter = ISTFormatter("『 𝐓𝐇𝐎𝐑 』™ | [%(levelname)-s -> %(asctime)s] | %(message)s | (%(filename)s -> %(lineno)d)")
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logging.basicConfig(level=logging.INFO, handlers=[handler])

# logging.basicConfig(level=logging.INFO, format="『 𝐓𝐇𝐎𝐑 』™ | %(levelname)-s | %(message)s | (%(filename)s : %(lineno)d)")
IST = pytz.timezone("Asia/Kolkata")

pending_size_input = {}
pending_opacity_input = {}


# ========================= Bot Initialization ============================
@bot.on_message(filters.command("tools"))
async def tools_status(_, message):
    try:
        ffmpeg = subprocess.getoutput("ffmpeg -version | head -n 1")
        ffprobe = subprocess.getoutput("ffprobe -version | head -n 1")
        aria2 = subprocess.getoutput("aria2c --version | head -n 1")
        mkvmerge = subprocess.getoutput("mkvmerge --version | head -n 1")
        ytDlp = subprocess.getoutput("yt-dlp --version")
        await message.reply(f"✅ ffmpeg: {ffmpeg}\n✅ ffprobe: {ffprobe}\n✅ aria2c: {aria2}\nmkvmerge : {mkvmerge}\nYt-Dlp : {ytDlp}")
    except Exception as e:
        await message.reply(f"❌ Error: {e}")

@bot.on_message(filters.command("id"))
async def get_user_id(_, m):
  await m.delete()
  if m.from_user:
    await m.reply_text(
    text=f"<blockquote>Your Telegram ID = `{m.from_user.id}`</blockquote>",
    reply_markup=ID_BUTTON)
  else:
    thread_id = m.message_thread_id if m.message_thread_id else "N/A"
    await m.reply_text(f"<blockquote>**📃 Your Channel Name :** {m.chat.title}</blockquote>\n\n**🆔 Your Channel ID :** `{m.chat.id}`\n🪪 **Thread ID :**`{thread_id}`.")



#========================= PW TOKEN =============================
@bot.on_message(filters.command(['pwtype']) & filters.user(owner_id))
async def change_pw_dl_type(bot: Client, msg: Message):
    Editable = await bot.send_message(msg.chat.id, "Send Type (mpd/m3u8) to set PW Downloading Method..")
    Input: Message = await bot.ask(msg.chat.id, '')
    result = ActiveUsersCollection.update_one(
        {"bot": bot.me.username},
        {"$set": {"pwType": f'{Input.text}'}})
    if result.modified_count > 0:
        await Input.delete()
        await Editable.edit(f"PW Downloading Method Updated to {Input.text}")

@bot.on_message(filters.command("pwtoken"))
@checkUser_PremiumStatus()
async def set_pwtoken(bot: Client, msg: Message):
    text = "<blockquote>🌟 PHYSICS WALLAH INFORMATION 🌟</blockquote>\n\n<blockquote>__To Update Your PHYSICS WALLAH [PW] AUTHORIZATION TOKEN__</blockquote>\n\nSimply Send **Recently Extracted Physics Wallah Authorization Token 🎫**."
    editable = await bot.send_photo(msg.chat.id, photo="https://envs.sh/rp_.jpg", caption=text)
    input_msg = await bot.ask(msg.chat.id, "")
    await editable.delete()
    result = await update_user_settings(msg.from_user.id, bot.me.username, default_name=None, extension_name=None, pdf_thumbnail=None, vid_thumbnail=None, watermark_color=None, text_watermark=None, quality=None, captStyle=None, ytcookie=None, pwtoken=input_msg.text, credit=None)
    await input_msg.delete()
    await msg.reply_text(f"**PHYSICS WALLAH [PW] TOKEN** 🎫 has been Updated Successfully🎉.")

#============================== COOKIES FILE ====================================
@bot.on_message(filters.command("cookies"))
@checkUser_PremiumStatus()
async def cookies_handler(bot: Client, msg: Message):
    await msg.delete()
    
    s_msg = await bot.send_photo(chat_id=msg.chat.id, photo="https://envs.sh/9SY.jpg", caption="<blockquote>🌟 **COOKIES INFORMATION** 🌟</blockquote>\n\n<blockquote>To Update Your COOKIES FILE</blockquote>\n\nSimply Upload **Recently Extracted Cookies File.txt 📄**.")
    try:
        input_message: Message = await bot.ask(msg.chat.id, "")
        if not input_message.document or not input_message.document.file_name.endswith(".txt"):
            await msg.reply_text("❌ Invalid file type. Please upload a .txt file.")
            return await s_msg.delete()
      
        cookies_path = await input_message.download()
        with open(cookies_path, 'r', encoding="utf-8") as file:
            cookies_data = file.read()
        resp = await update_user_settings(msg.from_user.id, bot.me.username, default_name=None, extension_name=None, pdf_thumbnail=None, vid_thumbnail=None, watermark_color=None, text_watermark=None, quality=None, captStyle=None, ytcookie=cookies_data, pwtoken=None, credit=None)
        await msg.reply_text(resp)
        await input_message.delete()
        
    except Exception as e:
        await msg.reply_text(f"⚠️ An error occurred: {str(e)}")
    await s_msg.delete()
  

@bot.on_message(filters.command("help"))
@checkUser_PremiumStatus()
async def help_command(bot: Client, msg: Message):
    userMention = (await bot.get_users(msg.from_user.id)).mention
    user = get_user_status(msg.from_user.id, bot.me.username)
    await bot.send_photo(msg.chat.id, photo="https://envs.sh/qEK.jpg", caption=f"<blockquote><b>✨ Welcome {userMention} To Your <i>{user['data']['planType']}</i> Bot! </b>✨</blockquote>\n\nExplore the powerful Features of our Bot with the following Commands.\nStay tuned for more Updates and Features! 🌟", reply_markup=TOOL_BUTTON)


@bot.on_callback_query(filters.regex("help_command"))
@checkUser_Premium_CallBack()
async def help_button(bot: Client, msg: CallbackQuery):
    userMention = (await bot.get_users(msg.from_user.id)).mention
    user = get_user_status(msg.from_user.id, bot.me.username)
    try:
        await msg.message.edit_media(InputMediaPhoto(media="https://envs.sh/qEK.jpg", caption=f"<blockquote><b>✨ Welcome {userMention} To Your <i>{user['data']['planType']}</i> Bot! </b>✨</blockquote>\n\nExplore the powerful Features of our Bot with the following Commands.\nStay tuned for more Updates and Features! 🌟"), reply_markup=TOOL_BUTTON)
        await msg.answer()
    except Exception as e:
        await msg.answer("⚠️ You are not Authorized to use this.", show_alert=True)


#========================== Back to Main Menu ===========================
@bot.on_callback_query(filters.regex("back_to_main_menu"))
@checkUser_Premium_CallBack()
async def back_to_main_menu(bot: Client, msg: CallbackQuery):
    userMention = (await bot.get_users(msg.from_user.id)).mention
    user = get_user_status(msg.from_user.id, bot.me.username)
    try:
        await msg.message.edit_media(
            InputMediaPhoto(media="https://envs.sh/qEK.jpg", caption=f"<blockquote>✨ <b>Welcome {userMention} To Your <i>{user['data']['planType']}</i> Bot! </b>✨</blockquote>\n\nExplore the powerful Features of our Bot with the following Commands.\nStay tuned for more Updates and Features! 🌟"),
            reply_markup=TOOL_BUTTON
        )
        await msg.answer()
    except Exception as e:
        await msg.answer("⚠️ You are not Authorized to use this.", show_alert=True)



# ========================= Chat/Topic View/Delte =========================
def build_chat_buttons(chats, page, per_page=5):
    start, end = page*per_page, (page+1)*per_page
    chunk = chats[start:end]
    
    buttons = []
    for idx, chat in enumerate(chunk, start=start+1):
        cid = chat['chat_id']
        buttons.append([InlineKeyboardButton(f"📂 Chat {cid}", callback_data=f"opchat|{cid}|0")])
    
    nav = []
    if page > 0: nav.append(InlineKeyboardButton("⬅️ Prev", callback_data=f"chats|{page-1}"))
    if end < len(chats): nav.append(InlineKeyboardButton("Next ➡️", callback_data=f"chats|{page+1}"))
    if nav: buttons.append(nav)

    buttons.append([InlineKeyboardButton("🔥 Delete All Chat", callback_data=f"delallchats")])
    buttons.append([InlineKeyboardButton("🔙 Back to Main Menu", callback_data="back_to_main_menu")])
    return InlineKeyboardMarkup(buttons)

def build_topic_buttons(topics, chat_id, page, per_page=5):
    start, end = page*per_page, (page+1)*per_page
    chunk = topics[start:end]

    buttons = []
    for t in chunk:
        tid, tname = t['topic_id'], t['topic_name']
        buttons.append([InlineKeyboardButton(f"✘ {tname}", callback_data=f"delt|{chat_id}|{tid}|{page}")])
    
    nav = []
    if page > 0: nav.append(InlineKeyboardButton("⬅️ Prev", callback_data=f"topics|{chat_id}|{page-1}"))
    if end < len(topics): nav.append(InlineKeyboardButton("Next ➡️", callback_data=f"topics|{chat_id}|{page+1}"))
    if nav: buttons.append(nav)

    buttons.append([InlineKeyboardButton("➕ Add Topic", callback_data=f"addt|{chat_id}|{page}"), InlineKeyboardButton("🗑️ Delete Chat", callback_data=f"delchat|{chat_id}|0")])
    buttons.append([InlineKeyboardButton("🔙 Back to Chat", callback_data="chats|0")])
    return InlineKeyboardMarkup(buttons)

@bot.on_callback_query(filters.regex(r"^chats\|"))
async def paginate_chats(bot: Client, msg:CallbackQuery):
    page = int(msg.data.split('|')[1])
    result = ActiveUsersCollection.find_one({"userId": msg.from_user.id, "bot": bot.me.username})
    chats = result.get('TopicsData', [])
    await msg.message.edit_media(InputMediaPhoto(media="https://ibb.co/nNvdpgHZ", caption="<blockquote>✅ <b>Groups List which have Active Topic Session :</b></blockquote>\n\n"), reply_markup=build_chat_buttons(chats, page))


def get_user_topic(user_id :int = None, bot_name:str = 'N/A', chat_id: int = None):
    result = ActiveUsersCollection.find_one({"userId": user_id, "bot": bot_name})

    TopicsData = result.get('TopicsData', [])
    if not TopicsData:
        return {} if chat_id is None else []
    
    if chat_id is None:
        data = {}
        for entry in TopicsData:
            cid = entry['chat_id']
            data[cid] = entry.get('topics', [])
        return data
    else:
        for entry in TopicsData:
            if entry['chat_id'] == chat_id:
                return entry.get('topics', [])
        return []

@bot.on_callback_query(filters.regex(r"^opchat\|"))
async def open_chat(bot: Client, msg:CallbackQuery):
    _, chat_id, page = msg.data.split('|')
    topics = get_user_topic(msg.from_user.id, bot.me.username, int(chat_id))
    await msg.message.edit_text(f"Topics in chat {chat_id}", reply_markup=build_topic_buttons(topics, int(chat_id), int(page)))

@bot.on_callback_query(filters.regex(r"^topics\|"))
async def paginate_topics(bot, msg: CallbackQuery):
    _, chat_id, page = msg.data.split("|")
    topics = get_user_topic(msg.from_user.id, bot.me.username, int(chat_id))
    if not topics: return await msg.answer("❌ No Topics found in this Chat", show_alert=True)
    await msg.message.edit_text(f"📂 Topics in Chat {chat_id}:", reply_markup=build_topic_buttons(topics, int(chat_id), int(page)))

@bot.on_callback_query(filters.regex(r"^delt\|"))
async def remove_topic(bot: Client, msg: CallbackQuery):
    _, chat_id, topic_id, page = msg.data.split("|")
    result = ActiveUsersCollection.update_one(
        {"userId": msg.from_user.id, "bot": bot.me.username, "TopicsData.chat_id": int(chat_id)},
        {"$pull": {"TopicsData.$.topics": {"topic_id": int(topic_id)}}}
    )
    if result.modified_count > 0:
        await msg.answer("✔️ Topic has been Deletd")
    topics = get_user_topic(msg.from_user.id, bot.me.username, int(chat_id))
    await msg.message.edit_text(f"📂 Topics in Chat {chat_id}:", reply_markup=build_topic_buttons(topics, int(chat_id), int(page)))

@bot.on_callback_query(filters.regex(r"addt\|"))
async def add_custom_topic(bot: Client, msg: CallbackQuery):
    _, chat_id, page = msg.data.split('|')

    Editable = await bot.send_message(msg.message.chat.id, "<b>Enter __TopicId:TopicName__</b>")
    Input: Message = await bot.ask(msg.message.chat.id, '')
    new_tid, new_tname = Input.text.split(':')
    topics = get_user_topic(msg.from_user.id, bot.me.username, int(chat_id))
    for t in topics:
        if t['topic_name'].lower() == new_tname.lower() and t['topic_id'] == int(new_tid):
            return await Editable.edit(f"⚠️ Topic '{new_tname}' Already Exists with TopicId : {t['topic_id']}")
    
    # Step 1: Try to push the topic if chat_id already exists in TopicsData
    result = ActiveUsersCollection.update_one(
            {"userId": msg.from_user.id, "bot": bot.me.username, "TopicsData.chat_id": int(chat_id)},  # <-- This checks if the chat_id already exists in TopicsData
            {"$push": {"TopicsData.$.topics": {"topic_id": int(new_tid), "topic_name": new_tname.upper()}}}  # <-- This pushes into the topics array of the matched chat_id
    )
    # Step 2: If chat_id doesn't exist, create a new entry with the chat_id and the topic
    if result.matched_count == 0:
        ActiveUsersCollection.update_one(
            {"userId": msg.from_user.id, "bot": bot.me.username},
            {"$push": {"TopicsData": {"chat_id": int(chat_id), "topics": [{"topic_id": new_tid, "topic_name": new_tname.upper()}]}}},
            upsert=True
        )
    Topics = get_user_topic(msg.from_user.id, bot.me.username, int(chat_id))
    await Editable.edit(f"[✔️] Topic '{new_tname}' (Id={new_tid}) Added!")

@bot.on_callback_query(filters.regex(r"^delchat\|"))
async def remove_chat(bot: Client, msg: CallbackQuery):
    _, chat_id, page = msg.data.split("|")
    result = ActiveUsersCollection.update_one(
        {"userId": msg.from_user.id, "bot": bot.me.username},
        {"$pull": {"TopicsData": {"chat_id": int(chat_id)}}}
    )
    if result.modified_count > 0:
        await msg.answer('Chat  Deleted')
        rest = ActiveUsersCollection.find_one({"userId": msg.from_user.id, "bot": bot.me.username})
        if not rest: return await msg.answer("❌ Currently, No Group has Active Topics.", show_alert=True)
        chats = rest.get('TopicsData', [])
        await msg.message.edit_media(InputMediaPhoto(media="https://ibb.co/BKF17rDv", caption="<blockquote>✅ <b>Groups List which have Active Topic Session :</b></blockquote>\n\n"), reply_markup=build_chat_buttons(chats, 0))
    else:
        await msg.message.edit_media(InputMediaPhoto(media="https://ibb.co/BKF17rDv", caption="<blockquote>✅ <b>Groups List which have Active Topic Session :</b></blockquote>\n\n"), reply_markup=BACK_MENU)

@bot.on_callback_query(filters.regex(r"^delallchats$"))
async def remove_all(bot:Client, msg: CallbackQuery):
    result = ActiveUsersCollection.update_one(
        {"userId": msg.from_user.id, "bot": bot.me.username},
        {"$set": {"TopicsData": []}})
    if result.modified_count > 0:
        await msg.answer("🔥 All chats deleted")
    await msg.message.edit_media(InputMediaPhoto(media="https://ibb.co/BKF17rDv", caption="<blockquote>✅ <b>Groups List which have Active Topic Session :</b></blockquote>\n\n"), reply_markup=BACK_MENU)

@bot.on_callback_query(filters.regex("ViewTopics"))
@checkUser_Premium_CallBack()
async def ViewChats_with_Topic(bot: Client, msg: CallbackQuery):
    result = ActiveUsersCollection.find_one({"userId": msg.from_user.id, "bot": bot.me.username})
    if not result:
        return await msg.answer("❌ Currently, No Group has Active Topics.", show_alert=True)
    chats = result.get('TopicsData', [])
    await msg.message.edit_media(InputMediaPhoto(media="https://ibb.co/BKF17rDv", caption="<blockquote>✅ <b>Groups List which have Active Topic Session :</b></blockquote>\n\n"), reply_markup=build_chat_buttons(chats, 0))



# ================================== PREMIUM MEMBERSHP INFO =========================================
@bot.on_message(filters.command("info"))
async def subscription_info_ommand(bot: Client, msg: Message):
    UserName = f"@{msg.from_user.username}" if msg.from_user.username else "N/A"
    
    user = get_user_status(msg.from_user.id, bot.me.username)
    if user.get('data'):
        join_date_ist = IST.localize(datetime.strptime(user['data']['createdAtIST'], "%I:%M:%S %p  %d-%m-%Y"))
        end_date_ist= IST.localize(datetime.strptime(user['data']['expiresAtIST'], "%I:%M:%S %p  %d-%m-%Y"))
        
        SubsDuration = end_date_ist - join_date_ist
        SubHrs, SubRemainder = divmod(SubsDuration.seconds, 3600)
        SubMins, SubSec = divmod(SubRemainder, 60)
        
        time_diff = end_date_ist - datetime.now(IST)
        hours, remainder = divmod(time_diff.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        caption = (
            f"<b>🔻 <u><i>Premium User Details</i></u> 🔻 </b>\n"
            f"<blockquote expandable>**🙋🏻‍♂️ First Name :** {msg.from_user.first_name}\n🧖‍♂️ **Second Name :** {msg.from_user.last_name}\n🧑🏻‍🎓 **Username :** {UserName}\n"
            f"🆔 **Telegram ID :** {msg.from_user.id}\n📱 <b>Phone No. :</b> {msg.from_user.phone_number}\n🌐 <b>DC ID :</b> {msg.from_user.dc_id}\n"
            f"✔️ <b>Verified Status :</b> {msg.from_user.is_verified}\n🏴‍☠️ <b>Scam Status :</b> {msg.from_user.is_scam}\n🚫 <b>Restricted Status :</b> {msg.from_user.is_restricted}\n"
            f"🔗 <b>Profile Link :</b> [{msg.from_user.first_name}](tg://user?id={msg.from_user.id})</blockquote>\n\n"
            f"<b>🌟 <u><i>Premium Membership Details</i></u></b>\n"
            f"<blockquote>📊 **PLAN STAT :** {(user['status']).upper()}\n"
            f"📅 **Join DateTime :** {user['data']['createdAtIST']}\n"
            f"🔒 **Subscription Duration :** {SubsDuration.days} Days, {SubHrs} Hrs, {SubMins} Min\n"
            f"⏳ **Expiration DateTime :** {user['data']['expiresAtIST']}\n"
            f"⏰ **Remaining Time :** {time_diff.days} Days, {hours} Hrs, {minutes} Min, and {seconds} Sec.</blockquote>\n\n"
            f"<blockquote>🤖 **SubsCription Type :** {user['data']['planType']}</blockquote>\n"
        )
        await bot.send_photo(msg.chat.id, photo="https://envs.sh/qho.jpg", caption=caption, reply_markup=BACK_MENU)
    else:
        caption = (
            f"<b>🔻 <u><i>Premium User Details</i></u> 🔻 </b>\n"
            f"<blockquote>**🙋🏻‍♂️ First Name :** {msg.from_user.first_name}\n🧖‍♂️ **Second Name :** {msg.from_user.last_name}\n🧑🏻‍🎓 **Username :** {UserName}\n"
            f"🆔 **Telegram ID :** {msg.from_user.id}\n📱 <b>Phone No. :</b> {msg.from_user.phone_number}\n🌐 <b>DC ID :</b> {msg.from_user.dc_id}\n"
            f"✔️ <b>Verified Status :</b> {msg.from_user.is_verified}\n🏴‍☠️ <b>Scam Status :</b> {msg.from_user.is_scam}\n🚫 <b>Restricted Status :</b> {msg.from_user.is_restricted}\n"
            f"🔗 <b>Profile Link :</b> [{msg.from_user.first_name}](tg://user?id={msg.from_user.id})</blockquote>\n\n"
            f"<blockquote>🚨 <b>You don't have an Unlocked Subscription..</b>🚨</blockquote>\n\n"
            f"<blockquote>💬 **Contact : [『 𝐓𝐇𝐎𝐑 🧑‍💻 』™](t.me/Stormy_thor)⁬** to Get The Subscription 🎫 and unlock the full potential of your new bot! 🔓</blockquote>"
        )
        await bot.send_photo(msg.chat.id, photo="https://envs.sh/qQY.jpg", caption=caption, reply_markup=BACK_MENU)

@bot.on_callback_query(filters.regex("subs_info_command"))
async def plan_button(bot: Client, msg: CallbackQuery):
    UserName = f"@{msg.from_user.username}" if msg.from_user.username else "N/A"
    
    user = get_user_status(msg.from_user.id, bot.me.username)
    if user.get('data'):
        Credit = user['data']['CreditName']
        
        join_date_ist = IST.localize(datetime.strptime(user['data']['createdAtIST'], "%I:%M:%S %p  %d-%m-%Y"))
        end_date_ist= IST.localize(datetime.strptime(user['data']['expiresAtIST'], "%I:%M:%S %p  %d-%m-%Y"))
        SubsDuration = end_date_ist - join_date_ist
        SubHrs, SubRemainder = divmod(SubsDuration.seconds, 3600)
        SubMins, SubSec = divmod(SubRemainder, 60)
        
        time_diff = end_date_ist - datetime.now(IST)
        hours, remainder = divmod(time_diff.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        caption = (
            f"<b>🔻 <u><i>Premium User Details</i></u> 🔻 </b>\n"
            f"<blockquote expandable>**🙋🏻‍♂️ First Name :** {msg.from_user.first_name}\n🧖‍♂️ **Second Name :** {msg.from_user.last_name}\n🧑🏻‍🎓 **Username :** {UserName}\n"
            f"🆔 **Telegram ID :** {msg.from_user.id}\n📱 <b>Phone No. :</b> {msg.from_user.phone_number}\n🌐 <b>DC ID :</b> {msg.from_user.dc_id}\n"
            f"✔️ <b>Verified Status :</b> {msg.from_user.is_verified}\n🏴‍☠️ <b>Scam Status :</b> {msg.from_user.is_scam}\n🚫 <b>Restricted Status :</b> {msg.from_user.is_restricted}\n"
            f"🔗 <b>Profile Link :</b> [{msg.from_user.first_name}](tg://user?id={msg.from_user.id})</blockquote>\n\n"
            f"<b>🌟 <u><i>Premium Membership Details</i></u></b>\n"
            f"<blockquote>📊 **PLAN STAT :** {(user['status']).upper()}\n"
            f"📅 **Join DateTime :** {user['data']['createdAtIST']}\n"
            f"🔒 **Subscription Duration :** {SubsDuration.days} Days, {SubHrs} Hrs, {SubMins} Min\n"
            f"⏳ **Expiration DateTime :** {user['data']['expiresAtIST']}\n"
            f"⏰ **Remaining Time :** {time_diff.days} Days, {hours} Hrs, {minutes} Min, and {seconds} Sec.</blockquote>\n\n"
            f"<blockquote>🤖 **SubsCription Type :** {user['data']['planType']}</blockquote>\n"
        )
        await msg.message.edit_media(InputMediaPhoto(media="https://envs.sh/qho.jpg", caption=caption), reply_markup=BACK_MENU)
    else:
        Credit = "[『 𝐓𝐇𝐎𝐑 🧑‍💻 』™](t.me/Stormy_thor)⁬"
        caption = (
            f"<b>🔻 <u><i>Premium User Details</i></u> 🔻 </b>\n"
            f"<blockquote>**🙋🏻‍♂️ First Name :** {msg.from_user.first_name}\n🧖‍♂️ **Second Name :** {msg.from_user.last_name}\n🧑🏻‍🎓 **Username :** {UserName}\n"
            f"🆔 **Telegram ID :** {msg.from_user.id}\n📱 <b>Phone No. :</b> {msg.from_user.phone_number}\n🌐 <b>DC ID :</b> {msg.from_user.dc_id}\n"
            f"✔️ <b>Verified Status :</b> {msg.from_user.is_verified}\n🏴‍☠️ <b>Scam Status :</b> {msg.from_user.is_scam}\n🚫 <b>Restricted Status :</b> {msg.from_user.is_restricted}\n"
            f"🔗 <b>Profile Link :</b> [{msg.from_user.first_name}](tg://user?id={msg.from_user.id})</blockquote>\n\n"
            f"<blockquote>🚨 <b>You don't have an Unlocked Subscription..</b>🚨</blockquote>\n\n"
            f"<blockquote>💬 **Contact : {Credit}** to Get The Subscription 🎫 and unlock the full potential of your new bot! 🔓</blockquote>"
        )
        await msg.message.edit_media(InputMediaPhoto(media="https://envs.sh/qQY.jpg", caption=caption), reply_markup=BACK_MENU)
    await msg.answer()


#======================= SETTINGS ===========================
@bot.on_message(filters.command("Settings"))
@checkUser_PremiumStatus()
async def settings_command(bot: Client, msg: Message):
    await bot.send_photo(msg.chat.id, photo="https://envs.sh/T8Z.jpg", caption="<blockquote>**Choose a Setting to Modify :**</blockquote>", reply_markup=ST_BUTTON)

@bot.on_callback_query(filters.regex("set_command"))
@checkUser_Premium_CallBack()
async def settings_button(_, msg: CallbackQuery):
    await msg.message.edit_media(InputMediaPhoto(media="https://envs.sh/T8Z.jpg", caption="<blockquote>**Choose a Setting to Modify :**</blockquote>"), reply_markup=ST_BUTTON)
    await msg.answer()

@bot.on_callback_query(filters.regex("back_to_st"))
async def back_to_st(_, msg: CallbackQuery):
    await msg.message.edit_media(InputMediaPhoto(media="https://envs.sh/T8Z.jpg", caption="<blockquote>**Choose a Setting to Modify :**</blockquote>"), reply_markup=ST_BUTTON)
    await msg.answer()

#========================= Extension : NAME =============================
@bot.on_callback_query(filters.regex("extension"))
@checkUser_Premium_CallBack()
async def extension_button(bot: Client, msg: CallbackQuery):
    user = get_user_status(msg.from_user.id, bot.me.username)
    try:
        caption = f"<blockquote>Your Extension Name : {user['data']['extensionName']}</blockquote>"
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("✍️ Change Name", callback_data="exname")], [InlineKeyboardButton("🔙 Back", callback_data="back_to_st")]])
        await msg.message.edit_media(InputMediaPhoto(media="https://envs.sh/T8Z.jpg", caption=caption), reply_markup=keyboard)
        await msg.answer()
    except Exception as e:
        await msg.answer(f"⚠️ You are not Authorized to use this. {e}")

@bot.on_callback_query(filters.regex("exname"))
@checkUser_Premium_CallBack()
async def set_exname_callback(bot: Client, query: CallbackQuery):
    editable = await query.message.reply_text(f"<blockquote>Send me a Name that will be apply on **Extension Name**</blockquote>")
    input_msg = await bot.ask(query.message.chat.id, "")
    await input_msg.delete()
    await editable.delete()
    result = await update_user_settings(query.from_user.id, bot.me.username, default_name=None, extension_name=input_msg.text)
    await query.answer(f"Congratulation 🎉 Your Extension Name has Successfully Update to\n  **{input_msg.text}**", show_alert=True)
    await back_to_st(client, query)


#========================= Credit : NAME =============================
@bot.on_callback_query(filters.regex("df_command"))
@checkUser_Premium_CallBack()
async def extension_button(bot: Client, msg: CallbackQuery):
    user = get_user_status(msg.from_user.id, bot.me.username)
    try:
        caption = f"<blockquote>Your Default Name : {user['data']['defaultName']}</blockquote>"
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("✍️ Change Name", callback_data="crname")], [InlineKeyboardButton("🔙 Back to Setting", callback_data="back_to_st")]])
        await msg.message.edit_media(InputMediaPhoto(media="https://envs.sh/T8Z.jpg", caption=caption), reply_markup=keyboard)
        await msg.answer()
    except Exception as e:
        await msg.answer(f"⚠️ You are not Authorized to use this. {e}")

@bot.on_callback_query(filters.regex("crname"))
@checkUser_Premium_CallBack()
async def set_exname_callback(bot: Client, query: CallbackQuery):
    editable = await query.message.reply_text(f"<blockquote>Send me a Name that will be apply on **Extracted By Name**</blockquote>")
    input_msg = await bot.ask(query.message.chat.id, "")
    await input_msg.delete()
    await editable.delete()
    result = await update_user_settings(query.from_user.id, bot.me.username, input_msg.text)
    await query.answer(f"Congratulation 🎉 Your Default Name has Successfully Update to\n  **{input_msg.text}**", show_alert=True)
    await back_to_st(bot, query)

@bot.on_callback_query(filters.regex("cap_style"))
async def caption_button(bot: Client, msg: CallbackQuery):
    user = get_user_status(msg.from_user.id, bot.me.username)
    current_style = user['data']['captionStyle']
    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Default ❤️" if current_style == "default" else "Default", callback_data="default_")],
            [InlineKeyboardButton("Style 1 ✅" if current_style == "style1" else "Style 1", callback_data="style10"), InlineKeyboardButton("Style 2 ✅" if current_style == "style2" else "Style 2", callback_data="style20")],
            [InlineKeyboardButton("Style 3 ✅" if current_style == "style3" else "Style 3", callback_data="style30"), InlineKeyboardButton("Style 4 ✅" if current_style == "style4" else "Style 4", callback_data="style40")],
            [InlineKeyboardButton("Style 5 ✅" if current_style == "style5" else "Style 5", callback_data="style50"), InlineKeyboardButton("Style 6 ✅" if current_style == "style6" else "Style 6", callback_data="style60")],
            [InlineKeyboardButton("🔙 Back to Setting", callback_data="back_to_st")]
       ]
    )
    text = f"<blockquote>Here is different types of Caption Style</blockquote>\nYou can Choose anyone from these."
    await msg.message.edit_media(InputMediaPhoto(media="https://envs.sh/T8Z.jpg", caption=text), reply_markup=keyboard)
    await msg.answer()

@bot.on_callback_query(filters.regex("back_to_cap"))
async def back_to_cap(bot: Client, msg: CallbackQuery):
    user = get_user_status(msg.from_user.id, bot.me.username)
    current_style = user['data']['captionStyle']
    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Default ❤️" if current_style == "default" else "Default", callback_data="default_")],
            [InlineKeyboardButton("Style 1 ✅" if current_style == "style1" else "Style 1", callback_data="style10"), InlineKeyboardButton("Style 2 ✅" if current_style == "style2" else "Style 2", callback_data="style20")],
            [InlineKeyboardButton("Style 3 ✅" if current_style == "style3" else "Style 3", callback_data="style30"), InlineKeyboardButton("Style 4 ✅" if current_style == "style4" else "Style 4", callback_data="style40")],
            [InlineKeyboardButton("Style 5 ✅" if current_style == "style5" else "Style 5", callback_data="style50"), InlineKeyboardButton("Style 6 ✅" if current_style == "style6" else "Style 6", callback_data="style60")],
            [InlineKeyboardButton("🔙 Back to Setting", callback_data="back_to_st")]
        ]
    )
    await msg.message.edit_media(InputMediaPhoto(media="https://envs.sh/T8Z.jpg", caption="<blockquote>Here is different types of Caption Style</blockquote>\nYou can Choose anyone from these."),reply_markup=keyboard)
    await msg.answer()

@bot.on_callback_query(filters.regex("default_"))
async def set_default_caption_style(bot: Client, msg: CallbackQuery):
    result = await update_user_settings(msg.from_user.id, bot.me.username, default_name=None, extension_name=None, pdf_thumbnail=None, vid_thumbnail=None, watermark_color=None, text_watermark=None, quality=None, captStyle="default", ytcookie=None, pwtoken=None, credit=None)
    await msg.answer("Caption style set to Default", show_alert=True)
    await back_to_st(bot, msg)


@bot.on_callback_query(filters.regex("style10"))
async def cap_style(client: Client, callback_query: CallbackQuery):
    text = f"**┏━━━━━━━━━ ✦ File Info ✦ ━━━━━━━━━━━┓**\n**┃ 📋 Title :** [Bio] Class 31 - Bio Blood\n**┃ 🎥 Extension :** THOR.mkv\n**┃ 📏 Resolution :** [854×480]\n┗━━━━━━━━━━ ✦ 324 ✦ ━━━━━━━━━━┛\n\n<blockquote>🧾 **Course :** GS SPL-03 [Live + VOD]</blockquote>\n\n💻 **Extracted By :** 『 𝐓𝐇𝐎𝐑 』™"
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("Set as Caption", callback_data="style1_")],  [InlineKeyboardButton("🔙 Back to Caption Style", "back_to_cap")]])
    await callback_query.message.edit_media(InputMediaPhoto(media="https://envs.sh/T8Z.jpg", caption=text), reply_markup=keyboard)
    await callback_query.answer()
@bot.on_callback_query(filters.regex("style1_"))
async def set_style1_caption_style(bot: Client, msg: CallbackQuery):
    result = await update_user_settings(msg.from_user.id, bot.me.username, default_name=None, extension_name=None, pdf_thumbnail=None, vid_thumbnail=None, watermark_color=None, text_watermark=None, quality=None, captStyle="style1", ytcookie=None, pwtoken=None, credit=None)
    await msg.answer("Caption style set to Style1", show_alert=True)
    await back_to_st(bot, msg)

@bot.on_callback_query(filters.regex("style20"))
async def cap_style(client: Client, callback_query: CallbackQuery):
    text = f"❖────────────── 324 ──────────────❖\n\n📋 Title: [Bio] Class 31 - Bio Blood\n🎞️ File: THOR.mkv\n📏 Resolution : [854×480]\n\n<blockquote>📘 Course: GS SPL-03 [Live + VOD]</blockquote>\n\n❖──────── 『 𝐓𝐇𝐎𝐑 』™ ────────❖"
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("Set as Caption", callback_data="style2_")], [InlineKeyboardButton("🔙 Back to Caption Style", "back_to_cap")]])
    await callback_query.message.edit_media(InputMediaPhoto(media="https://envs.sh/T8Z.jpg", caption=text), reply_markup=keyboard)
    await callback_query.answer()
@bot.on_callback_query(filters.regex("style2_"))
async def set_style2_caption_style(bot: Client, msg: CallbackQuery):
    result = await update_user_settings(msg.from_user.id, bot.me.username, default_name=None, extension_name=None, pdf_thumbnail=None, vid_thumbnail=None, watermark_color=None, text_watermark=None, quality=None, captStyle="style2", ytcookie=None, pwtoken=None, credit=None)
    await msg.answer("Caption style set to Style2", show_alert=True)
    await back_to_st(bot, msg)

@bot.on_callback_query(filters.regex("style30"))
async def cap_style(client: Client, callback_query: CallbackQuery):
    text = f"────────── ✧ 324 ✧ ──────────\n📝 Title:\n  ➜ [Bio] Class 31 - Bio Blood\n🎞️ File Info:\n  • Extension: THOR.mkv\n  • Resolution: [854×480]\n\n📘 Course:\n  ➜ GS SPL-03 [Live + VOD]\n\n⭐ Extracted By: 『 𝐓𝐇𝐎𝐑 』™"
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("Set as Caption", callback_data="style3_")], [InlineKeyboardButton("🔙 Back to Caption Style", "back_to_cap")]])
    await callback_query.message.edit_media(InputMediaPhoto(media="https://envs.sh/T8Z.jpg", caption=text), reply_markup=keyboard)
    await callback_query.answer()
@bot.on_callback_query(filters.regex("style3_"))
async def set_style3_caption_style(bot: Client, msg: CallbackQuery):
    result = await update_user_settings(msg.from_user.id, bot.me.username, default_name=None, extension_name=None, pdf_thumbnail=None, vid_thumbnail=None, watermark_color=None, text_watermark=None, quality=None, captStyle="style3", ytcookie=None, pwtoken=None, credit=None)
    await msg.answer("Caption style set to Style3", show_alert=True)
    await back_to_st(bot, msg)

@bot.on_callback_query(filters.regex("style40"))
async def cap_style(client: Client, callback_query: CallbackQuery):
    text = f"────────── ✧ 324 ✧ ──────────\n\n**[📽] Title :** [Bio] Class 31 - Bio Blood-[854×480]_THOR.mkv\n\n<blockquote>📚 Batch Name : GS SPL-03 [Live + VOD]</blockquote>\n\n🌟 **Extracted By :**『 𝐓𝐇𝐎𝐑 』™"
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("Set as Caption", callback_data="style4_")], [InlineKeyboardButton("🔙 Back to Caption Style", "back_to_cap")]])
    await callback_query.message.edit_media(InputMediaPhoto(media="https://envs.sh/T8Z.jpg", caption=text), reply_markup=keyboard)
    await callback_query.answer()
@bot.on_callback_query(filters.regex("style4_"))
async def set_style3_caption_style(bot: Client, msg: CallbackQuery):
    result = await update_user_settings(msg.from_user.id, bot.me.username, default_name=None, extension_name=None, pdf_thumbnail=None, vid_thumbnail=None, watermark_color=None, text_watermark=None, quality=None, captStyle="style4", ytcookie=None, pwtoken=None, credit=None)
    await msg.answer("Caption style set to Style4", show_alert=True)
    await back_to_st(bot, msg)

@bot.on_callback_query(filters.regex("style60"))
async def cap_style(client: Client, callback_query: CallbackQuery):
    text = f"📋 Title: [Bio] Class 31 - Bio Blood\n🎞️ File: THOR.mkv\n📏 Resolution : [854×480]\n\n<blockquote>📘 Course: GS SPL-03 [Live + VOD]</blockquote>\n\n❖──────── 『 𝐓𝐇𝐎𝐑 』™ ────────❖"
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("Set as Caption", callback_data="style6_")], [InlineKeyboardButton("🔙 Back to Caption Style", "back_to_cap")]])
    await callback_query.message.edit_media(InputMediaPhoto(media="https://envs.sh/T8Z.jpg", caption=text), reply_markup=keyboard)
    await callback_query.answer()
@bot.on_callback_query(filters.regex("style6_"))
async def set_style3_caption_style(bot: Client, msg: CallbackQuery):
    result = await update_user_settings(msg.from_user.id, bot.me.username, default_name=None, extension_name=None, pdf_thumbnail=None, vid_thumbnail=None, watermark_color=None, text_watermark=None, quality=None, captStyle="style6", ytcookie=None, pwtoken=None, credit=None)
    await msg.answer("Caption style set to Style6", show_alert=True)
    await back_to_st(bot, msg)


@bot.on_callback_query(filters.regex("quality"))
async def quality_button(bot: Client, msg: CallbackQuery):
    user = get_user_status(msg.from_user.id, bot.me.username)
    current_qua = user['data']['quality']
    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("144 ✅" if current_qua == "144" else "144", callback_data="144_"), InlineKeyboardButton("240 ✅" if current_qua == "240" else "240", callback_data="240_")],
            [InlineKeyboardButton("360 ✅" if current_qua == "360" else "360", callback_data="360_"), InlineKeyboardButton("480 ✅" if current_qua == "480" else "480", callback_data="480_")],
            [InlineKeyboardButton("720 ✅" if current_qua == "720" else "720", callback_data="720_"), InlineKeyboardButton("1080 ✅" if current_qua == "1080" else "1080", callback_data="1080_")],
            [InlineKeyboardButton("🔙 Back to Setting", callback_data="back_to_st")]
        ]
    )
    text = f"<blockquote>Current Quality : {current_qua}</blockquote>\n\nChoose Video Quality."
    await msg.message.edit_media(InputMediaPhoto(media="https://envs.sh/T8Z.jpg", caption=text), reply_markup=keyboard)
    await msg.answer()

@bot.on_callback_query(filters.regex("144_"))
async def set_144_quality(bot: Client, msg: CallbackQuery):
    result = await update_user_settings(msg.from_user.id, bot.me.username, default_name=None, extension_name=None, pdf_thumbnail=None, vid_thumbnail=None, watermark_color=None, text_watermark=None, quality="144", captStyle=None, ytcookie=None, pwtoken=None, credit=None)
    await msg.answer("Default Quality set to 144p", show_alert=True)
    await back_to_st(bot, msg)

@bot.on_callback_query(filters.regex("240_"))
async def set_240_quality(bot: Client, msg: CallbackQuery):
    result = await update_user_settings(msg.from_user.id, bot.me.username, default_name=None, extension_name=None, pdf_thumbnail=None, vid_thumbnail=None, watermark_color=None, text_watermark=None, quality="240", captStyle=None, ytcookie=None, pwtoken=None, credit=None)
    await msg.answer("Default Quality set to 240p", show_alert=True)
    await back_to_st(bot, msg)

@bot.on_callback_query(filters.regex("360_"))
async def set_360_quality(bot: Client, msg: CallbackQuery):
    result = await update_user_settings(msg.from_user.id, bot.me.username, default_name=None, extension_name=None, pdf_thumbnail=None, vid_thumbnail=None, watermark_color=None, text_watermark=None, quality="360", captStyle=None, ytcookie=None, pwtoken=None, credit=None)
    await msg.answer("Default Quality set to 360p", show_alert=True)
    await back_to_st(bot, msg)

@bot.on_callback_query(filters.regex("480_"))
async def set_480_quality(bot: Client, msg: CallbackQuery):
    result = await update_user_settings(msg.from_user.id, bot.me.username, default_name=None, extension_name=None, pdf_thumbnail=None, vid_thumbnail=None, watermark_color=None, text_watermark=None, quality="480", captStyle=None, ytcookie=None, pwtoken=None, credit=None)
    await msg.answer("Default Quality set to 480p", show_alert=True)
    await back_to_st(bot, msg)

@bot.on_callback_query(filters.regex("720_"))
async def set_720_quality(bot: Client, msg: CallbackQuery):
    result = await update_user_settings(msg.from_user.id, bot.me.username, default_name=None, extension_name=None, pdf_thumbnail=None, vid_thumbnail=None, watermark_color=None, text_watermark=None, quality="720", captStyle=None, ytcookie=None, pwtoken=None, credit=None)
    await msg.answer("Default Quality set to 720p", show_alert=True)
    await back_to_st(bot, msg)

@bot.on_callback_query(filters.regex("1080_"))
async def set_1080_quality(bot: Client, msg: CallbackQuery):
    result = await update_user_settings(msg.from_user.id, bot.me.username, default_name=None, extension_name=None, pdf_thumbnail=None, vid_thumbnail=None, watermark_color=None, text_watermark=None, quality="1080", captStyle=None, ytcookie=None, pwtoken=None, credit=None)
    await msg.answer("Default Quality set to 1080p", show_alert=True)
    await back_to_st(bot, msg)

#============================= DEFAULT THUMBNAIL =================================
@bot.on_callback_query(filters.regex("thumb_st"))
async def default_thumbnail(bot: Client, msg: CallbackQuery):
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🎞️ Video Thumbnail", callback_data="vid_thumb"), InlineKeyboardButton("📄 PDF Thumbnail", callback_data="pdf_thumb")], [InlineKeyboardButton("🔙 Back to Setting", callback_data="back_to_st")]])
    await msg.message.edit_media(InputMediaPhoto(media="https://envs.sh/T8Z.jpg", caption="Choose the Default Thumbnail Preference"), reply_markup=keyboard)
    await msg.answer()

@bot.on_callback_query(filters.regex("vid_thumb"))
async def default_vid_thumbnail(bot: Client, msg: CallbackQuery):
    user = get_user_status(msg.from_user.id, bot.me.username)
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("✍️ Change Thumbnail", callback_data="ch_thumb")], [InlineKeyboardButton("🔙 Back to Setting", callback_data="back_to_st")]])
    await msg.message.edit_media(InputMediaPhoto(media="https://envs.sh/T8Z.jpg", caption=f"<blockquote>Your current Video Thumbnail : {user['data']['vidThumbnail']}</blockquote>"), reply_markup=keyboard)
    await msg.answer() 

@bot.on_callback_query(filters.regex("ch_thumb"))
async def set_default_vid_thumb(bot: Client, msg: CallbackQuery):
    editable = await msg.message.reply_text(f"Now Send the **Thumbnail URL 🔗** or Send `no`")
    input: Message = await bot.ask(msg.message.chat.id, "")
    try:
        if input.text.startswith(("http://", "https://")):
            result = await update_user_settings(msg.from_user.id, bot.me.username, default_name=None, extension_name=None, pdf_thumbnail=None, vid_thumbnail=f"{input.text}", watermark_color=None, text_watermark=None, quality=None, captStyle=None, ytcookie=None, pwtoken=None, credit=None)
            await msg.answer("Congratulation 🎉 Video Thumbnail has been Enabled ✅.", show_alert=True)
        else:
            result = await update_user_settings(msg.from_user.id, bot.me.username, default_name=None, extension_name=None, pdf_thumbnail=None, vid_thumbnail="no", watermark_color=None, text_watermark=None, quality=None, captStyle=None, ytcookie=None, pwtoken=None, credit=None)
            await msg.answer("Congratulation 🎉 Video Thumbnail has been Disabled ❌.", show_alert=True)
        await input.delete()
        await editable.delete()
        await back_to_st(bot, msg)
    except Exception as e:
        logging.error(e)
        pass

@bot.on_callback_query(filters.regex("pdf_thumb"))
async def default_pdf_thumbnail(bot: Client, msg: CallbackQuery):
    user = get_user_status(msg.from_user.id, bot.me.username)
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("✍️ Change Thumbnail", callback_data="ch1_thumb")], [InlineKeyboardButton("🔙 Back to Setting", callback_data="back_to_st")]])
    await msg.message.edit_media(
    InputMediaPhoto(media="https://envs.sh/T8Z.jpg", caption=f"<blockquote>Your current PDF Thumbnail : {user['data']['pdfThumbnail']}</blockquote>"), reply_markup=keyboard)
    await msg.answer() 

@bot.on_callback_query(filters.regex("ch1_thumb"))
async def set_default_pdf_thumb(bot: Client, msg: CallbackQuery):
    editable = await msg.message.reply_text(f"Now Send the **Thumbnail URL 🔗** or Send `no`")
    input: Message = await bot.ask(msg.message.chat.id, "")
    try:
        if input.text.startswith(("http://", "https://")):
            result = await update_user_settings(msg.from_user.id, bot.me.username, default_name=None, extension_name=None, pdf_thumbnail=f"{input.text}", vid_thumbnail=None, watermark_color=None, text_watermark=None, quality=None, captStyle=None, ytcookie=None, pwtoken=None, credit=None)
            await msg.answer("Congratulation 🎉 PDF Thumbnail has been Enabled ✅.", show_alert=True)
        else:
            result = await update_user_settings(msg.from_user.id, bot.me.username, default_name=None, extension_name=None, pdf_thumbnail="no", vid_thumbnail=None, watermark_color=None, text_watermark=None, quality=None, captStyle=None, ytcookie=None, pwtoken=None, credit=None)
            await msg.answer("Congratulation 🎉 PDF Thumbnail has been Disabled ❌.", show_alert=True)
        await input.delete()
        await editable.delete()
        await back_to_st(bot, msg)
    except Exception as e:
        logging.error(f"{e}")
        pass


# ==================== ADVANCED WATERMARK SETTINGS ====================

@bot.on_callback_query(filters.regex("text_settings_"))
async def text_watermark_main(bot: Client, msg: CallbackQuery):
    user = get_user_status(msg.from_user.id, bot.me.username)
    data = user.get('data', {})
    
    overlay_text = data.get('textWatermark') or "Not Set"
    text_color = data.get('watermarkColor', 'white')
    font_style = data.get('fontStyle', 'DejaVu Sans')
    font_size = data.get('fontSize', '80')
    opacity = data.get('opacity', '0.8')
    enabled = data.get('watermarkEnabled', 'yes')
    
    status_emoji = "✅" if enabled == "yes" else "❌"
    status_text = "Enabled" if enabled == "yes" else "Disabled"
    
    caption = (
        f"<blockquote><b>Your Current Overlay Details:</b></blockquote>\n\n"
        f"<b>🖊 Overlay Text :</b> {overlay_text}\n"
        f"<b>🎨 Text Colour :</b> {text_color.title()}\n"
        f"<b>🔤 Font Style :</b> {font_style}\n"
        f"<b>🔍 Font Size :</b> {font_size}\n"
        f"<b>💧 Opacity :</b> {opacity}\n"
        f"<b>{status_emoji} Status :</b> {status_text}\n\n"
        f"<blockquote><b>Choose the Text WaterMark Settings Preference</b></blockquote>"
    )
    
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("✍️ Change Text", callback_data="wt_text_")],
        [InlineKeyboardButton("🎨 Change Colour", callback_data="wt_color_menu")],
        [InlineKeyboardButton("🔤 Change Font Style", callback_data="wt_font_menu")],
        [InlineKeyboardButton("🔍 Change Font Size", callback_data="wt_size_menu")],
        [InlineKeyboardButton("💧 Change Opacity", callback_data="wt_opacity_menu")],
        [InlineKeyboardButton(f"{'❌ Disable' if enabled == 'yes' else '✅ Enable'} Watermark", callback_data="wt_toggle")],
        [InlineKeyboardButton("🔙 Back to Settings", callback_data="back_to_st")]
    ])
    
    await msg.message.edit_media(
        InputMediaPhoto(media="https://envs.sh/T8Z.jpg", caption=caption),
        reply_markup=keyboard
    )
    await msg.answer()

@bot.on_callback_query(filters.regex("wt_color_menu"))
async def watermark_color_menu(bot: Client, msg: CallbackQuery):
    user = get_user_status(msg.from_user.id, bot.me.username)
    current_color = user.get('data', {}).get('watermarkColor', 'white')
    
    colors = [
        "White", "Black", "Red", "Blue", "Green", "Golden", "Yellow", "Orange",
        "Purple", "Pink", "Magenta", "Teal", "Sky Blue", "Beige", "Mint", "Coral",
        "Sea Green", "Khaki", "Brown", "Lime", "Maroon", "Turquoise", "Peach",
        "Crimson", "Rose", "Slate Blue", "Gray", "Cyan", "Navy", "Olive",
        "Indigo", "Lavender", "Salmon", "Periwinkle", "Ivory", "Chartreuse"
    ]
    
    keyboard = []
    row = []
    for color in colors:
        display = f"{'✅ ' if color.lower() == current_color.lower() else ''}{color}"
        row.append(InlineKeyboardButton(display, callback_data=f"wt_color_set_{color.lower()}"))
        if len(row) == 2:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)
    
    keyboard.append([InlineKeyboardButton("🔙 Back", callback_data="text_settings_")])
    
    await msg.message.edit_caption(
        caption=f"<blockquote><b>Current Color:</b> {current_color.title()}</blockquote>\n\nChoose a color:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

@bot.on_callback_query(filters.regex(r"wt_color_set_(.*)"))
async def set_watermark_color(bot: Client, msg: CallbackQuery):
    color = msg.data.split("_")[-1]
    await update_user_settings(msg.from_user.id, bot.me.username, watermark_color=color)
    await msg.answer(f"Color changed to {color.title()}", show_alert=True)
    await text_watermark_main(bot, msg)


@bot.on_callback_query(filters.regex("wt_font_menu"))
async def watermark_font_menu(bot: Client, msg: CallbackQuery, page: int = 0):
    from helper import FONT_LIST
    user = get_user_status(msg.from_user.id, bot.me.username)
    current_font = user.get('data', {}).get('fontStyle', 'DejaVu Sans')
    
    per_page = 8
    start = page * per_page
    end = start + per_page
    page_fonts = FONT_LIST[start:end]
    total_pages = (len(FONT_LIST) + per_page - 1) // per_page
    
    keyboard = []
    for font_name in page_fonts:
        display = f"{'✅ ' if font_name == current_font else ''}{font_name}"
        keyboard.append([InlineKeyboardButton(display, callback_data=f"wt_font_preview_{font_name}")])
    
    nav_buttons = []
    if page > 0:
        nav_buttons.append(InlineKeyboardButton("⬅️ Prev", callback_data=f"wt_font_page_{page-1}"))
    if page < total_pages - 1:
        nav_buttons.append(InlineKeyboardButton("Next ➡️", callback_data=f"wt_font_page_{page+1}"))
    if nav_buttons:
        keyboard.append(nav_buttons)
    
    keyboard.append([InlineKeyboardButton("🔙 Back", callback_data="text_settings_")])
    
    caption = (
        f"<blockquote><b>Current Font:</b> {current_font}</blockquote>\n\n"
        f"Choose your preferred font style:\nPage {page+1}/{total_pages}"
    )
    await msg.message.edit_caption(caption, reply_markup=InlineKeyboardMarkup(keyboard))

@bot.on_callback_query(filters.regex(r"wt_font_page_(\d+)"))
async def font_page_nav(bot: Client, msg: CallbackQuery):
    page = int(msg.data.split("_")[-1])
    await watermark_font_menu(bot, msg, page)

@bot.on_callback_query(filters.regex(r"wt_font_preview_(.+)"))
async def preview_font(bot: Client, msg: CallbackQuery):
    from helper import generate_watermark_preview
    import os
    font_name = msg.data.replace("wt_font_preview_", "")
    user = get_user_status(msg.from_user.id, bot.me.username)
    data = user.get('data', {})
    overlay_text = data.get('textWatermark') or "MARCO"
    color = data.get('watermarkColor', 'white')
    font_size = data.get('fontSize', '80')
    opacity = data.get('opacity', '0.8')
    
    preview_path = await generate_watermark_preview(overlay_text, font_name, color, font_size, opacity)
    
    caption = (
        f"<blockquote><b>Font Preview</b></blockquote>\n\n"
        f"<b>Text:</b> {overlay_text}\n"
        f"<b>Font:</b> {font_name}\n"
        f"<b>Color:</b> {color.title()}\n\n"
        f"If you like it, tap confirm below."
    )
    
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("✔ Confirm", callback_data=f"wt_font_set_{font_name}")],
        [InlineKeyboardButton("🔙 Back", callback_data="wt_font_menu")]
    ])
    
    await msg.message.edit_media(
        InputMediaPhoto(media=preview_path, caption=caption),
        reply_markup=keyboard
    )
    os.remove(preview_path)

@bot.on_callback_query(filters.regex(r"wt_font_set_(.+)"))
async def set_font(bot: Client, msg: CallbackQuery):
    font_name = msg.data.replace("wt_font_set_", "")
    await update_user_settings(msg.from_user.id, bot.me.username, font_style=font_name)
    await msg.answer(f"Font '{font_name}' saved!", show_alert=True)
    await text_watermark_main(bot, msg)


@bot.on_callback_query(filters.regex("wt_size_menu"))
async def watermark_size_menu(bot: Client, msg: CallbackQuery):
    user = get_user_status(msg.from_user.id, bot.me.username)
    current_size = int(user.get('data', {}).get('fontSize', '80'))
    
    caption = (
        f"<blockquote><b>Send me the new font size:</b></blockquote>\n\n"
        f"• Current size: <b>{current_size}</b>\n"
        f"• Minimum size: 50\n"
        f"• Maximum size: 200\n"
        f"• Must be a whole number\n\n"
        f"Send /cancel to cancel"
    )
    
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("-10", callback_data=f"wt_size_adjust_{-10}"),
            InlineKeyboardButton("-5", callback_data=f"wt_size_adjust_{-5}"),
            InlineKeyboardButton(f"{current_size}", callback_data="noop"),
            InlineKeyboardButton("+5", callback_data=f"wt_size_adjust_5"),
            InlineKeyboardButton("+10", callback_data=f"wt_size_adjust_10")
        ],
        [InlineKeyboardButton("✍️ Type Custom", callback_data="wt_size_input")],
        [InlineKeyboardButton("🔙 Back", callback_data="text_settings_")]
    ])
    
    await msg.message.edit_caption(caption=caption, reply_markup=keyboard)

@bot.on_callback_query(filters.regex(r"wt_size_adjust_(-?\d+)"))
async def adjust_font_size(bot: Client, msg: CallbackQuery):
    delta = int(msg.data.split("_")[-1])
    user = get_user_status(msg.from_user.id, bot.me.username)
    current = int(user.get('data', {}).get('fontSize', '80'))
    new_size = max(50, min(200, current + delta))
    
    await update_user_settings(msg.from_user.id, bot.me.username, font_size=str(new_size))
    await watermark_size_menu(bot, msg)

@bot.on_callback_query(filters.regex("wt_size_input"))
async def input_font_size(bot: Client, msg: CallbackQuery):
    sent = await msg.message.reply_text(
        "📝 Please reply with a number between 50-200:",
        reply_markup=ForceReply(selective=True)
    )
    pending_size_input[msg.from_user.id] = True
    await msg.answer()

@bot.on_message(filters.reply & filters.text & ~filters.command(["cancel"]))
async def handle_font_size_input(bot: Client, message: Message):
    user_id = message.from_user.id
    if pending_size_input.get(user_id):
        try:
            size = int(message.text.strip())
            if 50 <= size <= 200:
                await update_user_settings(user_id, bot.me.username, font_size=str(size))
                await message.reply_text(f"✅ Font size set to {size}")
                pending_size_input.pop(user_id, None)
            else:
                await message.reply_text("❌ Size must be between 50-200. Try again or /cancel")
        except ValueError:
            await message.reply_text("❌ Please enter a valid number.")


@bot.on_callback_query(filters.regex("wt_opacity_menu"))
async def opacity_menu(bot: Client, msg: CallbackQuery):
    user = get_user_status(msg.from_user.id, bot.me.username)
    current_opacity = float(user.get('data', {}).get('opacity', '0.8'))
    
    caption = (
        f"<blockquote><b>Set Watermark Opacity</b></blockquote>\n\n"
        f"Current opacity: <b>{current_opacity}</b>\n"
        f"• Range: 0.1 to 1.0\n"
        f"• Lower = more transparent\n\n"
        f"Send a value like 0.7 or use buttons:"
    )
    
    quick_values = [0.2, 0.4, 0.6, 0.8, 1.0]
    row = []
    for val in quick_values:
        row.append(InlineKeyboardButton(str(val), callback_data=f"wt_opacity_set_{val}"))
    
    keyboard = InlineKeyboardMarkup([
        row,
        [InlineKeyboardButton("✍️ Enter Manually", callback_data="wt_opacity_input")],
        [InlineKeyboardButton("🔙 Back", callback_data="text_settings_")]
    ])
    
    await msg.message.edit_caption(caption=caption, reply_markup=keyboard)

@bot.on_callback_query(filters.regex(r"wt_opacity_set_(.*)"))
async def set_opacity(bot: Client, msg: CallbackQuery):
    opacity = msg.data.split("_")[-1]
    await update_user_settings(msg.from_user.id, bot.me.username, opacity=opacity)
    await msg.answer(f"Opacity set to {opacity}", show_alert=True)
    await text_watermark_main(bot, msg)

@bot.on_callback_query(filters.regex("wt_opacity_input"))
async def input_opacity(bot: Client, msg: CallbackQuery):
    sent = await msg.message.reply_text(
        "💧 Please reply with a number between 0.1 and 1.0:",
        reply_markup=ForceReply(selective=True)
    )
    pending_opacity_input[msg.from_user.id] = True
    await msg.answer()

@bot.on_message(filters.reply & filters.text & ~filters.command(["cancel"]))
async def handle_opacity_input(bot: Client, message: Message):
    user_id = message.from_user.id
    if pending_opacity_input.get(user_id):
        try:
            opacity = float(message.text.strip())
            if 0.1 <= opacity <= 1.0:
                await update_user_settings(user_id, bot.me.username, opacity=str(opacity))
                await message.reply_text(f"✅ Opacity set to {opacity}")
                pending_opacity_input.pop(user_id, None)
            else:
                await message.reply_text("❌ Opacity must be between 0.1 and 1.0")
        except ValueError:
            await message.reply_text("❌ Please enter a valid number.")


@bot.on_callback_query(filters.regex("wt_toggle"))
async def toggle_watermark(bot: Client, msg: CallbackQuery):
    user = get_user_status(msg.from_user.id, bot.me.username)
    current = user.get('data', {}).get('watermarkEnabled', 'yes')
    new_state = 'no' if current == 'yes' else 'yes'
    await update_user_settings(msg.from_user.id, bot.me.username, watermark_enabled=new_state)
    await msg.answer(f"Watermark {'Enabled' if new_state == 'yes' else 'Disabled'}", show_alert=True)
    await text_watermark_main(bot, msg)


# ========================== OLD TEXT WATERMARK CALLBACK (Keep as is) ==========================
@bot.on_callback_query(filters.regex("wt_text_"))
async def set_text_watermark(bot: Client, msg: CallbackQuery):
    editable = await msg.message.reply_text(f"Now Send the **TEXT** for overlay or Send `no` for no Overlay")
    input: Message = await bot.ask(msg.message.chat.id, "")
    try:
        result = await update_user_settings(msg.from_user.id, bot.me.username, default_name=None, extension_name=None, pdf_thumbnail=None, vid_thumbnail=None, watermark_color=None, text_watermark=input.text, quality=None, captStyle=None, ytcookie=None, pwtoken=None, credit=None)
        if str(input.text).lower() != "no":
            await msg.answer("Congratulation 🎉 Text Overlay has been Updated ✅.", show_alert=True)
        else:
            await msg.answer("Congratulation 🎉 Text Overlay has been Disabled ❌.", show_alert=True)
        await input.delete()
        await editable.delete()
        await back_to_st(bot, msg)
    except Exception as e:
        logging.error(f"{e}")
        pass


@bot.on_message(filters.command("reboot"))
@checkUser_PremiumStatus()
async def clean_heroku(_, m: Message):
    await m.reply_text("<blockquote>Be Patient! BOT's System is Rebooting..🔄️</blockquote>")
    
    gc.collect()  # Run garbage collection
    await helper.check_and_clear_temp_files()
    logging.info("[✔] Unused memory cleared.")
    sys.exit(0)

@bot.on_message(filters.command("root"))
@checkUser_PremiumStatus()
async def root_command(_, msg: Message):
    await msg.reply_text("<blockquote><b>Bot Rooted Sucessfully.</b></blockquote>", True)
    await helper.check_and_clear_temp_files()
    os.execl(sys.executable, sys.executable, *sys.argv)

@bot.on_message(filters.command("ytplaylist"))
@checkUser_PremiumStatus()
async def ytplaylist_to_txt(_, m):
  editable = await bot.send_message(m.chat.id, "Please send the YouTube playlist URL")
  input = await bot.ask(m.chat.id, "")
  channel_url = input.text.strip()
  await input.delete(True)
  await editable.edit("Extracting videos... This might take a while for channels with many videos...")
  
  video_links, channel_name = get_all_videos(channel_url)
  if video_links and channel_name:
    """Save videos to file with better formatting."""
    sanitized_channel_name = re.sub(r'[^\w\s-]', '', channel_name).strip()
    sanitized_channel_name = re.sub(r'\s+', '_', sanitized_channel_name)
    if not sanitized_channel_name:
      sanitized_channel_name = "Unknown_Channel"
    
    filename = f"{sanitized_channel_name}.txt".replace("_", "")
    with open(filename, 'w', encoding='utf-8') as file:
      for number, (title, url) in video_links.items():
        formatted_url = format_video_url(url)
        if formatted_url:
          file.write(f"{title}: {formatted_url}\n")

    await bot.send_document(m.chat.id, document=filename, caption=f"Here is the .txt file of video list from {channel_name}")
  else:
    await editable.edit("Failed to extract videos. Please check the URL and try again.")
  



# Make sure this directory exists
REPO_DIR = ""
@bot.on_message(filters.command("json"))
@checkUser_PremiumStatus()
async def handle_json_file(_, message):
  editable = await bot.send_message(message.chat.id, "Send Your YouTube Token JSON") 
  input_doc = await bot.ask(message.chat.id, "")
  document = input_doc.document
  await input_doc.delete(True)

  # Check if it's a .json file
  if not document.file_name.endswith(".json"):
    await message.reply("Please send only a .json file.")
    return

  await editable.delete(True)
  # Download the file
  file_path = await input_doc.download()

  # Read and parse JSON
  try:
    with open(file_path, "r", encoding="utf-8") as f:
      data = json.load(f)
  except json.JSONDecodeError:
    await message.reply("This is not a valid JSON file.")
    return

  # Print JSON data in console
  logging.info("Received JSON data: %s", json.dumps(data, indent=2))

  # Save to repository directory with a fixed name
  save_path = os.path.join(REPO_DIR, "token.json")
  with open(save_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

  await message.reply(f"JSON file has been saved successfully: {save_path}")




def send_startup_message():
    current_time = helper.get_current_time_ist()
    resp = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/getMe").json()
    try:
        username = resp['result']['username']
        activeUser = list(ActiveUsersCollection.find({"bot": username}))
        for data in activeUser:
            user_id = data.get('userId', 7974818772)
            start_msg = (
                f"<blockquote>Welcome Back, <b>Dear User</b>!!</blockquote>\n\n"
                f"🔄️ <b><u>Bot Status Update</u> :</b>\n"
                f"<b>• Successfully Restarted at :</b> {current_time}\n"
                f"<b>• Running Version :</b> {BotVersion} \n"
                f"<b>• All Features are Working Perfectly.</b>\n\n"
                f"<blockquote><b>❤️ Thanks for being an Awesome User!</b></blockquote>"
            )
            requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", data={"chat_id": user_id,  "text": start_msg, "parse_mode": "HTML"})
            logging.info("[✔] Startup message sent.")
    except Exception as e:
        logging.warning(f"❗ Failed to send startup message: {str(e)}")

def reset_and_set_commands():
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/setMyCommands"
    requests.post(url, json={"commands": []})
    commands = [
        {"command": "start", "description": "🏁 To Fire Up The Bot"},
        {"command": "id", "description": "🆔 Get Your ID"},
        {"command": "info", "description": "🪪 Get Your Plan Details"},
        {"command": "help", "description": "🆘 If you're a noob, still!"},
        {"command": "drm", "description": "📃 Send/Upload Your .txt File"},
        {"command": "stop", "description": "🚫 Stop the current Ongoing Process"},
        {"command": "settings", "description": "⚙️ Default Bot Upload Settings"},
        {"command": "cookies", "description": "🍪 To Upload Yt cookies for YT dl.."},
        {"command": "terms", "description": "📜 Terms & Conditions"},
        {"command": "ytplaylist", "description": "🌐 YouTube → .txt Converter"},
        {"command": "txt", "description": "📜 Text → .txt Convertor.."},
        {"command": "root", "description": "🔄 refresh & reload all database info & Stop all the Ongoing Processes"},
        {"command": "reboot", "description": "🔋 charge & reload the BOT..."}
    ]
    requests.post(url, json={"commands": commands})

if __name__ == "__main__":
    logging.info("🟢🟢🟢 Starting bot...🟢🟢🟢")
    reset_and_set_commands()
    try:
        send_startup_message()
    except Exception:
        pass
    bot.run()