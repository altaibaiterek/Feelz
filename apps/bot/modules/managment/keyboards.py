from aiogram.utils.keyboard import InlineKeyboardBuilder

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def back_to_group_button(
    student_group_id,
) -> InlineKeyboardMarkup:

    keyboard = InlineKeyboardBuilder()

    keyboard.add(
        InlineKeyboardButton(
            text="🔙 Назад к группе",
            callback_data=f"student_group_{student_group_id}",
        )
    )

    return keyboard.adjust(1).as_markup()

