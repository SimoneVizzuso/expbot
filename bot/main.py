import logging
from datetime import datetime

from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

from connection import insert_player, get_player, gain_exp, check_player_level_up, get_top_ten

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="I'm at your service, sir!\n"
                                  "This bot provide a rank system for your chat or group\n"
                                  "Automatically adds the players when they write the first message\n"
                                  "Chack your stats with /status and the chat ranks with /leaderboard")


def status(update: Update, context: CallbackContext):
    user = update.effective_message.from_user
    chat = update.effective_message.chat
    player = get_player(user.id, chat.id)
    if not player:
        update.message.reply_text("I don't know who you are!\nPlease, type /register to start your journey")
    else:
        update.message.reply_text("Hi {}, your current level is {}.\n"
                                  "You've earn {} experience in this group."
                                  .format(user.username, player.level, player.experience))


def echo(update: Update, context: CallbackContext):
    user = update.effective_message.from_user
    chat = update.effective_message.chat
    player = get_player(user.id, chat.id)
    if player is not None:
        if not antiflood(user.id, chat.id):
            gain_exp(user.id, chat.id)
            level_up = check_player_level_up(user.id, chat.id)
            name = user.username if user.username else user.first_name
            if level_up:
                context.bot.send_message(chat_id=update.effective_chat.id,
                                         text="{} you have gained enough experience to level up!\n"
                                              "Your current level is {}."
                                         .format(name, player.level + 1))
    else:
        insert_player(user.id, chat.id)
        gain_exp(user.id, chat.id)


def rank(update: Update, context: CallbackContext):
    chat = update.effective_message.chat
    leaderboard = get_top_ten(chat.id)
    if not leaderboard:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="No one is currently registered! How dare you...")
    else:
        response = "Ladies and Gentlemen, this is the current leaderboard\n"
        i = 1
        for player in leaderboard:
            if context.bot.getChatMember(chat.id, player.user_id).user.username:
                name = str(context.bot.getChatMember(chat.id, player.user_id).user.username)
            elif context.bot.getChatMember(chat.id, player.user_id).user.first_name:
                name = str(context.bot.getChatMember(chat.id, player.user_id).user.first_name)
            else:
                name = str(context.bot.getChatMember(chat.id, player.user_id).user.id)

            response = response + str(i) + "# place " + name + \
                       " al level " + str(player.level) + " (exp " + str(player.experience) + ")\n"
            i = i + 1
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=response)


def unknown(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I don't know how to execute that command, not yet")


bursts = {}


def antiflood(user_id, chat_id):
    key = f"{user_id}@{chat_id}"
    burst = bursts.get(key, {"begin": datetime.now(), "count": 0})

    if (datetime.now() - burst["begin"]).total_seconds() < 3:
        burst["count"] += 1
        bursts[key] = burst
        return burst["count"] > 4
    else:
        bursts[key] = {"begin": datetime.now(), "count": 1}
        return True


updater = Updater(token='', use_context=True)


def main():
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('status', status))
    dp.add_handler(CommandHandler('leaderboard', rank))
    dp.add_handler(MessageHandler(Filters.text & (~Filters.command), echo))

    updater.start_polling()
    updater.idle()
    updater.stop()


if __name__ == '__main__':
    main()
