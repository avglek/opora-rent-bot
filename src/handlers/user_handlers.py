from aiogram import Router,F
from aiogram.types import Message,CallbackQuery
from aiogram.filters import Command, CommandStart
from src.lexicon.lexicon_ru import LEXICON_RU,BUTONS_START,BUTON_HOME
from src.keyboards import create_inline_kb
from src.services.db_service import get_category,get_rents_by_id
from src.models import CategoryCallbackFactory,RentCallbackFactory,PriceCallbackFactory,BackCallbackFactory

router = Router()

# Этот хэндлер срабатывает на команду /start
@router.message(CommandStart())
async def process_start_command(message: Message):

    keyboard = create_inline_kb(1, **BUTONS_START)

    await message.answer(
        text=LEXICON_RU['/start'],
        reply_markup=keyboard
    )

# Этот хэндлер срабатывает на команду /help
@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON_RU['/help'])


# Обработка просмотра каталога

@router.callback_query(F.data == 'review')
async def process_review_press_button(callback: CallbackQuery):

    keys = get_category()
    keys.update(BUTON_HOME)

    keyboard = create_inline_kb(1,**keys)

    await callback.message.edit_text(
        text = f'Просмотр каталога опалубки. Выберите категорию',
        reply_markup= keyboard
    )

@router.callback_query(F.data == 'rent')
async def process_rend_press_button(callback: CallbackQuery):

    keys = get_category()
    keys.update(BUTON_HOME)

    keyboard = create_inline_kb(1,**keys)

    await callback.message.edit_text(
        text = f'Аренда опалубки. Выберите категорию',
        reply_markup= keyboard
    )

@router.callback_query(F.data == 'calculate')
async def process_calc_press_button(callback: CallbackQuery):

    keyboard = create_inline_kb(1,"Оформить заявку",**BUTON_HOME)

    await callback.message.edit_text(
        text = f'Подайте заявку на расчет опалубки',
        reply_markup= keyboard
    )

@router.callback_query(F.data == 'other')
async def process_other_press_button(callback: CallbackQuery):

    keyboard = create_inline_kb(1,**BUTON_HOME)

    await callback.message.edit_text(
        text = f'Напишите, что Вас интересует.',
        reply_markup=keyboard
    )

@router.callback_query(F.data == 'home')
async def process_home_press_button(callback: CallbackQuery):

    keyboard = create_inline_kb(1, **BUTONS_START)

    await callback.message.edit_text(
        text=LEXICON_RU['/start'],
        reply_markup=keyboard
    )

@router.callback_query(CategoryCallbackFactory.filter())
async def process_category_inline_button_press(callback: CallbackQuery,
                                          callback_data:CategoryCallbackFactory):
    rents = get_rents_by_id(callback_data.category_id)
    rents[BackCallbackFactory(back_prefix="category").pack()]=LEXICON_RU['but_back']
    rents.update(BUTON_HOME)

    keyboard = create_inline_kb(1,**rents)

    await callback.message.edit_text(
        text = f'Категория: {callback_data.name}',
        reply_markup= keyboard
    )

@router.callback_query(BackCallbackFactory.filter())
async def process_back_button_press(callback:CallbackQuery,callback_data:BackCallbackFactory):
    if(callback_data.back_prefix == "category"):
        await process_home_press_button(callback)
