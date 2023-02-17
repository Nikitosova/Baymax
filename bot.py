from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from work_func import get_best_urls

bot = TeleBot('6157933964:AAHCFOsbaTQI5Y9XSZCAWbjXT3GvSDynZOE')

# 1004886438
hello_message = 'Приветствую тебя в моём боте. Меня зовут BayMax. ' \
                'Я помогу тебе разобраться в себе. Как тебя зовут?' \
    # 'Напиши, какие статьи тебе подобрать.'

storage = {}
keyboard_next_back = InlineKeyboardMarkup(row_width=2)
keyboard_next = InlineKeyboardMarkup(row_width=2)
keyboard_back = InlineKeyboardMarkup(row_width=2)

but_next = InlineKeyboardButton(text='Следующая', callback_data='Далее')
but_back = InlineKeyboardButton(text='Предыдущая', callback_data='Назад')


keyboard_next_back.add(but_back, but_next)
keyboard_back.add(but_back)
keyboard_next.add(but_next)


@bot.message_handler(commands=['start'])
def main_handler(message):
    user_id = message.from_user.id
    bot.send_message(user_id, hello_message)
    bot.register_next_step_handler(message, say_hello_after_name)


def say_hello_after_name(message):
    user_id = message.from_user.id
    text = message.text
    bot.send_message(user_id, f'Рад познакомиться. Меня тоже раньше звали {text}.\n'
                              f'На какие темы тебе подобрать статьи?')


@bot.message_handler()
def main_handler(message):
    user_id = message.from_user.id
    user_text = message.text
    print('Запрос', user_text, user_id)
    urls = get_best_urls(user_text)
    if len(urls) == 0:
        bot.send_message(user_id, 'Я ничего не нашёль')
    else:
        storage[user_id] = {
            'current_index': 0,
            'urls': urls
        }
        result_text = f'Количество найденный статей: {len(urls)} . Статья № 1/{len(urls)}\n' + urls[0]
        bot.send_message(user_id, result_text, reply_markup=keyboard_next)


def is_callback_back(callback):
    if callback.data == 'Назад':
        return True
    else:
        return False


@bot.callback_query_handler(func=is_callback_back)
def back_callback(callback):
    user_id = callback.from_user.id
    if user_id not in storage:
        bot.send_message(user_id, 'Извини, я всё забыл, что ты там просил. Попроси ещё разок.')
        return
    next_index = storage[user_id]['current_index'] - 1
    if next_index >= 0:
        next_url = storage[user_id]['urls'][next_index]
        storage[user_id]['current_index'] = next_index
        text = f'Статья № {next_index + 1}/{len(storage[user_id]["urls"])}\n{next_url}'

        if next_index == 0:
            keyboard = keyboard_next
        else:
            keyboard = keyboard_next_back

        bot.send_message(user_id, text, reply_markup=keyboard)

    else:
        bot.send_message(user_id, 'Упс, статьи закончились', reply_markup=keyboard_back)


def is_callback_next(callback):
    if callback.data == 'Далее':
        return True
    else:
        return False


@bot.callback_query_handler(func=is_callback_next)
def next_callback(callback):
    user_id = callback.from_user.id
    if user_id not in storage:
        bot.send_message(user_id, 'Извини, я всё забыл, что ты там просил. Попроси ещё разок.')
        return
    next_index = storage[user_id]['current_index'] + 1
    if next_index < len(storage[user_id]['urls']):
        next_url = storage[user_id]['urls'][next_index]
        storage[user_id]['current_index'] = next_index
        text = f'Статья № {next_index + 1}/{len(storage[user_id]["urls"])}\n{next_url}'

        if next_index == len(storage[user_id]['urls']) - 1:
            keyboard = keyboard_back
        else:
            keyboard = keyboard_next_back

        bot.send_message(user_id, text, reply_markup=keyboard)

    else:
        bot.send_message(user_id, 'Упс, статьи закончились', reply_markup=keyboard_back)


print('Запускаю бота')
# r = bot.send_message(1004886438, 'Прикольно, правда?)')
# print(r)
bot.infinity_polling()
