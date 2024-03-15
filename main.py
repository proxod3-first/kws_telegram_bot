# -*- coding: utf-8 -*-
from aiogram import Bot, Dispatcher, executor, types
import api_token
import uuid
import os


bot = Bot(api_token.API_KEY)
dp = Dispatcher(bot)
temp_message = None
main_commands = ["Быстрее", "Медленнее", "Налево", "Направо", "Вперед", "Назад", "Бегом", "Стоп", "Привет", "Ура"]
noise_commands = ["Клюшка", "Голос", "Макароны", "Лампочка", "Закат", "Рука", "Величие", "Носок", "Бред", "Фонарь"]


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    desc = 'Привет!\nЯ бот, который нужен для сбора данных для проекта по распознованию слов.\n\n\
Сначала появится снизу клавиатура для выбора слова. Выберите слово, которое будете говорить. Затем скажите его и отправьте голосовое сообщение (1-3 секунды).\n\n\
Приветствуется - разные интонации сказанного и выбор слова больше одного раза.'
    
    kb_main = [
        [
             types.KeyboardButton('Шум (список иных слов)'),
         ],
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
            types.KeyboardButton('Привет'),
            types.KeyboardButton('Ура')
        ],
    ]

    markup = types.ReplyKeyboardMarkup(keyboard=kb_main, one_time_keyboard=True, resize_keyboard=True, input_field_placeholder="Выберите слово для голосового сообщения")
    await message.reply(desc, reply_markup=markup)


@dp.message_handler(lambda message: message.text in main_commands or message.text in noise_commands)
async def without_puree(message: types.Message):
    global temp_message
    temp_message = message
    await message.reply(f"Теперь в голосовом сообщение скажите: {message.text}")


@dp.message_handler(lambda message: message.text == "Шум (список иных слов)")
async def without_puree(message: types.Message):
    desc="Приведен список слов для инициализации шума в клавиатуре, которые позволят обучить лучше модель для распознования слов"
    
    kb_noise = [
    [
        types.KeyboardButton('Вернуться к основным словам'),
    ],
    [
        types.KeyboardButton('Клюшка'),
        types.KeyboardButton('Голос'),
    ],
    [
        types.KeyboardButton('Макароны'),
        types.KeyboardButton('Лампочка')
    ],
    [
        types.KeyboardButton('Закат'),
        types.KeyboardButton('Рука')
    ],
    [
        types.KeyboardButton('Величие'),
        types.KeyboardButton('Носок')
    ],
    [
        types.KeyboardButton('Бред'),
        types.KeyboardButton('Фонарь'),
    ],
    ]
    
    markup = types.ReplyKeyboardMarkup(keyboard=kb_noise, one_time_keyboard=True, resize_keyboard=True, input_field_placeholder="Выберите слово для голосового сообщения")
    await message.reply(desc, reply_markup=markup)


@dp.message_handler(lambda message: message.text == "Вернуться к основным словам")
async def without_puree(message: types.Message):
    await start(message)


@dp.message_handler(content_types=['voice'])
async def voice_message(message: types.Message):
    file_id = message.voice.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    if temp_message.text in main_commands or temp_message.text in noise_commands:
        name = temp_message.text
        
        if temp_message.text in noise_commands:
             dir = "./data/noise/" + name
        else:
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