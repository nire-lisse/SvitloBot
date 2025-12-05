import telebot
import creds
import json
from datetime import datetime, timedelta
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards import (
    main_menu_reply_keyboard,
    profile_inline_keyboard,
    addresses_list_inline_keyboard,
    schedule_inline_keyboard,
    find_queue_inline_keyboard
)

bot = telebot.TeleBot(creds.api_key)

def load_data():
    with open("storage.json", "r", encoding="utf-8") as f:
        return json.load(f)


@bot.message_handler(commands=['help'])
def help_command(message):
    keyboard = main_menu_reply_keyboard()
    bot.send_message(
        message.chat.id,
        '<b>Текст допомоги</b>',
        parse_mode='html',
        reply_markup=keyboard
    )

@bot.message_handler(commands=["start"])
def start(msg):
    keyboard = main_menu_reply_keyboard()
    bot.send_message(
        msg.chat.id,
        "Привіт! Я СвітлоБот. Скористайся кнопками нижче:",
        reply_markup=keyboard
    )

@bot.message_handler(func=lambda message: message.text == '👤 Профіль')
def handle_profile(message):
    keyboard = profile_inline_keyboard()
    bot.send_message(
        message.chat.id,
        "Налаштування профілю:",
        reply_markup=keyboard
    )

@bot.message_handler(func=lambda message: message.text == '⚡ Графік світла')
def handle_schedule(message):
    data = load_data()
    today = next(iter(data), None)
    if today:
        queue_numbers = list(data[today].keys())
        keyboard = schedule_inline_keyboard(queue_numbers)
        bot.send_message(
            message.chat.id,
            "Обери чергу або скористайся опціями:",
            reply_markup=keyboard
        )
    else:
        bot.send_message(message.chat.id, "На жаль, дані про графік тимчасово відсутні.")

@bot.message_handler(func=lambda message: message.text == '👇 Дізнатися чергу')
def handle_find_queue(message):
    keyboard = find_queue_inline_keyboard()
    bot.send_message(
        message.chat.id,
        "Як ви хочете дізнатися свою чергу?",
        reply_markup=keyboard
    )

@bot.message_handler(func=lambda message: message.text == '❓ Допомога')
def handle_help_button(message):
    help_command(message)


@bot.message_handler(func=lambda m: m.text.isdigit())
def get_schedule(msg):
    queue_num = msg.text.strip()
    data = load_data()
    today = next(iter(data))
    queues = data[today]

    if queue_num not in queues:
        bot.send_message(msg.chat.id, "Такої черги немає")
        return

    times = queues[queue_num]
    text = f"Графік на {today}\nЧерга {queue_num}:\n" + "\n".join(times)
    bot.send_message(msg.chat.id, text)


@bot.callback_query_handler(func=lambda call: call.data.startswith('profile_'))
def handle_profile_inline_buttons(call):
    action = call.data.split('_')[-1]

    if action == 'myaddresses':
        keyboard = addresses_list_inline_keyboard()
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="Список ваших адрес. Оберіть дію:",
            reply_markup=keyboard
        )
    elif action == 'notifications':
        bot.answer_callback_query(call.id, "Сповіщення увімкнено/вимкнено")
    else:
        bot.answer_callback_query(call.id, f"Дія: {action} (у розробці)")

@bot.callback_query_handler(func=lambda call: call.data.startswith('back_to_profile'))
def handle_back_button(call):
    keyboard = profile_inline_keyboard()
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="Налаштування профілю:",
        reply_markup=keyboard
    )
    bot.answer_callback_query(call.id)


@bot.callback_query_handler(func=lambda call: call.data.startswith('schedule_select_'))
def handle_schedule_inline_buttons(call):
    queue_num = call.data.replace("schedule_select_", "")

    bot.edit_message_text(
        f"Ви обрали чергу *{queue_num}*.\nОберіть день:",
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        parse_mode='Markdown',
        reply_markup=schedule_day_choice_keyboard(queue_num)
    )
    bot.answer_callback_query(call.id)


def schedule_day_choice_keyboard(queue_num):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton("📅 На сьогодні", callback_data=f'schedule_day_today_{queue_num}')
    )
    keyboard.add(
        InlineKeyboardButton("📆 На завтра", callback_data=f'schedule_day_tomorrow_{queue_num}')
    )
    return keyboard


@bot.callback_query_handler(func=lambda call: call.data.startswith('schedule_day_'))
def handle_day_buttons(call):
    data = load_data()
    parts = call.data.split('_')
    day_type = parts[2]    
    queue_num = parts[3]

    today = datetime.now().date()
    if day_type == "today":
        selected_date = today
    else:
        selected_date = today + timedelta(days=1)

    selected_date_str = selected_date.strftime("%d.%m.%Y")

    if selected_date_str not in data or queue_num not in data[selected_date_str]:
        bot.answer_callback_query(call.id, "Даних немає ❗")
        return

    times = data[selected_date_str][queue_num]
    times_text = "\n".join([f"• {t}" for t in times]) if times else "Немає відключень 👍"

    text = f"📅 Графік на {selected_date_str}\nЧерга *{queue_num}*:\n\n{times_text}"

    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, text, parse_mode='Markdown')


bot.polling(none_stop=True)
