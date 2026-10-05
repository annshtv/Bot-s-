from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

from .keyboards import main_keyboard, back_keyboard
from .templates import (
    get_start_text,
    get_services_text,
    get_contacts_text,
    get_about_text,
    get_booking_text,
    get_faq_text,
)


def create_router(config):
    router = Router()

    @router.message(CommandStart())
    async def start_handler(message: Message):
        await message.answer(
            get_start_text(config),
            reply_markup=main_keyboard(config),
        )

    @router.callback_query(F.data == "services")
    async def services_handler(callback: CallbackQuery):
        await callback.message.edit_text(
            get_services_text(config),
            reply_markup=back_keyboard(),
        )
        await callback.answer()

    @router.callback_query(F.data == "booking")
    async def booking_handler(callback: CallbackQuery):
        await callback.message.edit_text(
            get_booking_text(config),
            reply_markup=back_keyboard(),
        )
        await callback.answer()

    @router.callback_query(F.data == "contacts")
    async def contacts_handler(callback: CallbackQuery):
        await callback.message.edit_text(
            get_contacts_text(config),
            reply_markup=back_keyboard(),
        )
        await callback.answer()

    @router.callback_query(F.data == "about")
    async def about_handler(callback: CallbackQuery):
        await callback.message.edit_text(
            get_about_text(config),
            reply_markup=back_keyboard(),
        )
        await callback.answer()

    @router.callback_query(F.data == "faq")
    async def faq_handler(callback: CallbackQuery):
        await callback.message.edit_text(
            get_faq_text(),
            reply_markup=back_keyboard(),
        )
        await callback.answer()

    @router.callback_query(F.data == "main_menu")
    async def main_menu_handler(callback: CallbackQuery):
        await callback.message.edit_text(
            get_start_text(config),
            reply_markup=main_keyboard(config),
        )
        await callback.answer()

    return router