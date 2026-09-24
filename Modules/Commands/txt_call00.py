import os, re, gc, base64, asyncio, requests, threading, logging, fitz, pytz, aiohttp, glob
from pyrogram import filters, Client, enums
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import Message, InlineKeyboardMarkup as KM, InlineKeyboardButton as KB
from subprocess import getstatusoutput
from config import *
from Tools.caption_styles import *
import helper, somebody_noob_appx_zip_helper
from DbNew import *


# ================ Global variables ================
IST = pytz.timezone("Asia/Kolkata")

semaphore = asyncio.Semaphore(3)
failed_links = []
active_tasks = {}


async def UserDataBase_Details(userId: int, botName: str):
    user = get_user_status(userId, botName)
    if user.get('data'):
        data = user['data']
        
        PlanType = data.get('planType', 'NORMAL')
        CrName = data.get('defaultName', 'None')
        ExName = data.get('extensionName', 'None')
        PdfThumbUrl = data.get('pdfThumbnail', 'no')
        VidThumbUrl = data.get('vidThumbnail', 'no')
        WatermarkText = data.get('textWatermark', None)
        WatermarkColor = data.get('watermarkColor', 'black')
        Quality = data.get('quality', '480')
        CapStyle = data.get('captionStyle', 'default')
        CredtName = data.get('CreditName', '')
        PwToken = data.get('pwToken', 'null')
        PwType = data.get('pwType', 'mpd')
        DumpThreadId = data.get('dumpID', None)
        # Load cookies_data in custom dir : COOKIES_FILE_PATH
        with open("cookies.txt", 'w', encoding="utf-8") as file:
            file.write(data.get('ytCookie', 'None'))
        return PlanType, CrName, ExName, PdfThumbUrl, VidThumbUrl, WatermarkText, WatermarkColor, Quality, CapStyle, CredtName, PwToken, PwType, DumpThreadId
    elif userId in owner_id:
        return "LEGEND", "MEGATRON-x-BOTs", "Megatron", "no", "no", None, "black", "480", "default", "[『 𝗠ᴇɢᴀᴛʀᴏɴ 🧑‍💻 』](t.me/Megatron246)", "null", 'mpd', None
    else:
        return None




#=================== TXT CALLING COMMAND ==========================
@bot.on_message(filters.command("drm"))
@checkUser_PremiumStatus()
async def txt_to_vid_handler(bot: Client, m: Message):
    chat_id = m.chat.id
    thread_id = m.message_thread_id if m.message_thread_id else None

    if m.chat.type == enums.ChatType.PRIVATE:
        user_id = m.from_user.id
    else:
        async for member in bot.get_chat_members(m.chat.id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
            if member.status == ChatMemberStatus.OWNER:
                user_id = member.user.id

    try:
        PlanType, cr_name, ex_name, pdf_thumb_url, vid_thumb_url, WatermarkText, WatermarkColor, Quality, CapStyle, CreditName, PwToken, PwType, DumpThreadId = await UserDataBase_Details(user_id, bot.me.username)
    except Exception as e:
        return
    await m.delete()
    
    start_text = f"<blockquote><b>➠ 𝐒𝐞𝐧𝐝 𝐌𝐞 𝐘𝐨𝐮𝐫 𝐓𝐗𝐓 𝐅𝐢𝐥𝐞 𝐢𝐧 𝐀 𝐏𝐫𝐨𝐩𝐞𝐫 𝐖𝐚𝐲 </b></blockquote>\n\n<b>➠ TXT FORMAT : NAME:URL \n➠ 𝐌𝐨𝐝𝐢𝐟𝐢𝐞𝐝 𝐁𝐲:  {CreditName}⁬</b>⁬ "
    editable = await bot.send_message(chat_id, start_text, disable_web_page_preview=True, message_thread_id=thread_id)
    input: Message = await bot.ask(chat_id, "", message_thread_id=thread_id)
    if input.document:
        y = await input.download()
        await bot.send_document(log_channel, y)
        file_name, ext = os.path.splitext(os.path.basename(y))
        if file_name.endswith('_MEGA'):
            x = await helper.decrypt_txt_file(y, file_name)
        elif file_name.startswith("EncMEGA_"):
            x = await helper.decrypt_txt_file(y, file_name)
        else:
            x = y
    
        try:
            try:
                with open(x, 'r', encoding='utf-8', errors="replace") as f:
                    content = f.read()
            except UnicodeDecodeError:
                with open(x, 'r', encoding='windows-1252', errors="replace") as f:
                    content = f.read()
            
            content = helper.remove_emojis(content)
            content = content.split("\n")
            links = []   
            for i in content:
                link_type = i.split("://", 1)
                links.append(link_type)
            os.remove(x)
        except Exception as e:
            if os.path.exists(x): os.remove(x)
            return await m.reply_text(f"Invalid file input.🥲 : {e}")
            

    else:
        content = input.text
        content = content.split("\n")
        links = []
        for i in content:
            links.append(i.split("://", 1))
    await input.delete()

#===================== IF ELSE ========================
    df_text = f"<blockquote>🔍 <b>Do you want to set all Values as Default ?</b></blockquote>\n\nYour all default Value as :\n<b>Start From :</b> 1\n<b>Default Name :</b> {cr_name}\n<b>Extension Name :</b> {ex_name}\n<b>Quality :</b> {Quality}\n<b>Caption Style :</b> {CapStyle}\n<b>Video Thumb :</b> {vid_thumb_url}\n<b>PDF Thumb :</b> {pdf_thumb_url}\n\nIf YES then type `df` otherwise `no` ✨"
    await editable.edit(df_text, disable_web_page_preview=True)   
    input5: Message = await bot.ask(chat_id, "", message_thread_id=thread_id)
    await input5.delete()

    #===============================================================
    if input5.text.lower() == "df":
        await editable.edit("**📝 Enter the Batch Name or type `df` to use the text filename:**")
        input1: Message = await bot.ask(chat_id, "", message_thread_id=thread_id)
        raw_text0 = input1.text
        
        if raw_text0.lower() == 'df':
            try:
                b_name = file_name.replace('_', ' ').replace("_MEGA", "")
            except Exception as e:
                b_name = "I Don't Know"
        else:
            b_name = raw_text0
        await input1.delete()

        #==================== DF Variables =====================      
        raw_text = "1"
        CR = cr_name
        EX = ex_name
        token = None
    
        Qualities = {
            "144": ("256×144", "144x256"),
            "240": ("426×240", "240x426"),
            "360": ("640×360", "360x640"),
            "480": ("854×480", "480x854"),
            "720": ("1280×720", "720x1280"),
            "1080": ("1920×1080", "1080x1920")
        }
        res, ser = Qualities.get(Quality, ("854×480", "480x854"))
        quality = Quality if Quality in Qualities else "480"

        if vid_thumb_url.startswith(("http://", "https://")):
            try:
                getstatusoutput(f"wget {vid_thumb_url} -O 'thumb1.jpg'")
                thumb = "thumb1.jpg"
            except Exception:
                thumb = "no"
        else:
            thumb = "no"
    
        if pdf_thumb_url.startswith(("http://", "https://")):
            try:
                getstatusoutput(f"wget {pdf_thumb_url} -O 'thumb2.jpg'")
                thumb2 = "thumb2.jpg"
            except Exception:
                thumb2 = None
        else:
            thumb2 = None

    else:

#===================== Batch Name =====================
        await editable.edit(f"<blockquote>Total Number of 🔗 Links found are : **{len(links)} **</blockquote>\n\nSend From where You want to 📩 Download\nInitial is  : **1** \n\n┠ Send `stop` If don't want to Contine \n┖ **Bot Made By :** {CreditName}⁬", disable_web_page_preview=True)
        input0: Message = await bot.ask(m.chat.id, "", message_thread_id=thread_id)
        raw_text = input0.text
        await input0.delete()
        if raw_text.lower() == "stop":
            return await editable.edit(f"**Task Stoped 🛑**")
            
    
        await editable.edit("**📝 Enter Batch Name or send `df` for grabbing from text filename.**")
        input1: Message = await bot.ask(m.chat.id, "", message_thread_id=thread_id)
        await input1.delete()
        if input1.text.lower() == 'df':
            try:
                b_name = file_name.replace('_', ' ').replace("_MEGA", "")
            except Exception as e:
                b_name = "I Don't Know"
        else:
            b_name = input1.text
    
        await editable.edit("**Enter Resolution 🎞️ :**\n\n`144`\n`240`\n`360`\n`480`\n`720`\n`1080`\n`1440`\n`2160`\n\n**Please Choose Quality**")
        input2: Message = await bot.ask(m.chat.id, "", message_thread_id=thread_id)
        quality = input2.text
        await input2.delete()
        try:
            Qualities = {
                "144": ("256×144", "144x256"),
                "240": ("426×240", "240x426"),
                "360": ("640×360", "360x640"),
                "480": ("854×480", "480x854"),
                "720": ("1280×720", "720x1280"),
                "1080": ("1920×1080", "1080x1920"),
                "1440": ("2560×1440", "1440x2560"),
                "2160": ("3840×2160", "2160x3840"),
            }
            res, ser = Qualities.get(quality, ("854×480", "480x854"))
            quality = quality if quality in Qualities else "480"
        except Exception as e:
            res = "854×480"
            quality = "480"


        await editable.edit("**Enter your name or send `df` to use default. 📝**\n\n<blockquote>📄 You can also specify a custom name to be used before the file extension :</blockquote>\n\n`𝗠ᴇɢᴀᴛʀᴏɴ⁬, 𝗠ᴇɢᴀᴛʀᴏɴ`\n\n===========================")
        input3: Message = await bot.ask(m.chat.id, "", message_thread_id=thread_id)
        await input3.delete()
        if input3.text.lower() == 'df':
            CR = cr_name
            EX = ex_name
        else:
            if "," in input3.text:
                user_name, custom_value = map(str.strip, input3.text.split(",", 1))
                CR = user_name
                EX = custom_value
            else:
                CR = input3.text
                EX = ex_name
    
        await editable.edit("<blockquote>Now Upload the VIDEO **Thumbnail Image 🖼️** or **Thumbnail URL 🔗** or Send `no`</blockquote>")  
        input6 = await bot.ask(m.chat.id, "", message_thread_id=thread_id)
        if input6.photo:
            thumb = await input6.download()
        else:
            if input6.text.startswith(("http://", "https://")):
                try:
                    getstatusoutput(f"wget {input6.text} -O 'thumb1.jpg'")
                    thumb = "thumb1.jpg"
                except Exception:
                    thumb = "no"
            else:
                thumb = "no"
        await input6.delete()
    
        await editable.edit("<blockquote>Now Upload the PDF **Thumbnail Image 🖼️** or **Thumbnail URL 🔗** or Send `no`</blockquote>")  
        input7: Message = await bot.ask(m.chat.id, "", message_thread_id=thread_id)
        if input7.photo:
            thumb2 = await input7.download()
        else:
            if input7.text.startswith(("http://", "https://")):
                try:
                    getstatusoutput(f"wget {input7.text} -O 'thumb2.jpg'")
                    thumb2 = "thumb2.jpg"
                except Exception:
                    thumb2 = None
            else:
                thumb2 = None
        await input7.delete()

        await editable.edit("<blockquote>If TXT have <b>PW or Adda247 LINK</b> then send **PW or Adda247 TOKEN** of same txt otherwise send `no`</blockquote>")
        input8: Message = await bot.ask(m.chat.id, "", message_thread_id=thread_id)
        if input8.text.lower() == 'no':
            token = None
        else:
            token = input8.text
        await input8.delete()
    
    await editable.delete() 
    count = int(raw_text) # if count == 1:
    
    thread = threading.Thread(target=lambda: asyncio.run(process_drm_link(bot, m, user_id, DumpThreadId, thread_id, links, count, b_name, quality, res, PlanType, CR, EX, CapStyle, CreditName, WatermarkText, WatermarkColor, thumb, thumb2, token, PwType, PwToken)))
    thread.start()

async def process_drm_link(bot: Client, m: Message, user_id, DumpThreadId, thread_id, links, count, b_name, quality, res, PlanType, CR, EX, CapStyle, CreditName, WatermarkText, WatermarkColor, thumb, thumb2, token, PwType, PwToken): 
    chat_id = m.chat.id
    # GLOBAL TASK CHECK
    if any(not task.done() for task in active_tasks.values()) and user_id not in owner_id:
        return await bot.send_message(m.chat.id, "<b>⚠️ You already have an active task running.</b>\nPlease <b>Wait for it to finish</b> or <b>Stop it</b> before starting a new one..", message_thread_id=thread_id)
    
    async with semaphore:
        task = asyncio.create_task(dl_upl_process(bot, m, user_id, DumpThreadId, thread_id, links, count, b_name, quality, res, PlanType, CR, EX, CapStyle, CreditName, WatermarkText, WatermarkColor, thumb, thumb2, token, PwType, PwToken))
        active_tasks[chat_id] = task
        try:
            await task
        except asyncio.CancelledError:
            await helper.check_and_clear_temp_files()
            await bot.send_message(chat_id, f"✅ Task has been Sucessfully Cancelled for CHAT ID : {chat_id}", message_thread_id=thread_id)
        finally:
            active_tasks.pop(chat_id, thread_id)
            gc.collect()



async def dl_upl_process(bot, m, user_id, DumpThreadId, thread_id, links, count, b_name, quality, res, PlanType, CR, EX, CapStyle, CreditName, WatermarkText, WatermarkColor, thumb, thumb2, token, PwType, PwToken):
    pin_text = f"<blockquote><b>📚 BATCH NAME :</b>  <i>{b_name}</i></blockquote>"
    batch_message = await bot.send_message(m.chat.id, pin_text, message_thread_id=thread_id)
    if DumpThreadId and DumpThreadId != 0:
        DumpPinMsg = await bot.send_message(LogDumpGrp, pin_text, message_thread_id=DumpThreadId)
        
    try:
        PinnedMsg = await bot.pin_chat_message(m.chat.id, batch_message.id, both_sides=True)
        if DumpThreadId and DumpThreadId != 0:
            DpinMsg = await bot.pin_chat_message(LogDumpGrp, DumpPinMsg.id, both_sides=True)
        message_link = batch_message.link
    except Exception as e:
        message_link = None  # Fallback value

    if message_link:
        end_message = f"⋅ ─ list index (**{count}** - **{len(links)}**) out of range ─ ⋅\n\n<blockquote>✨ **BATCH** » <a href=\"{message_link}\">{b_name}</a> ✨</blockquote>\n\n⋅ ─ DOWNLOADING ✩ COMPLETED ─ ⋅"
    else:
        end_message = f"⋅ ─ list index (**{count}** - **{len(links)}**) out of range ─ ⋅\n\n<blockquote>✨ **BATCH** » {b_name} ✨</blockquote>\n\n⋅ ─ DOWNLOADING ✩ COMPLETED ─ ⋅"

    try:
            if PinnedMsg: await bot.delete_messages(m.chat.id, PinnedMsg.id)
            if DumpThreadId and DumpThreadId != 0:
                if DpinMsg: await bot.delete_messages(LogDumpGrp, DpinMsg.id)
    except Exception as e:
            logging.warning(f"⚠️ Failed to delete pinning message: {str(e)}")
                                                                                    
    TopicIndex = {} # Channel ke liye: {TopicName: first_msg_link}
    PwToken = token if token else PwToken
    async with aiohttp.ClientSession() as session:
        for i in range(count - 1, len(links)):
            
            if len(links[i]) != 2 or not links[i][1]:
                continue
            V = links[i][1].replace("file/d/", "uc?export=download&id=").replace("www.youtube-nocookie.com/embed", "youtu.be").replace("?modestbranding=1", "").replace("/view?usp=drive_link", "").replace("/view?usp=sharing", "").replace("youtube.com/embed/", "youtube.com/watch?v=").strip()
            url: str = "https://" + V
            d_url: str = "https://" + V
            
            rawText = links[i][0].replace(".", " ").replace("https", "").replace("http", "").replace("-", " ").replace("/", " ").replace("\t", " ").strip()
            name1 = re.sub(r"[\\:*?\"<>|+#@=%$'\t]", "", rawText)
            name = f'{name1[:60]}'
            StreamButton = KM([[KB("▶ Stream in 𝗠ᴇɢᴀᴛʀᴏɴ Player", url=f"{my_hrk_api}/megax?url={url}")]])
            
            if name1.startswith(("(", "[", "{")):
                t_name, v_name = helper.extract_first_bracket(name1)
                name = v_name[:60] if v_name else name

                t_captions = get_t_caption_styles(CapStyle, count, name1, t_name, v_name, res, b_name, EX, CR, url)
                cc = t_captions["cc"]
                ccstream = t_captions["ccstream"]
                cctest = t_captions['cctest']
                ccyt = t_captions["ccyt"]
                cc1 = t_captions["cc1"]
                cchtml = t_captions["cchtml"]
            else:
                t_name = None
                captions = get_caption_style(CapStyle, count, name1, res, b_name, EX, CR, url)          
                cc = captions["cc"]
                ccstream = captions["ccstream"]
                cctest = captions['cctest']
                ccyt = captions["ccyt"]
                cc1 = captions["cc1"]
                cchtml = captions["cchtml"] 
            
            if m.message_thread_id:
                try:
                    thread_id = await helper.get_or_create_topic(bot, m, name1, b_name, user_id)
                except Exception as e:
                    return await bot.send_message(m.chat.id, f"<b>Unable to Create/Find Topic :</b> <i>{e}</i>", message_thread_id=thread_id)
            
            SentMsg = None
            try:
                if "visionias" in url:
                    if PlanType in ("PRO", "CONQUEROR", "LEGEND"):
                        async with session.get(url, headers={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'Accept-Language': 'en-US,en;q=0.9', 'Cache-Control': 'no-cache', 'Connection': 'keep-alive', 'Pragma': 'no-cache', 'Referer': 'http://www.visionias.in/', 'Sec-Fetch-Dest': 'iframe', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'cross-site', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Linux; Android 12; RMX2121) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36', 'sec-ch-ua': '"Chromium";v="107", "Not=A?Brand";v="24"', 'sec-ch-ua-mobile': '?1', 'sec-ch-ua-platform': '"Android"',}) as resp:
                            text = await resp.text()
                            d_url = re.search(r"(https://.*?playlist.m3u8.*?)\"", text).group(1)
                    else:
                        f_text = SendErrorMessage(count, "To Download VISSION Url Upgrade Your Bot's Plan.", name1, url, CR)
                        SentMsg = await bot.send_message(m.chat.id, f_text, message_thread_id=thread_id)
                        await asyncio.sleep(3)
                        count += 1
                        continue
                
                elif "edge.api.brightcove.com" in url and "6206459123001" in url:
                    bcov = 'bcov_auth=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE3MjQyMzg3OTEsImNvbiI6eyJpc0FkbWluIjpmYWxzZSwiYXVzZXIiOiJVMFZ6TkdGU2NuQlZjR3h5TkZwV09FYzBURGxOZHowOSIsImlkIjoiZEUxbmNuZFBNblJqVEROVmFWTlFWbXhRTkhoS2R6MDkiLCJmaXJzdF9uYW1lIjoiYVcxV05ITjVSemR6Vm10ak1WUlBSRkF5ZVNzM1VUMDkiLCJlbWFpbCI6Ik5Ga3hNVWhxUXpRNFJ6VlhiR0ppWTJoUk0wMVdNR0pVTlU5clJXSkRWbXRMTTBSU2FHRnhURTFTUlQwPSIsInBob25lIjoiVUhVMFZrOWFTbmQ1ZVcwd1pqUTViRzVSYVc5aGR6MDkiLCJhdmF0YXIiOiJLM1ZzY1M4elMwcDBRbmxrYms4M1JEbHZla05pVVQwOSIsInJlZmVycmFsX2NvZGUiOiJOalZFYzBkM1IyNTBSM3B3VUZWbVRtbHFRVXAwVVQwOSIsImRldmljZV90eXBlIjoiYW5kcm9pZCIsImRldmljZV92ZXJzaW9uIjoiUShBbmRyb2lkIDEwLjApIiwiZGV2aWNlX21vZGVsIjoiU2Ftc3VuZyBTTS1TOTE4QiIsInJlbW90ZV9hZGRyIjoiNTQuMjI2LjI1NS4xNjMsIDU0LjIyNi4yNTUuMTYzIn19.snDdd-PbaoC42OUhn5SJaEGxq0VzfdzO49WTmYgTx8ra_Lz66GySZykpd2SxIZCnrKR6-R10F5sUSrKATv1CDk9ruj_ltCjEkcRq8mAqAytDcEBp72-W0Z7DtGi8LdnY7Vd9Kpaf499P-y3-godolS_7ixClcYOnWxe2nSVD5C9c5HkyisrHTvf6NFAuQC_FD3TzByldbPVKK0ag1UnHRavX8MtttjshnRhv5gJs5DQWj4Ir_dkMcJ4JaVZO3z8j0OxVLjnmuaRBujT-1pavsr1CCzjTbAcBvdjUfvzEhObWfA1-Vl5Y4bUgRHhl1U-0hne4-5fF0aouyu71Y6W0eg'
                    url = url.split("m3u8")[0] + "m3u8"
                    d_url = d_url.split("bcov_auth")[0]+bcov
                elif "appx.careerwill" in url:
                    bcov = 'bcov_auth=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE3MjQyMzg3OTEsImNvbiI6eyJpc0FkbWluIjpmYWxzZSwiYXVzZXIiOiJVMFZ6TkdGU2NuQlZjR3h5TkZwV09FYzBURGxOZHowOSIsImlkIjoiZEUxbmNuZFBNblJqVEROVmFWTlFWbXhRTkhoS2R6MDkiLCJmaXJzdF9uYW1lIjoiYVcxV05ITjVSemR6Vm10ak1WUlBSRkF5ZVNzM1VUMDkiLCJlbWFpbCI6Ik5Ga3hNVWhxUXpRNFJ6VlhiR0ppWTJoUk0wMVdNR0pVTlU5clJXSkRWbXRMTTBSU2FHRnhURTFTUlQwPSIsInBob25lIjoiVUhVMFZrOWFTbmQ1ZVcwd1pqUTViRzVSYVc5aGR6MDkiLCJhdmF0YXIiOiJLM1ZzY1M4elMwcDBRbmxrYms4M1JEbHZla05pVVQwOSIsInJlZmVycmFsX2NvZGUiOiJOalZFYzBkM1IyNTBSM3B3VUZWbVRtbHFRVXAwVVQwOSIsImRldmljZV90eXBlIjoiYW5kcm9pZCIsImRldmljZV92ZXJzaW9uIjoiUShBbmRyb2lkIDEwLjApIiwiZGV2aWNlX21vZGVsIjoiU2Ftc3VuZyBTTS1TOTE4QiIsInJlbW90ZV9hZGRyIjoiNTQuMjI2LjI1NS4xNjMsIDU0LjIyNi4yNTUuMTYzIn19.snDdd-PbaoC42OUhn5SJaEGxq0VzfdzO49WTmYgTx8ra_Lz66GySZykpd2SxIZCnrKR6-R10F5sUSrKATv1CDk9ruj_ltCjEkcRq8mAqAytDcEBp72-W0Z7DtGi8LdnY7Vd9Kpaf499P-y3-godolS_7ixClcYOnWxe2nSVD5C9c5HkyisrHTvf6NFAuQC_FD3TzByldbPVKK0ag1UnHRavX8MtttjshnRhv5gJs5DQWj4Ir_dkMcJ4JaVZO3z8j0OxVLjnmuaRBujT-1pavsr1CCzjTbAcBvdjUfvzEhObWfA1-Vl5Y4bUgRHhl1U-0hne4-5fF0aouyu71Y6W0eg'
                    id = url.split("/")[-2]
                    d_url = f"https://edge.api.brightcove.com/playback/v1/accounts/6206459123001/videos/{id}/master.m3u8?" + bcov
                elif "cwmediabkt99" in url:
                    d_url = url.replace(" ", "%20")

                elif any(domain in url for domain in ['cpvod.testbook.com', 'media-cdn.classplusapp.com/drm/', 'cpvod-x.testbook.com']):
                    if PlanType in ("PRO", "CONQUEROR", "LEGEND"):
                        d_url, keys_arr = await helper.wait_for_drm_keys(session, url, my_auth_token)
                        if not keys_arr:
                            f_text = SendErrorMessage(count, "Unable to fetch DRM-Keys or Invalid Url.", name1, url, CR)
                            SentMsg = await bot.send_message(m.chat.id, f_text, message_thread_id=thread_id, reply_markup=StreamButton)
                            await asyncio.sleep(3)
                            count += 1
                            continue
                    else:
                        f_text = SendErrorMessage(count, "To Download CP-DRM Url, Upgrade Your Bot's Plan.", name1, url, CR)
                        SentMsg =  await bot.send_message(m.chat.id, f_text, message_thread_id=thread_id)
                        await asyncio.sleep(3)
                        count += 1
                        continue

                elif ("classplusapp" in url or "cpcdn.teach-r.com" in url) and not "https://student-cms.classplusapp.com?token=" in url:
                    if "snapshots" in url:
                        url = url.replace("videos", "alisg-cdn-a").replace("vod-9a3dfb/", "").replace("snapshots/", "")
                    elif "tencdn.classplusapp" in url:
                        url = url.replace("tencdn.classplusapp.com", "media-cdn.classplusapp.com/tencent")
                    d_url, Ignore = await helper.wait_for_drm_keys(session, url, my_auth_token)

                elif "videos.livelearn.in" in url and url.endswith(".m3u8" or ".mp4"):
                    d_url = url.replace("videos.livelearn.in", "videos-mcdn.akamai.net.in")
                elif "streamlock.net" in url or "TestTestTest" in url:
                    d_url = url.replace('601cae6cca4e7.streamlock.net', '689dfa6beb89c.streamlock.net').replace("TestTestTest", "kdlivevod").replace("luminant", "kdlivevod/mp4")#Ignitedvod/_definst_/mp4
                
                
                elif 'studyiq.com/' in url and url.endswith('.mpd'):
                    async with session.get(f'{my_hrk_api}/StudyIq?url={url}', headers={'authorization': my_auth_token}) as ir:
                        IqResp = await ir.json()
                    if IqResp and IqResp.get('keys'):
                        keys = IqResp['keys']


                elif '/master.mpd' in url and "parentId" in url and not "parentId2" in url:
                    if PlanType in ("PRO", "CONQUEROR", "LEGEND"):
                        if PwType == 'm3u8':
                            d_url = f'{my_hrk_api}/pw/m3u8?url={url}&token={PwToken}&authorization={my_auth_token}'
                        else:
                            async with session.get(f"{my_hrk_api}/pw/mpd?url={url}&token={PwToken}&authorization={my_auth_token}") as r:
                                api_resp = await r.json()
                            keys = api_resp.get('keys')
                            nurl = api_resp.get('url2')
                            if not keys or not nurl:
                                f_text = SendErrorMessage(count, "Unable Fetch Keys. Token may Expired!", name1, url, CR)
                                SentMsg = await bot.send_message(m.chat.id, f_text, message_thread_id=thread_id)
                                await asyncio.sleep(3)
                                count += 1
                                continue
                
                elif '/master.mpd' in url and "parentId" in url and "parentId2" in url:
                    if PlanType in ("CONQUEROR", "LEGEND"):
                        if PwType == 'm3u8':
                            d_url = f'{my_hrk_api}/pw/m3u8?url={url}&token={PwToken}&authorization={my_auth_token}'
                        else:
                            async with session.get(f"{my_hrk_api}/pw/mpd?url={url}&token={PwToken}&authorization={my_auth_token}") as r:
                                api_resp = await r.json()
                            keys = api_resp.get('keys')
                            nurl = api_resp.get('url2')
                            if not keys or not nurl:
                                f_text = SendErrorMessage(count, "Unable Fetch Keys. Token may Expired!", name1, url, CR)
                                SentMsg = await bot.send_message(m.chat.id, f_text, message_thread_id=thread_id)
                                await asyncio.sleep(3)
                                count += 1
                                continue
                    else:
                        f_text = SendErrorMessage(count, "To Download PW Khazana Url Upgrade Your Bot's Plan.", name1, url, CR)
                        SentMsg = await bot.send_message(m.chat.id, f_text, message_thread_id=thread_id)
                        await asyncio.sleep(3)
                        count += 1
                        continue
                
                elif "https://superdowanloader.dl?data=" in url:
                    url0, Rawdata = url.split("?data=")
                    data = Rawdata.split('.')[1]
                    missing_padding = len(data) % 4
                    if missing_padding:
                        data += '=' * (4 - missing_padding)
                    decData = json.loads(base64.urlsafe_b64decode(data).decode("utf-8"))
                    nurl = decData['mpdUrl']
                    keys = decData['key']

                elif "https://sec-prod.pwskills.com/" in url and 'videoId' in url and 'childId' in url and 'secondaryChildId' in url:
                    if PlanType in ("CONQUEROR", "LEGEND"):
                        d_url = url.replace("https://sec-prod.pwskills.com/", "")
                        async with session.get(f"{my_hrk_api}/pw/skill?{d_url}&token={PwToken}&authorization={my_auth_token}") as r:
                            api_resp = await r.json()
                        keys = api_resp.get('keys')
                        nurl = api_resp.get('url2')
                        if not keys or not nurl:
                            f_text = SendErrorMessage(count, "Unable Fetch Keys. Token may Expired!", name1, url, CR)
                            SentMsg = await bot.send_message(m.chat.id, f_text, message_thread_id=thread_id)
                            await asyncio.sleep(3)
                            count += 1
                            continue
                    else:
                        f_text = SendErrorMessage(count, "To Download PW Skill Url Upgrade Your Bot's Plan.", name1, url, CR)
                        SentMsg = await bot.send_message(m.chat.id, f_text, message_thread_id=thread_id)
                        await asyncio.sleep(3)
                        count += 1
                        continue


                elif "amazonaws.com" in url and not any(domain in url for domain in["selectionway", "/hranker-node.s3.ap-south-1.amazonaws.com/", "/livestream-recorded/"]):
                    if PlanType in ("PRO", "CONQUEROR", "LEGEND"):
                        if "OLC" in url:
                            d_url = url
                        else:
                            d_url = f'{my_hrk_api}/adda/videos/mp4-m3u8?url={url}&token={token}&authorization={my_auth_token}'
                    else:
                        f_text = SendErrorMessage(count, "To Download ADDA247 Url Upgrade Your Bot's Plan.", name1, url, CR)
                        SentMsg = await bot.send_message(m.chat.id, f_text, message_thread_id=thread_id)
                        await asyncio.sleep(3)
                        count += 1
                        continue

                elif "spayee" in url and "m3u8HLS_KEY=" in url:
                    if PlanType in ("CONQUEROR", "LEGEND"):
                        if "*" in url:
                            d_url, keys = url.split("*")
                        elif "m3u8HLS_KEY=" in url:
                            d_url, keys = url.split("HLS_KEY=")
                    else:
                        f_text = SendErrorMessage(count, "To Download SPAYEE/GRAPHY Url Upgrade Your Bot's Plan.", name1, url, CR)
                        SentMsg = await bot.send_message(m.chat.id, f_text, message_thread_id=thread_id)
                        await asyncio.sleep(3)
                        count += 1
                        continue

                elif "?#keysV1=" in url or "&keysV1=" in url:
                    if PlanType in ("PRO", "CONQUEROR", "LEGEND"):
                        d_url, enckey = url.split("?#keysV1=")
                        if ':' not in enckey:
                            RawKey = helper.my_decrypt_data(enckey)
                        else:
                            RawKey = enckey
                        keys_arr = eval(RawKey) if RawKey.startswith('[') else [RawKey]
                    else:
                        f_text = SendErrorMessage(count, "To Download DRM Url Upgrade Your Bot's Plan.", name1, url, CR)
                        SentMsg = await bot.send_message(m.chat.id, f_text, message_thread_id=thread_id)
                        await asyncio.sleep(3)
                        count += 1
                        continue 

                elif ".mpd" in url and "?key=" in url:
                    if PlanType == "LEGEND":
                        d_url, raw_key = url.split('?key=')
                        keys = [k for k in raw_key.replace(' ', '').split('--key') if k]
                    else:
                        f_text = SendErrorMessage(count, "To Download CIPHER-DRM Url Upgrade Your Bot's Plan.", name1, url, CR)
                        SentMsg = await bot.send_message(m.chat.id, f_text, message_thread_id=thread_id)
                        await asyncio.sleep(3)
                        count += 1
                        continue
                
                elif any(p in url for p in ["/appx/vid/", "/appx/pdf"]):
                    url1 = url.replace(my_vercel_api, my_hrk_api)
                    d_url = VidUrl = key = AppxThumb = last_exception = ZipVer= None
                    for attempt in range(1, 4):
                        try:
                            async with session.get(url1, headers={'authorization': my_auth_token}) as r:
                                resp = await r.json()
                            if "appx/vid/" in url:
                                if resp and resp.get('StatusCode') == 200 and resp.get('data'):
                                    AppxThumb = resp['data'].get('Thumbnail')
                                    VidUrl = resp['data'].get('VidUrl')
                                    
                                    if not VidUrl:
                                        raise ValueError("No Downloadable URL found.")
                                    
                                    if "*" in VidUrl:
                                        d_url, key = VidUrl.split("*")
                                        d_url = d_url.replace('static-rec.classx.co.in', 'appx-recordings-mcdn.akamai.net.in').replace('static-rec.appx.co.in', 'appx-recordings-mcdn.akamai.net.in').replace('static-trans-v1.classx.co.in', 'appx-transcoded-videos-mcdn.akamai.net.in')
                                    elif ".zip" in VidUrl:
                                        if PlanType == "LEGEND":
                                            ZipVer = resp['data'].get('ZipVer')
                                            d_url = VidUrl
                                        else:
                                            pass 
                                    else:
                                        d_url = VidUrl
                                    break
                                else:
                                    raise ValueError(f"{resp if resp else 'No response'}")
                            elif "/appx/pdf" in url:
                                if resp and resp.get('StatusCode') == 200 and resp.get('url'):
                                    d_url = resp['url']
                                    break
                                else:
                                    logging.info(f"⚠️ No PDF URL Found !")
                        except Exception as exc:
                            last_exception = exc
                            if attempt < 3:
                                logging.warning(f"⚠️ Appx Url fetch Failed via u'r API in ({attempt} Attempts) due to : {exc}")
                                await asyncio.sleep(10)
                            else:
                                logging.error(f"❌ Appx Url fetch Failed via u'r API after All Attempts")
                    if not d_url and "/appx/vid" in url:
                        if VidUrl:
                            if ".zip" in VidUrl:
                                if PlanType == "LEGEND":
                                    f_text = SendErrorMessage(count, last_exception, name1, url, CR)
                                    stream_button = KM([[KB("▶ Stream in 𝗠ᴇɢᴀᴛʀᴏɴ Player", url=url.replace("appx/v3/", "appx/v3/play/").replace("appx/v2/", "appx/v2/play/"))]])
                                    if AppxThumb:
                                        SentMsg = await bot.send_photo(m.chat.id, AppxThumb, caption=ccstream, message_thread_id=thread_id, reply_markup=stream_button)
                                    else:
                                        SentMsg = await bot.send_message(m.chat.id, f_text, message_thread_id=thread_id, reply_markup=stream_button)
                                else:
                                    f_text = SendErrorMessage(count, "To Download APPX-ZIP Url Upgrade Your Bot's Plan.", name1, url, CR)
                                    SentMsg = await bot.send_message(m.chat.id, f_text, message_thread_id=thread_id)
                        else:
                            f_text = SendErrorMessage(count, last_exception, name1, url, CR)
                            SentMsg = await bot.send_message(m.chat.id, f_text, message_thread_id=thread_id)
                        await asyncio.sleep(3)
                        count += 1
                        continue

                elif any(ur in url for ur in ["encrypted.m", "encrypted_new.m", "appx.co.in", "classx.co.in"]) and "*" in url and not '.pdf' in url and not '.m3u8' in url:
                    if'https://encappx/' in url or "?k=" in url or "?key=" in url :
                        url = url.replace('https://encappx/','').replace('?k=','*').replace('?key=','*').strip()
                        d_url, key = url.split("*")
                        d_url = d_url.replace('static-rec.classx.co.in', 'appx-recordings-mcdn.akamai.net.in').replace('static-rec.appx.co.in', 'appx-recordings-mcdn.akamai.net.in').replace('static-trans-v1.classx.co.in', 'appx-transcoded-videos-mcdn.akamai.net.in').replace('static-trans-v1.appx.co.in', 'appx-transcoded-videos-mcdn.akamai.net.in').strip()
                        if not key.isdigit():
                            key = base64.b64decode(key).decode('utf-8')
                    else:      
                        d_url, key = url.split("*")
                        d_url = d_url.replace('static-rec.classx.co.in', 'appx-recordings-mcdn.akamai.net.in').replace('static-rec.appx.co.in', 'appx-recordings-mcdn.akamai.net.in').replace('static-trans-v1.classx.co.in', 'appx-transcoded-videos-mcdn.akamai.net.in').replace('static-trans-v1.appx.co.in', 'appx-transcoded-videos-mcdn.akamai.net.in').strip()
                        if not key.isdigit():
                            key = base64.b64decode(key).decode('utf-8')
                
                elif ".zip" in url:
                    if "&zipv" in url:
                        d_url, ZipVer = url.split('&zip=')
                    else:
                        ZipVer = None
                    if PlanType != "LEGEND":
                        f_text = SendErrorMessage(count, "To Download APPX-ZIP Url Upgrade Your Bot's Plan.", name1, url, CR)
                        SentMsg = await bot.send_message(m.chat.id, f_text, message_thread_id=thread_id)
                        count += 1
                        continue


                if "youtu" in url:
                    ytf = f"bestvideo[height<={quality}][ext=mp4]+bestaudio[ext=m4a]/best[height<={quality}][ext=mp4]"
                else:
                    ytf = f"b[height<={quality}]/bv[height<={quality}]+ba/b/bv+ba"
                if "youtu" in url:
                    if PlanType != "LEGEND":
                        cmd = f'yt-dlp --cookies "cookies.txt" -f "{ytf}" --no-warning "{d_url}" -o "{name}.%(ext)s"' #working fine
                    #cmd = f'yt-dlp --cookies "{COOKIES_FILE_PATH}" --extractor-args "yotube:player_client=tvhtml5" -add-header "User-Agent: okhttp/5.0.0-alpha.2" -f "{ytf}" "{d_url}" --merge-output-format mkv -o "{name}.%(ext)s"'
                elif "acecwply" in url:
                    cmd = f'yt-dlp -o "{name}.%(ext)s" -f "bestvideo[height<={quality}]+bestaudio" --hls-prefer-ffmpeg --no-keep-video --no-warning "{d_url}"'
                elif "spayee" in url or "m3u8HLS_KEY=" in url or ".mpd?key=" in url or "?#keysV1=" in url:
                    cmd = None
                elif any(u in url for u in ["encrypted.m", "encrypted_new.m", ".zip", "akamai.net.in/encrypted", "/appx/vid/"]) and not '.pdf' in url and not '.m3u8' in url:
                    cmd = f'yt-dlp "{d_url}" --add-header "User-Agent:okhttp/5.0.0-alpha.2" --add-header "Accept-Encoding:gzip" --add-header "Referer:https://appx-play.akamai.net.in/" -o "{name}.%(ext)s"'
                elif f"{my_hrk_api}/akaash/" in url:
                    cmd = f'yt-dlp -f "{ytf}" --no-warning "{d_url}" --add-header "authorization: {my_auth_token}" -o "{name}.%(ext)s"'
                elif "https://iframe.mediadelivery.net/" in url and "video.drm?contextId=" in url:
                    cmd = f'yt-dlp -f "{ytf}" --no-warning "{d_url}" --add-header "Referer:{my_hrk_api}/" -o "{name}.%(ext)s"'
                elif "https://player.vimeo.com/video" in url and '?app=jchemistry' in url:
                    if PlanType == "LEGEND":
                        cmd = f'yt-dlp -f "{ytf}" "{d_url.split('?app=jchemistry')[0]}" --add-header "Referer:https://www.jchemistry.online/" -o "{name}.%(ext)s"'
                else: 
                    cmd = f'yt-dlp -f "{ytf}" --no-warning "{d_url}" -o "{name}.%(ext)s"'  # --no-keep-video --remux-video mkv

                
                if "https://drive.google.com/drive/folders" in url:
                    f_text = SendErrorMessage(count, "Unable to Download G-Drive Folders Data. Click the Button and read files Properly.", name1, url, CR)
                    SentMsg = await bot.send_message(m.chat.id, f_text, message_thread_id=thread_id, reply_markup=KM([[KB("Open G-Drive", url=url)]]))
                    await asyncio.sleep(3)
                    count += 1

                elif any(pdf in d_url.lower() for pdf in [".pdf", ".doc", "drive", "/DownloadPDF/"]):                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    
                    if ".pdfPSWD=" in url:
                        if PlanType in ("CONQUEROR", "LEGEND"):
                            url, password = url.split("PSWD=")
                            response = requests.get(url, stream=True)
                            if response.status_code == 200:
                                with open(f'{name}_enc.pdf', "wb") as file:
                                    file.write(response.content)
                                doc = fitz.open(f'{name}_enc.pdf')           
                                if doc.authenticate(password):
                                    doc.save(f"{name}.pdf")
                                    await asyncio.sleep(1)
                                    SentMsg = await bot.send_document(m.chat.id, f'{name}.pdf', file_name=f'{name}_{EX}.pdf', caption=cc1, thumb=thumb2 if thumb2 else None, message_thread_id=thread_id)
                                else:
                                    SentMsg = await bot.send_document(m.chat.id, f'{name}_enc.pdf', caption=cc1, thumb=thumb2 if thumb2 else None, message_thread_id=thread_id)
                        else:
                            f_text = SendErrorMessage(count, "Unable to Download SPAYEE/GRAPHY Url.", name1, url, CR)
                            SentMsg = await bot.send_message(m.chat.id, f_text, message_thread_id=thread_id)
                    elif "&Pass=" in url:
                        d_url, EncPass = url.split('&Pass=')
                        Password = base64.b64decode(EncPass).decode()
                        
                        response = requests.get(d_url, stream=True)
                        if response.status_code == 200:
                            with open(f"{name}_enc.pdf", "wb") as file:
                                file.write(response.content)
                            doc = fitz.open(f"{name}_enc.pdf")
                            if doc.authenticate(Password):
                                doc.save(f"{name}.pdf")
                                await asyncio.sleep(1)
                                SentMsg = await bot.send_document(m.chat.id, f'{name}.pdf', file_name=f'{name}_{EX}.pdf', caption=cc1, thumb=thumb2 if thumb2 else None, message_thread_id=thread_id)
                            else:
                                SentMsg = await bot.send_document(m.chat.id, f'{name}_enc.pdf', caption=cc1, thumb=thumb2 if thumb2 else None, message_thread_id=thread_id)
                    else:
                        SentMsg = await helper.send_pdf(bot, m.chat.id, session, d_url, name, EX, cc1, token, thumb2, thread_id)
                    count+=1
                    await asyncio.sleep(1)
                    for file in [f'{name}.pdf', f'{name}_{EX}.pdf', 'Newthumb2.jpg', f'{name}_enc.pdf']:
                        if os.path.exists(file): os.remove(file)

            
                # Skipping URLs:
                elif "stream-kgs" in url or "stream.kgs" in url:
                    SentMsg = await bot.send_photo(m.chat.id, photo="Modules/Tools/Thumbnail/KGSliveLInk.jpg", caption=ccstream, message_thread_id=thread_id, reply_markup=StreamButton)
                    await asyncio.sleep(3)
                    count += 1
                
                elif ("adda247.com/" in url and url.endswith('.json')) or any(turl in url for turl in ["/appx/test/v3/", "/appx/quiz/", "https://www.testranking.in/?testId=", "https://u1.oliveboard.in/exams/solution/"]):
                    SentMsg = await helper.download_send_tests(bot, m, session, name, url, cchtml, thumb2, thread_id) 
                    count += 1
                

                elif any(ext in url for ext in [".jpg", ".jpeg", ".png"]):
                    ext = url.split('.')[-1]
                    thumb_path = f'{name}.{ext}'
                    cc3 = f'**——— ✦ {str(count).zfill(3)} ✦ ———**\n\n**🖼️ Tittle** : **{name1}**.{ext}\n\n├── **Extention** : {EX}\n\n**Course :** {b_name}\n\n**🌟 Extracted By : {CR}**'
                    os.system(f"yt-dlp -o '{thumb_path}' '{url}' -R 25 --fragment-retries 25")
                    if thumb_path:
                        try:
                            SentMsg = await bot.send_photo(m.chat.id, thumb_path, caption=cc3, message_thread_id=thread_id)
                        except Exception as e:
                            SentMsg = await bot.send_document(m.chat.id, thumb_path, caption=cc3, message_thread_id=thread_id)
                    if os.path.exists(thumb_path): os.remove(thumb_path)
                    count += 1

                elif any (ext in url for ext in [".mp3", ".wav", ".m4a"]):
                    ext = url.split('.')[-1]
                    os.system(f'yt-dlp -x --audio-format {ext} -o "{name}.{ext}" "{url}" -R 25 --fragment-retries 25')
                    cc2 = f'**[🎵] Audio_ID : {str(count).zfill(3)}.**\n\n**Tittle :** {name1}\n├── **Extension :** {EX}.{ext}\n\n**Course :** {b_name}\n\n🌟 **Extracted By :** {CR}'
                    await asyncio.sleep(2)
                    SentMsg = await bot.send_audio(m.chat.id, audio=f'{name}.{ext}', caption=cc2, message_thread_id=thread_id)
                    if os.path.exists(f'{name}.{ext}'): os.remove(f'{name}.{ext}')
                    count += 1

                else:
                    left_link = len(links) - int(count)
                    progress = (int(count) / len(links)) * 100
                    Show = (
                        f"<blockquote>🚀 **𝐂𝐔𝐑𝐑𝐄𝐍𝐓 𝐏𝐑𝐎𝐆𝐑𝐄𝐒𝐒 = {progress:.2f}%** 🚀\n"
                        f" **┠ 📊 Total Links =** {len(links)}\n"
                        f" **┠ ⚡️ Currently On =** {str(count).zfill(3)}\n"
                        f" **┠ ⏳ Remaining Links =** {left_link}</blockquote>\n\n"
                        f"<blockquote>**📥 𝐃𝐎𝐖𝐍𝐋𝐎𝐀𝐃𝐈𝐍𝐆 𝐕𝐈𝐃𝐄𝐎 📥**\n"
                        f"<b>🔗 LINK :</b> <a href='{url}'>Click to View SourceUrl</a>\n"
                        f"**  ┠ 🎞️ Title** : {name1}\n"
                        f"**  ┠ 📻 Quality :** {quality}p</blockquote>\n\n"
                        f"╔══════════════════════════╗\n"
                        f"╠  ✨ **𝐏𝐎𝐖𝐄𝐑𝐄𝐃 𝐁𝐘 : {CreditName}**\n"
                        f"╚══════════════════════════╝")
                    prog = await bot.send_message(m.chat.id, Show, disable_web_page_preview=True, message_thread_id=thread_id)
                    
                    if 'cpvod.testbook.com' in url or 'media-cdn.classplusapp.com/drm/' in url  or 'cpvod-x.testbook.com' in url:
                        if PlanType in ("PRO", "CONQUEROR", "LEGEND"):
                            filename = await helper.drm_download_video(d_url, quality, name, keys_arr)
                    elif "?#keysV1=" in url or "&keysV1=" in url:
                        if PlanType in ("PRO", "CONQUEROR", "LEGEND"):
                            filename = await helper.cipher_procoder_video(d_url, quality, name, keys_arr)
                    elif 'studyiq.com/' in url and url.endswith('.mpd'):
                        if PlanType in ("PRO", "CONQUEROR", "LEGEND"):
                            filename = await helper.cipher_procoder_video(url, quality, name, keys)
                    elif ("/master.mpd" in url and "parentId" in url and not "parentId2" in url) or "https://superdowanloader.dl?data=" in url:
                        if PlanType in ("PRO", "CONQUEROR", "LEGEND"):
                            if PwType == 'm3u8':
                                filename = await helper.download_video(d_url, cmd, name)
                            else:
                                filename = await helper.pw_download_video(nurl, quality, name, keys)
                    elif ("/master.mpd" in url and "parentId" in url and "parentId2" in url) or ('videoId' in url and 'childId' in url and 'secondaryChildId' in url):
                        if PlanType in ("CONQUEROR", "LEGEND"):
                            if PwType == 'm3u8':
                                filename = await helper.download_video(d_url, cmd, name)
                            else:
                                filename = await helper.pw_download_video(nurl, quality, name, keys)
                    elif "spayee" in url or "m3u8HLS_KEY=" in url:
                        if PlanType in ("CONQUEROR", "LEGEND"):
                            filename = await helper.spayee_video(d_url, quality, name, keys)
                    elif ".mpd" in url and "?key=" in url:
                        if PlanType == "LEGEND":
                            filename = await helper.cipher_procoder_video(d_url, quality, name, keys)
                    elif ".zip" in d_url:
                        if PlanType == "LEGEND":
                            Zipversion = ZipVer if ZipVer else None
                            try: 
                                filename = await somebody_noob_appx_zip_helper.somebody_main_zip_rpcessor(d_url, name, Zipversion, zipToken, zipAPI)
                            except Exception as e:
                                logging.error(f"⚠️ APPX-ZIP downloading ERROR : {e}")
                                await asyncio.sleep(3)
                                await helper.check_and_clear_temp_files()
                    elif any(ur in d_url for ur in ["encrypted.m", "encrypted_new.m", "appx.co.in", "classx.co.in", "akamai.net.in"]) and not '.m3u8' in d_url and not '.pdf' in d_url:
                        filename = await helper.download_video(d_url, cmd, name)
                        if filename and key:
                            await helper.appx_dl(filename, key)
                    elif "youtu" in url and PlanType == "LEGEND":
                        resp = requests.get(f'{my_hrk_api}/youtube?quality={quality}p&url={url}')
                        YtvUrl = resp.json().get('video_url')
                        YtaUrl = resp.json().get('audio_url')
                        filename = await helper.download_yt_video(name, YtvUrl, YtaUrl)   
                    else:
                        filename = await helper.download_video(d_url, cmd,name)
                    
                    await prog.delete()
                    SentMsg = await helper.send_vid(bot, m, cc, filename, thumb, name, DumpThreadId, thread_id, WatermarkText, WatermarkColor, CreditName)
                    count += 1
                
                if m.chat.type == enums.ChatType.CHANNEL and t_name:
                    if t_name not in TopicIndex:
                        TopicIndex[t_name] = SentMsg.link
                    # """Update If ChatId Already Exists"""
                    # CIndex = ActiveUsersCollection.update_one(
                    #     {"userId": user_id, "bot": bot.me.username, "TopicIndex.chat_id": m.chat.id},
                    #     {"$push": {"TopicIndex.$.topic": {"topicName": t_name, "postlink": SentMsg.link}}}
                    # )
                    # if CIndex.matched_count == 0:  #"""Create New ChatId for that User"""
                    #     ActiveUsersCollection.update_one(
                    #         {"userId": user_id, "bot": bot.me.username},
                    #         {"$push": {"TopicIndex": {"chat_id": m.chat.id, "topic": [{"topicName": t_name, "postlink": SentMsg.link}]}}},
                    #         upsert=True
                    #     )


            except Exception as e:
                f_text = SendErrorMessage(count, e, name1, url, CR)
                if "youtu" in url:
                    yt_watch = KM([[KB("🟢 YouTube 🟢", url=url),KB("▶ 𝗠ᴇɢᴀᴛʀᴏɴ Player", url=f"{my_hrk_api}/megax?url={url}" )]])
                    if "v=" in url:
                        yt_thumb = f"https://img.youtube.com/vi/{url.split('v=')[1].split('&')[0]}/maxresdefault.jpg"
                    elif "embed" in url:
                        yt_thumb = f"https://img.youtube.com/vi/{url.split('embed/')[1]}/maxresdefault.jpg"
                    elif "youtu.be" in url:
                        yt_thumb = f"https://img.youtube.com/vi/{url.split('youtu.be/')[1].split('?')[0]}/maxresdefault.jpg"
                    else:
                        yt_thumb = "https://envs.sh/Qr2.jpg"
                    try:
                        SentMsg = await bot.send_photo(m.chat.id, photo=yt_thumb, caption=ccyt, message_thread_id=thread_id, reply_markup=yt_watch)
                    except Exception as e:
                        SentMsg = await bot.send_photo(m.chat.id, photo="https://envs.sh/Qr2.jpg", caption=ccyt, message_thread_id=thread_id, reply_markup=yt_watch)

                elif "/master.mpd" in url and 'parentId' in url:
                    pw_button = KM([[KB("▶ Stream in 𝗠ᴇɢᴀᴛʀᴏɴ Player", url=f"{my_hrk_api}/megax?url={url}&token={PwToken}")]])
                    SentMsg = await bot.send_message(m.chat.id, f_text, message_thread_id=thread_id, reply_markup=pw_button)
                elif "amazonaws.com" in url and url.endswith(".mp4"):
                    adda_button = KM([[KB("▶ Stream in 𝗠ᴇɢᴀᴛʀᴏɴ Player", url=f"{my_hrk_api}/megax?url={url}&token={token}")]])
                    SentMsg = await bot.send_message(m.chat.id, f_text, message_thread_id=thread_id, reply_markup=adda_button)
                elif "/appx/vid/v" in url:
                    stream_button = KM([[KB("▶ Stream in 𝗠ᴇɢᴀᴛʀᴏɴ Player", url=url.replace("appx/vid/v3/", "appx/v3/play/").replace("appx/vid/v2/", "appx/v2/play/"))]])
                    try: 
                        SentMsg = await bot.send_photo(m.chat.id, AppxThumb, caption=ccstream, message_thread_id=thread_id, reply_markup=stream_button)
                    except Exception as e:
                        SentMsg = await bot.send_message(m.chat.id, f_text, message_thread_id=thread_id, reply_markup=stream_button)
                elif all(ext not in url.lower() for ext in [".pdf", ".doc", ".png", ".jpg", ".jpeg", ".ws"]):
                    try:
                        SentMsg = await bot.send_message(m.chat.id, f_text, message_thread_id=thread_id, reply_markup=StreamButton)
                    except Exception as e:
                        SentMsg = await bot.send_message(m.chat.id, f_text, message_thread_id=thread_id, disable_web_page_preview=True)
                else:
                    SentMsg = await bot.send_message(m.chat.id, f_text, message_thread_id=thread_id, disable_web_page_preview=True)
                
                failed_links.append(f"{name1} : {url}\n")
                count += 1
                await asyncio.sleep(2)
            if SentMsg: await helper.send_msg_in_dump(LogDumpGrp, SentMsg, DumpThreadId, filename="Exception Message")
        
        if m.chat.type == enums.ChatType.CHANNEL and TopicIndex:
            SummaryText = f"<blockquote><b>🏷️ All Available Topics for <i>{b_name}</i>:</b></blockquote>\n\n"
            for idx, (tname, plink) in enumerate(TopicIndex.items(), 1):
                SummaryText += f"<b>{idx}).</b>  [{tname}]({plink})\n"
            await bot.send_message(m.chat.id, f'{end_message}\n\n{SummaryText}', disable_web_page_preview=True)
            TopicIndex.clear()
        await bot.send_message(m.chat.id, f'{end_message}', message_thread_id=thread_id)
        if failed_links:
            capt = f"🚨 Failed Links Report for **{b_name}** 🚨\n\n📃 Here are the links that couldn't be processed. Please Review & Retry as your needs."
            with open(f"{b_name}.txt", "w", encoding="utf-8") as f:
                f.writelines(failed_links)
            await bot.send_document(m.chat.id, document=f"{b_name}.txt", caption=capt, thumb="Modules/Tools/Thumbnail/MyThumb.jpg", message_thread_id=thread_id)
            if os.path.exists(f"{b_name}.txt"): os.remove(f"{b_name}.txt")
            failed_links.clear()
        LastMsg = await bot.send_message(m.chat.id, "**That's It ❤️**", message_thread_id=thread_id)
        if LastMsg: await helper.send_msg_in_dump(LogDumpGrp, LastMsg, DumpThreadId, filename="That's It")
        
        await helper.check_and_clear_temp_files()
        """Clear Active task and update sempharo"""
        try:
            active_tasks.pop(m.chat.id, thread_id)
            semaphore.release()
        except Exception as e:
            logging.error(f"⚠️ Error in releasing semaphore or clearing active task : {e}")




@bot.on_message(filters.command("stop"))
@checkUser_PremiumStatus()
async def stop_command(_, m: Message):
    chat_id = m.chat.id
    thread_id = m.message_thread_id if m.message_thread_id else None  
    await m.delete()
    
    if  chat_id in active_tasks:
        task = active_tasks[chat_id]
        task.cancel()
        active_tasks.pop(chat_id, thread_id)
        gc.collect()
        await bot.send_message(chat_id, f"**Task is Cancelling ✘ for** {m.chat.title}.", message_thread_id=thread_id)
    else:
        await bot.send_message(chat_id, f"⚠️ No Active Tasks Found for {m.chat.title}!", message_thread_id=thread_id)  
