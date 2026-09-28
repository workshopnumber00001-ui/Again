import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto, ForceReply, CallbackQuery
from datetime import datetime
from config import *
from DbNew import *
from Tools.buttons import *
IST = pytz.timezone("Asia/Kolkata")


# ================================ Authorization/DeAuthorization/Upgradation Command ================================
@bot.on_message(filters.command("auth") & filters.user(owner_id))
async def add_auth_user(bot: Client, msg: Message):
    try:
        if len(msg.command) < 6:
            return f"/auth <userId> <Days> <Hour> <Minute> <Plan Type : n, p, c, l>"
        
        userId = int(msg.command[1])
        Days = int(msg.command[2])
        Hour = int(msg.command[3])
        Minute = int(msg.command[4])
        plan_type = msg.command[5].lower()
        
        if plan_type == "p":
            PlanType = "PRO"
        elif plan_type == "c":
            PlanType = "CONQUEROR"
        elif plan_type == "l":
            PlanType = "LEGEND"
        else:
            PlanType = "NORMAL"
        
        # Check User Already Exists or not in Authorized User List
        ExtUser = ActiveUsersCollection.find_one({"userId": userId, "bot": bot.me.username})
        if ExtUser:
            Message = (
                f"<blockquote><b>[✔] User Already Exists in Active Authorized Users!</b>\n\n"
                f"<b>👨‍💼 UserId :</b> {ExtUser['userId']} | <b>🎟️ PlanType :</b> {ExtUser['planType']}\n"
                f"<b>🤖 BotLink :</b> https://t.me/{ExtUser['bot']}\n"
                f"<b>📆 JoinTime :</b> {ExtUser['createdAtIST']}\n"
                f"<b>⌛ ExpTime :</b>  {ExtUser['expiresAtIST']}\n</blockquote>")
            return await bot.send_message(msg.chat.id, Message)
        
        resp = await authorize_user(bot, userId, bot.me.username, duration_days=Days, duration_hours=Hour, duration_minutes=Minute, plan_type=PlanType)
        await msg.reply(resp)
    except Exception as e:
        return await msg.reply(f"❌ Error : {e}")
    
    await asyncio.sleep(1)
    userMention = (await bot.get_users(userId)).mention
    user = get_user_status(userId, bot.me.username)
    if user.get('data'):
        join_date_ist = IST.localize(datetime.strptime(user['data']['createdAtIST'], "%I:%M:%S %p  %d-%m-%Y"))
        end_date_ist= IST.localize(datetime.strptime(user['data']['expiresAtIST'], "%I:%M:%S %p  %d-%m-%Y"))
        SubsDuration = end_date_ist - join_date_ist
        SubDays = SubsDuration.days
        SubHrs, SubRemainder = divmod(SubsDuration.seconds, 3600)
        SubMins, SubSec = divmod(SubRemainder, 60)

        user_msg = (
            f"<blockquote>**🎉 Congratulations {userMention}! & Thanks for Purchasing Premium Subscription.**</blockquote>\n\n"
            f"<b><u>🌟 Great! You are a Premium Member! 🌟</u></b>\n\n"
            f"<blockquote>⏱️ <b>Join DateTime :</b> {user['data']['createdAtIST']}\n"
            f"🗓️ <b>Subscription Durantion :</b> {SubDays} Days, {SubHrs} Hours, {SubMins} Minutes\n"
            f"⏰ <b>Expiry DateTime :</b> {user['data']['expiresAtIST']}\n"
            f"🤖 <b>Subscription Type :</b> <u>{user['data']['planType']}</u></blockquote>\n"
            f"<blockquote><b>➠ 𝐌𝐚𝐝𝐞 𝐁𝐲 : {user['data']['CreditName']}</b></blockquote>\n\n"
            f"Press <b><u>Help Button</u></b> to Use Me properly"
        )
        await bot.send_photo(userId, photo="https://envs.sh/qho.jpg", caption=user_msg, reply_markup=HELP_BUTTON)
        await bot.send_message(LogDumpGrp, resp, message_thread_id=800)


@bot.on_message(filters.command("deauth") & filters.user(owner_id))
async def remove_auth_user(bot: Client, msg: Message):
    try:
        user_to_remove = int(msg.text.split(maxsplit=1)[1])
        user = get_user_status(user_to_remove, bot.me.username)
		
        if user.get('data'):
            UserMsg, OwnerMsg = await revoke_user_subscription(bot, user_to_remove, bot.me.username)
            await msg.reply(OwnerMsg)
            await bot.send_message(user_to_remove, UserMsg)
        else:
            await msg.reply(f"User `{user_to_remove}` is not in the authorized users list.")
    except (IndexError, ValueError) as e:
        await msg.reply(f"Please provide a valid user ID. {e}")


@bot.on_message(filters.command("inc") & filters.user(owner_id))
async def update_subs_plan(bot: Client, msg: Message):
    if len(msg.command) < 2:
        return f"/auth <userId> <Days> <Hour> <Minute> <Plan Type : n, p, c, l>"
    try:
        userId = int(msg.command[1])
    except ValueError:
        return await msg.reply("❌ Invalid User ID! Please send a numeric User ID.")
        
    user = get_user_status(userId, bot.me.username)
    try:
        if user['status'] == 'active':
            NewExpUTC = user['data']['expiresAtUTC'] + timedelta(days=1, hours=0, minutes=0)
            NewExpIST = NewExpUTC.replace(tzinfo=pytz.UTC).astimezone(IST).strftime("%I:%M:%S %p  %d-%m-%Y")
            
            ActiveUsersCollection.update_one({"userId": userId, "bot": bot.me.username}, 
                {"$set": {"expiresAtUTC": NewExpUTC, "expiresAtIST": NewExpIST}}
            )
            await asyncio.sleep(1)
            Newuser = get_user_status(userId, bot.me.username)
            join_ist = IST.localize(datetime.strptime(Newuser['data']['createdAtIST'], "%I:%M:%S %p  %d-%m-%Y"))
            new_end_ist = IST.localize(datetime.strptime(Newuser['data']['expiresAtIST'], "%I:%M:%S %p  %d-%m-%Y"))
    
            NewSubsDur = new_end_ist - join_ist
            NsubHrs, NsubRemainder = divmod(NewSubsDur.seconds, 3600)
            NsubMins, NsubSec = divmod(NsubRemainder, 60)
    
            user_msg = (
                f"<blockquote>**Dear {(await bot.get_users(userId)).mention}! Your Subscription Info has been Updated 🔄️.**</blockquote>\n\n"
                f"<blockquote><b><u>🌟 Your Updated Subscription details ! 🌟</u></b>\n"
                f"⏱️ <b>Joining Time :</b> {Newuser['data']['createdAtIST']}\n"
                f"🗓️ <b>New Subscription Duration :</b> {NewSubsDur.days} Days, {NsubHrs} Hrs, {NsubMins} Minutes\n"
                f"⌛ <b>Previous Expiry Time :</b> {user['data']['expiresAtIST']}\n"
                f"⏰ <b>New Expiry Time :</b> {Newuser['data']['expiresAtIST']}\n"
                f"🎟️ <b>Subscription Type : {Newuser['data']['planType']}</b></blockquote>\n\n"
                f"<blockquote>💖 Thanks you for being a part of our service! 😊\n"
                f"⬇️ Press the <b>Help Button</b> to Use Me properly ⬇️</blockquote>")

            await bot.send_photo(userId, photo="https://envs.sh/qho.jpg", caption=user_msg, reply_markup=HELP_BUTTON)
            await msg.reply(f"** DATE & TIME** has been Successfully Updated 🎉.")
    except IndexError:
        await msg.reply("Please provide a DATE TIME.")



# ========================== 1). OWNER/ADMIN DASHBOARD PANNEL ==========================
Dashcaption = "<blockquote><b>Welcome Captain 『 𝐓𝐇𝐎𝐑 』™!</blockquote>\nManage Your Bot's Subscription From Here.</b>"

@bot.on_message(filters.command('pannel') & filters.user(owner_id))
async def showAllData_Users(bot: Client, msg: Message):
    await bot.send_photo(msg.chat.id, photo="Modules/Tools/Thumbnail/AdminDashboard.jpg", caption=Dashcaption, reply_markup=OwnerButton)

@bot.on_callback_query(filters.regex('back\$pannel') & filters.user(owner_id))
async def back_to_pannel(bot: Client, msg: CallbackQuery):
    await msg.message.edit_media(InputMediaPhoto(media="Modules/Tools/Thumbnail/AdminDashboard.jpg", caption=Dashcaption), reply_markup=OwnerButton)


# ========================== 2). Show Global Authorized Users (Pagination + Optional Search) ==========================
@bot.on_callback_query(filters.regex("show\$AuthUsers"))
async def show_list(bot: Client, msg: CallbackQuery):
    await get_all_Authorized_User(bot, msg, page=1)

USER_PER_PAGE = 5
PENDING_SEARCH = {}
PENDING_EXPIRY = {}
async def get_all_Authorized_User(bot: Client, msg: CallbackQuery, page=1, search_id=None):
    try:
        if search_id:
            users = ActiveUsersCollection.find_one({"userId": int(search_id)})
        else:
            users = list(ActiveUsersCollection.find({}))
        if not users:
            return await msg.answer(f"❌ No Authorized User Found{' for ' + search_id if search_id else ''}!", show_alert=True)
        
        total_pages = (len(users) + USER_PER_PAGE-1)//USER_PER_PAGE
        page = max(1, min(page, total_pages))
        start = (page-1)*USER_PER_PAGE
        end = start+USER_PER_PAGE
        page_users = users[start:end]    

        buttons = []
        for idx, u in enumerate(page_users, start=start+1):
            uid = u.get('userId', 'N/A')
            botName = u.get('bot', 'N/A')
            buttons.append([InlineKeyboardButton(f"{idx}). {uid} | {botName}", callback_data=f"details:{uid}:{botName}")])
        
        nav_buttons = []
        if page>1: nav_buttons.append(InlineKeyboardButton("⬅️ Prev", callback_data=f"users_page:{page-1}"))
        if page<total_pages: nav_buttons.append(InlineKeyboardButton("Next ➡️", callback_data=f"users_page:{page+1}"))
        if nav_buttons: buttons.append(nav_buttons)

        # Search / Refresh
        buttons.append([InlineKeyboardButton("🔎 Search UserId", callback_data="global_search"), InlineKeyboardButton("🔁 Refresh", callback_data="users_page:1")])
        buttons.append([InlineKeyboardButton("🔙 Back", callback_data="back$pannel")])

        text = f"🌏 <b> Global Authorized Users</b>\nPage {page}/{total_pages}\n"
        if search_id: text+= f"🔎 Search result for: <b>{search_id}</b>\n"
        await msg.message.edit_media(InputMediaPhoto(media="Modules/Tools/Thumbnail/AdminDashboard.jpg", caption=text), reply_markup=InlineKeyboardMarkup(buttons))
    except Exception as e:
        return await msg.message.reply_text(f"<b>[✘] Error in Show Global Authorized Users :</b> <i>{e}</i>")
    
# - - - - - 3). Pagination - - - - - -
@bot.on_callback_query(filters.regex(r"users_page:(\d+)$") & filters.user(owner_id))
async def global_users_page(bot: Client, msg: CallbackQuery):
    page = int(msg.data.split(':')[1])
    await get_all_Authorized_User(bot, msg, page=page)

# # - - - - - - 4). Search - - - - - - -
# @bot.on_callback_query(filters.regex(r"^global_search$") & filters.user(owner_id))
# async def global_search(bot: Client, msg: CallbackQuery):
#     sent = await msg.message.reply_text("🔎 Send UserId to search:", reply_markup=ForceReply(selective=True))
#     PENDING_SEARCH[sent.chat.id, sent.id] = True

# @bot.on_callback_query(filters.reply & filters.user(owner_id))
# async def hanle_search(bot: Client, msg: Message):
#     if not msg.reply_to_message: return

#     key = (msg.chat.id, msg.id)
#     if key not in PENDING_SEARCH: return
    
#     PENDING_SEARCH.pop(key)
#     uid = msg.text.strip()
#     if not uid.isdigit(): return await msg.reply("⚠️ Invalid UserId!")
#     await get_all_Authorized_User(bot, msg, page=1, search_id=uid)

# ========================== 5). View Authorized User Details ==========================
@bot.on_callback_query(filters.regex(r"details:(\d+):(.*)$") & filters.user(owner_id))
async def global_users_details(_: Client, msg: CallbackQuery):
    try:
        user_id = int(msg.data.split(':')[1])
        botName = msg.data.split(':')[2]

        user = ActiveUsersCollection.find_one({"userId": user_id, "bot": botName})
        if not user:
            return await msg.answer("❌ User not found!", show_alert=True)

        end_date_ist= IST.localize(datetime.strptime(user['expiresAtIST'], "%I:%M:%S %p  %d-%m-%Y"))        
        time_diff = end_date_ist - datetime.now(IST)
        hours, remainder = divmod(time_diff.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        details = (
            f"<blockquote><b>👨‍💼 UserId :</b> {user.get('userId', 'N/A')}\n"
            f"<b>🤖 BotName :</b> @{user.get('bot', 'N/A')}\n"
            f"<b>🎟️ PlanType :</b> {user.get('planType', 'FREE')}\n"
            f"<b>📆 JoinTime :</b> {user.get('createdAtIST', 'N/A')}\n"
            f"<b>⌛ ExpTime :</b> {user.get('expiresAtIST', 'N/A')}\n"
            f"<b>⏰ RemainingTime :</b> {time_diff.days} Days, {hours} hrs, {minutes} min.</blockquote>\n"
        )
        buttons = [
            [InlineKeyboardButton("🗑️ Rovke Access", callback_data=f"revoke:{user_id}:{botName}")],
            [InlineKeyboardButton("🔁 Update Validity", callback_data=f"updateval:{user_id}:{botName}"), InlineKeyboardButton("🎟️ Update PlanType", callback_data=f"updateplan:{user_id}:{botName}")],
            [InlineKeyboardButton("👨‍💻 Set CreditName", callback_data=f"CrName:{user_id}:{botName}"), InlineKeyboardButton("📤 SET LOG-DUMPs", callback_data=f"setDumps:{user_id}:{botName}")],
            [InlineKeyboardButton("🔙 Back", callback_data="users_page:1")]]
        await msg.message.edit_media(InputMediaPhoto(media="Modules/Tools/Thumbnail/AdminDashboard.jpg", caption=details), reply_markup=InlineKeyboardMarkup(buttons))
    except Exception as e:
        return await msg.message.reply_text(f"<b>[✘] Error in get User Details :</b> <i>{e}</i>")


# ========================== 6). Revoke Access ==========================
@bot.on_callback_query(filters.regex(r"^revoke:(\d+):(\w+)$") & filters.user(owner_id))
async def revoke_access(_: Client, msg: CallbackQuery):
    user_id = int(msg.data.split(':')[1])
    BotName = msg.data.split(':')[2]
    userMention = (await bot.get_users(user_id)).mention
    
    try:
        ActiveUser = ActiveUsersCollection.find_one({"userId": user_id, "bot": BotName})
        ExpiredUser = ExpiredUsersCollection.find_one({"userId": user_id, "bot": BotName})
        if ActiveUser:
            result = ActiveUsersCollection.delete_one({"userId": user_id, "bot": BotName})
            ActiveUser['revokedAt'] = datetime.utcnow().replace(tzinfo=pytz.UTC).astimezone(IST).strftime("%I:%M:%S %p  %d-%m-%Y")
            RevokedUsersCollection.insert_one(ActiveUser)
            if result.deleted_count > 0:
                await msg.message.edit_media(InputMediaPhoto(media="Modules/Tools/Thumbnail/AdminDashboard.jpg", caption=f"[✔️] User <b>{user_id}</b> has been removed from @{BotName}"), reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="show$AuthUsers")]]))
                userText = (
                    f"<b>😔 Oops, Dear {userMention}!</b>\n"
                    f"<blockquote>❌ <b>Your Subscription has been Revoked.</b> ❌**</blockquote>\n\n"
                    f"<blockquote><b>Your Previous Subscription Detail</b>\n\n"
                    f"<b>⏰ Joined Time :</b> {ActiveUser['createdAtIST']}\n"
                    f"<b>⏰ Expiry Time :</b> {ActiveUser['expiresAtIST']}\n"
                    f"<b>⏱️ Acces Revoked At :</b> {ActiveUser['revokedAt']}\n"
                    f"<b>🤖 Subscription Type :</b> {ActiveUser['planType']}</blockquote>"
                )
                await bot.send_message(user_id, userText)
        elif ExpiredUser:
            ExpiredUsersCollection.delete_one({"userId": user_id, "bot": BotName})
            ExpiredUser['revokedAt'] = datetime.utcnow().replace(tzinfo=pytz.UTC).astimezone(IST).strftime("%I:%M:%S %p  %d-%m-%Y")
            RevokedUsersCollection.insert_one(ExpiredUser)
            await bot.send_message(user_id, "[✘] Your Subscription has been Already Expired.")
            await msg.answer("[✔️] User Revoked from Expired Users.", show_alert=True)
        else:
            return await msg.answer(f"⚠️ *{user_id}* not found or Already Revoked or Expired!", show_alert=True)
    except Exception as e:
        return await msg.message.reply_text(f"<b>[✘] Error in Revoking User Access :</b> <i>{e}</i>")


# ========================== 7). Plan Validity Modification ==========================
@bot.on_callback_query(filters.regex(r"updateval:(\d+):(\w+)$") & filters.user(owner_id))
async def subscription_modification(_: Client, msg: CallbackQuery):
    userId = int(msg.data.split(':')[1])
    botName = msg.data.split(':')[2]
    
    Editable = await msg.message.reply_text("**Enter data : (__add/min Days Hour__)**")
    try:
        InputData: Message = await bot.ask(msg.message.chat.id, "")
        type, Days, Hour = InputData.text.split()[0], int(InputData.text.split()[1]), int(InputData.text.split()[2])
        await InputData.delete()
    
        user = get_user_status(userId, botName)
        if user.get('status') != 'active':
            return await msg.answer(f"User *{userId}* not Found in Active Users!", show_alert=True)
        
        if type.lower() == 'add':
            NewExpUTC = user['data']['expiresAtUTC'] + timedelta(days=Days, hours=Hour, minutes=0)
        elif type.lower() == 'min':
            NewExpUTC = user['data']['expiresAtUTC'] - timedelta(days=Days, hours=Hour, minutes=0)
            
        NewExpIST = NewExpUTC.replace(tzinfo=pytz.UTC).astimezone(IST).strftime("%I:%M:%S %p  %d-%m-%Y")
        ActiveUsersCollection.update_one({"userId": userId, "bot": botName}, {"$set": {"expiresAtUTC": NewExpUTC, "expiresAtIST": NewExpIST}})
        await asyncio.sleep(1)
            
        Newuser = get_user_status(userId, botName)
        join_ist = IST.localize(datetime.strptime(Newuser['data']['createdAtIST'], "%I:%M:%S %p  %d-%m-%Y"))
        new_end_ist = IST.localize(datetime.strptime(Newuser['data']['expiresAtIST'], "%I:%M:%S %p  %d-%m-%Y"))

        NewSubsDur = new_end_ist - join_ist
        NsubHrs, NsubRemainder = divmod(NewSubsDur.seconds, 3600)
        NsubMins, NsubSec = divmod(NsubRemainder, 60)
    
        await Editable.edit_text(
            f"<blockquote><b><u>🌟 {userId} Updated Subscription details! 🌟</u></b>\n"
            f"⏱️ <b>Joining Time :</b> {Newuser['data']['createdAtIST']}\n"
            f"🗓️ <b>New Subscription Duration :</b> {NewSubsDur.days} Days, {NsubHrs} Hrs, {NsubMins} Minutes\n"
            f"⌛ <b>Previous Expiry Time :</b> {user['data']['expiresAtIST']}\n"
            f"⏰ <b>New Expiry Time :</b> {Newuser['data']['expiresAtIST']}\n"
            f"🎟️ <b>Subscription Type : {Newuser['data']['planType']}</b></blockquote>")
        
        user_msg = (
            f"<blockquote>**Dear {(await bot.get_users(userId)).mention}! Your Subscription Info has been Updated 🔄️.**</blockquote>\n\n"
            f"<blockquote><b><u>🌟 Your Updated Subscription details ! 🌟</u></b>\n"
            f"⏱️ <b>Joining Time :</b> {Newuser['data']['createdAtIST']}\n"
            f"🗓️ <b>New Subscription Duration :</b> {NewSubsDur.days} Days, {NsubHrs} Hrs, {NsubMins} Minutes\n"
            f"⌛ <b>Previous Expiry Time :</b> {user['data']['expiresAtIST']}\n"
            f"⏰ <b>New Expiry Time :</b> {Newuser['data']['expiresAtIST']}\n"
            f"🎟️ <b>Subscription Type : {Newuser['data']['planType']}</b></blockquote>\n\n"
            f"<blockquote>💖 Thanks you for being a part of our service! 😊\n"
            f"⬇️ Press the <b>Help Button</b> to Use Me properly ⬇️</blockquote>"
        )
        return await bot.send_photo(userId, photo="https://envs.sh/qho.jpg", caption=user_msg, reply_markup=HELP_BUTTON)
    except Exception as e:
        return await Editable.edit_text(f"<b>[✘] Error in Plan Validity Modification :</b> <i>{e}</b>")


# ========================== 8). Change PlanType ==========================
@bot.on_callback_query(filters.regex(r"^updateplan:(\d+):(\w+)$") & filters.user(owner_id))
async def update_planType(_: Client, msg: CallbackQuery):
    try:
        user_id = int(msg.data.split(':')[1])
        BotName = msg.data.split(':')[2]
        user = ActiveUsersCollection.find_one({"userId": user_id, "bot": BotName})
        if not user:
            return await msg.answer("❌ User Not Found!", show_alert=True)
    
        CurrentPlanType = user.get('planType', 'NORMAL')
        buttons = []
        for plan in ['NORMAL', 'PRO', 'CONQUEROR', 'LEGEND']:
            text = f"{'✔️' if plan == CurrentPlanType else ''} {plan}"
            buttons.append([InlineKeyboardButton(text, callback_data=f"setplan:{user_id}:{plan}:{BotName}")])
        buttons.append([InlineKeyboardButton("🔙 Back", callback_data=f"details:{user_id}:{BotName}")])
        await msg.message.edit_media(InputMediaPhoto(media="Modules/Tools/Thumbnail/AdminDashboard.jpg", caption=f"📝 Select new PlanType for <b>{user_id}</b>:\n\n<b>Current Plan :</b> {CurrentPlanType}"), reply_markup=InlineKeyboardMarkup(buttons))
    except Exception as e:
        return await msg.message.reply_text(f"<b>[✘] Error in PlanType Modification :</b> <i>{e}</i>")

@bot.on_callback_query(filters.regex(r"^setplan:(\d+):(\w+):(\w+)$") & filters.user(owner_id))
async def set_planType(bot: Client, msg: CallbackQuery):
    try:
        user_id = int(msg.data.split(':')[1])
        NewPlan = msg.data.split(':')[2]
        BotName = msg.data.split(':')[3]
        ActiveUsersCollection.update_one({"userId": user_id, "bot": BotName}, {"$set": {"planType": NewPlan}})

        # Refresh Menu with Updated Info
        Newuser = ActiveUsersCollection.find_one({"userId": user_id, "bot": BotName})
        if not Newuser:
            return await msg.answer(f"⚠️ Subscription has been Expired for *{user_id}*", show_alert=True)
        CurrentPlanType = Newuser.get('planType', 'NORMAL')
        buttons = []
        for plan in ['NORMAL', 'PRO', 'CONQUEROR', 'LEGEND']:
            text = f"{'✔️' if plan == CurrentPlanType else ''} {plan}"
            buttons.append([InlineKeyboardButton(text, callback_data=f"setplan:{user_id}:{plan}:{BotName}")])
        buttons.append([InlineKeyboardButton("🔙 Back", callback_data=f"details:{user_id}:{BotName}")])
        await msg.message.edit_media(InputMediaPhoto(media="Modules/Tools/Thumbnail/AdminDashboard.jpg", caption=f"📝 Select new PlanType for <b>{user_id}</b>:\n\n<b>Current Plan :</b> {CurrentPlanType}"), reply_markup=InlineKeyboardMarkup(buttons))
    except Exception as e:
        return await msg.message.reply_text(f"<b>[✘] Error in SetPlanType :</b> <i>{e}</i>")

# ========================== 9). Set Dump-Logs ThreadId ==========================
@bot.on_callback_query(filters.regex(r"setDumps:(\d+):(\w+)$") & filters.user(owner_id))
async def set_dump_channel(bot: Client, msg: CallbackQuery):
    user_id = int(msg.data.split(':')[1])
    botName = msg.data.split(':')[2]
    try:
        Editable = await msg.message.reply_text("Send the ThreadId where you want to DUmps.")
        Input: Message = await bot.ask(msg.message.chat.id, "")
        
        # 🟢 FIX: Check karein ki input sahi number hai ya nahi
        if not Input.text or not Input.text.isdigit():
            await Input.delete()
            return await Editable.edit_text("❌ Invalid Thread ID! Please send a valid numeric Thread ID.")
            
        await Input.delete()
        await Editable.delete()
    
        result = ActiveUsersCollection.update_one({"userId": user_id, "bot": botName}, {"$set": {"dumpID": int(Input.text)}})
        if result.matched_count:
            return await msg.message.reply_text(f"<b>[✔] Dumps Thread-Id has been updated to __{Input.text}__ for @{botName}</b>")
        else:
            return await msg.answer(f"⚠️ User not Found or Expired or Revoked!", show_alert=True)
    except Exception as e:
        return await msg.message.reply_text(f"<b>[✘] Error in set Dump Thread-Id :</b> __{e}__")


# ==================== 10). Fetch full history of a user from Active, Revoked & Expired collections ====================
@bot.on_callback_query(filters.regex('show\$UserLogs') & filters.user(owner_id))
async def get_user_logs(bot: Client, msg: CallbackQuery):
    Editable = await msg.message.reply_text("Send the UserId to get his Subscription History.")
    input: Message = await bot.ask(msg.message.chat.id, "")
    
    # 🟢 FIX: Check karein ki input sahi number hai ya nahi
    if not input.text or not input.text.isdigit():
        await input.delete()
        return await Editable.edit_text("❌ Invalid User ID! Please send a valid numeric User ID.")
        
    user_id = int(input.text)
    await input.delete()
    
    logs = []
    active = list(ActiveUsersCollection.find({"userId": user_id}))
    revoked = list(RevokedUsersCollection.find({"userId": user_id}))
    expired = list(ExpiredUsersCollection.find({"userId": user_id}))

    if active:
        logs.append("✅ Active Records:")
        for u in active: logs.append(f"🤖 <b>Bot :</b> @{u['bot']} | <b>PlanType :</b> {u['planType']}\n⏳ <b>Expires :</b> {u['expiresAtIST']}\n📅 <b>Created :</b> {u['createdAtIST']}\n<b>━━━━━━━━━━━━━━</b>")
    if revoked:
        logs.append("⛔ Revoked Records:")
        for u in revoked:
            logs.append(f"🤖 <b>Bot :</b> @{u['bot']} | <b>PlanType :</b> {u['planType']}\n❌ <b>Revoked At :</b> {u['revokedAt']}\n<b>━━━━━━━━━━━━━━</b>")
    if expired:
        logs.append("⚠️ Expired Records:")
        for u in expired: logs.append(f"🤖 <b>Bot :</b> @{u['bot']} | <b>PlanType :</b> {u['planType']}\n⏳ <b>Expired At :</b> {u['expiredAt']}\n<b>━━━━━━━━━━━━━━</b>")

    if not logs:
        return await Editable.edit_text(f"🙅 No records found for User {user_id}")
    return await Editable.edit_text("\n".join(logs))


# ========================== 11). UPDATE CREDIT-NAME ==========================
@bot.on_callback_query(filters.regex(r"CrName:(\d+):(\w+)$") & filters.user(owner_id))
async def set_CreditName(bot: Client, msg: CallbackQuery):
    userId = int(msg.data.split(':')[1])
    botName = msg.data.split(':')[2]

    Editable = await msg.message.reply_text(f"<blockquote>Send the CreditName.</blockquote>")
    Input: Message = await bot.ask(msg.message.chat.id, "")
    await Input.delete()

    try:
        result = ActiveUsersCollection.update_one({"userId": userId, "bot": botName}, {"$set": {"CreditName": Input.text}})
        if result.matched_count:
            return await Editable.edit_text(f"<blockquote>Congratulation 🎉 Your **Powered By Name** has Successfully Update : **{Input.text}**.</blockquote>")
        else:
            return await msg.answer(f"UserId {userId} Not Found!", show_alert=True)
    except Exception as e:
        return await Editable.edit_text(f"❌ <b>Unable to Update CreditName :</b> {e}")
