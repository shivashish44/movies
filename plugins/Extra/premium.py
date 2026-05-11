from datetime import timedelta, datetime
import pytz
import datetime as dt
from Script import script 
from info import ADMINS, LOG_CHANNEL
from utils import get_seconds
from database.users_chats_db import db 
from pyrogram import Client, filters 
from pyrogram.errors.exceptions.bad_request_400 import MessageTooLong
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

@Client.on_message(filters.command("add_premium"))
async def give_premium_cmd_handler(client, message):
    user_id = message.from_user.id
    if user_id not in ADMINS:
        await message.reply("ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴀɴʏ ᴘᴇʀᴍɪꜱꜱɪᴏɴ ᴛᴏ ᴜꜱᴇ ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ.")
        return
    
    if len(message.command) == 3:
        try:
            target_id = int(message.command[1])
            user = await client.get_users(target_id)
            duration = message.command[2]        
            seconds = await get_seconds(duration)
            
            if seconds > 0:
                # Expiry time calculate karein
                expiry_time = dt.datetime.now() + dt.timedelta(seconds=seconds)
                user_data = {"id": target_id, "expiry_time": expiry_time} 
                await db.update_user(user_data) 
                
                # Notifications set karein
                time_zone = dt.datetime.now(pytz.timezone("Asia/Kolkata"))
                current_time_str = time_zone.strftime("%d-%m-%Y\n⏱️ ᴊᴏɪɴɪɴɢ ᴛɪᴍᴇ : %I:%M:%S %p")           
                
                # Expiry ko IST mein convert karein
                expiry_ist = expiry_time.replace(tzinfo=dt.timezone.utc).astimezone(pytz.timezone("Asia/Kolkata"))
                expiry_str_in_ist = expiry_ist.strftime("%d-%m-%Y\n⏱️ ᴇxᴘɪʀʏ ᴛɪᴍᴇ : %I:%M:%S %p")  

                await message.reply_text(f"ᴘʀᴇᴍɪᴜᴍ ᴀᴅᴅᴇᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ᴛᴏ ᴛʜᴇ ᴜꜱᴇʀꜱ.\n👤 ᴜꜱᴇʀ ɴᴀᴍᴇ : {user.mention}\n⚡ ᴜꜱᴇʀ ɪᴅ : {user.id}\n⏰ ᴘʀᴇᴍɪᴜᴍ ᴀᴄᴄᴇꜱꜱ : {duration}")
                
                await client.send_message(
                    chat_id=target_id,
                    text=f"ᴘʀᴇᴍɪᴜᴍ ᴀᴅᴅᴇᴅ ᴛᴏ ʏᴏᴜʀ ᴀᴄᴄᴏᴜɴᴛ ꜰᴏʀ {duration} ᴇɴᴊᴏʏ 😀\n\n⏳ ᴊᴏɪɴɪɴɢ ᴅᴀᴛᴇ : {current_time_str}\n\n⌛️ ᴇxᴘɪʀʏ ᴅᴀᴛᴇ : {expiry_str_in_ist}",                
                )
                
                await client.send_message(LOG_CHANNEL, text=f"#Added_Premium\n\n👤 ᴜꜱᴇʀ : {user.mention}\n⚡ ᴜꜱᴇʀ ɪᴅ : {user.id}\n⏰ ᴘʀᴇᴍɪᴜᴍ ᴀᴄᴄᴇꜱꜱ : {duration}\n\n⏳ ᴊᴏɪɴɪɴɢ ᴅᴀᴛᴇ : {current_time_str}\n\n⌛️ ᴇxᴘɪʀʏ ᴅᴀᴛᴇ : {expiry_str_in_ist}", disable_web_page_preview=True)
            else:
                await message.reply_text("Invalid time format.")
        except Exception as e:
            await message.reply_text(f"Error: {e}")
    else:
        await message.reply_text("Usage: /add_premium user_id 10day")

@Client.on_message(filters.command("myplan"))
async def check_plans_cmd(client, message):
    user_mention = message.from_user.mention
    user_id = message.from_user.id
    
    if await db.has_premium_access(user_id):         
        remaining_time = await db.check_remaining_uasge(user_id)             
        days = remaining_time.days
        hours, remainder = divmod(remaining_time.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        formatted_remaining_time = f"{days} ᴅᴀʏꜱ, {hours} ʜᴏᴜʀꜱ, {minutes} ᴍɪɴᴜᴛᴇꜱ, {seconds} ꜱᴇᴄᴏɴᴅꜱ"
        
        # Current time mein remaining delta add karke expiry nikalna
        expiry_dt = dt.datetime.now() + remaining_time
        ist_zone = pytz.timezone("Asia/Kolkata")
        expiry_ist = expiry_dt.replace(tzinfo=dt.timezone.utc).astimezone(ist_zone)
        
        expiry_date = expiry_ist.strftime("%d-%m-%Y")
        expiry_time_str = expiry_ist.strftime("%I:%M:%S %p")
        
        await message.reply_text(f"📝 <u>ʏᴏᴜʀ ᴘʀᴇᴍɪᴜᴍ ꜱᴜʙꜱᴄʀɪᴘᴛɪᴏɴ ᴅᴇᴛᴀɪʟꜱ</u> :\n\n👤 ᴜꜱᴇʀ ɴᴀᴍᴇ : {user_mention}\n🏷️ ᴜꜱᴇʀ ɪᴅ : <code>{user_id}</code>\n⏱️ ᴇxᴘɪʀʏ ᴅᴀᴛᴇ : {expiry_date}\n⏱️ ᴇxᴘɪʀʏ ᴛɪᴍᴇ : {expiry_time_str}\n⏳ ʀᴇᴍᴀɪɴɪɴɢ ᴛɪᴍᴇ : {formatted_remaining_time}")
    else:
        btn = [ 
            [InlineKeyboardButton("ɢᴇᴛ ꜰʀᴇᴇ ᴛʀᴀɪʟ ꜰᴏʀ 𝟻 ᴍɪɴᴜᴛᴇꜱ ☺️", callback_data="give_trial")],
            [InlineKeyboardButton("ʙᴜʏ sᴜʙsᴄʀɪᴘᴛɪᴏɴ : ʀᴇᴍᴏᴠᴇ ᴀᴅs", callback_data="seeplans")],
        ]
        await message.reply_text(f"😔 ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴀɴʏ ᴘᴇʀᴍɪꜱꜱɪᴏɴ...", reply_markup=InlineKeyboardMarkup(btn))

@Client.on_message(filters.command("remove_premium"))
async def remove_premium(client, message):
    if message.from_user.id not in ADMINS:
        return await message.reply_text("ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴘᴇʀᴍɪꜱꜱɪᴏɴ.")
    
    if len(message.command) == 2:
        try:
            target_id = int(message.command[1])
            user = await client.get_users(target_id)
            if await db.remove_premium_access(target_id):
                await message.reply_text("ᴜꜱᴇʀ ʀᴇᴍᴏᴠᴇᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ !")
                await client.send_message(target_id, text=f"<b>ʜᴇʏ {user.mention}, ʏᴏᴜʀ ᴘʀᴇᴍɪᴜᴍ ᴘʟᴀɴ ʜᴀꜱ ʙᴇᴇɴ ᴇxᴘɪʀᴇᴅ.</b>")
            else:
                await message.reply_text("ᴜɴᴀʙʟᴇ ᴛᴏ ʀᴇᴍᴏᴠᴇ. ᴄʜᴇᴄᴋ ɪᴅ.")
        except:
            await message.reply_text("ɪɴᴠᴀʟɪᴅ ɪᴅ.")
    else:
        await message.reply_text("ᴜꜱᴀɢᴇ : /remove_premium user_id") 

@Client.on_message(filters.command("premium_users"))
async def premium_users_info(client, message):
    if message.from_user.id not in ADMINS:
        return await message.reply("ɴᴏ ᴘᴇʀᴍɪꜱꜱɪᴏɴ.")

    count = await db.all_premium_users()
    await message.reply(f"👥 ᴛᴏᴛᴀʟ ᴘʀᴇᴍɪᴜᴍ ᴜꜱᴇʀꜱ - {count}")

    users = await db.get_all_users()
    report = "📝 <u>ᴘʀᴇᴍɪᴜᴍ ᴜꜱᴇʀꜱ</u> :\n\n"
    user_count = 1
    
    async for user in users:
        data = await db.get_user(user['id'])
        if data and data.get("expiry_time"):
            expiry = data.get("expiry_time")
            # Timezone handling
            if expiry.tzinfo is None:
                expiry = pytz.utc.localize(expiry)
            
            current_time = dt.datetime.now(pytz.utc)
            
            if current_time > expiry:
                await db.remove_premium_access(user['id'])
                continue
            
            ist_expiry = expiry.astimezone(pytz.timezone("Asia/Kolkata"))
            time_left = ist_expiry - dt.datetime.now(pytz.timezone("Asia/Kolkata"))
            
            report += f"{user_count}. <code>{user['id']}</code> - {ist_expiry.strftime('%d-%m-%Y')} ({time_left.days} days left)\n"
            user_count += 1
    
    if len(report) > 4096:
        with open('info.txt', 'w') as f: f.write(report)
        return await message.reply_document('info.txt')
    await message.reply(report)

@Client.on_message(filters.command("plan"))
async def plan(client, message):
    btn = [[InlineKeyboardButton("🍁 𝗔𝗹𝗹 𝗣𝗹𝗮𝗻𝘀 🍁", callback_data='free')],
           [InlineKeyboardButton("❌ ᴄʟᴏꜱᴇ ❌", callback_data="close_data")]]
    await message.reply_photo(
        photo="https://graph.org/file/55a5392f88ec5a4bd3379.jpg", 
        caption=script.PREPLANS_TXT.format(message.from_user.mention), 
        reply_markup=InlineKeyboardMarkup(btn)
    )
