from aiogram.utils.keyboard import InlineKeyboardBuilder

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def get_student_attendance_menu(
    student_attendance,
    attendance_id
) -> InlineKeyboardMarkup:

    keyboard = InlineKeyboardBuilder()
    student_attendance_id = student_attendance.id

    skipped = '❌ Не был' if not student_attendance.skipped else '✅ Был'
    late = '❌ Не опоздал' if student_attendance.late <= 0 else f'⚠️ Опоздал на {student_attendance.late} минут'

    keyboard.add(
        InlineKeyboardButton(
            text=skipped,
            callback_data=f"student_attendance_skipped_status_{student_attendance_id}_{attendance_id}",
        )
    )

    keyboard.add(
        InlineKeyboardButton(
            text=late,
            callback_data=f"student_attendance_late_status_{student_attendance_id}_{attendance_id}",
        )
    )

    return keyboard.adjust(2).as_markup()


async def get_student_task_menu(
    student_task
) -> InlineKeyboardMarkup:

    keyboard = InlineKeyboardBuilder()
    student_task_id = student_task.id

    passed = '❌ Не сдал' if not student_task.passed else '✅ Сдал'
    mark = '❌ Не принято' if student_task.mark <= 0 else f'✅ {student_task.mark} баллов'

    keyboard.add(
        InlineKeyboardButton(
            text=passed,
            callback_data=f"student_task_passed_status_{student_task_id}",
        )
    )

    keyboard.add(
        InlineKeyboardButton(
            text=mark,
            callback_data=f"student_task_mark_status_{student_task_id}",
        )
    )

    return keyboard.adjust(2).as_markup()


async def return_lesson_menu(
    lesson_id
) -> InlineKeyboardMarkup:

    keyboard = InlineKeyboardBuilder()

    keyboard.add(
        InlineKeyboardButton(
            text='🔙 Назад к занятию',
            callback_data=f"lesson_{lesson_id}",
        )
    )

    return keyboard.adjust(2).as_markup()
