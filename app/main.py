from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from wekan_handler import create_new_card
import os
import logging

TELEGRAM_API_KEY = os.environ["TELEGRAM_API_KEY"]
TELEGRAM_GROUP_CHAT_ID = int(os.environ["TELEGRAM_GROUP_CHAT_ID"])  # -4126966079

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


async def task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if (
        update.effective_chat.id == TELEGRAM_GROUP_CHAT_ID
        and update.effective_message.reply_to_message is not None
    ):
        task_title = update.effective_message.text[6:]
        task_description = update.effective_message.reply_to_message.text

        new_card_link = create_new_card(title=task_title, description=task_description)
        await context.bot.sendMessage(
            chat_id=update.effective_chat.id,
            reply_to_message_id=update.effective_message.id,
            text=f"Card created: {new_card_link}",
        )


def main():
    application = Application.builder().token(TELEGRAM_API_KEY).build()
    application.add_handler(CommandHandler("task", callback=task))
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
