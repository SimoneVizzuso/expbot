from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm at your service, sir!")
    print(update.message.text)


def register(update: Update, context: CallbackContext):
    if 'id' in context.user_data:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="I already know you, {}".format(context.user_data['first_name']))
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Now i know you!")
        user = update.message.from_user
        context.user_data['id'] = user.id
        context.user_data['first_name'] = user.first_name
        context.user_data['last_name'] = user.last_name
        context.user_data['username'] = user.username
        print("Registered user: {}, id: {}".format(context.user_data['username'], context.user_data['id']))


"""
def echo(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)
    print(update.message.text)


def caps(update: Update, context: CallbackContext):
    if context.args:
        text_caps = ' '.join(context.args).upper()
        context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="I'm expecting something to CAPS!")
    print(update.message.text)
"""


def unknown(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I don't know how to execute that command, not yet")


def main():
    updater = Updater(token='1331836039:AAFxt9VD2nm-fqXQHolYIgn7CRQG3Kxy1mo', use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('registerMe', register))
    # dp.add_handler(MessageHandler(Filters.text & (~Filters.command), echo))
    dp.add_handler(MessageHandler(Filters.command, unknown))

    updater.start_polling()

    updater.idle()

    updater.stop()


if __name__ == '__main__':
    main()
