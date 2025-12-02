import telebot
import creds 


bot = telebot.TeleBot(creds.api_key)

@bot.message_handler(commands=['start'])
def main(message):
    bot.send_message(message.chat.id, 'Привіт, я світлоБот!')
    
    

bot.polling(none_stop=True)