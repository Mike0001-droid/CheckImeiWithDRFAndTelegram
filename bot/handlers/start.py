from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.types import Message
from decouple import config
from utils.imei_checker import check_imei

admins = [int(admin_id) for admin_id in config('ADMINS').split(',')]

start_router = Router()

@start_router.message(CommandStart())
async def start(message: Message):
    user_id = str(message.from_user.id)
    if message.from_user.id not in admins:
        return await message.answer(f"У вас нет доступа к боту. {user_id}")
    await message.answer("Отправьте IMEI для проверки.")

@start_router.message()
async def handle_imei(message: Message):
    if message.from_user.id not in admins:
        return await message.answer("У вас нет доступа к боту.")
    
    imei = message.text.strip()
    
    if not imei.isdigit() or len(imei) not in {14, 15}:
        return await message.answer("Некорректный IMEI. Попробуйте снова.")
    
    await message.answer("Проверяю IMEI, подождите...")

    response = await check_imei(imei)
    
    if response.get("status") == "successful":
        properties = response.get('properties', {})
        device_name = properties.get('deviceName', 'Неизвестное устройство')
        imei = properties.get('imei', 'Неизвестен')
        model_desc = properties.get('modelDesc', 'Неизвестная модель')
        purchase_country = properties.get('purchaseCountry', 'Неизвестная страна')
        sim_lock = "Да" if properties.get('simLock') else "Нет"
        image_url = properties.get('image', '')
        result_text = f"""
            - Результат проверки IMEI: {imei}
            - Модель устройства: {device_name}
            - IMEI: {imei}
            - Описание модели: {model_desc}
            - Страна покупки: {purchase_country}
            - SIM Lock: {sim_lock}
            Изображение устройства({image_url})
        """
    else:
        error = response.get('error', 'Неизвестная ошибка')
        result_text = f"Не удалось проверить IMEI. Причина: {error}"
    await message.answer(result_text)

