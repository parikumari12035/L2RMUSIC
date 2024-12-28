import asyncio
import importlib

from pyrogram import idle
from pytgcalls.exceptions import NoActiveGroupCall

import config
from L2RMUSIC import LOGGER, app, userbot
from L2RMUSIC.core.call import Ashish
from L2RMUSIC.misc import sudo
from L2RMUSIC.plugins import ALL_MODULES
from L2RMUSIC.utils.database import get_banned_users, get_gbanned
from config import BANNED_USERS


async def init():
    if (
        not config.STRING1
        and not config.STRING2
        and not config.STRING3
        and not config.STRING4
        and not config.STRING5
    ):
        LOGGER(__name__).error("Assistant client variables not defined, exiting...")
        exit()
    await sudo()
    try:
        users = await get_gbanned()
        for user_id in users:
            BANNED_USERS.add(user_id)
        users = await get_banned_users()
        for user_id in users:
            BANNED_USERS.add(user_id)
    except:
        pass
    await app.start()
    for all_module in ALL_MODULES:
        importlib.import_module("L2RMUSIC.plugins" + all_module)
    LOGGER("L2RMUSIC.plugins").info("Successfully Imported Modules...")
    await userbot.start()
    await Ashish.start()
    try:
        await Ashish.stream_call("https://te.legra.ph/file/29f784eb49d230ab62e9e.mp4")
    except NoActiveGroupCall:
        LOGGER("L2RMUSIC").error(
            "Please turn on the videochat of your log group\channel.\n\nStopping Bot..."
        )
        exit()
    except:
        pass
    await Ashish.decorators()
    LOGGER("L2RMUSIC").info("ᴠᴇɴᴏᴍxᴍᴜsɪᴄ ʙᴏᴛ sᴛᴀʀᴛᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ ɴᴏᴡ ᴇɴᴊᴏʏ")

    await idle()
    await app.stop()
    await userbot.stop()
    LOGGER("L2RMUSIC").info("Stopping L2RMUSIC Music Bot...")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(init())
