import telebot
import creds 
import json

bot = telebot.TeleBot(creds.api_key)

# @bot.message_handler(commands=['start'])
# def main(message):
#     bot.send_message(message.chat.id, 'Привіт, я світлоБот!')
    
@bot.message_handler(commands=['help'])
def main(message):
    bot.send_message(message.chat.id, '<b>Текст допомоги</b>', parse_mode='html')
    


def load_data():
    with open("storage.json", "r", encoding="utf-8") as f:
        return json.load(f)


@bot.message_handler(commands=["start"])
def start(msg):
    bot.send_message(msg.chat.id, "Привіт! Надішли номер черги ")


@bot.message_handler(func=lambda m: m.text.isdigit())
def get_schedule(msg):
    queue_num = msg.text.strip()
    data = load_data()

    today = next(iter(data))  # перша дата в JSON
    queues = data[today]

    if queue_num not in queues:
        bot.send_message(msg.chat.id, "Такої черги немає")
        return

    times = queues[queue_num]
    text = f"Графік на {today}\nЧерга {queue_num}:\n" + "\n".join(times)
    bot.send_message(msg.chat.id, text)


bot.polling(none_stop=True)
