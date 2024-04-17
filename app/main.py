from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from wekan_handler import create_new_card, backlog_list, todo_list
import os
import logging
from gitlab import get_latest_apk

TELEGRAM_API_KEY = os.environ["TELEGRAM_API_KEY"]
TELEGRAM_GROUP_CHAT_ID = int(os.environ["TELEGRAM_GROUP_CHAT_ID"])

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


def extract_card_title_from_message(update):
    message_without_command = update.effective_message.text.split()[1:]
    card_title = " ".join([str(x) for x in message_without_command])
    return card_title


def is_group_chat_and_reply_to_message(update):
    return (
        update.effective_chat.id == TELEGRAM_GROUP_CHAT_ID
        and update.effective_message.reply_to_message is not None
    )


def is_group_chat(update):
    return update.effective_chat.id == TELEGRAM_GROUP_CHAT_ID


async def backlog(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if is_group_chat_and_reply_to_message(update):
        reply_message_text = update.effective_message.reply_to_message.text
        card_title = extract_card_title_from_message(update)

        new_card_link = create_new_card(
            list=backlog_list, description=reply_message_text, title=card_title
        )
        await context.bot.sendMessage(
            chat_id=update.effective_chat.id,
            reply_to_message_id=update.effective_message.id,
            text=f"Card created: {new_card_link}",
        )


async def todo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if is_group_chat_and_reply_to_message(update):
        reply_message_text = update.effective_message.reply_to_message.text
        card_title = extract_card_title_from_message(update)

        new_card_link = create_new_card(
            list=todo_list, description=reply_message_text, title=card_title
        )
        await context.bot.sendMessage(
            chat_id=update.effective_chat.id,
            reply_to_message_id=update.effective_message.id,
            text=f"Card created: {new_card_link}",
        )


async def get_latest_build(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if is_group_chat(update):
        apk_name = get_latest_apk()
        await context.bot.sendDocument(
            chat_id=update.effective_chat.id, document=apk_name
        )


def main():
    application = Application.builder().token(TELEGRAM_API_KEY).build()
    application.add_handler(CommandHandler("backlog", callback=backlog))
    application.add_handler(CommandHandler("todo", callback=todo))
    application.add_handler(CommandHandler("getlatestbuild", callback=get_latest_build))
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
