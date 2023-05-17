from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Text
from aiogram.types import (KeyboardButton, Message, ReplyKeyboardMarkup,
                           ReplyKeyboardRemove)

# Вместо BOT TOKEN HERE нужно вставить токен вашего бота,
# полученный у @BotFather
API_TOKEN: str = '6245798122:AAG9WztsZo4Flm9pKdT2NYQk8MZQQLDCWMw'


# Создаем объекты бота и диспетчера
bot: Bot = Bot(token=API_TOKEN)
dp: Dispatcher = Dispatcher()

buttons: list[KeyboardButton] = []
keyboard: list[list[KeyboardButton]] = []

# Заполняем список списками с кнопками
for i in range(1, 101):
    buttons.append(KeyboardButton(text=str(i)))
    if not i % 12:
        keyboard.append(buttons)
        buttons = []
    if  i > 99:
        keyboard.append(buttons)

# Создаем объект клавиатуры, добавляя в него список списков с кнопками
keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
                                        keyboard=keyboard,
                                        resize_keyboard=True)
# Этот хэндлер будет срабатывать на команду "/start"
# и отправлять в чат клавиатуру
@dp.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(text='Чего кошки боятся больше?',
                         reply_markup=keyboard)


# Этот хэндлер будет срабатывать на ответ "Собак 🦮" и удалять клавиатуру
@dp.message(Text(text='Собак 🦮'))
async def process_dog_answer(message: Message):
    await message.answer(text='Да, несомненно, кошки боятся собак. '
                              'Но вы видели как они боятся огурцов?',
                         reply_markup=ReplyKeyboardRemove())


# Этот хэндлер будет срабатывать на ответ "Огурцов 🥒" и удалять клавиатуру
@dp.message(Text(text='Огурцов 🥒'))
async def process_cucumber_answer(message: Message):
    await message.answer(text='Да, иногда кажется, что огурцов '
                              'кошки боятся больше',
                         reply_markup=ReplyKeyboardRemove())


if __name__ == '__main__':
    dp.run_polling(bot)