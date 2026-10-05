import { useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { useCreateBot } from "../context/CreateBotContext.jsx";

export default function CreateBotStructure() {
  const navigate = useNavigate();

  // Получаем данные, которые пришли с предыдущей страницы
  const location = useLocation();

  const { description, features, toggleFeature } = useCreateBot();

  // sections пришли от FastAPI через navigate()
  const generatedSections = location.state?.sections || [];

  useEffect(() => {
    // Если пользователь попал сюда без описания бизнеса,
    // возвращаем его на предыдущий экран
    if (!description.trim()) {
      navigate("/create/describe", { replace: true });
    }
  }, [description, navigate]);

  return (
    <div>
      <p className="mb-4 text-sm text-gray-400">
        Создать бота / <span className="text-gray-600">Структура</span>
      </p>

      <div className="max-w-2xl rounded-xl2 bg-white p-8 shadow-sm">
        <h1 className="font-display text-2xl font-bold text-navy-950">
          Структура бота готова
        </h1>

        <p className="mt-1 text-sm text-gray-500">
          Backend предложил структуру на основе описания вашего бизнеса
        </p>

        {/* Результат, который реально пришёл от FastAPI */}
        {generatedSections.length > 0 && (
          <div className="mt-5">
            <p className="mb-2 text-sm font-medium text-navy-950">
              Предложенные разделы:
            </p>

            <div className="flex flex-wrap gap-2">
              {generatedSections.map((section) => (
                <span
                  key={section}
                  className="rounded-full bg-accent-500/10 px-3 py-1.5 text-sm font-medium text-accent-600"
                >
                  {section}
                </span>
              ))}
            </div>
          </div>
        )}

        <p className="mt-6 text-sm text-gray-500">
          Включите или выключите функции перед настройкой
        </p>

        <div className="mt-4 grid grid-cols-1 gap-3 sm:grid-cols-2">
          {Object.entries(features).map(([key, feature]) => (
            <label
              key={key}
              className="flex items-center justify-between rounded-lg bg-gray-50 px-4 py-3"
            >
              <span>
                <span className="block text-sm font-medium text-navy-950">
                  {feature.label}
                </span>

                <span className="block text-xs text-gray-400">
                  {feature.hint}
                </span>
              </span>

              <input
                type="checkbox"
                checked={feature.enabled}
                onChange={() => toggleFeature(key)}
                className="relative h-5 w-9 cursor-pointer appearance-none rounded-full bg-gray-300 transition-colors before:absolute before:left-0.5 before:top-0.5 before:h-4 before:w-4 before:rounded-full before:bg-white before:transition-transform checked:bg-accent-500 checked:before:translate-x-4"
              />
            </label>
          ))}
        </div>

        <div className="mt-8 flex justify-between">
          <button
            onClick={() => navigate("/create/describe")}
            className="rounded-lg border border-gray-300 px-5 py-2.5 text-sm font-semibold text-navy-950 hover:bg-gray-50"
          >
            Назад
          </button>

          <button
            onClick={() =>
              navigate("/create/setup", {
                state: {
                  sections: generatedSections,
                },
              })
            }
            className="rounded-lg bg-navy-950 px-5 py-2.5 text-sm font-semibold text-white hover:bg-navy-900"
          >
            Настроить бота
          </button>
        </div>
      </div>
    </div>
  );
}