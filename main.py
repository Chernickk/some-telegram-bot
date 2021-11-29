import os
from time import time

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.utils.deep_linking import get_start_link, decode_payload

from config import BOT_TOKEN, DATABASE_URL
# from logger import bot_message_logger
from movie_maker.moviemaker import MovieMaker
from db import DBConnect

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply('загрузка...')
    try:
        payload = decode_payload(message.get_args())

        with DBConnect(DATABASE_URL) as conn:
            movie_record = conn.get_movie(payload)

        camera = eval(movie_record.camera)

        start_time = time()

        mm = MovieMaker(camera, 'media')
        mm.get_video(movie_record.dt_start, movie_record.dt_finish, 'test')

        await message.reply(f'Время загрузки видео {time() - start_time} сек')

        with open(os.path.join('media', 'test.mp4'), 'rb') as video:
            await message.reply_video(video)
        os.remove(os.path.join('media', 'test.mp4'))

    except FileNotFoundError as error:
        await message.reply(f'Ошибка!\nФайл не найден или превышает допустимые 180 сек.\n{error}')
    except AttributeError as error:
        await message.reply(f'Ошибка!\nДанная запись отсутствует в базе данных.\n{error}')


@dp.message_handler(commands=['getlink'])
async def process_start_command(message: types.Message):
    result = await get_start_link(message.get_args(), encode=True)
    await message.reply(result)


if __name__ == '__main__':
    executor.start_polling(dp)
