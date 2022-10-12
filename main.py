from pyrogram import Client
from pyrogram.types import (
    InlineQueryResultArticle,
    InputTextMessageContent,
    InlineQueryResultVoice,
)
from config import Config
import logging

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
    inline_query.answer(
        results=[
            InlineQueryResultArticle(
                title="Test",
                input_message_content=InputTextMessageContent("Test"),
            )
        ]
    )


try:
    bot.run()
except KeyboardInterrupt:
    bot.stop()
