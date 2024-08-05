import telebot # type: ignore
from extensions import APIException, CurrencyConverter
import configparser

bot = telebot.TeleBot('7484500925:key')

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    text = """I am a bot that can show you the price of a certain amount of currency.
To find out the price, write me a message in the format:
<first value, whose price you want to know> <second value, /
in which you want to know the price> <amount of the first valute>
For example: USD EUR 100
Also, you can use comands:
/values - show list of all availible values"""
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def show_values(message):
    text = 'Availible values:'
    for cur in CurrencyConverter.keys:
        text += f'\n{cur}'
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def convert(message):
    try:
        base, quote, amount = message.text.split()
    except ValueError:
        bot.reply_to(message, 'Invalid input format. Try again.')
        return

    try:
        result = CurrencyConverter.get_price(base, quote, amount)
    except APIException as e:
        bot.reply_to(message, f'Error: {e}')
    else:
        text = f'Price {amount} {base} in {quote} - {result}'
        bot.reply_to(message, text)
bot.polling(non_stop=True)

