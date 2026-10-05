from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def main_keyboard(config):
    buttons = []

    if config.category == "cafe":
        if config.features.get("catalog", True):
            buttons.append(
                [
                    InlineKeyboardButton(
                        text="Меню",
                        callback_data="services",
                    )
                ]
            )

        if config.features.get("booking", True):
            buttons.append(
                [
                    InlineKeyboardButton(
                        text="Забронировать",
                        callback_data="booking",
                    )
                ]
            )

    elif config.category == "courses":
        if config.features.get("catalog", True):
            buttons.append(
                [
                    InlineKeyboardButton(
                        text="Курсы",
                        callback_data="services",
                    )
                ]
            )

        if config.features.get("booking", True):
            buttons.append(
                [
                    InlineKeyboardButton(
                        text="Записаться",
                        callback_data="booking",
                    )
                ]
            )

    else:
        if config.features.get("catalog", True):
            buttons.append(
                [
                    InlineKeyboardButton(
                        text="Услуги",
                        callback_data="services",
                    )
                ]
            )

        if config.features.get("booking", True):
            buttons.append(
                [
                    InlineKeyboardButton(
                        text="Записаться",
                        callback_data="booking",
                    )
                ]
            )

    if config.features.get("faq", True):
        buttons.append(
            [
                InlineKeyboardButton(
                    text="Частые вопросы",
                    callback_data="faq",
                )
            ]
        )

    buttons.append(
        [
            InlineKeyboardButton(
                text="Контакты",
                callback_data="contacts",
            )
        ]
    )

    buttons.append(
        [
            InlineKeyboardButton(
                text="О нас",
                callback_data="about",
            )
        ]
    )

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def back_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Главное меню",
                    callback_data="main_menu",
                )
            ]
        ]
    )