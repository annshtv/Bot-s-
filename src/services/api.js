const API_URL = "http://127.0.0.1:8000";

// Отправляет описание бизнеса backend
// и получает предложенную структуру бота
export async function generateStructure(description) {
    const response = await fetch(`${API_URL}/api/generate-structure`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            description: description,
        }),
    });

    if (!response.ok) {
        throw new Error("Failed to generate bot structure");
    }

    return response.json();
}


// Создаёт нового бота и сохраняет конфигурацию
export async function createBot(botData) {
    const response = await fetch(`${API_URL}/api/bots`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(botData),
    });

    if (!response.ok) {
        throw new Error("Failed to create bot");
    }

    return response.json();
}


// Получает сохранённого бота по id
export async function getBot(id) {
    const response = await fetch(`${API_URL}/api/bots/${id}`);

    if (!response.ok) {
        throw new Error("Failed to load bot");
    }

    return response.json();
}