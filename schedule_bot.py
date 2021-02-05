import datetime
import time
import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton


def read_file() -> dict:
    """
    Read file with schedule and returns 
    schedule as a dict object.
    """
    sched = {}
    curr_day = ''
    with open('schedule1.2.1.txt', 'r', encoding='utf-8') as schedule:
        for line in schedule:
            line = line.split()
            if (len(line) == 1) and (line[0] != ''):
                sched[line[0]] = {}
                curr_day = line[0]
            
            elif len(line) >= 2:
                sched[curr_day].setdefault(line[0], line[1:])

    return sched


def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    
    if content_type != 'text':
        # print(bot.getUpdates())
        sticker = 'CAACAgUAAxkBAAIHW2AdXtvOUk73fpptmMpcJLlkjl2EAAKVAwAC6QrIAxPjuNsqJjnAHgQ'
        bot.sendSticker(chat_id, sticker)
        message = 'Слухай, я розумію тільки команду */start* і коли ти натискаєш *кнопки на кастомній клаві внизу)*'
        bot.sendMessage(chat_id, message, parse_mode='Markdown')
        return

    usr_msg = msg['text']

    if usr_msg == '/start':
        usr_name = bot.getUpdates()[0]['message']['from']['first_name']
        message = f'Доров {usr_name}!\nЯ тобі буду допомагати з розкладом!'
        keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='розклад на сьогодні')], 
                                                 [KeyboardButton(text='загальний розклад')], 
                                                 [KeyboardButton(text='наступна лекція')]], resize_keyboard=True)
        sticker = 'CAACAgUAAxkBAAIHoWAdY5RGvv4m2GpDOrfaJbLXQAHwAAJvAwAC6QrIA6_OvtkCul10HgQ'
        bot.sendSticker(chat_id, sticker)
        bot.sendMessage(chat_id, message, parse_mode='Markdown', reply_markup=keyboard)
    
    elif usr_msg == 'загальний розклад':
        message = ''
        for day in list(sched.keys()):
            message += day.upper() + '\n'
            for time in list(sched[day].keys()):
                line = ''
                for word in sched[day][time]:
                    line += word + '  '
                message += line + '\n'
            message += '\n'
            message += '\n'

        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='скрін розкладу', callback_data='photos/schedule.png')]])

        bot.sendMessage(chat_id, message, parse_mode='Markdown', reply_markup=keyboard)
    
    elif usr_msg == 'розклад на сьогодні':
        day = datetime.datetime.now().strftime('%A')  # get day

        if (day == 'Saturday') or (day == 'Sunday'):
            bot.sendMessage(chat_id, '*Сьогодні вихідний, що забув?*\nРоби домашку, розбирайся зі всім. *Все буде добре)*', parse_mode='Markdown')

        else:
            day_sched = sched[day]
            # print(day_sched)
            message = f'{day}\n'
            for key in list(day_sched.keys()):
                for word in day_sched[key]:
                    message += word + ' '
                message += '\n'

            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='скрін розкладу', callback_data=f'photos/{day}.png')]])

            bot.sendMessage(chat_id, message, parse_mode='Markdown', reply_markup=keyboard)

    elif usr_msg == 'наступна лекція':
        now = datetime.datetime.now()  # get time
        day = datetime.datetime.now().strftime('%A')  # get day

        if (day == 'Saturday') or (day == 'Sunday'):
            bot.sendMessage(chat_id, '*Сьогодні вихідний, що забув?*\nРоби домашку, розбирайся зі всім. *Все буде добре)*', parse_mode='Markdown')

        else:
            day_sched = sched[day]
            for key in list(day_sched.keys()):
                key_time = datetime.datetime.strptime(key, '%H:%M:%S')
                # print(key_time.time() > now.time(), f'{key} > {now}')
                if key_time.time() > now.time():
                    # print('key =', key, 'now =', now)
                    message = ' '.join(day_sched[key])
                    bot.sendMessage(chat_id, message, parse_mode='Markdown')
                    break
                else:
                    if key == list(day_sched.keys())[-1]:
                        bot.sendMessage(chat_id, '*Сьогодні вже лекцій нема!*', parse_mode='Markdown')

    else:
        sticker = 'CAACAgUAAxkBAAIHaGAdYLxwOroMEP4_-L6jN2YUZQuDAAKqAwAC6QrIA4wyt12i0AVhHgQ'
        bot.sendSticker(chat_id, sticker)
        message = 'Там внизу є *кнопочки*, спілкуйся зі мною через них, інакше я не розумію(\nДо речі може */start* тобі допоможе'
        bot.sendMessage(chat_id, message, parse_mode='Markdown')

def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    print('Callback Query:', query_id, from_id, query_data)

    bot.answerCallbackQuery(query_id, text='зрозумів, відсилаю!')

    if query_data == 'photos/schedule.png':
        bot.sendPhoto(from_id, photo=open(query_data, 'rb'))
    else:
        bot.sendPhoto(from_id, photo=open(query_data, 'rb'))



TOKEN = '1535213260:AAHDcjKVgJHeDW4BgbsXCcsdEu2WAZZdLfE'
bot = telepot.Bot(TOKEN)

sched = read_file()

MessageLoop(bot, {'chat': on_chat_message,
                  'callback_query': on_callback_query}).run_as_thread()
while 1:
    time.sleep(10)