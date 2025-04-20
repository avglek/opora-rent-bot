from aiogram.filters.callback_data import CallbackData

class RentCallbackFactory(CallbackData,prefix="rent"):
    rent_id:int

class CategoryCallbackFactory(CallbackData,prefix="category"):
    category_id:int
    name:str

class PriceCallbackFactory(CallbackData,prefix="price"):
    price_id:int

class BackCallbackFactory(CallbackData,prefix="back"):
    back_prefix:str