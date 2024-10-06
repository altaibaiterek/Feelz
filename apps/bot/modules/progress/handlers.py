from aiogram import Router, F

from aiogram.types import CallbackQuery, Message

from apps.account.models import Student

from apps.bot.modules.progress.keyboards import get_student_attendance_menu, get_student_task_menu, return_lesson_menu
from apps.bot.utils.orm_queries import get_attendance_data_by_student_attendance, get_attendance_info_by_id, get_lesson_data_by_attendance, get_lesson_data_by_task, get_lesson_id_by_task, get_student_data_by_attendance, get_student_data_by_task, get_students_attendance_by_lesson_attendance, get_students_tasks_by_lesson_task, get_task_data_by_student_task, get_task_info_by_id
from apps.bot.utils.utils import escape_markdown, extract_student_late_info, extract_student_mark_info, send_lesson_attendance, send_students_tasks
from apps.education.models import Attendance, Task
from apps.progress.models import StudentAttendance, StudentTask


progress_router = Router(name="progress_router info")


@progress_router.message(F.text.regexp(r"^\d+$") & F.reply_to_message)
async def input_student_info_status(
    message: Message,
) -> None:
    
    input_value = int(message.text)
    previous_message = message.reply_to_message.text
    
    try:
        student_data = await extract_student_late_info(previous_message)
        student = await Student.objects.aget(phone_number=student_data['phone_number'])
        attendance = await Attendance.objects.aget(id=student_data['attendance_id'])
        student_attendance = await StudentAttendance.objects.aget(student=student, attendance=attendance)

        student_attendance.late = input_value
        await student_attendance.asave()

        lesson_data = await get_lesson_data_by_attendance(attendance)

        await message.answer(
            f"""
🎉 *Опоздание в «{input_value}» минут успешно занесено в журнал!*

✅ *Действие:* Перекличка

👨‍🎓 *Студент:* {student_data['first_name']} {student_data['last_name']}  
📞 *Телефон:* {student_data['phone_number']}

📘 *Спасибо за внимательность!*
            """,
            reply_markup=await return_lesson_menu(lesson_data['id'])
        )
    except Exception as e:
        student_data = await extract_student_mark_info(previous_message)
        student = await Student.objects.aget(phone_number=student_data['phone_number'])
        task = await Task.objects.aget(id=student_data['task_id'])
        student_task = await StudentTask.objects.aget(student=student, task=task)

        student_task.mark = input_value
        await student_task.asave()

        lesson_id = await get_lesson_id_by_task(task)

        await message.answer(
            f"""
🎉 *Оценка в «{input_value}» балл успешно занесена в журнал!*

✅ *Действие:* Оценка задания

👨‍🎓 *Студент:* {student_data['first_name']} {student_data['last_name']}  
📞 *Телефон:* {student_data['phone_number']}

📘 *Благодарим за вашу работу!*
            """,
            reply_markup=await return_lesson_menu(lesson_id)
        )


################################################################################################################
################################################################################################################
################################################################################################################


@progress_router.callback_query(F.data.startswith("task_"))
async def task_view(
        callback: CallbackQuery,
) -> None:
    
    task_id = callback.data.split("task_")[1]
    task = await get_task_info_by_id(task_id)

    lesson_data = await get_lesson_data_by_task(task_id)
    task_lesson_name = escape_markdown(lesson_data['topic'])
    task_body = escape_markdown(task.body)

    callback_answer_text = task_lesson_name
    answer_text = f"""
📝 *Задание на уроке:* {task_lesson_name}

📖 *Описание задания:*
{task_body}

✨ *Пожалуйста, ознакомьтесь с заданием и выполните его в срок!*
"""
    
    await callback.answer(callback_answer_text)
    await callback.message.answer(answer_text)

    students_tasks = await get_students_tasks_by_lesson_task(task)

    await send_students_tasks(
        update_type=callback,
        students_tasks=students_tasks,
        students_tasks_keyboard=get_student_task_menu
    )



@progress_router.callback_query(F.data.startswith("student_task_passed_status_"))
async def update_student_task_passed_status(
    callback: CallbackQuery,
) -> None:
    
    student_task_id = callback.data.split("student_task_passed_status_")[1]
    student_task = await StudentTask.objects.aget(id=student_task_id)

    student_task.passed = not student_task.passed

    if student_task.passed:
        await callback.answer("✅ Студент сдал задание.")
        student_task.passed = True
    else:
        await callback.answer("❌ Студент не сдал задание.")
        student_task.passed = False

    await student_task.asave()

    updated_status = await get_student_task_menu(student_task=student_task)
    
    await callback.message.edit_reply_markup(
        reply_markup=updated_status
    )


@progress_router.callback_query(F.data.startswith("student_task_mark_status_"))
async def update_student_task_mark_status(
    callback: CallbackQuery,
) -> None:
    
    student_task_id = callback.data.split("student_task_mark_status_")[1]
    student_task = await StudentTask.objects.aget(id=student_task_id)

    student_data = await get_student_data_by_task(student_task)
    task_data = await get_task_data_by_student_task(student_task)

    student_name = (student_data['first_name'] + ' ' + student_data['last_name']).upper()
    student_phone = student_data['phone_number']

    menu_text = f"""
*Задние №{task_data['id']}: {task_data['body']}*
📝 *Укажите, сколько баллов получил студент за задание:*

*{student_name} ({student_phone})*
"""
    menu_answer_text = '✍️ Запись оценки'

    await callback.answer(menu_answer_text)
    
    await callback.message.answer(
        text=menu_text,
    )


################################################################################################################
################################################################################################################
################################################################################################################


@progress_router.callback_query(F.data.startswith("attendance_"))
async def attendance_view(
        callback: CallbackQuery,
) -> None:
    attendance_id = callback.data.split("attendance_")[1]
    attendance = await get_attendance_info_by_id(attendance_id)

    students_attendance = await get_students_attendance_by_lesson_attendance(attendance)

    await send_lesson_attendance(
        update_type=callback,
        students_attendance=students_attendance,
        attendance_id=attendance_id,
        students_attendance_keyboard=get_student_attendance_menu
    )


@progress_router.callback_query(F.data.startswith("student_attendance_skipped_status_"))
async def update_student_attendance_skipped_status(
    callback: CallbackQuery,
) -> None:
    
    student_attendance_id = callback.data.split("student_attendance_skipped_status_")[1].split('_')[0]
    student_attendance = await StudentAttendance.objects.aget(id=student_attendance_id)

    student_attendance.skipped = not student_attendance.skipped

    if student_attendance.skipped:
        await callback.answer("✅ Студент присутствовал на занятии.")
        student_attendance.skipped = True
    else:
        await callback.answer("❌ Студент не был на занятии.")
        student_attendance.skipped = False

    await student_attendance.asave()

    attendance_data = await get_attendance_data_by_student_attendance(student_attendance)

    updated_status = await get_student_attendance_menu(
        student_attendance=student_attendance,
        attendance_id=attendance_data['id']
                                                       )
    
    await callback.message.edit_reply_markup(
        reply_markup=updated_status
    )


@progress_router.callback_query(F.data.startswith("student_attendance_late_status_"))
async def update_student_attendance_late_status(
    callback: CallbackQuery,
) -> None:
    
    student_attendance_id = callback.data.split("student_attendance_late_status_")[1].split('_')[0]
    attendance_id = callback.data.split("student_attendance_late_status_")[1].split('_')[1]
    
    student_attendance = await StudentAttendance.objects.aget(id=student_attendance_id, attendance=attendance_id)
    attendance = await Attendance.objects.aget(id=attendance_id)
    attendance_lesson = await get_lesson_data_by_attendance(attendance)
    student_data = await get_student_data_by_attendance(student_attendance)

    student_name = (student_data['first_name'] + ' ' + student_data['last_name']).upper()
    student_phone = student_data['phone_number']

    menu_text = f"""
*Урок №{attendance_id}: {attendance_lesson['topic']}*
🕒 *Укажите, на сколько минут опоздал студент:*

*{student_name} ({student_phone})*
"""
    menu_answer_text = '✍️ Запись опоздания'

    await callback.answer(menu_answer_text)
    
    await callback.message.answer(
        text=menu_text,
    )
