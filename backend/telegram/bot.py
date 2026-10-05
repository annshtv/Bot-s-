import asyncio

from aiogram import Bot, Dispatcher

from .handlers import create_router
from .models import BotConfig, Service


async def run_bot(config: BotConfig):
    bot = Bot(token=config.token)
    dispatcher = Dispatcher()

    dispatcher.include_router(create_router(config))

    try:
        await dispatcher.start_polling(bot)
    finally:
        await bot.session.close()


def create_demo_config(token: str):
    return BotConfig(
        token=token,
        business_name="Beauty Studio",
        description="Салон красоты с услугами для ухода за собой.",
        category="beauty",
        features={
            "booking": True,
            "catalog": True,
            "reminders": True,
            "faq": True,
            "payments": False,
            "reviews": False,
        },
        services=[
            Service("Стрижка", 5000),
            Service("Маникюр", 4000),
            Service("Окрашивание", 12000),
        ],
        hours="Пн–Сб, 10:00–20:00",
        address="Алматы",
        channel="@beauty_studio",
    )


if __name__ == "__main__":
    token = input("Введите Telegram Bot Token: ").strip()
    config = create_demo_config(token)
    asyncio.run(run_bot(config))