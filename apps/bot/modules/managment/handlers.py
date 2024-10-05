from aiogram import Router, F

from aiogram.types import CallbackQuery, Message


managment_router = Router(name="Managment menu")


@managment_router.callback_query(F.data.startswith("add_lesson_to_group_"))
async def add_lesson_view(
        callback: CallbackQuery,
) -> None:

    group_id = callback.data.split("add_lesson_to_group_")[1]


    await callback.message.answer('test add lesson')

#     student_group = await get_student_group_by_id(student_group_id)

#     callback_answer_text = student_group.name

#     answer_text = f"""
# 👥 *Выбранная группа:* {student_group.name}

# 📖 *Описание группы:*
# {student_group.description if student_group.description else 'Нет доступной информации.'}

# ✨ *Пожалуйста, выберите урок для получения дальнейшей информации:*
# """

#     await get_info_answer(
#         update_type=callback,
#         answer_text=answer_text,
#         callback_answer_text=callback_answer_text,
#         keyboard=await get_group_lessons_list(student_group_id),
#     )

