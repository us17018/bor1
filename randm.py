import random

from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Text, Command
from aiogram.types import (KeyboardButton, Message, ReplyKeyboardMarkup,
                           ReplyKeyboardRemove)


# Вместо BOT TOKEN HERE нужно вставить токен вашего бота,
# полученный у @BotFather
BOT_TOKEN: str = '6245798122:AAG9WztsZo4Flm9pKdT2NYQk8MZQQLDCWMw'

# Создаем объекты бота и диспетчера
bot: Bot = Bot(BOT_TOKEN)
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



# Количество попыток, доступных пользователю в игре
ATTEMPTS: int = 100

# Словарь, в котором будут храниться данные пользователя
user: dict = {'in_game': False,
              'secret_number': None,
              'attempts': None,
              'total_games': 0,
              'wins': 0}


# Функция возвращающая случайное целое число от 1 до 100
def get_random_number() -> int:
    return random.randint(1, 100)

sp = ['У самой заботливой в мире девочки хомячок весит 22 килограмма.','Сколько раз бросал курить, но недалеко. Сигареты то лёгкие.','Карантин — как запой: выходить надо постепенно.']

# Этот хэндлер будет срабатывать на команду "/start"
@dp.message(Command(commands=['start']))
async def process_start_command(message: Message):
    await message.answer('Привет!\nДавай сыграем в игру "Угадай число"?\n\n'
                         'Чтобы получить правила игры и список доступных '
                         'команд - отправьте команду /help\n если хочешь шутку напиши /funny')
    # проверка id пользователя
    if message.from_user.id not in user:
        user[message.from_user.id] = {'in_game': False,
                                       'secret_number': None,
                                       'attempts': None,
                                       'total_games': 0,
                                       'wins': 0}


@dp.message(Command(commands=['funny']))
async def process_start_command(message: Message):
    await message.answer(random.choice(sp))

# Этот хэндлер будет срабатывать на команду "/help"
@dp.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(f'Правила игры:\n\nЯ загадываю число от 1 до 100, '
                         f'а вам нужно его угадать\nУ вас есть {ATTEMPTS} '
                         f'попыток\n\nДоступные команды:\n/help - правила '
                         f'игры и список команд\n/cancel - выйти из игры\n'
                         f'/stat - посмотреть статистику\n\nДавай сыграем?')


# Этот хэндлер будет срабатывать на команду "/stat"
@dp.message(Command(commands=['stat']))
async def process_stat_command(message: Message):
    await message.answer(f'Всего игр сыграно: {user["total_games"]}\n'
                         f'Игр выиграно: {user["wins"]}')


# Этот хэндлер будет срабатывать на команду "/cancel"
@dp.message(Command(commands=['cancel']))
async def process_cancel_command(message: Message):
    if user['in_game']:
        await message.answer('Вы вышли из игры. Если захотите сыграть '
                             'снова - напишите об этом',
                             reply_markup=ReplyKeyboardRemove())
        user['in_game'] = False
    else:
        await message.answer('А мы итак с вами не играем. '
                             'Может, сыграем разок?')


# Этот хэндлер будет срабатывать на согласие пользователя сыграть в игру
@dp.message(Text(text=['Да', 'Давай', 'Сыграем', 'Игра',
                       'Играть', 'Хочу играть','Го'], ignore_case=True))
async def process_positive_answer(message: Message):
    if not user['in_game']:
        await message.answer('Ура!\n\nЯ загадал число от 1 до 100, '
                             'попробуй угадать!',
                             reply_markup=keyboard)
        user['in_game'] = True
        user['secret_number'] = get_random_number()
        user['attempts'] = ATTEMPTS
    else:
        await message.answer('Пока мы играем в игру я могу '
                             'реагировать только на числа от 1 до 100 '
                             'и команды /cancel и /stat')


# Этот хэндлер будет срабатывать на отказ пользователя сыграть в игру
@dp.message(Text(text=['Нет', 'Не', 'Не хочу', 'Не буду'], ignore_case=True))
async def process_negative_answer(message: Message):
    if not user['in_game']:
        await message.answer('Жаль :(\n\nЕсли захотите поиграть - просто '
                             'напишите об этом',
                             reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer('Мы же сейчас с вами играем. Присылайте, '
                             'пожалуйста, числа от 1 до 100')


# Этот хэндлер будет срабатывать на отправку пользователем чисел от 1 до 100
@dp.message(lambda x: x.text and x.text.isdigit() and 1 <= int(x.text) <= 100)
async def process_numbers_answer(message: Message):
    if user['in_game']:
        if int(message.text) == user['secret_number']:
            await message.answer_sticker('CAACAgIAAxkBAAIDJGRSYJjuSOKzbfZSqtBIs2pdHVsgAAILIwACNPfhSIrIZ8jHPLvwLwQ',
                                         reply_markup=ReplyKeyboardRemove())
            user['in_game'] = False
            user['total_games'] += 1
            user['wins'] += 1
        elif int(message.text) > user['secret_number']:
            await message.answer('Мое число меньше')
            user['attempts'] -= 1
        elif int(message.text) < user['secret_number']:
            await message.answer('Мое число больше')
            user['attempts'] -= 1

        if user['attempts'] == 0:
            await message.answer('ты проиграл :(',
                                 reply_markup=ReplyKeyboardRemove())
            await message.answer_sticker('CAACAgIAAxkBAAICnGRSXjVDpLocBKN8DS3174Lyx8QEAAKHJQACiY5BSPQT6Jq4ykxWLwQ')
            user['in_game'] = False
            user['total_games'] += 1
    else:
        await message.answer('Мы еще не играем. Хотите сыграть?')


# Этот хэндлер будет срабатывать на остальные любые сообщения
@dp.message()
async def process_other_text_answers(message: Message):
    if user['in_game']:
        await message.answer('Мы же сейчас с вами играем. '
                             'Присылайте, пожалуйста, числа от 1 до 100')
    else:
        await message.answer('Я довольно ограниченный бот, давайте '
                             'просто сыграем в игру?')

if __name__ == '__main__':
    dp.run_polling(bot)