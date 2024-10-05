# import math

# from aiogram.utils.keyboard import InlineKeyboardBuilder

# from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# from apps.apps.progressucation.models import Task

# from apps.bot.utils import get_student_groups, get_group_lessons, get_or_create_attendance_by_lesson


# ################################################################################################################


# async def get_student_groups_list() -> InlineKeyboardMarkup:
    
#     groups = await get_student_groups()

#     group_buttons = [
#         InlineKeyboardButton(
#             text=f"{group.name}",
#             callback_data=f"student_group_{group.id}"
#         )
#         for group in groups
#     ]

#     total_groups = len(group_buttons)

#     if total_groups == 0:
#         return InlineKeyboardMarkup(inline_keyboard=[])

#     optimal_columns = math.ceil(math.sqrt(total_groups))

#     group_rows = [
#         group_buttons[i: i + optimal_columns]
#         for i in range(0, total_groups, optimal_columns)
#     ]

#     return InlineKeyboardMarkup(inline_keyboard=group_rows)


# async def get_group_lessons_list(student_group_id) -> InlineKeyboardMarkup:

#     lessons = await get_group_lessons(student_group_id)

#     lessons_list_buttons = [
#         InlineKeyboardButton(
#             text=f"{lesson.topic}",
#             callback_data=f"lesson_{lesson.id}"
#         )
#         for lesson in lessons
#     ]

#     total_lessons = len(lessons_list_buttons)

#     if total_lessons == 0:
#         return InlineKeyboardMarkup(
#             inline_keyboard=[
#                 [
#                     InlineKeyboardButton
#                     (
#                         text="🔙 Назад",
#                         callback_data='back_to_menu'
#                     )
#                 ]
#             ]
#         )

#     optimal_columns = math.ceil(math.sqrt(total_lessons))

#     lesson_rows = [
#         lessons_list_buttons[i: i + optimal_columns]
#         for i in range(0, total_lessons, optimal_columns)
#     ]

#     lesson_rows.append(
#         [
#             InlineKeyboardButton(
#                 text="🔙 Назад",
#                 callback_data='back_to_menu'
#             )
#         ]
#     )

#     return InlineKeyboardMarkup(inline_keyboard=lesson_rows)


# ################################################################################################################


# async def get_lesson_menu(
#     student_group_id,
#     lesson
# ) -> InlineKeyboardMarkup:

#     keyboard = InlineKeyboardBuilder()
#     attendance = await get_or_create_attendance_by_lesson(lesson, student_group_id)
#     task, creatapps.progress = await Task.objects.aget_or_create(lesson=lesson)

#     keyboard.add(
#         InlineKeyboardButton(
#             text="🔍 Проверка заданий",
#             callback_data=f"task_{task.id}",
#         )
#     )

#     keyboard.add(
#         InlineKeyboardButton(
#             text="📈 Посещаемость",
#             callback_data=f"attendance_{attendance.id}",
#         )
#     )

#     keyboard.add(
#         InlineKeyboardButton(
#             text="🔙 Назад",
#             callback_data=f"student_group_{student_group_id}",
#         )
#     )

#     return keyboard.adjust(2).as_markup()


# ################################################################################################################


# async def get_student_attendance_menu(
#     student_attendance
# ) -> InlineKeyboardMarkup:

#     keyboard = InlineKeyboardBuilder()
#     student_attendance_id = student_attendance.id

#     skippapps.progress = '❌ Не был' if student_attendance.skippapps.progress else '✅ Был'
#     late = '❌ Не опоздал' if student_attendance.late <= 0 else f'⚠️ Опоздал на {student_attendance.late} минут'

#     keyboard.add(
#         InlineKeyboardButton(
#             text=skippapps.progress,
#             callback_data=f"student_attendance_skippapps.progress_status_{student_attendance_id}",
#         )
#     )

#     keyboard.add(
#         InlineKeyboardButton(
#             text=late,
#             callback_data=f"student_attendance_late_status_{student_attendance_id}",
#         )
#     )

#     return keyboard.adjust(2).as_markup()


# async def get_student_task_menu(
#     student_task
# ) -> InlineKeyboardMarkup:

#     keyboard = InlineKeyboardBuilder()
#     student_task_id = student_task.id

#     passapps.progress = '❌ Не сдал' if student_task.passapps.progress else '✅ Сдал'
#     mark = '❌ Не принято' if student_task.mark <= 0 else f'✅ {student_task.mark} баллов'

#     keyboard.add(
#         InlineKeyboardButton(
#             text=passapps.progress,
#             callback_data=f"student_task_passapps.progress_status_{student_task_id}",
#         )
#     )

#     keyboard.add(
#         InlineKeyboardButton(
#             text=mark,
#             callback_data=f"student_task_mark_status_{student_task_id}",
#         )
#     )

#     return keyboard.adjust(2).as_markup()



