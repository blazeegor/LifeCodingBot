from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from interceptor import OutputInterceptor


router = Router()


@router.message(Command("start"))
async def start_command(message: Message, state: FSMContext):
    await message.answer('👨‍💻 <b>Введите код программы:</b>')
    await state.set_state('code_input')


@router.message(StateFilter('code_input'))
async def code_input(message: Message, state: FSMContext):
    code = message.text
    is_success = True
    error_text = ''
    with OutputInterceptor() as output:
        try:
            exec(code)
        except Exception as exception:
            is_success = False
            error_text = exception.__str__()
    result = '\n'.join(output)
    if result:
        await message.answer(f'Вывод программы:\n\n{result}\n\n' + error_text)
    else:
        if is_success:
            await message.answer('<b>Процесс успешно завершён без какого-либо вывода в консоль.</b>')
        else:
            await message.answer(f'Ошибка!\n\n{error_text}', parse_mode=None)
    await state.clear()