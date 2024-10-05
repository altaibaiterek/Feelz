from aiogram import Router, F

from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from django.db import IntegrityError

from apps.account.models import StudentGroup
from apps.bot.modules.managment.keyboards import back_to_group_button
from apps.bot.modules.managment.states import AddLessonFSM
from apps.education.models import Lesson, Task


managment_router = Router(name="Managment menu")


@managment_router.callback_query(F.data.startswith("add_lesson_to_group_"))
async def add_lesson_view(
        callback: CallbackQuery,
        state: FSMContext
) -> None:
    group_id = callback.data.split("add_lesson_to_group_")[1]

    await state.update_data(group_id=group_id)

    await callback.answer('📚 Добавление нового занятия')

    await callback.message.answer(
        '🔖 Пожалуйста, укажите *название урока*, которое вы хотите добавить для выбранной группы:'
    )

    await state.set_state(AddLessonFSM.waiting_for_lesson_name)


@managment_router.message(AddLessonFSM.waiting_for_lesson_name)
async def input_lesson_name(
    message: Message,
    state: FSMContext
) -> None:
    lesson_name = message.text

    await state.update_data(lesson_name=lesson_name)

    await message.answer(
        f'📋 Название урока *«{lesson_name}»* принято!\n\nТеперь укажите *описание урока* для студентов:'
    )

    await state.set_state(AddLessonFSM.waiting_for_lesson_description)


@managment_router.message(AddLessonFSM.waiting_for_lesson_description)
async def input_lesson_description(
    message: Message,
    state: FSMContext
) -> None:
    lesson_description = message.text

    await state.update_data(lesson_description=lesson_description)

    await message.answer(
        '📚 Описание урока успешно сохранено!\n\nТеперь укажите *слова или задание*, которое нужно будет выучить или выполнить:'
    )

    await state.set_state(AddLessonFSM.waiting_for_task)


@managment_router.message(AddLessonFSM.waiting_for_task)
async def input_lesson_task(
    message: Message,
    state: FSMContext
) -> None:
    task_body = message.text

    data = await state.get_data()
    lesson_name = data['lesson_name']
    lesson_description = data['lesson_description']
    group_id = data['group_id']

    try:
        group = await StudentGroup.objects.aget(id=group_id)

        lesson = Lesson(
            student_group=group,
            topic=lesson_name,
            body=lesson_description
        )
        await lesson.asave()

        task = Task(
            lesson=lesson,
            body=task_body
        )
        await task.asave()

        await message.answer(
            f"🎉 *Урок «{lesson_name}»* и задание успешно добавлены для группы *{group.name}*! \n\n"
            f"📖 _Описание урока:_\n{lesson_description}\n\n"
            f"📝 _Задание:_\n{task_body}\n\n"
            "✨ *Успех!* Урок доступен для студентов.",
            reply_markup=await back_to_group_button(group_id)
        )

    except StudentGroup.DoesNotExist:
        await message.answer(
            "❌ *Ошибка:* Группа с указанным ID не найдена. Пожалуйста, проверьте данные и попробуйте снова."
        )
    except IntegrityError:
        await message.answer(
            "❌ *Ошибка:* Не удалось добавить урок и задание. Пожалуйста, проверьте корректность данных."
        )

    await state.clear()
