from aiogram.fsm.state import StatesGroup,State

class AddItemsState(StatesGroup):
    INPUT_NAME = State()
    INPUT_DESCRIPTION = State()
    INPUT_PRICE = State()
    INPUT_PHOTO = State()
    INPUT_CATEGORY = State()
    CONFIRM = State()

class DeleteItemsState(StatesGroup):
    SELECT_ITEM = State()