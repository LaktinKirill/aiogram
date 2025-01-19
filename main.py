import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from config import TOKEN, OPENWEATHER_API_KEY, CITY
import requests


bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("weather"))
async def get_weather(message: types.Message):
    try:
        
        url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={OPENWEATHER_API_KEY}&units=metric&lang=ru"
        
        
        response = requests.get(url)
        data = response.json()
        
        
        temperature = data['main']['temp']
        description = data['weather'][0]['description']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']
        
        
        weather_message = (
            f"Сейчас погода в Кирове:\n"
            f" Температура: {temperature}°C\n"
            f" Состояние: {description}\n"
            f" Влажность: {humidity}%\n"
            f" Скорость ветра: {wind_speed} м/с"
        )
        
        # Отправляем сообщение
        await message.answer(weather_message)
        
    except Exception as e:
        await message.answer("Извините, произошла ошибка при получении данных о погоде.")
        print(f"Ошибка: {e}")

@dp.message(Command('help'))
async def help(message: Message):
    await message.answer('Этот бот умеет выполняить команды: \n /start, \n /help, \n /weather')

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer('Привет, я бот, который знает все о погоде в г. Киров!')


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())

