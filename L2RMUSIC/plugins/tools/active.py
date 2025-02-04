from pyrogram import filters
from pyrogram.types import Message
from unidecode import unidecode

from L2RMUSIC import app
from L2RMUSIC.misc import SUDOERS
from L2RMUSIC.utils.database import (
    get_active_chats,
    get_active_video_chats,
    remove_active_chat,
    remove_active_video_chat,
)


@app.on_message(filters.command(["activevc", "activevoice"]) & SUDOERS)
async def activevc(_, message: Message):
    mystic = await message.reply_text("» ɢᴇᴛᴛɪɴɢ ᴀᴄᴛɪᴠᴇ ᴠᴏɪᴄᴇ ᴄʜᴀᴛs ʟɪsᴛ...")
    served_chats = await get_active_chats()
    text = ""
    j = 0
    for chat_id in served_chats:
        try:
            chat = await app.get_chat(chat_id)
            title = chat.title
            username = chat.username
            if username:
                text += f"<b>{j + 1}.</b> <a href=https://t.me/{username}>{unidecode(title).upper()}</a> [<code>{chat_id}</code>]\n"
            else:
                text += f"<b>{j + 1}.</b> {unidecode(title).upper()} [<code>{chat_id}</code>]\n"
            j += 1
        except Exception as e:
            # Log the error for debugging
            print(f"Error processing chat {chat_id}: {e}")
            await remove_active_chat(chat_id)
            continue
    
    if not text:
        await mystic.edit_text(f"» ɴᴏ ᴀᴄᴛɪᴠᴇ ᴠᴏɪᴄᴇ ᴄʜᴀᴛs ᴏɴ {app.mention}.")
    else:
        await mystic.edit_text(
            f"<b>» ʟɪsᴛ ᴏғ ᴄᴜʀʀᴇɴᴛʟʏ ᴀᴄᴛɪᴠᴇ ᴠᴏɪᴄᴇ ᴄʜᴀᴛs :</b>\n\n{text}",
            disable_web_page_preview=True,
        )


@app.on_message(filters.command(["activev", "activevideo"]) & SUDOERS)
async def activevi_(_, message: Message):
    mystic = await message.reply_text("» ɢᴇᴛᴛɪɴɢ ᴀᴄᴛɪᴠᴇ ᴠɪᴅᴇᴏ ᴄʜᴀᴛs ʟɪsᴛ...")
    served_chats = await get_active_video_chats()
    text = ""
    j = 0
    for chat_id in served_chats:
        try:
            chat = await app.get_chat(chat_id)
            title = chat.title
            username = chat.username
            if username:
                text += f"<b>{j + 1}.</b> <a href=https://t.me/{username}>{unidecode(title).upper()}</a> [<code>{chat_id}</code>]\n"
            else:
                text += f"<b>{j + 1}.</b> {unidecode(title).upper()} [<code>{chat_id}</code>]\n"
            j += 1
        except Exception as e:
            # Log the error for debugging
            print(f"Error processing chat {chat_id}: {e}")
            await remove_active_video_chat(chat_id)
            continue

    if not text:
        await mystic.edit_text(f"» ɴᴏ ᴀᴄᴛɪᴠᴇ ᴠɪᴅᴇᴏ ᴄʜᴀᴛs ᴏɴ {app.mention}.")
    else:
        await mystic.edit_text(
            f"<b>» ʟɪsᴛ ᴏғ ᴄᴜʀʀᴇɴᴛʟʏ ᴀᴄᴛɪᴠᴇ ᴠɪᴅᴇᴏ ᴄʜᴀᴛs :</b>\n\n{text}",
            disable_web_page_preview=True,
        )
