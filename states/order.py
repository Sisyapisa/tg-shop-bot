from aiogram.fsm.state import StatesGroup, State

class OrderState(StatesGroup):
    INPUT_NAME = State()
    INPUT_PHONE = State()
    INPUT_ADDRESS = State()
    CONFIRM = State()