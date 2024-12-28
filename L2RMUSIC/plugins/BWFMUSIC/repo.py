from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from L2RMUSIC import app
from config import BOT_USERNAME
from L2RMUSIC.utils.errors import capture_err
import httpx 
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

start_txt = """
✰ 𝗪ᴇʟᴄᴏᴍᴇ ᴛᴏ 𝗧ᴇᴀᴍ 𝐈sᴛᴋʜᴀʀ 𝗥ᴇᴘᴏs ✰
 
✰ 𝗥ᴇᴘᴏ ᴛᴏ 𝗡ʜɪ 𝗠ɪʟᴇɢᴀ 𝗬ʜᴀ
 
✰ 𝗣ᴀʜʟᴇ 𝗣ᴀᴘᴀ 𝗕ᴏʟ 𝗥ᴇᴘᴏ 𝗢ᴡɴᴇʀ ᴋᴏ 

✰ || @L2R_KING ||
 
✰ 𝗥ᴜɴ 24x7 𝗟ᴀɢ 𝗙ʀᴇᴇ 𝗪ɪᴛʜᴏᴜᴛ 𝗦ᴛᴏᴘ
 
"""




@app.on_message(filters.command("repo"))
async def start(_, msg):
    buttons = [
        [ 
          InlineKeyboardButton("⛩️𝐀ᴅᴅ ᴍᴜsɪᴄ 𝐁σт⛩️", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")
        ],
        [
          InlineKeyboardButton("𝐑ᴇᴘᴏ", url="https://github.com/BWFTIME/L2RMUSIC"),
          InlineKeyboardButton("𝐿2𝙍ꨄ𝐊𝐈𝐍𝐆", url="https://t.me/L2R_KING"),
          ],
               [
                InlineKeyboardButton("Gʀᴏᴜᴘꨄ︎•ʙωғ❣️", url=f"https://t.me/BWF_MUSIC1"),
],
[
InlineKeyboardButton("[🥀✨➪ 𝙊𝙁𝙁𝙄𝘾𝙄𝘼𝙇⏎】☠︎︎", url=f"https://t.me/MentalMusicRobot"),

        ]]
    
    reply_markup = InlineKeyboardMarkup(buttons)
    
    await msg.reply_photo(
        photo="https://telegra.ph/file/e576aa8308c49d945f433.jpg",
        caption=start_txt,
        reply_markup=reply_markup
      )
