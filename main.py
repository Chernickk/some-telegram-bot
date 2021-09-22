from multiprocessing import Process

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from config import RECEIVER_TOKEN, SENDER_TOKEN, CHAT_ID
from logger import bot_message_logger

bot_receiver = Bot(token=RECEIVER_TOKEN)
bot_sender = Bot(token=SENDER_TOKEN)

dp_receiver = Dispatcher(bot_receiver)
dp_sender = Dispatcher(bot_sender)


@dp_receiver.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Привет!\nЯ бот который получает сообщения!")


@dp_sender.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Привет!\nЯ бот который пересылает сообщения!!")


@dp_receiver.message_handler()
async def echo_message(message: types.Message):
    bot_message_logger.info(message.text, {'user_id': message.from_user.id})
    [await bot_sender.send_message(CHAT_ID, letter) for letter in message.text.replace(' ', '')]


if __name__ == '__main__':
    for dp in (dp_receiver, dp_sender):
        proc = Process(target=executor.start_polling, args=(dp, ))
        proc.start()




