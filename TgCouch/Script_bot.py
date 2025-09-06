import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram import F
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from config_reader import config
from aiogram.client.default import DefaultBotProperties

logging.basicConfig(level=logging.INFO)
# объект бота
bot = Bot(
    token=config.bot_token.get_secret_value(),
    default=DefaultBotProperties(
        parse_mode=ParseMode.HTML
    )
)

dp = Dispatcher()

# хендлер на команду старт
@dp.message(F.text, Command('start'))
async def cmd_start(message: types.Message):
    await message.answer(
        'Привет, это помощник энергокоуча и психолога Александра Белякова.\n'
        'Меня зовут Беляш, давайте познакомимся?\n'
        '\n'
        '<b>(Напиши фамилию и имя)</b>'
    )

@dp.message(F.text, Command('check'))
async def cmd_check(message: types.Message):
    kb = [
        [
            types.KeyboardButton(text='Да, есть подписка'),
            types.KeyboardButton(text='Нет, не подписан(а)')
        ]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        one_time_keyboard=True,
        resize_keyboard=True
    )
    await message.answer(
        'Вы подписаны на канал "Ангелы Сани"?',
        reply_markup=keyboard
    )

@dp.message(F.text == 'Да, есть подписка')
async def with_sub(message: types.Message):
    await message.reply('Прекрасно, держи бесплатный аудиофайл')

@dp.message(F.text == 'Нет, не подписан(а)')
async def with_sub(message: types.Message):
    await message.reply(
        'Тогда скорей подписывайся и я тебе отправлю беспланый айдиофайл\n'
        'https://t.me/kolyamoskkva'
    )

@dp.message(Command('special'))
async def cmd_special(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.add(
        types.KeyboardButton(text='Скинуть свой номер', request_contact=True)
    )

    await message.answer(
        'Поделись своим номером телефона',
        reply_markup=builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
    )

@dp.message(Command('course'))
async def cmd_course(message: types.Message, bot: Bot):
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(
        text='Счёт - 001', url='https://payform.ru/tf83Hgg/'
    )
        )
    await message.answer(
        'Выбирете курс',
        reply_markup=builder.as_markup()
    )


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())