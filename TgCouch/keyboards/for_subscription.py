from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def get_response_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text='Да, подписан(а)')
    kb.button(text='Нет, не подписан(а)')
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)