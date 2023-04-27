from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from pprint import pprint
from aiogram.types import ContentType
from aiogram import F
from aiogram.filters import Text
from aiogram.filters import BaseFilter
# Вместо BOT TOKEN HERE нужно вставить токен вашего бота, полученный у @BotFather
API_TOKEN: str = '6245798122:AAG9WztsZo4Flm9pKdT2NYQk8MZQQLDCWMw'

# Создаем объекты бота и диспетчера
bot: Bot = Bot(token=API_TOKEN)
dp: Dispatcher = Dispatcher()

# Этот хэндлер будет срабатывать на команду "/start"
@dp.message(lambda msg: msg.text == '/start')
async def process_start_command(message: Message):
    await message.answer('Привет!\nМеня зовут Эхо-бот!\nНапиши мне что-нибудь')
    pprint(list(message))

# Этот хэндлер будет срабатывать на команду "/help"
@dp.message(lambda msg: msg.text == '/help')
async def process_help_command(message: Message):
    await message.answer('Напиши мне что-нибудь и в ответ '
                         'я пришлю тебе твое сообщение')

# Этот хэндлер будет срабатывать на команду "/help"
@dp.message(lambda msg: msg.text == '/private')
async def process_private_command(message: Message):
    await message.answer('это приватный бот')

@dp.message(lambda msg: msg.text == '/contacts')
async def process_contacs_command(message: Message):
    await message.answer('контактов не будет')

@dp.message(F.photo)
async def send_photo_echo(message: Message):
    print(message)
    await message.reply_photo(message.photo[0].file_id)

@dp.message(F.audio)
async def send_audio_echo(message: Message):
    pprint(list(message))
    await message.reply_audio(message.audio.file_id)

@dp.message(F.sticker)
async def send_sticker_echo(message: Message):
    pprint(list(message))
    await message.reply_sticker(message.sticker.file_id)

@dp.message(Text(contains=['python'], ignore_case=True))
async def process_text_python(message: Message):
    await message.answer(text='Python — это язык программирования, который широко используется в интернет-приложениях, разработке программного обеспечения, науке о данных и машинном обучении (ML). Разработчики используют Python, потому что он эффективен, прост в изучении и работает на разных платформах. Программы на языке Python можно скачать бесплатно, они совместимы со всеми типами систем и повышают скорость разработки.')

@dp.message(Text(text=['молоко','кефир'], ignore_case=True))
async def process_text_moloko(message: Message):
    await message.answer(text='это полезный продукт')

# Этот хэндлер будет срабатывать на любые ваши текстовые сообщения,
# кроме команд "/start" и "/help"
@dp.message()
async def send_echo(message: Message):
    await message.reply(text=message.text)
    pprint(message.chat.first_name)
    pprint(message.text)


if __name__ == '__main__':
    dp.run_polling(bot)