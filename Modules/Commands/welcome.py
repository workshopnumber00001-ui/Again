import asyncio
from datetime import datetime
from pyrogram import filters, Client
from pyrogram.types import Message, InputMediaPhoto, CallbackQuery
from config import *
from DbNew import *
from Tools.buttons import *


async def check_channel_membership(bot, msg):
  try:
    member = await bot.get_chat_member(FORCE_JOIN_CHANNEL, msg.chat.id)
    if member.status == "left" or member.status == "kicked":
      return False
  except:
    return False
  return True

async def join_channel_if_needed(bot, msg):
  if not await check_channel_membership(bot, msg):
    await msg.reply_text("<b><u>✨ Please join our channel to access this feature ✨.</b></u>", reply_markup=FORCE_JOIN_BUTTON)
    return False
  return True


# ====================== WELCOME MESSAGE =======================
class Data: 
    START = ("🌟 Welcome {0}! 🌟\n\n")

@bot.on_message(filters.command("start"))
async def start(bot: Client, msg: Message):
    start_message = await bot.send_photo(msg.chat.id, photo="https://ibb.co/cSP9xphs", caption=f"<blockquote>🌟 Welcome {msg.from_user.mention}! 🌟</blockquote>")

    await asyncio.sleep(1)
    await start_message.edit_text(Data.START.format(msg.from_user.mention) + "<blockquote>Initializing Uploader bot... 🤖</blockquote>\n\nProgress: [⬜⬜⬜⬜⬜⬜⬜⬜⬜] 0%\n\n")

    await asyncio.sleep(1)
    await start_message.edit_text(Data.START.format(msg.from_user.mention) + "<blockquote>Loading features... ⏳</blockquote>\n\nProgress: [🟥🟥🟥⬜⬜⬜⬜⬜⬜] 25%\n\n")
  
    await asyncio.sleep(1)
    await start_message.edit_text(Data.START.format(msg.from_user.mention) + "<blockquote>This may take a moment, sit back and relax! 😊</blockquote>\n\nProgress: [🟧🟧🟧🟧🟧⬜⬜⬜⬜] 50%\n\n")

    await asyncio.sleep(1)
    await start_message.edit_text(Data.START.format(msg.from_user.mention) + "<blockquote>Checking subscription status... 🔍</blockquote>\n\nProgress: [🟨🟨🟨🟨🟨🟨🟨⬜⬜] 75%\n\n")

    user = get_user_status(msg.chat.id, bot.me.username)
    if msg.from_user.id in owner_id:
        await asyncio.sleep(1)
        await start_message.edit_media(InputMediaPhoto(caption="Welcome to Owner/Admin Pannel", media="Modules/Tools/Thumbnail/AdminDashboard.jpg"), reply_markup=OwnerButton)
    
    elif user['status'] == "active":
        await asyncio.sleep(1)
        join_date_ist = IST.localize(datetime.strptime(user['data']['createdAtIST'], "%I:%M:%S %p  %d-%m-%Y"))
        end_date_ist= IST.localize(datetime.strptime(user['data']['expiresAtIST'], "%I:%M:%S %p  %d-%m-%Y"))
        SubsDuration = end_date_ist - join_date_ist
        SubDays = SubsDuration.days
        SubHrs, SubRemainder = divmod(SubsDuration.seconds, 3600)
        SubMins, SubSec = divmod(SubRemainder, 60)
        
        time_diff = end_date_ist - datetime.now(IST)
        days = time_diff.days
        hours, remainder = divmod(time_diff.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        st_paid_msg = (
            f"<blockquote>🌟 Welcome <b>{msg.from_user.mention}</b> !</blockquote>\n\n"
            f"<blockquote expandable><b><u>Great! You are a Premium Member</u>! 🌟</b>\n\n"
            f"<b>⏰ Join Datetime :</b> {user['data']['createdAtIST']}\n"
            f"<b>📅 Subscription Duration :</b> {SubDays} Days, {SubHrs} Hours, {SubMins} Minutes\n"
            f"<b>⏰ Expiry DateTime :</b> {user['data']['expiresAtIST']}\n"
            f"<b>⌛ Remaining Time :</b> {days} Days, {hours} Hours, {minutes} Minutes & {seconds} Seconds</blockquote>\n\n"
            f"<blockquote>**🤖 Subscription Type :** <u>{user['data']['planType']}</u>\n"
            f"**➠ 𝐌𝐚𝐝𝐞 𝐁𝐲 : {user['data']['CreditName']}**</blockquote>\n\n"
            f"<blockquote>Press **Help Button** or /help To Use Me Properly</blockquote>")
        await start_message.edit_media(InputMediaPhoto(caption=st_paid_msg, media="https://envs.sh/qho.jpg"), reply_markup=HELP_BUTTON)
    
    elif user['status'] == "expired":
        await asyncio.sleep(1)
        st_free_msg = (
            f"<blockquote>🌟 Welcome **{msg.from_user.mention}** !</blockquote>\n\n"
            f"**⚠️ Your Previous Subscription has been Expired ⚠️.**\n\n"
            f"<b>⏰ Joined Time :</b> {user['data']['createdAtIST']}\n"
            f"<b>⏰ Expired Time :</b> {user['data']['expiresAtIST']}\n\n"
            f"💬 **Contact : {user['data']['CreditName']}** to Renew The Subscription 🎫 and unlock the full potential of your Bot! 🔓")
        await start_message.edit_media(InputMediaPhoto(caption=st_free_msg, media="https://envs.sh/qQY.jpg"), reply_markup=FREE_BUTTON)
    
    else:
        await asyncio.sleep(0.5)
        st_free_msg = (
            f"<blockquote>🌟 Welcome **{msg.from_user.mention}** !</blockquote>\n\n"
            f"**You are currently using the free version.** 🆓\n\n"
            f"Im here to make your life easier by downloading videos from your **.txt** file 📄 and uploading them directly to Telegram!\n\n"
            f"**Want to get started? Press /id**\n\n"
            f"💬 **Contact : [『 𝐓𝐇𝐎𝐑 🧑‍💻 』™](t.me/Stormy_thor)** to Get The Subscription 🎫 and unlock the full potential of your new bot! 🔓")
        await start_message.edit_media(InputMediaPhoto(caption=st_free_msg, media="https://envs.sh/qQY.jpg"), reply_markup=FREE_BUTTON)


#======================== PLAN INFO =============================
@bot.on_callback_query(filters.regex("upgrade_command"))
async def upgrade_button(_, callback_query: CallbackQuery):
    await callback_query.message.edit_media(InputMediaPhoto(media="https://envs.sh/qEU.jpg", caption="<b>Choose Subscription Type according to Your Needs.</b>"),
        reply_markup=PLAN_BUTTON
    )
    await callback_query.answer()

@bot.on_callback_query(filters.regex("plan1_"))
async def normal_plan_button(_, callback_query: CallbackQuery):
    caption = (
       "<blockquote>🟢 <b><u>PLAN TYPE</u> : NORMAL</b> 🟢\n"
       "🌟 <i>Only Non-DRM Unlocked 🔓</i></blockquote>\n\n"
       "<blockquote><b>⏰ <u>Duration</u> & 💸 <u>Price Details</u> :</b>\n"
       "<b>(◉) 15 Days :</b> 250 ₹\n"
       "<b>(◉) 30 Days :</b> 400 ₹</blockquote>\n\n"
       "<blockquote>✅ <b><u>Download Supported</u> :</b></blockquote>\n"
       "<b>◉</b> All Non-DRM\n"
       "<b>◉</b>⁠ YT links (Cookies Your)\n"
       "⁠<b>◉</b> VidCrypt Application (Non-DRM)\n"
       "<b>◉</b> All Appx (Non-Zip)\n"
       "<b>◉</b> SeeDablu (Non-DRM)\n"
       "<b>◉</b> Classplus (N-DRM)\n"
       "<b>◉</b>⁠ Some Other Apps Support too"
    )
    try: await callback_query.message.edit_media(InputMediaPhoto(media="https://envs.sh/qEU.jpg", caption=caption), reply_markup=PLAN_BUTTON)
    except Exception as e: pass
    await callback_query.answer()

@bot.on_callback_query(filters.regex("plan2_"))
async def pro_plan_button(_, callback_query: CallbackQuery):
    caption = (
       "<blockquote>🔵 <b><u>PLAN TYPE</u> : PRO</b> 🔵\n"
       "🌟 <i>Moderate Level 🗡️</i></blockquote>\n\n"
       "<blockquote><b>⏰ <u>Duration</u> & 💸 <u>Price Details</u> :</b>\n"
       "<b>(◉) 7 Days :</b> 250 ₹\n"
       "<b>(◉) 15 Days :</b> 450 ₹\n"
       "<b>(◉) 30 Days :</b> 800 ₹</blockquote>\n\n"
       "<blockquote>✅ <b><u>Download Supported</u> :</b></blockquote>\n"
       "<b>◉</b> All Non-DRM\n"
       "<b>◉</b>⁠ YT links (Cookies Your)\n"
       "⁠<b>◉</b> VidCrypt Application (Drm too : If keys attached)\n"
       "<b>◉</b> All Appx (Non-Zip)\n"
       "<b>◉</b> SeeDablu (Drm too)\n"
       "<b>◉</b> Classplus (Drm + N-Drm)\n"
       "<b>◉</b> Physics Wallah\n"
       "<b>◉</b> Adda247 (Video + pdf)\n"
       "<b>◉</b> Vission IAS (Normal)\n"
       "<b>◉</b> Other Drm Url if Keys is Known\n"
       "<b>◉</b>⁠ Some Special Apps Support too\n\n"
       "<blockquote>✅ <b><u>Other Feature Includes</u> :</b></blockquote>\n"
       "<b>(◕)</b> Premium Corner Extraction [Extractor Bot]"
    )
    try: await callback_query.message.edit_media(InputMediaPhoto(media="https://envs.sh/qEU.jpg", caption=caption), reply_markup=PLAN_BUTTON)
    except Exception as e: pass
    await callback_query.answer()

@bot.on_callback_query(filters.regex("plan3_"))
async def conqueror_plan_button(_, callback_query: CallbackQuery):
    caption = (
       "<blockquote>🟣 <b><u>PLAN TYPE</u> : CONQUEROR</b> 🟣\n"
       "🌟 <i>Advanced Level ⚔️</i></blockquote>\n\n"
       "<blockquote><b>⏰ <u>Duration</u> & 💸 <u>Price Details</u> :</b>\n"
       "<b>(◉) 7 Days :</b> 300 ₹\n"
       "<b>(◉) 15 Days :</b> 550 ₹\n"
       "<b>(◉) 30 Days :</b> 950 ₹</blockquote>\n\n"
       "<blockquote>✅ <b><u>Download Supported</u> :</b></blockquote>\n"
       "<b>◉</b> All Non-DRM\n"
       "<b>◉</b>⁠ YT links (Cookies Your)\n"
       "⁠<b>◉</b> VidCrypt Application (Drm too : If keys attached)\n"
       "<b>◉</b> Spaaye/Graphy (vid+pdf)\n"
       "<b>◉</b> All Appx (All Non-Zip)\n"
       "<b>◉</b> SeeDablu (Drm too)\n"
       "<b>◉</b> Classplus (Drm + N-Drm)\n"
       "<b>◉</b> Physics Wallah [Khazana too]\n"
       "<b>◉</b> Adda247 (Video + pdf)\n"
       "<b>◉</b> Vission IAS (Normal)\n"
       "<b>◉</b> Other Drm Url if Keys is Known\n"
       "<b>◉</b>⁠ Some Special Apps Support too\n\n"
       "<blockquote>✅ <b><u>Other Feature Includes</u> :</b></blockquote>\n"
       "<b>(⁠◕⁠)</b> Txt Log Channel Access\n"
       "<b>(◕)</b> Premium Corner Extraction [Extractor Bot]\n"
       "<b>(⁠◕)</b> Some Apps without Purchase [Extractor Bot]\n"
    )
    try: await callback_query.message.edit_media(InputMediaPhoto(media="https://envs.sh/qEU.jpg", caption=caption), reply_markup=PLAN_BUTTON)
    except Exception as e: pass
    await callback_query.answer()

@bot.on_callback_query(filters.regex("plan4_"))
async def legend_plan_button(_, callback_query: CallbackQuery):
    caption = (
       "<blockquote>🟠 <b><u>PLAN TYPE</u> : LEGEND</b> 🟠\n"
       "🌟 <i>God-Mode ✨ All Unlocked 🔓</i></blockquote>\n\n"
       "<blockquote><b>⏰ <u>Duration</u> & 💸 <u>Price Details</u> :</b>\n"
       "<b>(◉) 7 Days :</b> 400 ₹\n"
       "<b>(◉) 15 Days :</b> 700 ₹\n"
       "<b>(◉) 30 Days :</b> 1200 ₹</blockquote>\n\n"
       "<blockquote>✅ <b><u>Download Supported</u> :</b></blockquote>\n"
       "<b>◉</b> All Non-DRM\n"
       "<b>◉</b>⁠ YT links (Cookies Your)\n"
       "⁠<b>◉</b> VidCrypt Application (Drm too : If keys attached)\n"
       "<b>◉</b> Cipher Drm (if Keys is attached with url or key is known)\n"
       "<b>◉</b> Spaaye/Graphy (vid+pdf)\n"
       "<b>◉</b> All Appx (Zip too : All version)\n"
       "<b>◉</b> SeeDablu (Drm too)\n"
       "<b>◉</b> Classplus (Drm + N-Drm)\n"
       "<b>◉</b> Physics Wallah [Khazana too]\n"
       "<b>◉</b> Adda247 (Video + pdf)\n"
       "<b>◉</b> Vission IAS (Normal)\n"
       "<b>◉</b> Other Drm Url if Keys is Known\n"
       "<b>◉</b>⁠ Some Special Apps Support too\n\n"
       "<blockquote>✅ <b><u>Other Feature Includes</u> :</b></blockquote>\n"
       "<b>(⁠◕⁠)</b> Txt Log Channel Access\n"
       "<b>(◕)</b> Premium Corner Extraction [Extractor Bot]\n"
       "<b>(⁠◕)</b> Some Apps without Purchase [Extractor Bot]\n"
       "<b>(⁠◕)</b> You can chnage bot CreditName (Made by..... wala name) [Uploader Bot]\n"
    )
    try: await callback_query.message.edit_media(InputMediaPhoto(media="https://envs.sh/qEU.jpg", caption=caption), reply_markup=PLAN_BUTTON)
    except Exception as e: pass
    await callback_query.answer()


ftCapt = (
    "<blockquote>🔻 <b><u>TXT to VIDEO Uplaoder BOT's Features</u> :🔻</b>\n\n"
    "<i>    ⪼  <b>U can Upload videos of more than 2GB size.</b>\n"
    "    ⪼  Auto Topic Creation in group & Uplaod Video in Group Topic with Automation Feature..\n"
    "    ⪼  Auto Pin 📌 Batch Name in group/channel/Bot's DM.\n"
    "    ⪼  Auto Pin 📌 topic Name in group Topics.\n"
    "    ⪼  U can add Your Name as Watermark on Videos 🤗  [Watermark text color is changable too..]\n"
    "    ⪼  Video + Pdf Image Thumbnail also support\n"
    "    ⪼  U have also a option to change Caption Style\n"
    "    ⪼  Your Name as File name too</i></blockquote>\n\n"
    "<blockquote>🔻 <b><u>Extractor BOT's Features</u> :🔻</b>\n\n"
    "    ⪼ Many Plattform Extraction Support\n"
    "    ⪼ Txt Split Feature as Topic-Wise\n"
    "    ⪼ Txt to html Feature [ Topic Wise folder in html too]</blockquote>\n"
)
@bot.on_callback_query(filters.regex("feat_command"))
async def feature_button(_, callback_query: CallbackQuery): 
    await callback_query.message.edit_media(
        InputMediaPhoto(media="https://envs.sh/qHV.jpg", caption=ftCapt),
        reply_markup=FT_BUTTON
    )
    await callback_query.answer()

@bot.on_callback_query(filters.regex("back_to_ft"))
async def back_to_ft(_, callback_query: CallbackQuery):
    await callback_query.message.edit_media(
        InputMediaPhoto(media="https://envs.sh/qHV.jpg", caption=ftCapt),
        reply_markup=FT_BUTTON
    )
    await callback_query.answer()

@bot.on_callback_query(filters.regex("2gb_command"))
async def pin_button(_, callback_query: CallbackQuery):
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Feature", callback_data="back_to_ft")]])
    caption = f"**Example for 📂 2GB+ File Supported :**\nSupported Large Files over 2GB, with Automatically Spilling into Parts."
    await callback_query.message.edit_media(
        InputMediaPhoto(media="https://ibb.co/twmRYxyL",caption=caption),
        reply_markup=keyboard
    )

@bot.on_callback_query(filters.regex("editor_command"))
async def editor_button(_: Client, callback_query: CallbackQuery):
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Feature", callback_data="back_to_ft")]])
    caption = f"<blockquote>**🤖 Available Commands**</blockquote>\n\n◆ /h2t - Convert HTML file into TEXT file.\n◆ /h2p - Convert HTML file into PDF file.\n\n**📝 Usage 📘:**\n◆/h2t - Converts an HTML file into plain text format.\n◆/edit_txt - Edits a TXT file by adding names, removing words, or cleaning the file.\n◆/json2txt-Converts a JSON file to a TXT file.\n/correct_json-Corrects formatting issues in a JSON file.\n◆/split_txt- Splits a TXT file containing links into separate lines."
    await callback_query.message.edit_media(
        InputMediaPhoto(media="https://ibb.co/nNvdpgHZ",caption=caption),
        reply_markup=keyboard
    )
