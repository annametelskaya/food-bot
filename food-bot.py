import telebot
import schedule
import time
import random
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from TimeSaver import TimeSaver

bot = telebot.TeleBot("813519675:AAGPKuP_RocPPjQUoQGqxm5U7asF_As539I")
time_saver = TimeSaver()
text_to_send = ["Уважаемые, время столовки!", "Пошлите есть", "Го есть", "Время еды!", "Пора в столовку))))))))))))"]


def gen_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 4
    markup.add(InlineKeyboardButton("10:00", callback_data="10:00"),
               InlineKeyboardButton("10:30", callback_data="10:30"),
               InlineKeyboardButton("11:00", callback_data="11:00"),
               InlineKeyboardButton("11:30", callback_data="11:30"),
               InlineKeyboardButton("12:00", callback_data="12:00"),
               InlineKeyboardButton("12:30", callback_data="12:30"),
               InlineKeyboardButton("13:00", callback_data="13:00"),
               InlineKeyboardButton("13:30", callback_data="13:30"),
               InlineKeyboardButton("14:00", callback_data="14:00"),
               InlineKeyboardButton("14:30", callback_data="14:30"),
               InlineKeyboardButton("15:00", callback_data="15:00"),
               InlineKeyboardButton("15:30", callback_data="15:30"))
    return markup


@bot.message_handler(commands=['set_time'])
def message_handler(message):
    bot.send_message(message.chat.id, "Выберете время", reply_markup=gen_markup())


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    time_saver.set_time(call.data)
    bot.answer_callback_query(call.id, "Время установленно на %s" % time_saver.get_time())


@bot.message_handler(commands=['get_time'])
def get_time(message):
    bot.send_message(message.chat.id, "Время установленно на %s" % time_saver.get_time())


@bot.message_handler(commands=['start'])
def send_welcome(message):
    local_time = "00:00"
    while True:
        if message.chat.type == "group":
            if local_time != time_saver.get_time():
                local_time = time_saver.get_time()
                schedule.jobs.clear()
                schedule.every().monday.at(local_time).do(get_text_to_send, message=message)
                schedule.every().tuesday.at(local_time).do(get_text_to_send, message=message)
                schedule.every().wednesday.at(local_time).do(get_text_to_send, message=message)
                schedule.every().thursday.at(local_time).do(get_text_to_send, message=message)
                schedule.every().friday.at(local_time).do(get_text_to_send, message=message)
            else:
                time.sleep(1)
            schedule.run_pending()


def get_text_to_send(message):
    bot.send_message(message.chat.id, text_to_send[random.randint(0, len(text_to_send) - 1)])


bot.polling()
