from aiogram import Router,F
from aiogram.types import Message,CallbackQuery
from aiogram.filters import Command, CommandStart
from src.lexicon.lexicon_ru import LEXICON_RU,BUTONS_START
from src.keyboards import create_inline_kb
from src.services.db_service import get_category_kb

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

#press button

@router.callback_query(F.data == 'init-1')
async def process_press_button(callback: CallbackQuery):

    keyboard = create_inline_kb(1,**get_category_kb())

    await callback.message.edit_text(
        text = f'Каталог опалубки',
        reply_markup= keyboard
    )
