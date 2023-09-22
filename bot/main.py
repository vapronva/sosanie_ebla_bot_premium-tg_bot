import logging

import requests
import sentry_sdk
from config import Config
from pyrogram import Client  # type: ignore
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InlineQueryResultArticle,
    InlineQueryResultVoice,
    InputTextMessageContent,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%H:%M:%S",
    handlers=[logging.StreamHandler()],
)

CONFIG = Config()

sentry_sdk.init(
    dsn=CONFIG.get_sentry_dsn(),
    release=CONFIG.get_deployment_release(),
    environment=CONFIG.get_deployment_environment(),
    traces_sample_rate=1.0,
    enable_tracing=True,
)

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
                        "<b>Sosanie Ebla Bot Premium</b>\n\n<i>Semi-public text-to-speech bot aimed to provide new level of comfort to its users at creating incredible and funny voice messages with high-quality TTS voices.</i>\n\n<code>;;</code> <a href='https://vprw.ru/redirect/telegrambot/sseblopremiumbot/source-code'>source code</a>\n<code>;;</code> <a href='https://vprw.ru/redirect/telegrambot/sseblopremiumbot/author'>author</a>\n\n<b>Usage:</b>\n<code>-</code> enter your query\n<code>-</code> select the desired voice, emotion and provider company (<code>[T]</code> — Tinkoff VoiceKit; <code>[Y]</code> — Yandex SpeechKit; <code>[S]</code> — SberBank SaluteSpeech; <code>[V]</code> — VK / MailRu Cloud Voice) with a given language (<code>[RU]</code> — Russian; <code>[DE]</code> — German; <code>[EN]</code> — English (US); <code>[KK]</code> — Kazakh; <code>[UZ]</code> — Uzbek); <code>[HE]</code> — Hebrew\n<code>-</code> laugh <i>:)</i>",
                    ),
                    thumb_url="https://gl.vprw.ru/sosanie-ebla-bot/sseblopremiumbot/-/raw/main/_assets/botpic@2x.png",
                ),
            ],
            cache_time=600,
        )
        return
    USER_ID = inline_query.from_user.id
    try:
        IS_ALLOWED = requests.get(
            f"https://{CONFIG.get_vprw_api_endpoint()}/allowed",
            timeout=25,
            params={"user_id": USER_ID},
            headers={"X-API-Token": CONFIG.get_vprw_api_key()},
        ).json()["result"]["data"]["allowed"]
    except Exception as e:  # skipcq: PYL-W0703
        logging.error(e)
        IS_ALLOWED = False
    logging.info("User %s is allowed to perform TTS: %s", USER_ID, IS_ALLOWED)
    if not IS_ALLOWED:
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
        timeout=25,
        json={"user_id": USER_ID, "query": QUERY_TEXT},
        headers={"X-API-Token": CONFIG.get_vprw_api_key()},
    ).json()
    RESULTING_VOICE_MESSAGES = [
        InlineQueryResultVoice(
            title=ttsv["title"],
            voice_url=ttsv["url"],
            caption=ttsv["caption"],
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text="💬",
                            callback_data=f"getshwsgt-{ttsv['callbackData']['getVoiceTextID']}",
                        ),
                        InlineKeyboardButton(
                            text="⬇️",
                            url=f"{ttsv['callbackData']['publicVoiceWavUrl']}",
                        ),
                        InlineKeyboardButton(
                            text="🤖",
                            switch_inline_query_current_chat=inline_query.query,
                        ),
                    ],
                ],
            ),
        )
        for ttsv in response["result"]["data"]
    ]
    inline_query.answer(
        results=RESULTING_VOICE_MESSAGES,
        cache_time=response["result"]["cacheTime"],
    )
    logging.info(
        "Answered inline query with %s results for %s",
        len(RESULTING_VOICE_MESSAGES),
        USER_ID,
    )


@bot.on_callback_query()
def answer_callback_query(_, callback_query):
    try:
        callback_action, request_id_part, callback_id = callback_query.data.split("-")
    except ValueError as e:
        logging.error(e)
        return
    if any([callback_action is None, request_id_part is None, callback_id is None]):
        return
    if callback_action == "getshwsgt":
        response = requests.get(
            url=f"https://{CONFIG.get_vprw_api_endpoint()}/callback/action/getshwsgt/{request_id_part}-{callback_id}",
            timeout=25,
            headers={"X-API-Token": CONFIG.get_vprw_api_key()},
        ).json()
        try:
            callback_query.answer(
                (response["result"]["data"]["text"][:190] + '..."')
                if len(response["result"]["data"]["text"]) > 190
                else response["result"]["data"]["text"],
                show_alert=response["result"]["data"]["show_alert"],
            )
        except KeyError as e:
            logging.error(e)


bot.run()
