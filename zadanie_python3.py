from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import Message
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import filters
from aiogram.utils import executor

API_TOKEN = '7965811318:AAFmcgKrr8_H9u6oofWTCHEpTvjZCCkteSM'

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

class CalculatorState(StatesGroup):
    waiting_for_first_number = State()
    waiting_for_second_number = State()
    waiting_for_operation = State()

@dp.message_handler(commands=['start'], state="*")
async def send_welcome(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Здарова, пользователь!\nТы попал сюды на моего бота калькулятора.\nВведите первое число:")
    await CalculatorState.waiting_for_first_number.set()

@dp.message_handler(state=CalculatorState.waiting_for_first_number)
async def process_first_number(message: types.Message, state: FSMContext):
    try:
        first_number = float(message.text.strip())
        await state.update_data(first_number=first_number)
        await message.answer("Введите второе число:")
        await CalculatorState.waiting_for_second_number.set()  
    except ValueError:
        await message.answer("Это не число. Попробуйте снова.\nВведите первое число:")

@dp.message_handler(state=CalculatorState.waiting_for_second_number)
async def process_second_number(message: types.Message, state: FSMContext):
    try:
        second_number = float(message.text.strip())
        await state.update_data(second_number=second_number)
        await message.answer("Выберите действие (+, -, *, /):")
        await CalculatorState.waiting_for_operation.set() 
    except ValueError:
        await message.answer("Это не число. Попробуйте снова.\nВведите второе число:")

@dp.message_handler(state=CalculatorState.waiting_for_operation)
async def process_operation(message: types.Message, state: FSMContext):
    operation = message.text.strip()
    data = await state.get_data()
    first_number = data['first_number']
    second_number = data['second_number']

    if operation in ['+', '-', '*', '/']:
        await state.finish()  

        if operation == '+':
            result = first_number + second_number
        elif operation == '-':
            result = first_number - second_number
        elif operation == '*':
            result = first_number * second_number
        elif operation == '/':
            if second_number == 0:
                await message.answer("Деление на ноль невозможно.")
                return
            result = first_number / second_number

        await message.answer(f"Результат: {result}")
    else:
        await message.answer("Неверное действие. Попробуйте снова.\nВыберите действие (+, -, *, /):")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)


