import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters
import db
import requests
import json
from PIL import Image
import logging
import comparator



TOKEN = '1769102250:AAEAEww2WgyvfKMq4nOfbLy61JR55rAcnzk'

updater = Updater(token=TOKEN, use_context=True)
bot = telegram.Bot(TOKEN)

ghaar_rejects = []

conn = db.connect('localhost', 'root', 'sajadcr7', 'Ghaar')
#logging.basicConfig(level=logging.DEBUG,format='%(asctime)s-%(name)s-%(levelname)s-%(message)s')

def get_markdown_call(name, id):
    return name
    # return f"[{name}](tg://user?id={id})"


def is_ghaar(text):
    text = f'{text[0]}'.join(
        [text[i] for i in range(1, len(text)) if text[i - 1] != text[i]])
    return text == "اغر"


def button(update: telegram.Update, context: telegram.ext.CallbackContext):
    query = update.callback_query
    ghaar_rejects.append(query.from_user.id)
    query.edit_message_text(text='غار بمولا\n' + str(len(ghaar_rejects)) + 'گفتن غار نیس',
                            reply_markup=InlineKeyboardMarkup([[
                                InlineKeyboardButton('غار نبود',callback_data='1')]]), parse_mode="Markdown")

def forward_handler(update: telegram.Update, context: telegram.ext.CallbackContext):
    group_id = update.message.chat_id
    chat_id=update.message.message_id

    text=""
    try:
        text = update.message.text
    except:
        pass
    imgpic_id=update.message.photo[-1].file_id
    picurl=f"https://api.telegram.org/bot{TOKEN}/getFile?file_id={imgpic_id}"
    tt=requests.get(picurl)
    tt=tt.json()
    file_path=tt["result"]["file_path"]
    pic_to_download=f"https://api.telegram.org/file/bot{TOKEN}/{file_path}"
    imgpic=Image.open(requests.get(pic_to_download, stream=True).raw)
    hash_img=comparator.gethash_by_image(imgpic)
    all_forwarded=db.get_all_forwarded_messages(conn,group_id)
    if len(all_forwarded)==0:
        db.insert_forwarded_message_by_data(conn,group_id,chat_id,text,hash_img,"")
    else:
        ghaar_flag=False
        ghaar_message_id=""
        for forwarded_message in all_forwarded:
            second_hash=forwarded_message[3]
            #print(second_hash)
            if comparator.compare_pics_hash(hash_img,second_hash):
                ghaar_flag=True
                ghaar_message_id=forwarded_message[1]
                break
            else:
                pass
        if ghaar_flag:
            update.message.reply_text(text="I think YOU ARE GHAAAR!")
            context.bot.send_message(chat_id=group_id,text="Inam madrak",reply_to_message_id=ghaar_message_id)
        else:
            db.insert_forwarded_message_by_data(conn, group_id, chat_id, text, hash_img, "")





def text_handler(update: telegram.Update, context: telegram.ext.CallbackContext):
    text = update.message.text
    if is_ghaar(text):
        chat_id = update.message.chat_id
        ghaar_user_id = update.message.reply_to_message.from_user.id
        ghaar_user_name = update.message.reply_to_message.from_user.full_name
        ghaar_message_id = update.message.reply_to_message.message_id
        if ghaar_user_id == 1769102250:
            update.message.reply_text(text='داش ایسگامونو نگیر')
        elif ghaar_user_id == 354614756:
            update.message.reply_text(text='حاجی این که کلا غاره تنهایی فک کردی؟')
        else:
            if db.get_ghaar_message(conn, chat_id, ghaar_message_id) is None:
                if db.get_ghaar_user(conn, chat_id, ghaar_user_id) is None:
                    db.insert_ghaar_user(
                        conn, chat_id, ghaar_user_id, ghaar_user_name)
                db.increase_ghaar_count(conn, chat_id, ghaar_user_id)
                db.insert_ghaar_message(conn, chat_id, ghaar_message_id)
                keyboard = [[InlineKeyboardButton('غار نبود', callback_data='1')]]
                mark_up = InlineKeyboardMarkup(keyboard)
                update.message.reply_to_message.reply_text(text="غار بمولا",
                                                           reply_markup=mark_up,
                                                           parse_mode="Markdown")
            else:
                update.message.reply_to_message.reply_text(
                    text="انقد غار بودی نفهمیدی این غار بوده!")


def start(update: telegram.Update, context: telegram.ext.CallbackContext):
    update.message.reply_text(text='به ربات غارگیران راه پیرو خوش آمدید')


def stats_person(update: telegram.Update, context: telegram.ext.CallbackContext):
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id
    result = db.get_ghaar_user(conn, chat_id, user_id)
    if result is None:
        update.message.reply_text(
            text="تا حالا تو این گروه غار نبودی!")
    else:
        update.message.reply_text(
            text=f"تا حالا{result[3]} بار غاار بودی تو این گروه!")


def stats_group(update: telegram.Update, context: telegram.ext.CallbackContext):
    chat_id = update.message.chat_id
    result = db.get_group_ghaar_users(conn, chat_id)
    message = "سربازان گمنام پیرو\n"
    for i, tup in enumerate(result):
        message += f"{i + 1}. {get_markdown_call(tup[2], tup[1])} : {tup[3]} غاااار! \n"
    update.message.reply_text(text=message)


dispatcher = updater.dispatcher
dispatcher.add_handler(CallbackQueryHandler(button))
dispatcher.add_handler(MessageHandler(Filters.reply, text_handler))
dispatcher.add_handler(MessageHandler(Filters.forwarded, forward_handler))
dispatcher.add_handler(CommandHandler("stats_group", stats_group))
dispatcher.add_handler(CommandHandler("stats_person", stats_person))
dispatcher.add_handler(CommandHandler("start", start))
updater.start_polling()