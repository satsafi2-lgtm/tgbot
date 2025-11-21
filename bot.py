import re
import math
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import asyncio

TOKEN = "8368799810:AAEMT2V6potur9pwAcjm3pSjZPLhkUSwlGw"

bot = Bot(token=TOKEN)
dp = Dispatcher()


# ---------- ФУНКЦИЯ РЕШЕНИЯ КВ. УРАВНЕНИЯ ----------
def solve(a, b, c):
    solution = f"Уравнение: {a}x² + {b}x + {c} = 0\n\n"

    D = b*b - 4*a*c
    solution += f"Дискриминант: D = {b}² - 4·{a}·{c} = {D}\n\n"

    if D < 0:
        solution += "➡ Корней нет (D < 0)"
    elif D == 0:
        x = -b / (2*a)
        solution += f"➡ Один корень:\n x = {-b}/(2·{a}) = {x}"
    else:
        x1 = (-b + math.sqrt(D)) / (2*a)
        x2 = (-b - math.sqrt(D)) / (2*a)
        solution += (
            "➡ Два корня:\n"
            f"x₁ = (-{b} + √{D}) / (2·{a}) = {x1}\n"
            f"x₂ = (-{b} - √{D}) / (2·{a}) = {x2}"
        )

    return solution


# ---------- ПАРСИНГ УРАВНЕНИЯ ----------
def parse_equation(eq):
    eq = eq.replace(" ", "")
    eq = eq.replace("²", "**2")   # поддержка x²
    eq = eq.replace("^2", "**2")

    # Приводим к стандартному виду
    pattern = r"([+-]?\d*)x\*\*2([+-]?\d*)x([+-]?\d+)"
    match = re.match(pattern, eq)

    if not match:
        return None

    a, b, c = match.groups()

    def fix(v):
        if v in ["", "+"]: return 1
        if v == "-": return -1
        return int(v)

    return fix(a), fix(b), int(c)


# ---------- СТАРТ ----------
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "👋 Привет! Я бот для решения квадратных уравнений.\n\n"
        "Ты можешь писать:\n"
        "✔ полное уравнение: `2x²+5x-3`\n"
        "✔ или команду /solve чтобы вводить a, b, c по очереди\n\n"
        "Напиши уравнение:"
    )


# ---------- РЕШЕНИЕ УРАВНЕНИЯ ТЕКСТОМ ----------
@dp.message()
async def equation_message(message: types.Message):
    eq = message.text.lower()

    parsed = parse_equation(eq)
    if parsed is None:
        await message.answer("❗ Не понял уравнение. Пиши в виде: `2x²+5x-3`")
        return

    a, b, c = parsed
    answer = solve(a, b, c)
    await message.answer(answer)


# ---------- ЗАПУСК ----------
async def main():
    print("Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())