from aiogram import Router,F
from aiogram.types import Message,CallbackQuery,FSInputFile
from aiogram.filters import Command, CommandStart,StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from src.lexicon.lexicon_ru import LEXICON_RU, BUTTONS_START, BUTTON_HOME, BUTTON_BACK
from src.keyboards import create_inline_kb
from src.services.db_service import get_category,get_rents_by_category_id,get_description_by_rent_id
from src.models import CategoryCallbackFactory,RentCallbackFactory,PriceCallbackFactory

router = Router()

class FSMRent(StatesGroup):
    category = State()
    rent = State()
    price = State()


#################### LEVEL 0 #########################
# Этот хэндлер срабатывает на команду /start
@router.message(CommandStart())
async def process_start_command(message: Message, state: FSMContext):

    keyboard = create_inline_kb(1, **BUTTONS_START)

    if await state.get_state() is not None:
        await state.clear()

    await state.update_data(status="start")
    await message.answer(
        text=LEXICON_RU['/start'],
        reply_markup=keyboard
    )

# Этот хэндлер срабатывает на команду /help
@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON_RU['/help'])


#################### LEVEL 1 #########################
# Обработка просмотра каталога

@router.callback_query(F.data == 'review')
async def process_review_press_button(callback: CallbackQuery,state: FSMContext):

    keys = get_category()
    keys.update(BUTTON_HOME)

    keyboard = create_inline_kb(1,**keys)

    await state.set_state({"status":"review","category":None,"rent":None,})
    await callback.message.edit_text(
        text = f'Просмотр каталога опалубки. Выберите категорию',
        reply_markup= keyboard
    )

@router.callback_query(F.data == 'rent')
async def process_rend_press_button(callback: CallbackQuery,state: FSMContext):

    keys = get_category()
    keys.update(BUTTON_HOME)

    keyboard = create_inline_kb(1,**keys)

    await state.set_state({"status":"rent","category":None,"rent":None})
    await callback.message.edit_text(
        text = f'Аренда опалубки. Выберите категорию',
        reply_markup= keyboard
    )

@router.callback_query(F.data == 'calculate')
async def process_calc_press_button(callback: CallbackQuery):

    keyboard = create_inline_kb(1,"Оформить заявку",**BUTTON_HOME)

    await callback.message.edit_text(
        text = f'Подайте заявку на расчет опалубки',
        reply_markup= keyboard
    )

@router.callback_query(F.data == 'other')
async def process_other_press_button(callback: CallbackQuery):

    keyboard = create_inline_kb(1,**BUTTON_HOME)

    await callback.message.edit_text(
        text = f'Напишите, что Вас интересует.',
        reply_markup=keyboard
    )

#################### LEVEL 2 #########################

@router.callback_query(CategoryCallbackFactory.filter())
async def process_category_inline_button_press(callback: CallbackQuery, state: FSMContext,
                                          callback_data:CategoryCallbackFactory):
    print(state)
    rents = get_rents_by_category_id(callback_data.category_id)
    rents.update(BUTTON_BACK)
    rents.update(BUTTON_HOME)

    keyboard = create_inline_kb(1,**rents)

    await state.update_data(status="category",category=callback_data.category_id,rent=None)
    await callback.message.edit_text(
        text = f'Категория: {callback_data.name}',
        reply_markup= keyboard
    )

#################### LEVEL 3 #########################

@router.callback_query(RentCallbackFactory.filter())
async def process_rent_description_inline_button_press(callback: CallbackQuery,
                                                       state: FSMContext,
                                                       callback_data:RentCallbackFactory):

    rent_message = get_description_by_rent_id(callback_data.rent_id)
    keys = dict()
    keys.update(BUTTON_BACK)
    keys.update(BUTTON_HOME)
    keyboard = create_inline_kb(1,**keys)

    await callback.message.delete()
    await callback.message.answer_photo(
        photo=FSInputFile(rent_message['photo_file']),
        caption=rent_message['data'],
        reply_markup=keyboard
    )

#################### LEVEL ALL #########################

@router.callback_query(F.data == 'home')
async def process_home_press_button(callback: CallbackQuery,state: FSMContext):

    #await callback.message.delete()
    await process_start_command(callback.message,state)

@router.callback_query(F.data == 'back')
async def process_back_button_press(callback:CallbackQuery,state:FSMContext):

    status = await state.get_state()
    print(status)