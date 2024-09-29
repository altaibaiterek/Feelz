import re

from aiogram import Router, F

from asgiref.sync import sync_to_async

from aiogram.filters import Command, CommandStart

from aiogram.types import CallbackQuery, Message

from apps.account.models import Student
from apps.attendance.models import StudentAttendance, StudentTask
from apps.bot.keyboards import get_student_attendance_menu, get_student_groups_list, get_group_lessons_list, get_lesson_menu, get_student_task_menu

from apps.bot.utils import extract_student_late_info, extract_student_mark_info, get_info_answer, get_date_info, get_student_by_attendance, get_student_data_by_attendance, get_student_data_by_task, get_student_group_by_id, get_lesson_info_by_id, \
    get_student_group_id_by_lesson, get_students_by_group_id, get_attendance_info_by_id, \
    get_students_attendance_by_lesson_attendance, get_students_tasks_by_lesson_task, get_task_info_by_id, send_lesson_attendance, send_students_tasks


main_router = Router(name="Main info/menu")
group_router = Router(name="Group info")
lesson_router = Router(name="Lesson info")
attendance_router = Router(name="Attendance info")
education_router = Router(name="Education info")


@group_router.callback_query(F.data == 'back_to_menu')
async def back_to_menu_view(
        callback: CallbackQuery,
) -> None:

    await main_view(callback.message)
    await callback.answer('Возвращаемся в меню')


@main_router.message(Command('menu'))
@main_router.message(CommandStart())
async def main_view(
        message: Message,
) -> None:
    answer_text = await get_date_info()
    await get_info_answer(
        update_type=message,
        answer_text=answer_text,
        keyboard=await get_student_groups_list(),
    )


@group_router.callback_query(F.data.startswith("student_group_"))
async def group_view(
        callback: CallbackQuery,
) -> None:

    student_group_id = callback.data.split("student_group_")[1]
    student_group = await get_student_group_by_id(student_group_id)

    answer_text = student_group.name
    callback_answer_text = student_group.name

    await get_info_answer(
        update_type=callback,
        answer_text=answer_text,
        callback_answer_text=callback_answer_text,
        keyboard=await get_group_lessons_list(student_group_id),
    )


@lesson_router.callback_query(F.data.startswith("lesson_"))
async def lesson_view(
        callback: CallbackQuery,
) -> None:

    lesson_id = callback.data.split("lesson_")[1]
    lesson = await get_lesson_info_by_id(lesson_id)

    student_group_id = await get_student_group_id_by_lesson(lesson)

    answer_text = lesson.topic
    callback_answer_text = lesson.topic

    await get_info_answer(
        update_type=callback,
        answer_text=answer_text,
        callback_answer_text=callback_answer_text,
        keyboard=await get_lesson_menu(student_group_id, lesson),
    )


@attendance_router.callback_query(F.data.startswith("attendance_"))
async def attendance_view(
        callback: CallbackQuery,
) -> None:
    attendance_id = callback.data.split("attendance_")[1]
    attendance = await get_attendance_info_by_id(attendance_id)

    students_attendance = await get_students_attendance_by_lesson_attendance(attendance)

    await send_lesson_attendance(
        update_type=callback,
        students_attendance=students_attendance,
        students_attendance_keyboard=get_student_attendance_menu
                                 )


@attendance_router.callback_query(F.data.startswith("student_attendance_skipped_status_"))
async def update_student_attendance_skipped_status(
    callback: CallbackQuery,
) -> None:
    
    student_attendance_id = callback.data.split("student_attendance_skipped_status_")[1]
    student_attendance = await StudentAttendance.objects.aget(id=student_attendance_id)

    student_attendance.skipped = not student_attendance.skipped

    if student_attendance.skipped:
        await callback.answer("❌ Не был")
        student_attendance.skipped = True
    else:
        await callback.answer("✅ Был")
        student_attendance.skipped = False

    await student_attendance.asave()

    updated_status = await get_student_attendance_menu(student_attendance=student_attendance)
    
    await callback.message.edit_reply_markup(
        reply_markup=updated_status
    )


@attendance_router.callback_query(F.data.startswith("student_attendance_late_status_"))
async def update_student_attendance_late_status(
    callback: CallbackQuery,
) -> None:
    
    student_attendance_id = callback.data.split("student_attendance_late_status_")[1]
    student_attendance = await StudentAttendance.objects.aget(id=student_attendance_id)

    student_data = await get_student_data_by_attendance(student_attendance)

    student_name = (student_data['first_name'] + ' ' + student_data['last_name']).upper()
    student_phone = student_data['phone']

    menu_text = f"Укажите на сколько минут опоздал студент {student_name} ({student_phone}):"
    menu_answer_text = 'Запись опоздания'

    await callback.answer(menu_answer_text)
    
    await callback.message.answer(
        text=menu_text,
        parse_mode="HTML"
        )
    

@attendance_router.message(F.text.regexp(r"^\d+$"))
async def input_student_attendance_late_status(
    message: Message,
) -> None:
    
    input_value = int(message.text)
    previous_message = message.reply_to_message.text

    student_data = await extract_student_late_info(previous_message)
    
    if student_data:
        student = await Student.objects.aget(phone=student_data['phone'])
        student_attendance = await StudentAttendance.objects.aget(student=student)

        student_attendance.late = input_value
        await student_attendance.asave()

        await message.answer(
            f"""
            Время опоздания {input_value} минут успешно записано для студента {student_data['first_name'] + ' ' + student_data['last_name']} ({student_data['phone']})
            """
            )
    else:
        student_data = await extract_student_mark_info(previous_message)

        student = await Student.objects.aget(phone=student_data['phone'])
        student_task = await StudentTask.objects.aget(student=student)

        student_task.mark = input_value
        await student_task.asave()

        await message.answer(
            f"""
            Оценка за задание {input_value} баллов успешно записано для студента {student_data['first_name'] + ' ' + student_data['last_name']} ({student_data['phone']})
            """
            )



@education_router.callback_query(F.data.startswith("task_"))
async def task_view(
        callback: CallbackQuery,
) -> None:
    task_id = callback.data.split("task_")[1]
    task = await get_task_info_by_id(task_id)

    students_tasks = await get_students_tasks_by_lesson_task(task)

    await send_students_tasks(
        update_type=callback,
        students_tasks=students_tasks,
        students_tasks_keyboard=get_student_task_menu
                                 )


@attendance_router.callback_query(F.data.startswith("student_task_passed_status_"))
async def update_student_task_passed_status(
    callback: CallbackQuery,
) -> None:
    
    student_task_id = callback.data.split("student_task_passed_status_")[1]
    student_task = await StudentTask.objects.aget(id=student_task_id)

    student_task.passed = not student_task.passed

    if student_task.passed:
        await callback.answer("❌ Не сдал")
        student_task.passed = True
    else:
        await callback.answer("✅ сдал")
        student_task.passed = False

    await student_task.asave()

    updated_status = await get_student_task_menu(student_task=student_task)
    
    await callback.message.edit_reply_markup(
        reply_markup=updated_status
    )


@attendance_router.callback_query(F.data.startswith("student_task_mark_status_"))
async def update_student_task_mark_status(
    callback: CallbackQuery,
) -> None:
    
    student_task_id = callback.data.split("student_task_mark_status_")[1]
    student_task = await StudentTask.objects.aget(id=student_task_id)

    student_data = await get_student_data_by_task(student_task)

    student_name = (student_data['first_name'] + ' ' + student_data['last_name']).upper()
    student_phone = student_data['phone']

    menu_text = f"Укажите на сколько баллов получил студент {student_name} ({student_phone}):"
    menu_answer_text = 'Запись оценки'

    await callback.answer(menu_answer_text)
    
    await callback.message.answer(
        text=menu_text,
        parse_mode="HTML"
        )
    

# @attendance_router.message(F.text.regexp(r"^\d+$"))
# async def input_student_task_mark_status(
#     message: Message,
# ) -> None:
    
#     mark_points = int(message.text)
#     previous_message = message.reply_to_message.text
    
    # student_data = await extract_student_mark_info(previous_message)

    # student = await Student.objects.aget(phone=student_data['phone'])
    # student_task = await StudentTask.objects.aget(student=student)

    # student_task.mark = mark_points
    # await student_task.asave()

    # await message.answer(
    #     f"""
    #     Оценка за задание {mark_points} баллов успешно записано для студента {student_data['first_name'] + ' ' + student_data['last_name']} ({student_data['phone']})
    #     """
    #     )
