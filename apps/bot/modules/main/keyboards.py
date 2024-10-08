import math
from datetime import datetime

from aiogram.utils.keyboard import InlineKeyboardBuilder

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from apps.bot.utils.orm_queries import get_group_lessons, get_or_create_attendance_by_lesson, get_student_groups

from apps.education.models import Task

from core.settings import WEB_URL


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

    group_rows.append([
        InlineKeyboardButton(
            text="➕ Добавить ученика",
            url=f'{WEB_URL}admin/studentgroup/'
        )
    ])

    return InlineKeyboardMarkup(inline_keyboard=group_rows)


async def get_group_lessons_list(student_group_id) -> InlineKeyboardMarkup:

    lesson_rows = []

    lessons = await get_group_lessons(student_group_id)
    completed_lessons = f'{WEB_URL}admin/education/lesson/?student_group__id__exact={student_group_id}&q='

    today = datetime.now().date()
    today_lesson = next((lesson for lesson in lessons if lesson.created_at.date() == today), None)

    if today_lesson is None:
        lesson_rows.append([
            InlineKeyboardButton(
                text="Добавить занятие",
                callback_data=f'add_lesson_to_group_{student_group_id}'
            )
        ])
    else:
        lesson_rows.append([
            InlineKeyboardButton(
                text=f"{today_lesson.topic} [{today_lesson.created_at.strftime('%d.%m')}]",
                callback_data=f'lesson_{today_lesson.id}'
            )
        ])

    lesson_rows.append([
        InlineKeyboardButton(
            text="Пройденные темы",
            url=completed_lessons
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

