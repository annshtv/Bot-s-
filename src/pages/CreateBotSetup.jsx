import { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { useCreateBot } from "../context/CreateBotContext.jsx";
import { createBot } from "../services/api.js";

const categoryNames = {
  beauty: "Beauty Studio",
  cafe: "Cafe",
  manicure: "Manicure Studio",
  courses: "Online Courses",
};

export default function CreateBotSetup() {
  const navigate = useNavigate();
  const location = useLocation();

  const {
    category,
    description,
    features,
    services,
    setServices,
    contacts,
    setContacts,
  } = useCreateBot();

  // Разделы, которые до этого сгенерировал backend
  const sections = location.state?.sections || [];

  // Telegram token от BotFather
  const [telegramToken, setTelegramToken] = useState("");

  // Состояние кнопки
  const [loading, setLoading] = useState(false);

  // Ошибка от backend
  const [error, setError] = useState("");


  function updateService(index, field, value) {
    setServices((prev) =>
      prev.map((s, i) =>
        i === index
          ? { ...s, [field]: value }
          : s
      )
    );
  }


  function addService() {
    setServices((prev) => [
      ...prev,
      {
        name: "Новая услуга",
        price: 0,
      },
    ]);
  }


  function updateContact(field, value) {
    setContacts((prev) => ({
      ...prev,
      [field]: value,
    }));
  }


  async function handleLaunch() {
    // Без token backend не сможет проверить Telegram-бота
    if (!telegramToken.trim()) {
      setError("Введите Telegram token от BotFather.");
      return;
    }

    setLoading(true);
    setError("");

    try {
      // Получаем только включённые функции
      const enabledFeatures = Object.entries(features)
        .filter(([, feature]) => feature.enabled)
        .map(([key]) => key);

      // Формируем объект точно под наш FastAPI BotConfig
      const botData = {
        business_name:
          categoryNames[category] || "My Business",

        description: description,

        language: "ru",

        features: enabledFeatures,

        services: services.map((service) => ({
          name: service.name,
          price: Number(service.price),
        })),

        phone: "",

        address: contacts.address || "",

        working_hours: contacts.hours || "",

        telegram_token: telegramToken,

        // Backend сам получит username через Telegram getMe
        telegram_username: "",

        sections: sections,
      };

      // Отправляем всё в FastAPI
      const result = await createBot(botData);

      localStorage.setItem("lastBotId", result.id);

      console.log("Bot created:", result);

      // После успешного создания переходим в "Мои боты"
      // и передаём туда настоящий id и username
      navigate("/bots", {
        state: {
          botId: result.id,
          telegramUsername: result.telegram_username,
        },
      });

    } catch (err) {
      console.error(err);

      setError(
        "Не удалось создать бота. Проверьте Telegram token и работу backend."
      );

    } finally {
      setLoading(false);
    }
  }


  return (
    <div>
      <p className="mb-4 text-sm text-gray-400">
        Создать бота /{" "}
        <span className="text-gray-600">
          Настройка
        </span>
      </p>


      <div className="grid max-w-4xl grid-cols-1 gap-6 md:grid-cols-2">

        {/* УСЛУГИ */}
        <div className="rounded-xl2 bg-white p-8 shadow-sm">

          <h2 className="font-display text-xl font-bold text-navy-950">
            Услуги и цены
          </h2>


          <div className="mt-4 divide-y divide-gray-100">

            {services.map((service, i) => (
              <div
                key={i}
                className="flex items-center gap-3 py-3"
              >

                <input
                  value={service.name}

                  onChange={(e) =>
                    updateService(
                      i,
                      "name",
                      e.target.value
                    )
                  }

                  className="flex-1 bg-transparent text-sm text-navy-950 outline-none"
                />


                <input
                  type="number"

                  value={service.price}

                  onChange={(e) =>
                    updateService(
                      i,
                      "price",
                      Number(e.target.value)
                    )
                  }

                  className="w-24 bg-transparent text-right text-sm text-gray-500 outline-none"
                />


                <span className="text-sm text-gray-400">
                  ₸
                </span>

              </div>
            ))}

          </div>


          <button
            onClick={addService}

            className="mt-3 text-sm font-medium text-accent-600 hover:underline"
          >
            + Добавить услугу
          </button>

        </div>


        {/* КОНТАКТЫ */}
        <div className="rounded-xl2 bg-white p-8 shadow-sm">

          <h2 className="font-display text-xl font-bold text-navy-950">
            Контакты и график
          </h2>


          <div className="mt-4 flex flex-col gap-4">

            <Field
              label="Часы работы"

              value={contacts.hours}

              onChange={(v) =>
                updateContact("hours", v)
              }
            />


            <Field
              label="Адрес"

              value={contacts.address}

              placeholder="Алматы, ул. Достык 12"

              onChange={(v) =>
                updateContact("address", v)
              }
            />


            <Field
              label="Telegram-канал"

              value={contacts.channel}

              placeholder="@salon_beauty_bot"

              onChange={(v) =>
                updateContact("channel", v)
              }
            />


            {/* Реальный token для подключения Telegram */}
            <label className="block">

              <span className="mb-1 block text-xs text-gray-400">
                Telegram token
              </span>

              <input
                type="password"

                value={telegramToken}

                placeholder="Token от BotFather"

                onChange={(e) =>
                  setTelegramToken(e.target.value)
                }

                className="w-full rounded-lg bg-gray-50 px-4 py-2.5 text-sm text-navy-950 outline-none ring-1 ring-gray-200 focus:ring-accent-500"
              />

            </label>

          </div>

        </div>

      </div>


      {/* Ошибка */}
      {error && (
        <p className="mt-4 max-w-4xl text-sm text-red-500">
          {error}
        </p>
      )}


      <div className="mt-6 flex max-w-4xl justify-between">

        <button
          onClick={() =>
            navigate("/create/structure", {
              state: {
                sections: sections,
              },
            })
          }

          className="rounded-lg border border-gray-300 px-5 py-2.5 text-sm font-semibold text-navy-950 hover:bg-white"
        >
          Назад
        </button>


        <button
          onClick={handleLaunch}

          disabled={loading}

          className="rounded-lg bg-navy-950 px-5 py-2.5 text-sm font-semibold text-white hover:bg-navy-900 disabled:cursor-not-allowed disabled:opacity-50"
        >
          {loading
            ? "Сохраняем..."
            : "Сохранить и запустить"}
        </button>

      </div>

    </div>
  );
}


function Field({
  label,
  value,
  onChange,
  placeholder,
}) {
  return (
    <label className="block">

      <span className="mb-1 block text-xs text-gray-400">
        {label}
      </span>

      <input
        value={value}

        placeholder={placeholder}

        onChange={(e) =>
          onChange(e.target.value)
        }

        className="w-full rounded-lg bg-gray-50 px-4 py-2.5 text-sm text-navy-950 outline-none ring-1 ring-gray-200 focus:ring-accent-500"
      />

    </label>
  );
}