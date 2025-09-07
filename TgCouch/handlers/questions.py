from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram import Bot
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from config_reader import config
from keyboards.for_subscription import get_response_kb

class Registration(StatesGroup):
    name = State()
    mobile_number = State()
    nickname = State()


router = Router()

def get_back_button():
    """Клавиатура с кнопкой 'Назад'"""
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(text="⬅️ Назад к выбору", callback_data="back_to_categories")
    )
    return builder.as_markup()


@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    await message.answer(
        'Привет, это помощник энергокоуча и психолога Александра Белякова.\n'
        'Меня зовут Беляш, давайте познакомимся?\n'
        '\n'
        '<b>(Напиши фамилию и имя)</b>',
    )
    await state.set_state(Registration.name)


@router.message(Registration.name, F.text)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(full_name=message.text)

    builder = ReplyKeyboardBuilder()
    builder.add(
        types.KeyboardButton(
            text='Скинуть свой номер',
            request_contact=True
        )
    )

    await message.answer(
        f"Приятно познакомиться, {message.text}! 🙌\n"
        "Теперь скинь, пожалуйста, свой номер телефона, нажав на кнопку ниже)",
        reply_markup=builder.as_markup(
            resize_keyboard=True,
            one_time_keyboard=True
        )
    )
    await state.set_state(Registration.mobile_number)


@router.message(Registration.mobile_number, F.contact)
async def process_mobile_number(message: Message, state: FSMContext):
    phone_number = message.contact.phone_number
    await state.update_data(phone_number=phone_number)

    await message.answer(
        'Отлично! А теперь напиши свой никнейм в Telegram (например, @sumasoshedshiy):'
    )
    await state.set_state(Registration.nickname)


@router.message(Registration.nickname, F.text)
async def process_nickname(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(nickname=message.text)

    data = await state.get_data()
    full_name = data['full_name']
    phone_number = data['phone_number']
    nickname = data['nickname']
    user_id = message.from_user.id

    admin_message = (
        "📩 <b>Новый клиент зарегистрирован!</b>\n"
        f"👤 <b>ФИО:</b> {full_name}\n"
        f"📞 <b>Телефон:</b> {phone_number}\n"
        f"🔗 <b>Никнейм:</b> {nickname}\n"
        f"🆔 <b>ID пользователя:</b> {user_id}"
    )

    try:
        await bot.send_message(
            chat_id=config.admin_id,
            text=admin_message,
            parse_mode="HTML"
        )
    except Exception as e:
        print(f"Не удалось отправить сообщение администратору: {e}")

    await message.answer(
        'Кстати, а ты подписан на канал "Ангелы Сани"?\n'
        'https://t.me/angeliSani',
        reply_markup=get_response_kb()
    )

    await state.clear()


@router.message(F.text.lower() == 'да, подписан(а)')
async def answer_yes(message: Message, bot: Bot):
    try:
        member = await bot.get_chat_member(chat_id=-1002485471071, user_id=message.from_user.id)

        if member.status in ["member", "administrator", "creator"]:
            builder = ReplyKeyboardBuilder()
            builder.add(types.KeyboardButton(text="Услуги Саши Белякова"))

            await message.answer(
                "✅ Подписка подтверждена! Держи подарок:",
                reply_markup=builder.as_markup(resize_keyboard=True)
            )

            await message.answer_audio(
                audio="CQACAgIAAxkBAAE6rgtovAABMrEzOXjdRrMAAcBQWYJf3SmIAAIdewACuZgYS4D-OA_oxMdSNgQ",
                caption="🎧 <b>Энергопрактика: Освобождение от излишнего напряжения</b>\n\n"
                        "Автор — Александр Беляков.\n"
                        "Слушай с закрытыми глазами, в тишине.",
                parse_mode="HTML"
            )
        else:
            await message.answer(
                "❌ Я не вижу тебя в подписчиках. Подпишись: https://t.me/angeliSani"
            )
    except Exception as e:
        await message.answer("❌ Произошла ошибка при проверке. Убедись, что подписан.")
        print(f"Ошибка проверки подписки: {e}")


@router.message(F.text.lower() == 'нет, не подписан(а)')
async def answer_no(message: Message):
    await message.answer(
        'Тогда обязательно подпишись на канал, чтобы получить подарок:\n'
        'https://t.me/angeliSani\n\n'
        'После этого вернись и нажми "Да, подписан(а)"',
        reply_markup=get_response_kb()
    )


@router.message(F.text == "Услуги Саши Белякова")
async def show_services(message: Message):
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="1. Личный Энергокоучинг", callback_data="coaching_personal"))
    builder.row(types.InlineKeyboardButton(text="2. Психологическая сессия", callback_data="psych_session"))
    builder.row(types.InlineKeyboardButton(text="3. Психомоторное письмо и МАК-карты", callback_data="mak_method"))
    builder.row(types.InlineKeyboardButton(text="4. Осознанное дыхание", callback_data="breathing_practice"))
    builder.row(types.InlineKeyboardButton(text="5. Курс «Ангелы Изобилия»", callback_data="angels_course"))

    await message.answer("Услуги Саши Белякова", reply_markup=builder.as_markup())
    await message.answer("Можешь выбрать категорию:", reply_markup=ReplyKeyboardRemove())


@router.callback_query(F.data == "coaching_personal")
async def show_coaching_personal(callback: types.CallbackQuery):
    text = (
        "<b>Энергокоучинг метод СОЛО</b>\n\n"
        "<b>№3</b> Личная Энерготерапия – 7000 руб.\n"
        "Оплата: https://payform.ru/tf83K7G/\n\n"
        "<b>№4</b> Первая/Студенческая Энерготерапия – 3500 руб.\n"
        "Оплата: https://payform.ru/gd83KgR/"
    )
    await callback.message.answer(text, parse_mode="HTML", reply_markup=get_back_button())
    await callback.answer()


@router.callback_query(F.data == "psych_session")
async def show_psych_session(callback: types.CallbackQuery):
    text = (
        "<b>Психологическая сессия</b>\n\n"
        "<b>№5</b> Стандартная сессия – 2000 руб.\n"
        "Оплата: https://payform.ru/908oCGZ/\n\n"
        "<b>№6</b> Первая сессия со скидкой 50% – 1000 руб.\n"
        "Оплата: https://payform.ru/de8oCZt/"
    )
    await callback.message.answer(text, parse_mode="HTML", reply_markup=get_back_button())
    await callback.answer()


@router.callback_query(F.data == "mak_method")
async def show_mak_method(callback: types.CallbackQuery):
    text = (
        "<b>Метод Психомоторного письма и МАК</b>\n\n"
        "<b>№7</b> Разовая консультация – 1000 руб.\n"
        "Оплата: https://payform.ru/sm8oD7A/\n\n"
        "<b>№8</b> Месячный курс (10 сессий) – 6000 руб.\n"
        "Оплата: https://payform.ru/ao8oDea/"
    )
    await callback.message.answer(text, parse_mode="HTML", reply_markup=get_back_button())
    await callback.answer()


@router.callback_query(F.data == "breathing_practice")
async def show_breathing_practice(callback: types.CallbackQuery):
    text = (
        "<b>Групповая практика осознанного дыхания</b>\n\n"
        "<b>№9</b> Занятие на ZOOM (1 раз в неделю) – 500 руб.\n"
        "Оплата: https://payform.ru/qb8oDmt/"
    )
    await callback.message.answer(text, parse_mode="HTML", reply_markup=get_back_button())
    await callback.answer()


@router.callback_query(F.data == "angels_course")
async def show_angels_course(callback: types.CallbackQuery):
    text = (
        "<b>Курс «Ангелы Изобилия»</b>\n\n"
        "<b>№1</b> Тариф «Ангел Изобилия» – 3333 руб.\n"
        "Оплата: https://payform.ru/tf83Hgg/\n\n"
        "<b>№2</b> Тариф «Серафим» – 11111 руб.\n"
        "Оплата: https://payform.ru/3b83JDE/"
    )
    await callback.message.answer(text, parse_mode="HTML", reply_markup=get_back_button())
    await callback.answer()


# Кнопка "Назад" — возвращает к выбору категорий
@router.callback_query(F.data == "back_to_categories")
async def back_to_categories(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="1. Личный Энергокоучинг", callback_data="coaching_personal"))
    builder.row(types.InlineKeyboardButton(text="2. Психологическая сессия", callback_data="psych_session"))
    builder.row(types.InlineKeyboardButton(text="3. Психомоторное письмо и МАК-карты", callback_data="mak_method"))
    builder.row(types.InlineKeyboardButton(text="4. Осознанное дыхание", callback_data="breathing_practice"))
    builder.row(types.InlineKeyboardButton(text="5. Курс «Ангелы Изобилия»", callback_data="angels_course"))

    await callback.message.answer("Услуги Саши Белякова?", reply_markup=builder.as_markup())
    await callback.answer()