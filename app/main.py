from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from wekan_handler import create_new_card, backlog_list, todo_list
import os
import logging

TELEGRAM_API_KEY = os.environ["TELEGRAM_API_KEY"]
TELEGRAM_GROUP_CHAT_ID = int(os.environ["TELEGRAM_GROUP_CHAT_ID"])

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


def is_group_chat_and_reply_to_message(update):
    return (
        update.effective_chat.id == TELEGRAM_GROUP_CHAT_ID
        and update.effective_message.reply_to_message is not None
    )


async def backlog(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if is_group_chat_and_reply_to_message(update):
        reply_message_text = update.effective_message.reply_to_message.text
        new_card_link = create_new_card(
            list=backlog_list, description=reply_message_text
        )
        await context.bot.sendMessage(
            chat_id=update.effective_chat.id,
            reply_to_message_id=update.effective_message.id,
            text=f"Card created: {new_card_link}",
        )


async def todo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if is_group_chat_and_reply_to_message(update):
        reply_message_text = update.effective_message.reply_to_message.text
        new_card_link = create_new_card(list=todo_list, description=reply_message_text)
        await context.bot.sendMessage(
            chat_id=update.effective_chat.id,
            reply_to_message_id=update.effective_message.id,
            text=f"Card created: {new_card_link}",
        )


def main():
    application = Application.builder().token(TELEGRAM_API_KEY).build()
    application.add_handler(CommandHandler("backlog", callback=backlog))
    application.add_handler(CommandHandler("todo", callback=todo))
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
