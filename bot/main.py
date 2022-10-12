from pyrogram import Client
from pyrogram.types import (
    InlineQueryResultVoice,
)
from config import Config
import logging
import uuid

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
    REQUEST_UUID = str(uuid.uuid4())
    if inline_query.query == "start":
        inline_query.answer(
        results=[
            InlineQueryResultVoice(
                voice_url=f"https://api.sosanie-ebla-bot-premium.vapronva.pw/voice/{REQUEST_UUID}",
                title="Ttle 2",
                id=REQUEST_UUID,
                caption="Caption 2",
            ),
        ],
        cache_time=1,
    )


try:
    bot.run()
except KeyboardInterrupt:
    bot.stop()
