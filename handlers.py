from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

import keyboards
from bot import bot, bot_bd


async def greeting(message: types.Message, state: FSMContext) -> None:
    """ Отлавливает команду /start, выводит соответствующую клавиатуру. """

    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()

    await bot.send_message(message.from_user.id, 'Приветствую!', reply_markup=keyboards.GREETING)


async def start_dialog(message: types.Message, state: FSMContext) -> None:
    """ Отлавливает команду кнопку, выводит соответствующую клавиатуру. """

    await bot.send_message(message.from_user.id, 'Пожалуйста, выберите предпочитаемую тему задач')

    await GetProblemListFSM.waiting_topic_name.set()


class GetProblemListFSM(StatesGroup):
    """ Машина состояний - диалог предоставления списка задач. """
    waiting_topic_name = State()
    waiting_complexity = State()


async def get_topic_name(message: types.Message, state: FSMContext) -> None:
    """ Отлавливает название темы """

    async with state.proxy() as data:
        data['topic_name'] = message.text.lower()
    await bot.send_message(message.from_user.id, 'Пожалуйста, выберите предпочитаемую сложность задач',
                           reply_markup=keyboards.COMPLEXITY_KEYBOARD)
    await GetProblemListFSM.next()


async def get_complexity_name(message: types.Message, state: FSMContext) -> None:
    """ Отлавливает сложность задачи, передаёт сложность и тему в запрос к бд, выводит задачи. """

    try:
        async with state.proxy() as data:
            data['complexity'] = message.text
        list_of_problems = bot_bd.get_list_of_problems(data['topic_name'], data['complexity'])

        result = ''
        for problem in list_of_problems:
            result += '\n' + ' - '.join(problem) + '\n'

        await bot.send_message(message.from_user.id, result, reply_markup=keyboards.GREETING)

    except Exception:
        await bot.send_message(message.from_user.id, 'Что-то не так, возможно, вы ошиблись при вводе данных',
                               reply_markup=keyboards.TOPICS_KEYBOARD)

    await state.finish()


def register_main_handlers(dp):
    dp.register_message_handler(greeting, commands=["start"], state="*"),
    dp.register_message_handler(start_dialog, text='Подобрать задачи'),
    dp.register_message_handler(get_topic_name, content_types=['text'], state=GetProblemListFSM.waiting_topic_name),
    dp.register_message_handler(get_complexity_name, content_types=['text'], state=GetProblemListFSM.waiting_complexity)
