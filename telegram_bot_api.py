import telebot
import config


bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start(message):
    bot.send_message(message.chat.id, "Этот бот служит для уведомления о завершении сделки, сюда будут приходить "
                                      "уведомления об успешно завершенных сделках с ее название и датой")


@bot.message_handler(content_types=['text'])
def send_text(message):
        bot.send_message(message.chat.id, "")


def send_message(message):
    bot.send_message(chat_id=config.CHAT_ID, text=message)


if __name__ == "__main__":
    bot.polling()
