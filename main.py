import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, BaseFilter, CallbackContext
import logging
import requests
import time


# class
class FilterStop(BaseFilter):
    def filter(self, message):
        return 'stop receiving btc' in message.text


def crawl_currency():
    current_time = str(time.time_ns())[0:12]
    req_url = requests.get('https://www.bitoex.com/api/v0/rate/' + current_time)
    response = req_url.json()
    return response['BTC']


# value
isRunning = False
userID = ''

# start up
updater = Updater('1041411939:AAFE7sIstwya3cxb9MksuOnBfE6dUwPnBHI', use_context=True)
job = updater.job_queue
print("Start Telegram Bot...")

# for detect error
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
dispatcher = updater.dispatcher


# function here
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="/BTC /stop")


def get_btc(update, context):
    price = crawl_currency()
    context.bot.send_message(chat_id=update.message.chat_id, text="Buy = " + price[0] + ", Sell = " + price[1])


def loopGetBTC(context: telegram.ext.CallbackContext):
    price = crawl_currency()
    context.bot.send_message(chat_id=1108395640, text="Buy = " + price[0] + ", Sell = " + price[1])


def setReceiveBTC(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="test")
    # print(update.message.chat_id)
    # global isRunning
    # if isRunning:
    #     job.stop()
    #     isRunning = False
    # else:
    #     job.run_repeating(loopGetBTC(context), interval=20, first=0)
    #     isRunning = True


# start main
# filter


# handler
start_handler = CommandHandler('start', start)
get_btc_handler = CommandHandler('BTC', get_btc)
test_handler = CommandHandler('test', setReceiveBTC)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(test_handler)
dispatcher.add_handler(get_btc_handler)

updater.start_polling()
