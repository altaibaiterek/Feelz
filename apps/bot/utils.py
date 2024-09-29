import re
import datetime
from typing import Union

from asgiref.sync import sync_to_async

from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup, CallbackQuery, Message

from apps.account.models import Student, StudentGroup
from apps.attendance.models import StudentAttendance
from apps.education.models import Lesson, Attendance


async def send_fake_message_update_by_callback(callback, text):
    fake_message = Message(
        message_id=callback.message.message_id,
        from_user=callback.from_user,
        chat=callback.message.chat,
        date=callback.message.date,
        text=text
    )
    return fake_message


async def get_date_info():
    current_date = datetime.datetime.today()
    date_str = current_date.strftime('%d.%m.%Y')
    day_of_week = current_date.strftime('%A')

    return f"{date_str} {day_of_week.capitalize()}"


async def get_info_answer(
    update_type: Union[CallbackQuery, Message],
    keyboard: Union[InlineKeyboardMarkup, ReplyKeyboardMarkup] = None,
    answer_text: str = None,
    callback_answer_text: str = None,
) -> None:

    text = answer_text if answer_text else 'Нет информации'
    callback_text = callback_answer_text if callback_answer_text else 'Нет информации'

    if isinstance(update_type, CallbackQuery):
        await update_type.answer(callback_text)
        await update_type.message.answer(
            text=text,
            reply_markup=keyboard,
        )
    else:
        await update_type.answer(
            text=text,
            reply_markup=keyboard,
        )


async def send_lesson_attendance(
    update_type: CallbackQuery,
    students_attendance: list,
    students_attendance_keyboard
) -> None:

    await update_type.answer('Список студентов')

    for student_attendance in students_attendance:
        student = await get_student_by_attendance(student_attendance)
        student_text = student.first_name

        await update_type.message.answer(
            text=student_text,
            reply_markup=await students_attendance_keyboard(student_attendance)
        )


async def send_attendance_late_menu(
    update_type: CallbackQuery,
    student_attendance,
) -> None:

    menu_text = 'Укажите на сколько опоздал студент'
    menu_answer_text = 'Опоздание'

    await update_type.answer(menu_answer_text)
    
    await update_type.message.answer(
        text=menu_text,
        )


    # for student_attendance in students_attendance:
    #     student = await get_student_by_attendance(student_attendance)
    #     student_text = student.first_name

    #     await update_type.message.answer(
    #         text=student_text,
    #         reply_markup=await students_attendance_keyboard(student_attendance)
    #     )


################################################################################################################
################################################################################################################
################################################################################################################


@sync_to_async
def get_student_groups():
    return list(StudentGroup.objects.all())


@sync_to_async
def get_student_group_by_id(student_group_id):
    return StudentGroup.objects.get(id=student_group_id)


@sync_to_async
def get_students_by_group_id(group_id):
    group = StudentGroup.objects.get(id=group_id)
    group_students = group.students.all()
    return list(group_students)


# @sync_to_async
def get_or_create_student_attendance(
    student,
    attendance
):
    student_attendance = StudentAttendance.objects.get_or_create(
            student=student,
            attendance=attendance
            )
    return student_attendance[0]


def get_or_create_students_attendance(attendance):
    group = attendance.student_group
    group_students = group.students.all()
    
    students_attendance = []
    for student in group_students:
        # student_attendance = StudentAttendance.objects.get_or_create(
        #     student=student,
        #     attendance=attendance
        #     )
        # students_attendance.append(student_attendance[0])
        students_attendance.append(get_or_create_student_attendance(student=student, attendance=attendance))
        

    return students_attendance


@sync_to_async
def get_students_attendance_by_lesson_attendance(attendance):
    students_attendance = get_or_create_students_attendance(attendance)
    return list(students_attendance)


@sync_to_async
def get_group_lessons(group_id):
    return list(Lesson.objects.filter(student_group=group_id))


@sync_to_async
def get_lesson_info_by_id(lesson_id):
    return Lesson.objects.get(id=lesson_id)


@sync_to_async
def get_attendance_info_by_id(attendance_id):
    return Attendance.objects.get(id=attendance_id)


@sync_to_async
def get_student_group_id_by_lesson(lesson):
    return lesson.student_group.id


@sync_to_async
def get_or_create_attendance_by_lesson(lesson, student_group_id):
    student_group = StudentGroup.objects.get(id=student_group_id)
    attendance = Attendance.objects.get_or_create(lesson=lesson, student_group=student_group)
    return attendance[0]


@sync_to_async
def get_student_by_attendance(student_attendance):
    # return Student.objects.get(attendance=student_attendance)
    return student_attendance.student


@sync_to_async
def get_student_data_by_attendance(student_attendance):
    return student_attendance.student.to_dict_data()


async def extract_student_info(message):
    pattern = r"Укажите на сколько минут опоздал студент (\w+)(?: (\w+))?(?: \(\+\d{12}\))?"
    match = re.search(pattern, message)

    if match:
        first_name = match.group(1)
        last_name = match.group(2) if match.group(2) else ""
        phone_pattern = r"(\(\+\d{12}\))"
        phone_match = re.search(phone_pattern, message)
        phone = phone_match.group(1).replace('(', '').replace(')', '') if phone_match else None
        return {"first_name": first_name, "last_name": last_name, "phone": phone}
    else:
        return None
