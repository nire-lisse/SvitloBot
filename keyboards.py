from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def main_menu_reply_keyboard():

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)

    btn_profile = KeyboardButton('👤 Профіль')
    keyboard.add(btn_profile)

    btn_schedule = KeyboardButton('⚡ Графік світла')
    keyboard.add(btn_schedule)

    btn_find_queue = KeyboardButton('👇 Дізнатися чергу')
    keyboard.add(btn_find_queue)

    btn_help = KeyboardButton('❓ Допомога')
    # btn_help = KeyboardButton('/help')
    keyboard.add(btn_help)

    return keyboard

def profile_inline_keyboard():

    keyboard = InlineKeyboardMarkup()

    keyboard.add(InlineKeyboardButton('➕ Додати адресу', callback_data='profile_add_address'))
    keyboard.add(InlineKeyboardButton('📍 Мої адреси', callback_data='profile_my_addresses'))
    keyboard.add(InlineKeyboardButton('🔔 Сповіщення', callback_data='profile_notifications'))
    keyboard.add(InlineKeyboardButton('⏰ Нагадування', callback_data='profile_reminders'))

    return keyboard


def addresses_list_inline_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=2)


    btn_edit = InlineKeyboardButton('📝 Редагувати', callback_data='address_edit')
    btn_delete = InlineKeyboardButton('🗑️ Видалити', callback_data='address_delete')
    keyboard.add(btn_edit, btn_delete)

    keyboard.add(InlineKeyboardButton('⬅️ Назад', callback_data='back_to_profile'))

    return keyboard


def schedule_inline_keyboard(queue_numbers):
    keyboard = InlineKeyboardMarkup()

    for num in queue_numbers:
        keyboard.add(InlineKeyboardButton(f'Черга {num}', callback_data=f'schedule_select_{num}'))

    # keyboard.add(InlineKeyboardButton('🔄 Оновити', callback_data='schedule_refresh'))
    # keyboard.add(InlineKeyboardButton('📍 Змінити адресу', callback_data='schedule_change_address'))

    return keyboard

def schedule_day_choice_keyboard(queue_num):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton("📅 На сьогодні", callback_data=f'schedule_day_today_{queue_num}')
    )
    keyboard.add(
        InlineKeyboardButton("📆 На завтра", callback_data=f'schedule_day_tomorrow_{queue_num}')
    )
    return keyboard


def find_queue_inline_keyboard():
    keyboard = InlineKeyboardMarkup()

    keyboard.add(InlineKeyboardButton('📍 Вибір адреси', callback_data='find_queue_select_address'))
    keyboard.add(InlineKeyboardButton('➕ Додати нову', callback_data='find_queue_add_new'))

    return keyboard
