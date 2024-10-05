import math

from aiogram.utils.keyboard import InlineKeyboardBuilder

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from apps.bot.utils.orm_queries import get_group_lessons, get_or_create_attendance_by_lesson, get_student_groups

from apps.education.models import Task


async def get_student_groups_list() -> InlineKeyboardMarkup:
    
    groups = await get_student_groups()

    group_buttons = [
        InlineKeyboardButton(
            text=f"{group.name}",
            callback_data=f"student_group_{group.id}"
        )
        for group in groups
    ]

    total_groups = len(group_buttons)

    if total_groups == 0:
        return InlineKeyboardMarkup(inline_keyboard=[])

    optimal_columns = math.ceil(math.sqrt(total_groups))

    group_rows = [
        group_buttons[i: i + optimal_columns]
        for i in range(0, total_groups, optimal_columns)
    ]

    return InlineKeyboardMarkup(inline_keyboard=group_rows)


async def get_group_lessons_list(student_group_id) -> InlineKeyboardMarkup:
    lessons = await get_group_lessons(student_group_id)

    lessons_list_buttons = [
        InlineKeyboardButton(
            text=f"{lesson.topic} [{lesson.created_at.strftime('%d.%m')}]",
            callback_data=f"lesson_{lesson.id}"
        )
        for lesson in lessons
    ]

    total_lessons = len(lessons_list_buttons)

    lesson_rows = []
    if total_lessons > 0:
        optimal_columns = math.ceil(math.sqrt(total_lessons))
        
        for i in range(0, total_lessons, optimal_columns):
            lesson_rows.append(lessons_list_buttons[i: i + optimal_columns])

    lesson_rows.append([
        InlineKeyboardButton(
            text="Добавить занятие",
            callback_data=f'add_lesson_to_group_{student_group_id}'
        )
    ])
    lesson_rows.append([
        InlineKeyboardButton(
            text="🔙 Назад",
            callback_data='back_to_menu'
        )
    ])

    return InlineKeyboardMarkup(inline_keyboard=lesson_rows)


async def get_lesson_menu(
    student_group_id,
    lesson
) -> InlineKeyboardMarkup:

    keyboard = InlineKeyboardBuilder()
    attendance = await get_or_create_attendance_by_lesson(lesson, student_group_id)
    task, created = await Task.objects.aget_or_create(lesson=lesson)

    keyboard.add(
        InlineKeyboardButton(
            text="🔍 Проверка заданий",
            callback_data=f"task_{task.id}",
        )
    )

    keyboard.add(
        InlineKeyboardButton(
            text="📈 Посещаемость",
            callback_data=f"attendance_{attendance.id}",
        )
    )

    keyboard.add(
        InlineKeyboardButton(
            text="🔙 Назад",
            callback_data=f"student_group_{student_group_id}",
        )
    )

    return keyboard.adjust(2).as_markup()

