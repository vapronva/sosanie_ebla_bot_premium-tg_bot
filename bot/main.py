from pyrogram import Client
from pyrogram.types import (
    InlineQueryResultVoice,
    InlineQueryResultArticle,
    InputTextMessageContent,
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
                    input_message_content=InputTextMessageContent(
                        "<b>Sosanie Ebla Bot Premium</b>\n\n<i>Semi-public text-to-speech bot aimed to provide new level of comfort to its users at creating incredible and funny voice messages with high-quality TTS voices.</i>\n\n<code>;;</code> <a href='https://vprw.ru/sseblopremiumbot-gitlab'>source code</a>\n<code>;;</code> <a href='https://vprw.ru/sseblopremiumbot-authorwebsite'>author</a>\n\n<b>Usage:</b>\n<code>-</code> enter your query\n<code>-</code> select the desired voice, emotion and provider company (<code>[T]</code> — Tinkoff VoiceKit; <code>[Y]</code> — Yandex SpeechKit) with a given language (<code>[RU]</code> — Russian; <code>[DE]</code> — German; <code>[EN]</code> — English (US); <code>[KK]</code> — Kazakh; <code>[UZ]</code> — Uzbek)\n<code>-</code> laugh <i>:)</i>",
                    ),
                    thumb_url="https://gitlab.vapronva.pw/vapronva/sosanie_ebla_bot_premium-tg_bot/-/raw/main/_assets/botpic@2x.png",
                ),
            ],
            cache_time=600,
        )
        return
    USER_ID = inline_query.from_user.id
    try:
        IS_ALLOWED = requests.get(
            f"https://{CONFIG.get_vprw_api_endpoint()}/allowed",
            params={"user_id": USER_ID},
            headers={"X-API-Token": CONFIG.get_vprw_api_key()},
        ).json()["result"]["data"]["allowed"]
    except Exception as e:  # skipcq: PYL-W0703
        logging.error(e)
        IS_ALLOWED = False
    logging.info("User %s is allowed to perform TTS: %s", USER_ID, IS_ALLOWED)
    if IS_ALLOWED is False:
        inline_query.answer(
            results=[
                InlineQueryResultArticle(
                    title="Access Denied",
                    description=f"You are not allowed to use this bot. Please contact @{CONFIG.get_bot_contact_username()} to request the access.",
                    input_message_content=InputTextMessageContent(
                        f"<b>Access Denied to Sosanie Ebla Bot Premium™</b>\n\nYou are <i>not allowed</i> to use the bot.\nPlease contact @{CONFIG.get_bot_contact_username()} to request the access.\nPlease provide your Telegram ID (<code>{inline_query.from_user.id}</code>) in the request and describe your use case.",
                    ),
                ),
            ],
            cache_time=10,
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
            ),
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
