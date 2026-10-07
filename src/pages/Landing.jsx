import { Link } from "react-router-dom";
import Logo from "../components/Logo.jsx";

export default function Landing() {
  return (
    <div className="min-h-screen bg-canvas">
      <header className="flex items-center justify-between gap-4 border-b border-gray-200 bg-white px-4 py-3 md:px-10 md:py-4">
        <Logo />
        <nav className="flex items-center gap-4 text-sm font-medium text-gray-600 md:gap-8">
          <a href="#features" className="hidden hover:text-navy-950 md:inline">
            Возможности
          </a>
           <a href="#pricing" className="hidden hover:text-navy-950 md:inline">
            Цены
          </a>
          <Link to="/overview" className="hover:text-navy-950">
            Войти
          </Link>
          <Link
            to="/create/describe"
            className="hidden rounded-lg bg-navy-950 px-4 py-2 text-white transition-colors hover:bg-navy-900 sm:inline-block"
          >
            Начать бесплатно
          </Link>
        </nav>
      </header>

      <section className="mx-auto grid max-w-6xl grid-cols-1 items-center gap-10 px-4 py-12 md:grid-cols-2 md:gap-16 md:px-10 md:py-24">
        <div>
          <h1 className="font-display text-4xl font-extrabold leading-tight md:text-5xl text-navy-950">
            От идеи до Telegram-бота за 5 минут
          </h1>
          <p className="mt-6 max-w-md text-gray-500">
            Опишите бизнес обычным текстом — платформа сама соберёт структуру
            бота. Без программиста и лишних затрат.
          </p>
         <div className="mt-8 flex flex-col gap-3 sm:flex-row">
            <Link
              to="/create/describe"
              className="rounded-lg bg-navy-950 px-5 py-3 text-sm font-semibold text-white text-center transition-colors hover:bg-navy-900"
            >
              Создать бота
            </Link>
            <a
              href="#features"
              className="rounded-lg border border-gray-300 px-5 py-3 text-sm font-semibold  text-center text-navy-950 hover:bg-white"
            >
              Как это работает
            </a>
          </div>
        </div>

        <div className="rounded-xl2 bg-white p-5 shadow-sm md:p-6">
          <p className="mb-3 text-xs font-medium text-gray-400">Пример</p>
          <div className="mb-3 ml-auto max-w-[85%] rounded-xl bg-[#1D6FA5] px-4 py-3 text-sm text-white">
  У меня салон красоты. Нужен бот для записи и напоминаний.
</div>

          <div className="max-w-[85%] rounded-xl bg-gray-100 px-4 py-3 text-sm text-navy-950">
            Готово: запись клиентов, каталог услуг, напоминания и ответы на
            частые вопросы.
          </div>
        </div>
      </section>
    </div>
  );
}
