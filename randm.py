import random
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Text, Command
from aiogram.types import (KeyboardButton, Message, ReplyKeyboardMarkup,
                           ReplyKeyboardRemove)
from pprint import pprint


# Вместо BOT TOKEN HERE нужно вставить токен вашего бота,
# полученный у @BotFather
BOT_TOKEN: str = '6245798122:AAG9WztsZo4Flm9pKdT2NYQk8MZQQLDCWMw'

# Создаем объекты бота и диспетчера
bot: Bot = Bot(BOT_TOKEN)
dp: Dispatcher = Dispatcher()


# Заполняем список списками с кнопками
button_1: KeyboardButton = KeyboardButton(text='Я хочу играть!')
button_2: KeyboardButton = KeyboardButton(text='Я не хочу играть!')
button_3: KeyboardButton = KeyboardButton(text='Правила игры')
button_4: KeyboardButton = KeyboardButton(text='Шутка')
button_5: KeyboardButton = KeyboardButton(text='Cтатистика')
# Создаем объект клавиатуры, добавляя в него список списков с кнопками

buttons: list[KeyboardButton] = []
my_keyboard: list[list[KeyboardButton]] = []

# Заполняем список списками с кнопками
# Создаем объект клавиатуры, добавляя в него список списков с кнопками
keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
                        keyboard=[[button_1, button_2, button_3],
                                        [button_4,button_5]],
                            resize_keyboard=True)

for i in range(1, 101):
    buttons.append(KeyboardButton(text=str(i)))
    if not i % 8:
        my_keyboard.append(buttons)
        buttons = []
    if i > 99:
        my_keyboard.append(buttons)

keyboard2: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
                        keyboard=my_keyboard,
                            resize_keyboard=True)

# Количество попыток, доступных пользователю в игре
ATTEMPTS: int = 7

# Словарь, в котором будут храниться данные пользователя
user: dict = {'in_game': False,
              'secret_number': None,
              'attempts': None,
              'total_games': 0,
              'wins': 0}


# Функция возвращающая случайное целое число от 1 до 100
def get_random_number() -> int:
    return random.randint(1, 100)

sp = ['У самой заботливой в мире девочки хомячок весит 22 килограмма.','Сколько раз бросал курить, но недалеко. Сигареты то лёгкие.','Карантин — как запой: выходить надо постепенно.',
      'Как называют человека, который продал свою печень? Обеспеченный','-Алло, это Чешская Республика? Почешите мне спинку.',
      'Почему среди фигуристов, не бывает цыган? Никто не верит что это их конёк.']

# Этот хэндлер будет срабатывать на команду "/start"
@dp.message(Command(commands=['start'],ignore_case=True))
async def process_start_command(message: Message):
    await message.answer('Привет!\nДавай сыграем в игру "Угадай число"?\n(у тебя есть 7 попыток)\n\n'                         
                         'Чтобы получить правила игры и список доступных '
                         'команд воспользуйтесь кнопкой - "Правила игры" \n если хотите шутку воспользуйтесь кнопкой - "Шутка"',
                         reply_markup=keyboard)
    # проверка id пользователя
    if message.from_user.id not in user:
        user[message.from_user.id] = {'in_game': False,
                                       'secret_number': None,
                                       'attempts': None,
                                       'total_games': 0,
                                       'wins': 0}


@dp.message(Text(text='Шутка'))
async def process_start_command(message: Message):
    await message.answer(random.choice(sp),
                         reply_markup=keyboard)

# Этот хэндлер будет срабатывать на команду "/help"
@dp.message(Text(text='Правила игры'))
async def process_help_command(message: Message):
    await message.answer(f'Правила игры:\n\nЯ загадываю число от 1 до 100, '
                         f'а вам нужно его угадать\nУ вас есть {ATTEMPTS} '
                         f'попыток\n\nДоступные команды: /cancel - выйти из игры\n'
                         f'\nДавай сыграем?')

# Этот хэндлер будет срабатывать на команду "/stat"
@dp.message(Text(text='Cтатистика'))
async def process_stat_command(message: Message):
    await message.answer(f'Всего игр сыграно: {user["total_games"]}\n'
                         f'Игр выиграно: {user["wins"]}',
                         reply_markup=keyboard)


# Этот хэндлер будет срабатывать на команду "/cancel"
@dp.message(Command(commands=['cancel']))
async def process_cancel_command(message: Message):
    if user['in_game']:
        await message.answer('Вы вышли из игры. Если захотите сыграть '
                             'снова - напишите об этом',
                             reply_markup=keyboard)

        user['in_game'] = False
    else:
        await message.answer('А мы итак с вами не играем. '
                             'Может, сыграем разок?')


# Этот хэндлер будет срабатывать на согласие пользователя сыграть в игру
@dp.message(Text(text=['Я хочу играть!'], ignore_case=True))
async def process_positive_answer(message: Message):
    if not user['in_game']:
        await message.answer('Ура!\n\nЯ загадал число от 1 до 100, '
                             'попробуй угадать!',
                             reply_markup=keyboard2)

        user['in_game'] = True
        user['secret_number'] = get_random_number()
        user['attempts'] = ATTEMPTS
    else:
        await message.answer('Пока мы играем в игру я могу '
                             'реагировать только на числа от 1 до 100 '
                             'и команды /cancel и /stat')


# Этот хэндлер будет срабатывать на отказ пользователя сыграть в игру
@dp.message(Text(text=['Я не хочу играть!'], ignore_case=True))
async def process_negative_answer(message: Message):
    if not user['in_game']:
        await message.answer('Жаль :(\n\nЕсли захотите поиграть - просто '
                             'напишите об этом')

    else:
        await message.answer('Мы же сейчас с вами играем. Присылайте, '
                             'пожалуйста, числа от 1 до 100')


# Этот хэндлер будет срабатывать на отправку пользователем чисел от 1 до 100
@dp.message(lambda x: x.text and x.text.isdigit() and 1 <= int(x.text) <= 100)
async def process_numbers_answer(message: Message):
    if user['in_game']:
        if int(message.text) == user['secret_number']:
            await message.answer('Ты победил :), поздравляю!',
                                 reply_markup=keyboard)
            await message.answer_sticker('CAACAgIAAxkBAAIF4GRVCrQDd7QbJD5D46BRCEyF_LFNAAKrCgACO36wSkxaoI6szpShLwQ')
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
                                 reply_markup=keyboard)
            await message.answer_sticker('CAACAgIAAxkBAAIF3mRVCpmVLULaH6GeKHqGBcFC4TElAAKBDAACE5WoSmr1do5SMwOELwQ')
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
pprint(Message)
if __name__ == '__main__':
    dp.run_polling(bot)