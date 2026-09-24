import pytz, json
from datetime import datetime, timedelta
from pymongo import MongoClient
from functools import wraps
from pyrogram import Client, enums
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import Message, CallbackQuery
from config import owner_id

IST = pytz.timezone("Asia/Kolkata")
client = MongoClient("mongodb+srv://adarshppandey937: uloPcIn9vXQBF0vP@cluster0.09mnbhb.mongodh.net/?")
db = client["UploaderSubscription"]
ActiveUsersCollection = db["Authorized_Users_Collection"]
RevokedUsersCollection = db["Revoked_Users_Collection"]
ExpiredUsersCollection = db["Expired_Users_Collection"]


"""Create indexes for automatic expiration of tokens after their expiry time
ActiveUsersCollection.create_index("expiresAtUTC", expireAfterSeconds=0)
#RevokedCollection.create_index("revokedAt", expireAfterSeconds=0)"""



def checkUser_PremiumStatus():
    def decorator(func):
        @wraps(func)
        async def wrapper(bot: Client, msg: Message, *args, **kwargs):
            if msg.chat.type == enums.ChatType.PRIVATE:
                userid = msg.from_user.id
            else:
                async for member in bot.get_chat_members(msg.chat.id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
                    if member.status == ChatMemberStatus.OWNER:
                        userid = member.user.id
            if userid in owner_id:
                return await func(bot, msg, *args, **kwargs)

            userStatus = get_user_status(userid, bot.me.username)
            
            if userStatus['status'] == "active":
                return await func(bot, msg, *args, **kwargs)
            elif userStatus['status'] == "expired":
                return await msg.reply(f"<blockquote><b>😔 𝐎𝐨𝐩𝐬, 𝐃𝐞𝐚𝐫 𝐔𝐬𝐞𝐫! 𝐘𝐨𝐮𝐫 𝐒𝐮𝐛𝐬𝐜𝐫𝐢𝐩𝐭𝐢𝐨𝐧 𝐡𝐚𝐬 𝐛𝐞𝐞𝐧 𝐄𝐱𝐩𝐢𝐫𝐞𝐝. ⚠️<b></blockquote>\n\n𝐘𝐨𝐮 𝐰𝐨𝐧𝐭 𝐛𝐞 𝐚𝐛𝐥𝐞 𝐭𝐨 𝐮𝐬𝐞 𝐏𝐫𝐞𝐦𝐢𝐮𝐦 𝐅𝐞𝐚𝐭𝐮𝐫𝐞𝐬 𝐨𝐟 𝐭𝐡𝐞 𝐁𝐎𝐓 𝐟𝐫𝐨𝐦 𝐧𝐨𝐰 𝐨𝐧.\n\n<blockquote><b>𝐓𝐨 𝐫𝐞𝐧𝐞𝐰 𝐘𝐨𝐮𝐫 𝐒𝐮𝐛𝐬𝐜𝐫𝐢𝐩𝐭𝐢𝐨𝐧, 𝐂𝐨𝐧𝐭𝐚𝐜𝐭 :</b> [『 𝐓𝐇𝐎𝐑 🧑‍💻 』™](t.me/Stormy_thor)</blockquote>")
            elif userStatus['status'] == "revoked":
                return await msg.reply(f"<blockquote><b>❌ 𝐘𝐨𝐮𝐫 𝐒𝐮𝐛𝐬𝐜𝐫𝐢𝐩𝐭𝐢𝐨𝐧 𝐡𝐚𝐬 𝐛𝐞𝐞𝐧 𝐑𝐞𝐯𝐨𝐤𝐞𝐝 𝐛𝐲 𝐎𝐰𝐧𝐞𝐫.<b></blockquote>\n\n𝐘𝐨𝐮 𝐰𝐨𝐧𝐭 𝐛𝐞 𝐚𝐛𝐥𝐞 𝐭𝐨 𝐮𝐬𝐞 𝐏𝐫𝐞𝐦𝐢𝐮𝐦 𝐅𝐞𝐚𝐭𝐮𝐫𝐞𝐬 𝐨𝐟 𝐭𝐡𝐞 𝐁𝐎𝐓 𝐟𝐫𝐨𝐦 𝐧𝐨𝐰 𝐨𝐧.\n\n<blockquote><b>To renew Your Subscription, Contact :</b> [『 𝐓𝐇𝐎𝐑 🧑‍💻 』™](t.me/Stormy_thor)</blockquote>")
            else:
                return await msg.reply(f"<b>🚫 <i>𝐘𝐨𝐮 𝐚𝐫𝐞 𝐧𝐨𝐭 𝐚𝐮𝐭𝐡𝐨𝐫𝐢𝐳𝐞𝐝 𝐭𝐨 𝐮𝐬𝐞 𝐭𝐡𝐢𝐬 𝐜𝐨𝐦𝐦𝐚𝐧𝐝</i>.</b>\n\n<b>𝐂𝐨𝐧𝐭𝐚𝐜𝐭 𝐡𝐞𝐫𝐞 𝐭𝐨 𝐠𝐞𝐭 𝐀𝐮𝐭𝐡𝐨𝐫𝐢𝐳𝐚𝐭𝐢𝐨𝐧 :</b> [『 𝐓𝐇𝐎𝐑 🧑‍💻 』™](t.me/Stormy_thor)")
        return wrapper
    return decorator

# === For CallBackQuery Functions ===
def checkUser_Premium_CallBack():
    def decorator(func):
        @wraps(func)
        async def wrapper(bot: Client, msg: CallbackQuery, *args, **kwargs):
            userid = msg.from_user.id

            if userid in owner_id:
                return await func(bot, msg, *args, **kwargs)

            userStatus = get_user_status(userid, bot.me.username)
            if userStatus['status'] == "active":
                return await func(bot, msg, *args, **kwargs)
            elif userStatus['status'] == "expired":
                return await msg.answer(f"⚠️ 𝐘𝐨𝐮𝐫 𝐒𝐮𝐛𝐬𝐜𝐫𝐢𝐩𝐭𝐢𝐨𝐧 𝐡𝐚𝐬 𝐛𝐞𝐞𝐧 𝐄𝐱𝐩𝐢𝐫𝐞𝐝.", show_alert=True)
            elif userStatus['status'] == "revoked":
                return await msg.answer(f"❌ 𝐘𝐨𝐮𝐫 𝐒𝐮𝐛𝐬𝐜𝐫𝐢𝐩𝐭𝐢𝐨𝐧 𝐡𝐚𝐬 𝐛𝐞𝐞𝐧 𝐑𝐞𝐯𝐨𝐤𝐞𝐝 𝐛𝐲 𝐎𝐰𝐧𝐞𝐫.", show_alert=True)
            else:
                return await msg.answer(f"🚫 𝐘𝐨𝐮 𝐚𝐫𝐞 𝐧𝐨𝐭 𝐚𝐮𝐭𝐡𝐨𝐫𝐢𝐳𝐞𝐝 𝐭𝐨 𝐮𝐬𝐞 𝐭𝐡𝐢𝐬 𝐟𝐞𝐚𝐭𝐮𝐫𝐞.", show_alert=True)
        return wrapper
    return decorator


async def authorize_user(bot: Client, UserId: int, bot_username: str, duration_days: int = 0, duration_hours: int = 0, duration_minutes: int = 0, plan_type: str = "NORMAL"):
    # --- Always work in UTC first ---
    CreatedAtUTC = datetime.utcnow()
    ExpiryTimeUTC = CreatedAtUTC + timedelta(days=duration_days, hours=duration_hours, minutes=duration_minutes)
    
    # --- Convert to IST for Saving/Display ---
    CreatedAtIST = CreatedAtUTC.replace(tzinfo=pytz.UTC).astimezone(IST).strftime("%I:%M:%S %p  %d-%m-%Y")
    ExpiryTimeIST = ExpiryTimeUTC.replace(tzinfo=pytz.UTC).astimezone(IST).strftime("%I:%M:%S %p  %d-%m-%Y")

    # --- 🟢 Clean Old Records from Revoked/Expired before re-authorization
    RevokedUsersCollection.delete_many({"userId": UserId, "bot": bot_username})
    ExpiredUsersCollection.delete_many({"userId": UserId, "bot": bot_username})

    # --- MongoDB me Save/Update Karo ---
    UserMention = (await bot.get_users(UserId)).mention
    UserName = (await bot.get_users(UserId)).username or "N/A"
    ActiveUsersCollection.insert_one({
            "userId": UserId, "bot": bot_username, "planType": plan_type,
            "createdAtUTC": CreatedAtUTC, "expiresAtUTC": ExpiryTimeUTC,
            "createdAtIST": CreatedAtIST, "expiresAtIST": ExpiryTimeIST,
            "defaultName": "None", "extensionName": "None",
            "pdfThumbnail": "no", "vidThumbnail": "no",
            "textWatermark": None, "watermarkColor": "white",
            "fontStyle": "Noto Sans", "fontSize": "80", "opacity": "0.8", "watermarkEnabled": "yes",
            "quality": "480", "captionStyle": "default",
            "CreditName": "[『 𝐓𝐇𝐎𝐑 🧑‍💻 』™](t.me/Stormy_thor)⁬",
            "ytCookie": "Null", "pwToken": "Null"
    })
    return (f"<blockquote>✅ New User `{UserId}` added to Authorized Users.</blockquote>\n\n"
                f"🌟 <b><u><i>HERE IS USER SUBSCRIPTION DETAILS</i></u>.</b> 🌟\n\n"
                f"<blockquote>🔖 <b>Subscription ID :</b> `{UserId}`\n"
                f"👤 User Name : @{UserName}\n"
                f"👨‍🦱 User Profile : {UserMention}\n"
                f"🤖 <b>Subscription Bot :</b> @{bot_username}\n"
                f"🎟️ <b>Subscription Type :</b> {plan_type}\n"
                f"⏱️ <b>Join DateTime :</b> {CreatedAtIST}\n"
                f"🗓️ <b>Subscription Duration :</b> {duration_days} days, {duration_hours} hrs, {duration_minutes} min\n"
                f"⏳ <b>Expiration DateTime :</b> {ExpiryTimeIST}</blockquote>")


"""Make a function to revoke user subscription and move his details to revoked collection"""
async def revoke_user_subscription(bot: Client, user_id: int, bot_username: str):
    userMention = (await bot.get_users(user_id)).mention

    ActiveUser = ActiveUsersCollection.find_one({"userId": user_id, "bot": bot_username})
    if ActiveUser:
        ActiveUsersCollection.delete_one({"userId": user_id, "bot": bot_username})
        ActiveUser['revokedAt'] = datetime.utcnow().replace(tzinfo=pytz.UTC).astimezone(IST).strftime("%I:%M:%S %p  %d-%m-%Y")
        RevokedUsersCollection.insert_one(ActiveUser)
        
        userText = (
            f"<b>😔 Oops, Dear {userMention}!</b>\n"
            f"<blockquote>❌ <b>𝐘𝐨𝐮𝐫 𝐒𝐮𝐛𝐬𝐜𝐫𝐢𝐩𝐭𝐢𝐨𝐧 𝐡𝐚𝐬 𝐛𝐞𝐞𝐧 𝐑𝐞𝐯𝐨𝐤𝐞𝐝.</b> ❌**</blockquote>\n\n"
            f"<blockquote><b>Your Previous Subscription Detail</b>\n\n"
            f"<b>⏰ Joined Time :</b> {ActiveUser['createdAtIST']}\n"
            f"<b>⏰ Expiry Time :</b> {ActiveUser['expiresAtIST']}\n"
            f"<b>⏱️ Acces Revoked At :</b> {ActiveUser['revokedAt']}\n"
            f"<b>🤖 Subscription Type :</b> {ActiveUser['planType']}</blockquote>"
        )
        OwnerText = (f"⛔ User {user_id} revoked from @{bot_username}.")
        return userText, OwnerText
    
    ExpiredUser = ExpiredUsersCollection.find_one({"userId": user_id, "bot": bot_username})
    if ExpiredUser:
        ExpiredUsersCollection.delete_one({"userId": user_id, "bot": bot_username})
        ExpiredUser['revokedAt'] = datetime.utcnow().replace(tzinfo=pytz.UTC).astimezone(IST).strftime("%I:%M:%S %p  %d-%m-%Y")
        RevokedUsersCollection.insert_one(ExpiredUser)
        return "[✘] Your Subscription has been Already Expired.", "User Revoked from Expired Users."

# ====== Check ====== User ====== Authorization ====== (Auto-Expire Move) ======
def get_user_status(user_id: int, bot_username: str):
    # --- Check Active Users ---
    ActiveUser = ActiveUsersCollection.find_one({"userId": user_id, "bot": bot_username})
    if ActiveUser:
        ExpiryTimeIST = ActiveUser['expiresAtUTC']
        CurrentTimeIST = datetime.utcnow()
        if CurrentTimeIST >= ExpiryTimeIST:
            # --- Move to Expired Collection ---
            ActiveUsersCollection.delete_one({"userId": user_id, "bot": bot_username})
            ActiveUser["expiredAt"] = CurrentTimeIST.strftime("%I:%M:%S %p  %d-%m-%Y")
            ExpiredUsersCollection.insert_one(ActiveUser)
            return {"status": "expired", "data": ActiveUser}
        return {"status": "active", "data": ActiveUser}
    
    RevokedUser = RevokedUsersCollection.find_one({"userId": user_id, "bot": bot_username})
    if RevokedUser:
        return {"status": "revoked", "data": RevokedUser}
    
    ExpiredUser = ExpiredUsersCollection.find_one({"userId": user_id, "bot": bot_username})
    if ExpiredUser:
        return {"status": "expired", "data": ExpiredUser}
    return {"status": "NotFound", "data": None}



async def update_user_settings(user_id: int, bot_username: str, default_name: str = None, extension_name: str = None, pdf_thumbnail: str = None, vid_thumbnail: str = None, watermark_color: str = None, text_watermark: str = None, quality: str = None, captStyle: str = None, ytcookie: str = None, pwtoken: str = None, credit: str = None, font_style: str = None, font_size: str = None, opacity: str = None, watermark_enabled: str = None):
    update_fields = {}
    if default_name:
        update_fields["defaultName"] = default_name
    if extension_name:
        update_fields["extensionName"] = extension_name
    if pdf_thumbnail:
        update_fields["pdfThumbnail"] = pdf_thumbnail
    if vid_thumbnail:
        update_fields["vidThumbnail"] = vid_thumbnail
    if watermark_color:
        update_fields["watermarkColor"] = watermark_color
    if text_watermark:
        if text_watermark.lower() == 'no':
            update_fields["textWatermark"] = None
        else:
            update_fields["textWatermark"] = text_watermark
    if quality:
        update_fields["quality"] = quality
    if captStyle:
        update_fields["captionStyle"] = captStyle
    if ytcookie:
        update_fields["ytCookie"] = ytcookie
    if pwtoken:
        update_fields["pwToken"] = pwtoken
    if credit:
        update_fields["CreditName"] = credit
    if font_style:
        update_fields["fontStyle"] = font_style
    if font_size:
        update_fields["fontSize"] = font_size
    if opacity:
        update_fields["opacity"] = opacity
    if watermark_enabled:
        update_fields["watermarkEnabled"] = watermark_enabled
    
    if update_fields:
        result = ActiveUsersCollection.update_one({"userId": user_id, "bot": bot_username}, {"$set": update_fields})
        if result.matched_count:
            return f"⚙️ Setting Updated for User {user_id}  @{bot_username}."
        else:
            return f"❌ User {user_id} not found in Active Users for @{bot_username}"
    else:
        return "❕ Nothing to Update"


# ===== UTILITY FUNCTION =====
async def list_active_users(bot_username: str):
    users = ActiveUsersCollection.find({"bot": bot_username})
    result = []
    for user in users:
        result.append({
            "userId": user.get("userId"), "planType": user.get("planType"),
            "expiresAtIST": user.get("expiresAtIST"), "createdAtIST": user.get("createdAtIST"),
            "botName": f'@{user.get("bot", "N/A")}'
        })
    return f"```json\n{json.dumps(result, indent=4)}\n```"

def list_revoked_users(bot_username: str):
    return list(RevokedUsersCollection.find({"bot": bot_username}))

def list_expired_users(bot_username: str):
    return list(ExpiredUsersCollection.find({"bot": bot_username}))


def print_all_user():
    ActiveUser = list(ActiveUsersCollection.find({}))
    if not ActiveUser:
        print("ERroro")
    for idx, id in enumerate(ActiveUser, 1):
        print(idx, id['userId'])
    print(len(ActiveUser))

#print_all_user()
