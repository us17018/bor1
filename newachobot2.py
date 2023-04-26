from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from pprint import pprint
from aiogram.types import ContentType
from aiogram import F

# Вместо BOT TOKEN HERE нужно вставить токен вашего бота, полученный у @BotFather
API_TOKEN: str = '6245798122:AAG9WztsZo4Flm9pKdT2NYQk8MZQQLDCWMw'

# Создаем объекты бота и диспетчера
bot: Bot = Bot(token=API_TOKEN)
dp: Dispatcher = Dispatcher()


# Этот хэндлер будет срабатывать на команду "/start"
@dp.message(Command(commands=["start"]))
async def process_start_command(message: Message):
    await message.answer('Привет!\nМеня зовут Эхо-бот!\nНапиши мне что-нибудь')


# Этот хэндлер будет срабатывать на команду "/help"
@dp.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer('Напиши мне что-нибудь и в ответ '
                         'я пришлю тебе твое сообщение')

@dp.message(F.content_type == ContentType.PHOTO)
async def send_photo_echo(message: Message):
    print(message)
    await message.reply_photo(message.photo[0].file_id)

@dp.message(F.content_type == ContentType.AUDIO)
async def send_audio_echo(message: Message):
    pprint(list(message))
    await message.reply_audio(message.audio.file_id)

@dp.message(F.content_type == ContentType.STICKER)
async def send_sticker_echo(message: Message):
    pprint(list(message))
    await message.reply_sticker(message.sticker.file_id)



# Этот хэндлер будет срабатывать на любые ваши текстовые сообщения,
# кроме команд "/start" и "/help"
@dp.message()
async def send_echo(message: Message):
    await message.reply(text=message.text)
    pprint(message.chat.first_name)
    pprint(message.text)


if __name__ == '__main__':
    dp.run_polling(bot)