from aiogram.fsm.state import State, StatesGroup


class AddLessonFSM(StatesGroup):
    waiting_for_lesson_name = State()
    waiting_for_lesson_description = State()
    waiting_for_task = State()
