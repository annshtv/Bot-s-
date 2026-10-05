START_TEXT = {
    "beauty": "Добро пожаловать! Здесь вы можете посмотреть услуги, записаться и узнать контакты.",
    "cafe": "Добро пожаловать! Здесь вы можете посмотреть меню, забронировать столик и узнать контакты.",
    "manicure": "Добро пожаловать! Здесь вы можете посмотреть услуги и записаться на процедуру.",
    "courses": "Добро пожаловать! Здесь вы можете узнать о курсах, записаться на пробный урок и задать вопросы.",
}


def get_start_text(config):
    return START_TEXT.get(
        config.category,
        "Добро пожаловать! Выберите нужный раздел.",
    )


def get_services_text(config):
    if not config.services:
        return "Список услуг пока не добавлен."

    if config.category == "cafe":
        title = "Наше меню:"
    elif config.category == "courses":
        title = "Наши курсы:"
    else:
        title = "Наши услуги:"

    lines = [title]

    for service in config.services:
        lines.append(f"• {service.name} — {service.price} ₸")

    return "\n".join(lines)


def get_contacts_text(config):
    parts = ["Наши контакты:"]

    if config.hours:
        parts.append(f"🕐 График: {config.hours}")

    if config.address:
        parts.append(f"📍 Адрес: {config.address}")

    if config.channel:
        parts.append(f"💬 Telegram: {config.channel}")

    return "\n".join(parts)


def get_about_text(config):
    if config.description:
        return config.description

    return "Информация о бизнесе пока не добавлена."


def get_booking_text(config):
    if config.category == "cafe":
        return "Для бронирования столика свяжитесь с нами по указанным контактам."

    if config.category == "courses":
        return "Для записи на пробный урок свяжитесь с нами по указанным контактам."

    return "Для записи выберите удобное время и свяжитесь с нами."


def get_faq_text():
    return "Если у вас есть вопрос, напишите нам в сообщении."