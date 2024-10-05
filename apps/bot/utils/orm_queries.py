# import re

# import datetime

# from typing import Union

# from asgiref.sync import sync_to_async

# from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup, CallbackQuery, Message

# from apps.account.models import StudentGroup

# from apps.education.models import Lesson, Attendance, Task

# from apps.progress.models import StudentAttendance, StudentTask


# @sync_to_async
# def get_student_groups():
#     return list(StudentGroup.objects.all())


# @sync_to_async
# def get_student_group_by_id(student_group_id):
#     return StudentGroup.objects.get(id=student_group_id)


# @sync_to_async
# def get_students_by_group_id(group_id):
#     group = StudentGroup.objects.get(id=group_id)
#     group_students = group.students.all()
#     return list(group_students)


# @sync_to_async
# def get_students_attendance_by_lesson_attendance(attendance):
#     students_attendance = get_or_create_students_attendance(attendance)
#     return list(students_attendance)


# @sync_to_async
# def get_students_tasks_by_lesson_task(lesson_task):
#     students_tasks = get_or_create_students_tasks(lesson_task)
#     return list(students_tasks)


# @sync_to_async
# def get_group_lessons(group_id):
#     return list(Lesson.objects.filter(student_group=group_id))


# @sync_to_async
# def get_lesson_info_by_id(lesson_id):
#     return Lesson.objects.get(id=lesson_id)


# @sync_to_async
# def get_attendance_info_by_id(attendance_id):
#     return Attendance.objects.get(id=attendance_id)


# @sync_to_async
# def get_task_info_by_id(task_id):
#     return Task.objects.get(id=task_id)


# @sync_to_async
# def get_student_group_id_by_lesson(lesson):
#     return lesson.student_group.id


# @sync_to_async
# def get_or_create_attendance_by_lesson(lesson, student_group_id):
#     student_group = StudentGroup.objects.get(id=student_group_id)
#     attendance = Attendance.objects.get_or_create(lesson=lesson, student_group=student_group)
#     return attendance[0]


# @sync_to_async
# def get_student_by_attendance(student_attendance):
#     return student_attendance.student


# @sync_to_async
# def get_student_obj_by_student_task(student_task):
#     return student_task.student


# @sync_to_async
# def get_student_data_by_attendance(student_attendance):
#     return student_attendance.student.to_dict_data()


# @sync_to_async
# def get_student_data_by_task(student_task):
#     return student_task.student.to_dict_data()


# @sync_to_async
# def get_lesson_data_by_task(task_id):
#     task = Task.objects.get(id=task_id)
#     lesson = task.lesson
#     return {'topic': lesson.topic, 'body': lesson.body, 'task_body': task.body}
