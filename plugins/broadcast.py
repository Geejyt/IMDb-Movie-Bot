from pyrogram import Client, filters
import datetime
import time
from database.users_chats_db import db
from info import ADMINS
from utils import broadcast_messages
import asyncio
        
@Client.on_message(filters.command("broadcast") & filters.user(ADMINS) & filters.reply)
# https://t.me/JosProjects
async def verupikkals(bot, message):
    users = await db.get_all_users()
    b_msg = message.reply_to_message
    sts = await message.reply_text(
        text='Diffuser vos messages...'
    )
    start_time = time.time()
    total_users = await db.total_users_count()
    done = 0
    blocked = 0
    deleted = 0
    failed =0

    success = 0
    async for user in users:
        pti, sh = await broadcast_messages(int(user['id']), b_msg)
        if pti:
            success += 1
        elif pti == False:
            if sh == "Blockée":
                blocked+=1
            elif sh == "Supprimée":
                deleted += 1
            elif sh == "Erreur":
                failed += 1
        done += 1
        await asyncio.sleep(2)
        if not done % 20:
            await sts.edit(f"Diffusion en cours:\n\nUtilisateurs totales {total_users}\nComplet: {done} / {total_users}\nSuccés: {success}\nBlockées: {blocked}\nSupprimée: {deleted}")    
    time_taken = datetime.timedelta(seconds=int(time.time()-start_time))
    await sts.edit(f"Diffusion Completet:\nComplet en {time_taken} secondes.\n\nUtilisateurs totales {total_users}\nComplet: {done} / {total_users}\nSuccés: {success}\nBlockées: {blocked}\nSupprimée: {deleted}")
