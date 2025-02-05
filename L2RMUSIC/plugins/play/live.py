from pyrogram import filters
from L2RMUSIC import YouTube, app
from L2RMUSIC.utils.channelplay import get_channeplayCB
from L2RMUSIC.utils.decorators.language import languageCB
from L2RMUSIC.utils.stream.stream import stream
from config import BANNED_USERS

@app.on_callback_query(filters.regex("LiveStream") & ~BANNED_USERS)
@languageCB
async def play_live_stream(client, CallbackQuery, _):
    callback_data = CallbackQuery.data.strip()
    
    # Parsing the callback data
    try:
        callback_request = callback_data.split(None, 1)[1]
        vidid, user_id, mode, cplay, fplay = callback_request.split("|")
    except Exception as e:
        # Return an alert if the callback data is malformed
        return await CallbackQuery.answer(_["playcb_1"], show_alert=True)

    # Ensure the callback query is from the correct user
    if CallbackQuery.from_user.id != int(user_id):
        try:
            return await CallbackQuery.answer(_["playcb_1"], show_alert=True)
        except Exception as e:
            # If the error happens here, just silently pass it
            print(f"Error during callback answer: {str(e)}")
            return
    
    # Fetch the chat id and channel info
    try:
        chat_id, channel = await get_channeplayCB(_, cplay, CallbackQuery)
    except Exception as e:
        print(f"Error in get_channeplayCB: {str(e)}")
        return await CallbackQuery.answer(_["playcb_2"], show_alert=True)
    
    # Determine if video is enabled based on 'mode'
    video = True if mode == "v" else None
    user_name = CallbackQuery.from_user.first_name

    # Delete the initial message that triggered the callback
    await CallbackQuery.message.delete()

    # Answer the callback query
    try:
        await CallbackQuery.answer()
    except Exception as e:
        # Catch any error in the callback response
        print(f"Error answering callback: {str(e)}")
        pass

    # Send a message indicating the start of the stream
    mystic = await CallbackQuery.message.reply_text(
        _["play_2"].format(channel) if channel else _["play_1"]
    )
    
    # Fetch the YouTube track details
    try:
        details, track_id = await YouTube.track(vidid, True)
    except Exception as e:
        print(f"Error fetching YouTube track: {str(e)}")
        return await mystic.edit_text(_["play_3"])

    # Determine if force play is enabled
    ffplay = True if fplay == "f" else None

    # If the video is not a live stream, send an appropriate message
    if not details.get("duration_min"):
        try:
            await stream(
                _,
                mystic,
                user_id,
                details,
                chat_id,
                user_name,
                CallbackQuery.message.chat.id,
                video,
                streamtype="live",
                forceplay=ffplay,
            )
        except Exception as e:
            ex_type = type(e).__name__
            err = e if ex_type == "AssistantErr" else _["general_2"].format(ex_type)
            return await mystic.edit_text(err)
    else:
        return await mystic.edit_text("» ɴᴏᴛ ᴀ ʟɪᴠᴇ sᴛʀᴇᴀᴍ.")

    # Delete the mystic message once the stream is successfully started
    await mystic.delete()
