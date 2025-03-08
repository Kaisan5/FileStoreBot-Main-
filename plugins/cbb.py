
from pyrogram import __version__
from bot import Bot
from config import OWNER_ID
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

@Bot.on_callback_query()
async def cb_handler(client: Bot, query: CallbackQuery):
    data = query.data
    if data == "about":
        await query.message.edit_text(
            text = f"<blockquote><b>○ 𝐍𝐞𝐭𝐰𝐨𝐫𝐤 : <a href='https://t.me/AnimeNexusNetwork'>𝐀𝐧𝐢𝐦𝐞 𝐍𝐞𝐱𝐮𝐬</a>\n○ 𝐀ɴɪᴍᴇ 𝐂ʜᴀɴɴᴇʟ : <a href='https://t.me/Anime_Eternals'>𝐀𝐧𝐢𝐦𝐞 𝐄𝐭𝐞𝐫𝐧𝐚𝐥𝐬</a>\n○ 𝐎ɴɢᴏɪɴɢ 𝐂ʜᴀɴɴᴇʟ : <a href='https://t.me/+VxWwaMA6g_JkNTA9'>𝐎𝐧𝐠𝐨𝐢𝐧𝐠 𝐀𝐢𝐫𝐢𝐧𝐠𝐬</a>\n○ 𝐀ɴɪᴍᴇ 𝐂ʜᴀᴛ : <a href='https://t.me/Stelleron_Hunter'>𝐒𝐭𝐞𝐥𝐥𝐞𝐫𝐨𝐧 𝐇𝐮𝐧𝐭𝐞𝐫</a></b></blockquote>",
            disable_web_page_preview = True,
            reply_markup = InlineKeyboardMarkup(
                [
                    [
                    InlineKeyboardButton("ᴄʟᴏsᴇ", callback_data = "close"),
                    InlineKeyboardButton('ɴᴇxᴜs', url='https://t.me/AnimeNexusNetwork/98')
                    ]
                ]
            )
        )
    elif data == "close":
        await query.message.delete()
        try:
            await query.message.reply_to_message.delete()
        except:
            pass
