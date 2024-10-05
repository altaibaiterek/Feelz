# import re

# import datetime

# from typing import Union

# from asgiref.sync import sync_to_async

# from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup, CallbackQuery, Message

# from apps.account.models import StudentGroup

# from apps.education.models import Lesson, Attendance, Task

# from apps.progress.models import StudentAttendance, StudentTask


# ################################################################################################################


# async def send_fake_message_update_by_callback(callback, text):
#     fake_message = Message(
#         message_id=callback.message.message_id,
#         from_user=callback.from_user,
#         chat=callback.message.chat,
#         date=callback.message.date,
#         text=text
#     )
#     return fake_message


# async def get_info_answer(
#     update_type: Union[CallbackQuery, Message],
#     keyboard: Union[InlineKeyboardMarkup, ReplyKeyboardMarkup] = None,
#     answer_text: str = None,
#     callback_answer_text: str = None,
# ) -> None:

#     text = answer_text if answer_text else 'Нет информации'
#     callback_text = callback_answer_text if callback_answer_text else 'Нет информации'

#     if isinstance(update_type, CallbackQuery):
#         await update_type.answer(callback_text)
#         await update_type.message.answer(
#             text=text,
#             reply_markup=keyboard,
#         )
#     else:
#         await update_type.answer(
#             text=text,
#             reply_markup=keyboard,
#         )


# async def send_students_tasks(
#     update_type: CallbackQuery,
#     students_tasks: list,
#     students_tasks_keyboard
# ) -> None:

#     for student_task in students_tasks:
#         student = await get_student_obj_by_student_task(student_task)
#         student_text = student.first_name

#         await update_type.message.answer(
#             text=student_text,
#             reply_markup=await students_tasks_keyboard(student_task)
#         )


# async def send_lesson_attendance(
#     update_type: CallbackQuery,
#     students_attendance: list,
#     students_attendance_keyboard
# ) -> None:

#     await update_type.answer('Список студентов')

#     for student_attendance in students_attendance:
#         student = await get_student_by_attendance(student_attendance)
#         student_text = student.first_name

#         await update_type.message.answer(
#             text=student_text,
#             reply_markup=await students_attendance_keyboard(student_attendance)
#         )


# ################################################################################################################


# async def get_date_info():
#     current_date = datetime.datetime.today()
#     date_str = current_date.strftime('%d.%m.%Y')
#     day_of_week = current_date.strftime('%A')

#     return f"{date_str} {day_of_week.capitalize()}"


# async def extract_student_late_info(message):
#     pattern = r"🕒 Укажите, на сколько минут опоздал студент:\s*\*?\s*([A-Za-zА-Яа-яёЁ]+)\s+([A-Za-zА-Яа-яёЁ]+)\s+\(\+(\d{12})\)"
#     match = re.search(pattern, message)

#     if match:
#         first_name = match.group(1)
#         last_name = match.group(2)
#         phone = match.group(3)
#         return {
#             "first_name": first_name,
#             "last_name": last_name,
#             "phone": '+' + phone
#         }
    
#     return None


# async def extract_student_mark_info(message):
#     pattern = r"📝 Укажите, сколько баллов получил студент за задание:\s*\*?\s*([A-Za-zА-Яа-яёЁ]+)\s+([A-Za-zА-Яа-яёЁ]+)\s*\(\+(\d{12})\)"
#     match = re.search(pattern, message)

#     if match:
#         first_name = match.group(1)
#         last_name = match.group(2)
#         phone = match.group(3)
#         return {
#             "first_name": first_name,
#             "last_name": last_name,
#             "phone": '+' + phone
#         }
    
#     return None

        
# ################################################################################################################


# def get_or_create_student_attendance(
#     student,
#     attendance
# ):
#     student_attendance = StudentAttendance.objects.get_or_create(
#             student=student,
#             attendance=attendance
#             )
#     return student_attendance[0]


# def get_or_create_student_task(
#     student,
#     task
# ):
#     student_task = StudentTask.objects.get_or_create(
#             student=student,
#             task=task
#             )
#     return student_task[0]


# def get_or_create_students_attendance(attendance):
#     group = attendance.student_group
#     group_students = group.students.all()
    
#     students_attendance = []
#     for student in group_students:
#         students_attendance.append(
#             get_or_create_student_attendance(
#                 student=student, 
#                 attendance=attendance
#                 )
#             )
        
#     return students_attendance


# def get_or_create_students_tasks(task):
#     group = task.lesson.student_group
#     group_students = group.students.all()
    
#     students_tasks = []
#     for student in group_students:
#         students_tasks.append(
#             get_or_create_student_task(
#                 student=student, 
#                 task=task
#                 )
#             )
        
#     return students_tasks

