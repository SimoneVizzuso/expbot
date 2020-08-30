import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

from connection import insert_player, get_player, delete_player, gain_exp, check_player_level_up

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm at your service, sir!")
    print(update.message.text)


def register(update: Update, context: CallbackContext):
    user = update.message.from_user
    chat = update.message.chat
    player = get_player(user.id, chat.id)
    if player:
        print(user.username + " already exist in this chat")
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="I already know you, {}.\n"
                                      "If you want to know your level, please type '/status'".format(user.username))
    else:
        insert_player(user.id, chat.id)
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Now i know you! Welcome aboard, rookie\n"
                                      + "In this group you are at level 1 with 0 experience")
        print("Registered, id: {}, chat_id: {}".format(user.id, chat.id))


def unregister(update: Update, context: CallbackContext):
    user = update.message.from_user
    chat = update.message.chat
    player = get_player(user.id, chat.id)
    if not player:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="I don't know who you are!\nPlease, type '/register' to start your journey")
    else:
        delete_player(user.id, chat.id)
        print("Unregistered id: {}, chat_id: {}".format(user.id, chat.id))
        context.bot.send_message(chat_id=update.effective_chat.id, text="See you space cowboy...")


def status(update: Update, context: CallbackContext):
    user = update.message.from_user
    chat = update.message.chat
    player = get_player(user.id, chat.id)
    if not player:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="I don't know who you are!\nPlease, type '/register' to start your journey")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Hi {}, your current level is {}.\n"
                                      "You've earn {} experience in this group."
                                 .format(user.username, player.level, player.experience))


def echo(update: Update, context: CallbackContext):
    user = update.message.from_user
    chat = update.message.chat
    player = get_player(user.id, chat.id)
    gain_exp(user.id, chat.id)
    level_up = check_player_level_up(user.id, chat.id)
    if level_up:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="{} you have gained enough experience to level up!\n"
                                      "Your current level is {}."
                                 .format(user.username, player.level + 1))


"""
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


updater = Updater(token='1331836039:AAFxt9VD2nm-fqXQHolYIgn7CRQG3Kxy1mo', use_context=True)


def main():
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('register', register))
    dp.add_handler(CommandHandler('unregister', unregister))
    dp.add_handler(CommandHandler('status', status))
    dp.add_handler(MessageHandler(Filters.text & (~Filters.command), echo))
    dp.add_handler(MessageHandler(Filters.command, unknown))

    updater.start_polling()

    updater.idle()

    updater.stop()


if __name__ == '__main__':
    main()
