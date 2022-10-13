from pyrogram import Client
from pyrogram.types import (
    InlineQueryResultVoice,
    InlineQueryResultArticle,
)
from config import Config
import logging
import requests

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%H:%M:%S",
    handlers=[logging.StreamHandler()],
)

CONFIG = Config()

bot = Client(
    "sosanie_ebla_bot_premium-1",
    api_id=CONFIG.get_telegram_api_id(),
    api_hash=CONFIG.get_telegram_api_hash(),
    bot_token=CONFIG.get_telegram_bot_token(),
)


@bot.on_inline_query()
def answer_inline_query(_, inline_query):
    if inline_query.query == "":
        inline_query.answer(
            results=[
                InlineQueryResultArticle(
                    title="Sosanie Ebla Bot Premium",
                    description="введите текст для озвучивания",
                    input_message_content=f"<b>sosania ebla bot premium</b>\n\n<i></i>",
                )
            ],
            cache_time=5,
        )
        return
    USER_ID = inline_query.from_user.id
    try:
        IS_ALLOWED = requests.get(
            f"https://{CONFIG.get_vprw_api_endpoint()}/allowed",
            params={"user_id": USER_ID},
            headers={"X-API-Token": CONFIG.get_vprw_api_key()},
        ).json()["result"]["data"]["allowed"]
    except Exception as e:
        logging.error(e)
        IS_ALLOWED = False
    logging.info("User %s is allowed to perform TTS: %s", USER_ID, IS_ALLOWED)
    if IS_ALLOWED is False:
        inline_query.answer(
            results=[
                InlineQueryResultArticle(
                    title="Access Denied",
                    description=f"You are not allowed to use this bot. Please contact @{CONFIG.get_bot_contact_username()} to get access.",
                    input_message_content=f"<b>Access Denied</b>\n\nYou are <i>not allowed</i> to use this bot.\nPlease contact @{CONFIG.get_bot_contact_username()} to get access.",
                )
            ],
            cache_time=5,
        )
        return
    QUERY_TEXT = inline_query.query
    response = requests.post(
        url=f"https://{CONFIG.get_vprw_api_endpoint()}/tts/request",
        json={"user_id": USER_ID, "query": QUERY_TEXT},
        headers={"X-API-Token": CONFIG.get_vprw_api_key()},
    ).json()
    RESULTING_VOICE_MESSAGES = []
    for ttsv in response["result"]["data"]:
        RESULTING_VOICE_MESSAGES.append(
            InlineQueryResultVoice(
                title=ttsv["title"],
                voice_url=ttsv["url"],
                caption=ttsv["caption"],
            )
        )
    inline_query.answer(
        results=RESULTING_VOICE_MESSAGES,
        cache_time=response["result"]["cacheTime"],
    )
    logging.info(
        "Answered inline query with %s results for %s",
        len(RESULTING_VOICE_MESSAGES),
        USER_ID,
    )


bot.run()
