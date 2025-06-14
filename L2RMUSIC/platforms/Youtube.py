import asyncio
import os
import random
import re
from typing import Union

import httpx
import yt_dlp
from pyrogram.enums import MessageEntityType
from pyrogram.types import Message
from youtubesearchpython.__future__ import VideosSearch

from L2RMUSIC.utils.formatters import time_to_seconds
from L2RMUSIC.utils.database import is_on_off


def cookies() -> str:
    cookie_dir = "cookies"
    cookies_files = [f for f in os.listdir(cookie_dir) if f.endswith(".txt")]
    if not cookies_files:
        raise FileNotFoundError("No cookie files found in 'cookies/' directory.")
    return os.path.join(cookie_dir, random.choice(cookies_files))


async def shell_cmd(cmd: str) -> str:
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    out, err = await proc.communicate()
    out_decoded, err_decoded = out.decode(), err.decode()
    if err and "unavailable videos are hidden" not in err_decoded.lower():
        return err_decoded
    return out_decoded


async def api_download(vidid: str, video: bool = False) -> Union[str, None]:
    API = "https://api.cobalt.tools/api/json"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0",
    }

    path = os.path.join("downloads", f"{vidid}.mp4" if video else f"{vidid}.m4a")
    data = {
        "url": f"https://www.youtube.com/watch?v={vidid}",
        "vQuality": "480" if video else None,
        "isAudioOnly": None if video else "True",
        "aFormat": None if video else "opus",
    }
    data = {k: v for k, v in data.items() if v is not None}

    async with httpx.AsyncClient(http2=True) as client:
        response = await client.post(API, headers=headers, json=data)
        response.raise_for_status()
        results = response.json().get("url")

    cmd = f"yt-dlp '{results}' -o '{path}'"
    await shell_cmd(cmd)

    return path if os.path.isfile(path) else None


class YouTubeAPI:
    def __init__(self):
        self.base = "https://www.youtube.com/watch?v="
        self.regex = r"(?:youtube\.com|youtu\.be)"
        self.listbase = "https://youtube.com/playlist?list="
        self.reg = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")

    async def exists(self, link: str, videoid: Union[bool, str] = None) -> bool:
        return bool(re.search(self.regex, self.base + link if videoid else link))

    async def url(self, message_1: Message) -> Union[str, None]:
        messages = [message_1]
        if message_1.reply_to_message:
            messages.append(message_1.reply_to_message)

        for message in messages:
            entities = message.entities or message.caption_entities
            if entities:
                for entity in entities:
                    if entity.type == MessageEntityType.TEXT_LINK:
                        return entity.url
                    elif entity.type == MessageEntityType.URL:
                        text = message.text or message.caption
                        return text[entity.offset:entity.offset + entity.length]
        return None

    async def details(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        link = link.split("&")[0]

        results = VideosSearch(link, limit=1)
        for result in (await results.next())["result"]:
            title = result["title"]
            duration_min = result["duration"] or "0:00"
            duration_sec = int(time_to_seconds(duration_min))
            thumbnail = result["thumbnails"][0]["url"].split("?")[0]
            vidid = result["id"]
            return title, duration_min, duration_sec, thumbnail, vidid
        return None

    async def title(self, link: str, videoid: Union[bool, str] = None):
        return (await self.details(link, videoid))[0]

    async def duration(self, link: str, videoid: Union[bool, str] = None):
        return (await self.details(link, videoid))[1]

    async def thumbnail(self, link: str, videoid: Union[bool, str] = None):
        return (await self.details(link, videoid))[3]

    async def video(self, link: str, videoid: Union[bool, str] = None):
        link = self.base + link if videoid else link.split("&")[0]
        proc = await asyncio.create_subprocess_exec(
            "yt-dlp", "--cookies", cookies(), "-g", "-f",
            "best[height<=?720][width<=?1280]", link,
            stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await proc.communicate()
        if stdout:
            return 1, stdout.decode().split("\n")[0]
        return 0, stderr.decode()

    async def playlist(self, link: str, limit: int, user_id, videoid: Union[bool, str] = None):
        link = self.listbase + link if videoid else link.split("&")[0]
        raw = await shell_cmd(
            f"yt-dlp -i --get-id --flat-playlist --playlist-end {limit} --skip-download --cookies {cookies()} {link}"
        )
        return list(filter(None, raw.split("\n")))

    async def track(self, link: str, videoid: Union[bool, str] = None):
        details = await self.details(link, videoid)
        title, duration_min, _, thumbnail, vidid = details
        return {
            "title": title,
            "link": self.base + vidid,
            "vidid": vidid,
            "duration_min": duration_min,
            "thumb": thumbnail,
        }, vidid

    async def formats(self, link: str, videoid: Union[bool, str] = None):
        link = self.base + link if videoid else link.split("&")[0]
        ydl_opts = {"quiet": True, "cookiefile": cookies()}
        formats_available = []

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(link, download=False)
            for fmt in info.get("formats", []):
                if "dash" in str(fmt.get("format", "")).lower():
                    continue
                if all(k in fmt for k in ("format", "filesize", "format_id", "ext", "format_note")):
                    formats_available.append({
                        "format": fmt["format"],
                        "filesize": fmt["filesize"],
                        "format_id": fmt["format_id"],
                        "ext": fmt["ext"],
                        "format_note": fmt["format_note"],
                        "yturl": link,
                    })
        return formats_available, link

    async def download(
        self,
        link: str,
        mystic=None,
        video: Union[bool, str] = None,
        videoid: Union[bool, str] = None,
        songaudio: Union[bool, str] = None,
        songvideo: Union[bool, str] = None,
        format_id: Union[bool, str] = None,
        title: Union[bool, str] = None,
    ) -> Union[str, tuple]:
        if videoid:
            vidid = link
            link = self.base + vidid
        else:
            match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11})", link)
            vidid = match.group(1) if match else None

        loop = asyncio.get_running_loop()

        def run_download(opts):
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(link, download=True)
                return os.path.join("downloads", f"{info['id']}.{info['ext']}")

        if songvideo:
            await loop.run_in_executor(None, run_download, {
                "format": f"{format_id}+140",
                "outtmpl
