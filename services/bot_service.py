import asyncio
from uuid import uuid4

from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.constants import ParseMode
from telegram.ext import ContextTypes, Application, InlineQueryHandler

from services.api_service import get_random_quote
from services.env_service import get_env_var
from services.stats_service import StatsService


class BotService:
    @staticmethod
    async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle the inline query. This is run when you type: @botusername <query>"""
        try:
            users = StatsService.get_users()
            players_text = '<b>Игроки:</b>\n'
            for usr in users:
                players_text += f'<a href="tg://user?id={usr["id"]}">@{usr["username"]}</a>\n'
        except Exception as e:
            players_text = 'Сервер не отвечает('

        quote = get_random_quote()
        print(quote)
        quote_text = f'<blockquote>{quote["quoteText"]}</blockquote>\n<i><b>©{quote["quoteAuthor"] or "Аноним"}</b></i>'

        results = [
            InlineQueryResultArticle(
                id=str(uuid4()),
                title="Игроки",
                input_message_content=InputTextMessageContent(players_text, parse_mode=ParseMode.HTML),
                thumbnail_url='https://cdn-icons-png.flaticon.com/512/1409/1409029.png'
            ),
            InlineQueryResultArticle(
                id=str(uuid4()),
                title="Цитата для брата",
                input_message_content=InputTextMessageContent(quote_text, parse_mode=ParseMode.HTML),
                thumbnail_url='https://cdn-icons-png.flaticon.com/128/2190/2190622.png'
            ),
        ]

        await update.inline_query.answer(results, cache_time=0)

    @staticmethod
    def run_telegram_bot() -> Application:
        bot_token = get_env_var("BOT_TOKEN")
        application = Application.builder().token(bot_token).updater(None).build()

        application.add_handler(InlineQueryHandler(callback=BotService.inline_query))

        # Start the Bot
        return application
