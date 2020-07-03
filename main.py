from telegram import Update
from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram import ChatAction
from telegram import ParseMode
from telegram.ext import Updater
from telegram.ext import CallbackContext
from telegram.ext import Filters, MessageHandler, CommandHandler, CallbackQueryHandler

import config
from build_menu import get_markup, button_list

from customize import send_action
from time import sleep
import datetime


button_text = "Button"


# ========================== Start callback ==========================


@send_action(ChatAction.TYPING)
def start_callback(update: Update, context: CallbackContext):
    # Just for demonstration
    sleep(1)
    if context.args:
        update.message.reply_text("You said: " + " ".join(context.args))
    else:
        update.message.reply_text("Hello")


# ========================== Button callback ==========================


def button_text_callback(update: Update, context: CallbackContext):
    # Removing the keyboard
    update.message.reply_text(
        text = "You pressed the button, text keyboard disappears",
        reply_markup = ReplyKeyboardRemove()
    )


# ========================== Inline button callback ==========================


def inline_button_callback(update: Update, context: CallbackContext):
    """
    This handler will receive every event from inline buttons
    """
    query = update.callback_query
    data = query.data
    # Why effective?..
    text = update.effective_message.text
    now = datetime.datetime.now()

    if data == button_list[0].callback_data:
        query.edit_message_text(text = "Pressed 1st button, keyboard disappears")
    elif data == button_list[1].callback_data:
        # It's crucial every time to make new message, or there will be an error
        query.edit_message_text(
            text = "Pressed 2nd button at {}, keyboard won't disappear".format(now),
            reply_markup = get_markup()
        )
    else:
        query.message.delete()
        query.message.reply_text(
            text = "Pressed 3rd button, keyboard's on the *NEW* message",
            reply_markup = get_markup(),
            parse_mode = ParseMode.MARKDOWN
        )


# ========================== Message callback ==========================


def message_callback(update: Update, context: CallbackContext):
    # Handling button press
    text = update.message.text
    if text == button_text:
        # No need to register this handler in the dispatcher
        return button_text_callback(update = update, context = context)
    elif text == "Get inline":
        update.message.reply_text(text = "Some buttons under the message", reply_markup = get_markup())
    else:
        # Creating keyboard
        reply_markup = ReplyKeyboardMarkup(
            resize_keyboard = True,
            keyboard = [
                [KeyboardButton(button_text), KeyboardButton(button_text)],
                [KeyboardButton(button_text)]
            ]
        )

        # Replying
        update.message.reply_text(text = "Added text keyboard", reply_markup = reply_markup)


# ========================== Main function ==========================


def main():
    # Updater fetches updates from Telegram
    updater = Updater(token = config.TOKEN, use_context = True)

    # Command handlers should be added before other handlers
    updater.dispatcher.add_handler(CommandHandler("start", start_callback))
    # Adding message handler
    updater.dispatcher.add_handler(MessageHandler(filters = Filters.text, callback = message_callback))
    updater.dispatcher.add_handler(CallbackQueryHandler(inline_button_callback, pass_chat_data = True))

    # Starting to fetch updater
    updater.start_polling()


if __name__ == "__main__":
    main()