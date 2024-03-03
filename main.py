# -*- coding: utf-8 -*-
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.markdown import link
import api_token
import uuid
import os


bot = Bot(api_token.API_KEY)
dp = Dispatcher(bot)
temp_message = None
commands = ["Быстрее", "Медленнее", "Налево", "Направо", "Вперед", "Назад", "Бегом", "Стоп", "Шум"]


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    desc = 'Привет!\nЯ бот, который нужен для сбора данных для проекта по распознованию слов.\n\n\
Сначала появится снизу клавиатура для выбора слова. Выберите слово, которое будете говорить. Затем скажите его и отправьте голосовое сообщение (1-3 секунды).\n\n\
Приветствуется - разные интонации сказанного и выбор слова больше одного раза.'
    
    kb = [
        [
            types.KeyboardButton('Быстрее'),
            types.KeyboardButton('Медленнее'),
         ],
        [
            types.KeyboardButton('Налево'),
            types.KeyboardButton('Направо')
        ],
        [
            types.KeyboardButton('Вперед'),
            types.KeyboardButton('Назад')
        ],
        [
            types.KeyboardButton('Бегом'),
            types.KeyboardButton('Стоп')
        ],
         [
             types.KeyboardButton('Шум (иное любое слово)'),
         ],
    ]

    markup = types.ReplyKeyboardMarkup(keyboard=kb, one_time_keyboard=True, resize_keyboard=True, input_field_placeholder="Выберите слово для голосового сообщения")
    await message.reply(desc, reply_markup=markup)


@dp.message_handler(lambda message: message.text in commands)
async def without_puree(message: types.Message):
    global temp_message
    temp_message = message
    await message.reply(f"Теперь в голосовом сообщение скажите: {message.text}")


@dp.message_handler(content_types=['voice'])
async def voice_message(message: types.Message):
    file_id = message.voice.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    if temp_message.text in commands:
        name = temp_message.text
        dir = "./data/" + name
        if not os.path.exists(dir):
            os.mkdir(dir)
        await bot.download_file(file_path, f"{dir}/{str(uuid.uuid4())[0:17]}.wav")
        await bot.send_message(message.chat.id, 'Сообщение получено и сохранено успешно.')
        await bot.send_message(message.chat.id, 'Отлично!\nТеперь повторите либо с этим же словом, либо с другим (клавиатура может быть скрыта).')
    else:
        await bot.send_message(message.chat.id, "Значение некорректное, введите еще раз /start")


@dp.callback_query_handler()
async def callback(call):
    await call.message.answer(call.data)


if __name__ == "__main__":
    try:
        executor.start_polling(dp)
    except Exception as e:
        print(e)