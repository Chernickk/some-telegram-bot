import os
from datetime import datetime

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.utils.deep_linking import get_start_link, decode_payload

from config import BOT_TOKEN, CHAT_ID, DATABASE_URL
# from logger import bot_message_logger
from db import DBConnect
from service import get_output_file

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    # Extract payload from start command
    await message.reply('видео загружается...')
    payload = decode_payload(message.get_args())
    # await message.reply(payload)
    uuid, datetime_string = payload.split()
    date, from_time, to_time = datetime_string.split(',')

    result = {
        'uuid': uuid,
        'from_datetime': datetime.strptime(f'{date} {from_time}', '%d.%m.%Y %H.%M.%S'),
        'to_datetime': datetime.strptime(f'{date} {to_time}', '%d.%m.%Y %H.%M.%S'),
    }

    with DBConnect(DATABASE_URL) as conn:
        records = conn.get_records(result['uuid'])

    clips = get_output_file(result['from_datetime'], result['to_datetime'], records)

    for clip in clips:
        media = types.InputFile(open(clip, 'rb'))
        await message.reply_document(media)
        os.remove(clip)


@dp.message_handler(commands=['getlink'])
async def process_start_command(message: types.Message):
    result = await get_start_link(message.get_args(), encode=True)
    await message.reply(result)


if __name__ == '__main__':
    executor.start_polling(dp)
