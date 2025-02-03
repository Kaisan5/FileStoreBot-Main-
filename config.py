#(©)t.me/Anime_Eternals

import os
import logging
from logging.handlers import RotatingFileHandler



#Bot token @Botfather
TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "")

#Your API ID from my.telegram.org
APP_ID = int(os.environ.get("APP_ID", ""))

#Your API Hash from my.telegram.org
API_HASH = os.environ.get("API_HASH", "")

#Your database channel Id
CHANNEL_ID = int(os.environ.get("CHANNEL_ID", ""))

#OWNER ID
OWNER_ID = int(os.environ.get("OWNER_ID", "7784698094"))

#Port
PORT = os.environ.get("PORT", "8080")

#Database 
DB_URI = os.environ.get("DATABASE_URL", "")
DB_NAME = os.environ.get("DATABASE_NAME", "")

#force sub channel id, if you want enable force sub
FORCE_SUB_CHANNEL_1 = int(os.environ.get("FORCE_SUB_CHANNEL_1", "0"))
FORCE_SUB_CHANNEL_2 = int(os.environ.get("FORCE_SUB_CHANNEL_2", "0"))
FORCE_SUB_CHANNEL_3 = int(os.environ.get("FORCE_SUB_CHANNEL_3", "0"))
FORCE_SUB_CHANNEL_4 = int(os.environ.get("FORCE_SUB_CHANNEL_4", "0"))


TG_BOT_WORKERS = int(os.environ.get("TG_BOT_WORKERS", "4"))

#start message
START_MSG = os.environ.get("START_MESSAGE", "<blockquote><b>𝑯𝒆𝒚!! {mention} 𝑾𝒆𝒍𝒄𝒐𝒎𝒆 𝑻𝒐 𝑶𝒖𝒓 𝑵𝒆𝒙𝒖𝒔 𝑪𝒐𝒎𝒎𝒖𝒏𝒊𝒕𝒚.𝑰𝒇 𝒚𝒐𝒖 𝒘𝒂𝒏𝒕 𝒕𝒐 𝒔𝒖𝒑𝒑𝒐𝒓𝒕 𝒐𝒖𝒓 𝒄𝒐𝒎𝒎𝒖𝒏𝒊𝒕𝒚, 𝒚𝒐𝒖 𝒄𝒂𝒏 𝒅𝒐 𝒔𝒐 𝒃𝒚 𝒔𝒖𝒃𝒔𝒄𝒓𝒊𝒃𝒊𝒏𝒈 𝒕𝒐 𝒐𝒖𝒓 𝒄𝒉𝒂𝒏𝒏𝒆𝒍. 𝑭𝒐𝒓 𝒎𝒐𝒓𝒆 𝒊𝒏𝒇𝒐𝒓𝒎𝒂𝒕𝒊𝒐𝒏 𝑱𝒐𝒊𝒏 𝒐𝒖𝒓 𝒄𝒉𝒂𝒏𝒏𝒆𝒍 » @AnimeNexusNetwork\n\n 𝑻𝒉𝒂𝒏𝒌𝒔 𝑭𝒐𝒓 𝒚𝒐𝒖𝒓 𝑺𝒖𝒑𝒑𝒐𝒓𝒕 @Stelleron_Hunter</a></b></blockquote>",)
try:
    ADMINS=[]
    for x in (os.environ.get("ADMINS", "").split()):
        ADMINS.append(int(x))
except ValueError:
        raise Exception("Your Admins list does not contain valid integers.")

#Force sub message 
FORCE_MSG = os.environ.get("FORCE_SUB_MESSAGE", "Hey {first}  you have to join my all channels first to access files..\n\n So please join my channels first and click on  \"Try Again\" button...!")

#set your Custom Caption here, Keep None for Disable Custom Caption
CUSTOM_CAPTION = os.environ.get("CUSTOM_CAPTION", "<b>» ʙʏ @Anime_Eternalst</b>")

#set True if you want to prevent users from forwarding files from bot
PROTECT_CONTENT = True if os.environ.get('PROTECT_CONTENT', "False") == "True" else False

#Set true if you want Disable your Channel Posts Share button
DISABLE_CHANNEL_BUTTON = os.environ.get("DISABLE_CHANNEL_BUTTON", None) == 'True'

BOT_STATS_TEXT = "<b>BOT UPTIME</b>\n{uptime}"
USER_REPLY_TEXT = "ʙᴀᴋᴋᴀ ! ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴍʏ ꜱᴇɴᴘᴀɪ!!\n\n» ᴍʏ ᴏᴡɴᴇʀ : @KaiXSen"

ADMINS.append(OWNER_ID)
ADMINS.append(7784698094)

LOG_FILE_NAME = "logs.txt"

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt='%d-%b-%y %H:%M:%S',
    handlers=[
        RotatingFileHandler(
            LOG_FILE_NAME,
            maxBytes=50000000,
            backupCount=10
        ),
        logging.StreamHandler()
    ]
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)


def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)
