from enum import IntEnum, auto

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


class HabitsCBData(CallbackData, prefix="habits_choosing"):
    id: int
    name_habit: str


class OptionsDeleteUpdate(IntEnum):
    delete = auto()
    update = auto()
    root = auto()


class OptionsDoneNotCompleted(IntEnum):
    done = auto()
    not_completed = auto()


class DoneNotCompetedCBData(CallbackData, prefix="done_not_completed_habit"):
    action: OptionsDoneNotCompleted
    id: int


class DeleteUpdateCBData(CallbackData, prefix="delete_update"):
    action: OptionsDeleteUpdate
    id: int


def habits_kb(habits: list) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for habit in habits:
        builder.button(
            text=habit["name_habit"],
            callback_data=HabitsCBData(
                name_habit=habit["name_habit"], id=habit["id"]
            ).pack(),
        )
    builder.adjust(1)
    return builder.as_markup()


def update_or_delete_kb(idd: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="back to habits",
        callback_data=DeleteUpdateCBData(
            action=OptionsDeleteUpdate.root, id=idd
        ).pack(),
    )
    builder.button(
        text="update",
        callback_data=DeleteUpdateCBData(
            action=OptionsDeleteUpdate.update, id=idd
        ).pack(),
    )
    builder.button(
        text="delete",
        callback_data=DeleteUpdateCBData(
            action=OptionsDeleteUpdate.delete, id=idd
        ).pack(),
    )
    builder.adjust(1)
    return builder.as_markup()


def execute_or_back_kb(idd: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="back to habits",
        callback_data=DeleteUpdateCBData(
            action=OptionsDeleteUpdate.root, id=idd
        ).pack(),
    )
    builder.button(
        text="done",
        callback_data=DoneNotCompetedCBData(
            action=OptionsDoneNotCompleted.done, id=idd
        ).pack(),
    )
    builder.button(
        text="not completed",
        callback_data=DoneNotCompetedCBData(
            action=OptionsDoneNotCompleted.not_completed, id=idd
        ).pack(),
    )
    builder.adjust(1)
    return builder.as_markup()
