from aiogram import Router, F

from aiogram.filters import Command, CommandStart

from aiogram.types import CallbackQuery, Message

from apps.bot.modules.main.keyboards import get_group_lessons_list, get_lesson_menu, get_student_groups_list
from apps.bot.utils.orm_queries import get_lesson_info_by_id, get_student_group_by_id, get_student_group_id_by_lesson
from apps.bot.utils.utils import get_date_info, get_info_answer, ensure_text_length

main_router = Router(name="Main menu")


@main_router.message(Command('menu'))
@main_router.message(CommandStart())
async def main_view(
        message: Message,
) -> None:
    date_info = await get_date_info()
    answer_text = f"""
📅 *Дата:* {date_info}

✨ *Выберите группу из списка ниже, чтобы продолжить:*
"""

    answer_text = ensure_text_length(answer_text)

    await get_info_answer(
        update_type=message,
        answer_text=answer_text,
        keyboard=await get_student_groups_list(),
    )


@main_router.callback_query(F.data.startswith("student_group_"))
async def group_view(
        callback: CallbackQuery,
) -> None:
    student_group_id = callback.data.split("student_group_")[1]
    student_group = await get_student_group_by_id(student_group_id)

    callback_answer_text = student_group.name

    answer_text = f"""
👥 *Выбранная группа:* {student_group.name}

📖 *Описание группы:*
{student_group.description if student_group.description else 'Нет доступной информации.'}

✨ *Пожалуйста, выберите урок для получения дальнейшей информации:*
"""

    answer_text = ensure_text_length(answer_text)

    await get_info_answer(
        update_type=callback,
        answer_text=answer_text,
        callback_answer_text=callback_answer_text,
        keyboard=await get_group_lessons_list(student_group_id),
    )


@main_router.callback_query(F.data.startswith("lesson_"))
async def lesson_view(
        callback: CallbackQuery,
) -> None:
    lesson_id = callback.data.split("lesson_")[1]
    lesson = await get_lesson_info_by_id(lesson_id)

    student_group_id = await get_student_group_id_by_lesson(lesson)

    callback_answer_text = lesson.topic
    answer_text = f"""
📚 *Урок:* {lesson.topic}

📝 *Подробности урока:*
{lesson.body if lesson.body else 'Нет подробной информации о уроке.'}

✨ *Пожалуйста, выберите дальнейшие действия:*
"""

    answer_text = ensure_text_length(answer_text)

    await get_info_answer(
        update_type=callback,
        answer_text=answer_text,
        callback_answer_text=callback_answer_text,
        keyboard=await get_lesson_menu(student_group_id, lesson),
    )


@main_router.callback_query(F.data == 'back_to_menu')
async def back_to_menu_view(
        callback: CallbackQuery,
) -> None:
    await main_view(callback.message)
    await callback.answer('🔙 Назад')
