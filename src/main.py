import telegram
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters

TOKEN = '1769102250:AAEAEww2WgyvfKMq4nOfbLy61JR55rAcnzk'

updater = Updater(token=TOKEN, use_context=True)
bot = telegram.Bot(TOKEN)

def text_handler (update: telegram.Update, context: telegram.ext.CallbackContext):
    text = update.message.text
    chat_id=update.message.chat_id
    user_id=update.message.reply_to_message.from_user.id
    text = f'{text[0]}'.join([text[i] for i in range(1, len(text)) if text[i - 1] != text[i]])
    if text == 'اغر':
        update.message.reply_to_message.reply_text(text= update.message.reply_to_message.from_user.id)

def start (update: telegram.Update, context: telegram.ext.CallbackContext):
    update.message.reply_text(text='hi')

def stats_person(update: telegram.Update, context: telegram.ext.CallbackContext):
    user_id = update.message.reply_to_message.from_user.id
    print(user_id)

dispatcher = updater.dispatcher
dispatcher.add_handler(MessageHandler(Filters.reply, text_handler))
dispatcher.add_handler(CommandHandler("stats_group", stats_group))
dispatcher.add_handler(CommandHandler("stats_person", stats_person))
dispatcher.add_handler(CommandHandler("start", start))
updater.start_polling()


