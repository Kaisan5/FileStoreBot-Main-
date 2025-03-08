"""
Module made by t.me/Zrekryu
Date: Tue, Feb 25 2025
Support chat at t.me/KangersChat
"""

import io
from typing import TypeAlias

import httpx

from telegram.constants import ParseMode
from telegram.ext import CommandHandler, ContextTypes
from telegram import (
    Animation,
    Document,
    File,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
    PhotoSize,
    Sticker,
    Update
    )

# Replace "YourRobot" with your telegram robot package name.
from YourRobot import application

SupportedMediaTypes: TypeAlias = Animation | Document | PhotoSize | Sticker

ENDPOINT: str = "https://sasta-api.vercel.app/googleLensSearch"

httpx_client: httpx.AsyncClient = httpx.AsyncClient(timeout=60)

class UnsupportedDocumentMimeType(Exception):
    def __init__(self, mime_type: str) -> None:
        self.mime_type = mime_type
        
        super().__init__(f"Unsupported MIME type: {self.mime_type}")

class STRINGS:
    PROCESSING = (
        "⏳ <b>Processing...</b>\n\n"
        "🔄 Please wait while we process your request."
        )
    
    USAGE: str = (
        "📕 <b>Usage:</b>\n"
        "🤖 <b>Command:</b> <code>/reverse (image_url)</code>\n"
        "▪ <i>image_url is optional.</i>\n"
        "▪ <i>Reply to a message containing media to search it.</i>\n"
        "▪ <i>If multiple media files are present, only the first one will be selected.</i>\n\n"
        "╭── 🗂️ <b>Supported Media Types:</b>\n"
        "├── 🎞️ <code>Animation (GIF)</code>\n"
        "├── 📄 <code>Document</code>\n"
        "├── 🖼️ <code>Photo</code>\n"
        "╰── 🏷️ <code>Sticker</code>"
        )
    
    UNSUPPORTED_DOCUMENT_TYPE: str = (
        "⚠️ <b>Unsupported Document Type:</b> <code>{unsupported_document_type}</code>\n\n"
        "╭── 🗂️ <b>Supported Document Types:</b>\n"
        "├── 🎞️ <code>Animation (GIF)</code>\n"
        "├── 📄 <code>Document</code>\n"
        "├── 🖼️ <code>Photo</code>\n"
        "╰── 🏷️ <code>Sticker</code>"
        )
    
    REPLIED_MESSAGE_HAS_NO_SUPPORTED_MEDIA: str = (
        "⚠️ <b>No supported media found!</b>\n\n"
        "ℹ️ The replied message does not contain any supported media types.\n\n"
        "╭── 🗂️ <b>Supported Media Types:</b>\n"
        "├── 🎞️ <code>Animation (GIF)</code>\n"
        "├── 📄 <code>Document</code>\n"
        "├── 🖼️ <code>Photo</code>\n"
        "╰── 🏷️ <code>Sticker</code>"
        )
    
    REQUESTING_TO_API_SERVER: str = "📡 Requesting to <b>API Server</b>... 📶"
    SERVER_ERROR_OCCURRED: str = (
        "❌ <b>An error occurred!</b>\n\n"
        "⚠️ <b>Error:</b>\n"
        "<code>{error}</code>"
        )
    
    DOWNLOADING_MEDIA: str = "⏳ <b>Downloading media...</b>"
    FAILED_TO_DOWNLOAD_MEDIA: str = (
        "❌ <b>Failed to download media</b>\n\n"
        "⚠️ <b>Error:</b>\n"
        "<code>{error}</code>"
        )
    
    PARSING_SEARCH_RESULT: str = "💻 <b>Parsing search result...</b>"
    
    RELATED_SEARCHES_FORMAT: str = (
        "<code>{name}</code>"
        " — "
        "<a href='{link}'>Link</a>"
        )
    
    SEARCH_RESULT: str = (
        "╭── 🔍 <b>Related Searches:</b>\n{related_searches}\n\n"
        "🔗 <b>Search Result Page Link:</b> <a href='{search_url}'>Link</a>\n"
        "✨ <b>Credits:</b> <a href='https://t.me/KangersNetwork/'>Kangers Network</a>"
        )
    
    OPEN_SEARCH_RESULT_PAGE: str = "↗️ Open Search Result Page 🔗"

async def request_by_file(file_name: str, file: io.BytesIO, mime_type: str) -> httpx.Response:
    response: httpx.Response = await httpx_client.post(
        url=ENDPOINT,
        files={"file": (file_name, file, mime_type)}
        )
    return response

async def request_by_url(image_url: str) -> httpx.Response:
    params: dict[str, str] = {
        "image_url": image_url
    }
    response: httpx.Response = await httpx_client.get(
        url=ENDPOINT,
        params=params
        )
    return response

async def download_media_to_memory(media: SupportedMediaTypes) -> io.BytesIO:
    file: File = await media.get_file()
    
    file_stream: io.Bytes = io.BytesIO()
    await file.download_to_memory(file_stream)
    
    return file_stream

def extract_media(message: Message) -> tuple[str, SupportedMediaTypes, str] | None:
    if message.animation:
        return (message.animation.file_name, message.animation, message.animation.mime_type)
    elif message.document:
        if not message.document.mime_type.startswith("image/"):
            raise UnsupportedDocumentMimeType(mime_type=message.document.mime_type)
        else:
            return (message.document.file_name, message.document, message.document.mime_type)
    elif message.photo:
        return ("image.jpg", message.photo[-1], "image/jpeg")
    elif message.sticker:
        sticker_mime_type: str = "image/webp"
        if message.sticker.is_animated:
            sticker_mime_type = "application/x-tgsticker"
        elif message.sticker.is_video:
            sticker_mime_type = "video/webm"
        
        return ("sticker.webp", message.sticker, sticker_mime_type)
    else:
        return None

async def request_by_file_or_url(file_or_url: io.BytesIO | str, file_name: str | None = None, mime_type: str | None = None) -> httpx.Response:
    if isinstance(file_or_url, io.BytesIO):
        return await request_by_file(file_name, file_or_url, mime_type)
    elif isinstance(file_or_url, str):
        return await request_by_url(file_or_url)
    else:
        raise TypeError(f"file_or_url must be an instance of either io.BytesIO or str, not {type(file_or_url)}")

async def on_google_lens_search(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message: Message = update.effective_message
    
    status_msg: Message = await message.reply_text(
        text=STRINGS.PROCESSING,
        parse_mode=ParseMode.HTML
        )
    
    file_name: str
    file: io.BytesIO
    mime_type: str
    image_url: str
    file_name, file, mime_type, image_url = None, None, None, None
    
    reply_msg: Message
    if (reply_msg := message.reply_to_message):
        try:
            media: SupportedMediaTypes
            file_name, media, mime_type = extract_media(reply_msg)
        except UnsupportedDocumentMimeType as exc:
            await status_msg.edit_text(
                text=STRINGS.UNSUPPORTED_DOCUMENT_TYPE.format(unsupported_document_type=exc.mime_type),
                parse_mode=ParseMode.HTML
                )
            return
        
        if media is not None:
            await status_msg.edit_text(
                text=STRINGS.DOWNLOADING_MEDIA,
                parse_mode=ParseMode.HTML
                )
            
            try:
                file: io.BytesIO = await download_media_to_memory(media)
            except Exception as exc:
                await status_msg.edit_text(
                    text=STRINGS.FAILED_TO_DOWNLOAD_MEDIA.format(error=exc),
                    parse_mode=ParseMode.HTML
                    )
                return
        else:
            await status_msg.edit_text(
                text=STRINGS.REPLIED_MESSAGE_HAS_NO_SUPPORTED_MEDIA,
                parse_mode=ParseMode.HTML
                )
            return
    else:
        url: str = context.args[0] if context.args else None
    
    if file is None and url is None:
        await status_msg.edit_text(
            text=STRINGS.USAGE,
            parse_mode=ParseMode.HTML
            )
        return
    
    await status_msg.edit_text(
        text=STRINGS.REQUESTING_TO_API_SERVER,
        parse_mode=ParseMode.HTML
        )
    response: httpx.Response = await request_by_file_or_url(
        file_or_url=file or url,
        file_name=file_name,
        mime_type=mime_type
        )
    
    if response.status_code != 200:
        try:
            response_json = response.json()
            error = response.json().get("error", response_json)
        except httpx.JsonDecodeError:
            error = response.text
        
        await status_msg.edit_text(
            text=STRINGS.SERVER_ERROR_OCCURRED.format(error=error),
            parse_mode=ParseMode.HTML
            )
        return
    
    await status_msg.edit_text(
        text=STRINGS.PARSING_SEARCH_RESULT,
        parse_mode=ParseMode.HTML
        )
    
    result: dict[str, list[tuple[str, str]] | str] = response.json()
    
    related_searches: list[tuple[str, str]] = result["related_searches"]
    search_url: str = result["search_url"]
    
    if related_searches:
        related_searches_parsed: str = "\n".join(
            ("├── " if i < len(related_searches) - 1 else "╰── ") +
            STRINGS.RELATED_SEARCHES_FORMAT.format(name=name, link=link)
            for i, (name, link) in enumerate(related_searches)
            )
    else:
        related_searches_parsed: str = "╰── ❌ <i>Not Found</i>" 
    
    text: str = STRINGS.SEARCH_RESULT.format(
        related_searches=related_searches_parsed,
        search_url=search_url
        )
    
    keyboard: list[list[InlineKeyboardButton]] = [
        [InlineKeyboardButton(text=STRINGS.OPEN_SEARCH_RESULT_PAGE, url=search_url)]
    ]
    await status_msg.edit_text(
        text=text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True
        )

GOOGLE_LENS_SEARCH_HANDLER: CommandHandler = CommandHandler(
    command=("reverse", "grs", "gis", "lens", "glens"),
    callback=on_google_lens_search
    )

application.add_handler(GOOGLE_LENS_SEARCH_HANDLER)

__mod_name__ = "Google Lens Search"
__command_list__ = ["reverse", "grs", "gis", "lens", "glens"]
__handlers__ = [GOOGLE_LENS_SEARCH_HANDLER]