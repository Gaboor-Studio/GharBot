import telegram
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters
import db

TOKEN = '1769102250:AAEAEww2WgyvfKMq4nOfbLy61JR55rAcnzk'

updater = Updater(token=TOKEN, use_context=True)
bot = telegram.Bot(TOKEN)
conn = db.connect('localhost', 'root', 'Amirparsa96', 'Ghaar')


def get_markdown_call(name, id):
    return f"[{name}](tg://user?id={id})"


def is_ghaar(text):
    text = f'{text[0]}'.join(
        [text[i] for i in range(1, len(text)) if text[i - 1] != text[i]])
    return text == "اغر"


def text_handler(update: telegram.Update, context: telegram.ext.CallbackContext):
    chat_id = update.message.chat_id
    ghaar_user_id = update.message.reply_to_message.from_user.id
    ghaar_user_name = update.message.reply_to_message.from_user.full_name
    ghaar_message_id = update.message.reply_to_message.message_id
    text = update.message.text
    if is_ghaar(text):
        if db.get_ghaar_message(conn, chat_id, ghaar_message_id) is None:
            if db.get_ghaar_user(conn, chat_id, ghaar_user_id) is None:
                db.insert_ghaar_user(
                    conn, chat_id, ghaar_user_id, ghaar_user_name)
            db.increase_ghaar_count(conn, chat_id, ghaar_user_id)
            db.insert_ghaar_message(conn, chat_id, ghaar_message_id)
            update.message.reply_to_message.reply_text(text="Ghaar be mola!")
        else:
            update.message.reply_to_message.reply_text(
                text="enghad ghaari nemiduni in ghaar bude!")


def start(update: telegram.Update, context: telegram.ext.CallbackContext):
    update.message.reply_text(text='hi')


def stats_person(update: telegram.Update, context: telegram.ext.CallbackContext):
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id
    result = db.get_ghaar_user(conn, chat_id, user_id)
    if result == None:
        update.message.reply_text(
            text="Ta hala tu in gp ghaar nabudi!")
    else:
        update.message.reply_text(
            text=f"Ta hala {result[3]} bar ghaar budi tuye in gp!")


def stats_group(update: telegram.Update, context: telegram.ext.CallbackContext):
    print("salam")
    chat_id = update.message.chat_id
    print("salam")
    result = db.get_group_ghaar_users(conn, chat_id)
    print("salam")
    message = "Sarbazane gomname Peyro:\n"
    print(result)
    for i, tup in enumerate(result):
        message += f"{i+1}. {get_markdown_call(tup[2],tup[1])} : {tup[3]} GHAAAAAR! \n"
    print("salam")
    update.message.reply_text(text=message, parse_mode='MarkDown')


dispatcher = updater.dispatcher
dispatcher.add_handler(MessageHandler(Filters.reply, text_handler))
dispatcher.add_handler(CommandHandler("stats_group", stats_group))
dispatcher.add_handler(CommandHandler("stats_person", stats_person))
dispatcher.add_handler(CommandHandler("start", start))
updater.start_polling()
