from pyrogram import Client, filters
from pyrogram.errors import BotBlocked,UserDeactivated
import asyncio
from datetime import datetime, timedelta
from sqlalchemy import create_engine


# Информация о таблице базы данных
db_table = "users"
db_fields = ["id","created_at", "status", "status_updated_at"]

# Создание клиента Pyrogram
app = Client("webinar_bot", api_id="YOUR_API_ID", api_hash="YOUR_API_HASH")

# Функция для отправки сообщения клиенту
async def send_message(user_id, text):
    try:
        await app.send_message(user_id, text)
    except (BotBlocked, UserDeactivated):
        # Обработка ошибок связанных с заблокированными или деактивированными пользователями
        print(f"Ошибка при отправке сообщения пользователю {user_id}.")
        # Обновляем статус пользователя в базе данных
        update_user_status(user_id, "dead")

# Функция для обновления статуса пользователя в базе данных
def update_user_status(user_id, status):
    # Обновляем статус пользователя и время обновления

    app.send_chat_action(user_id, "typing")  # Отправляем действие "набирает текст"

    app.update_profile(status=status)  # Обновляем статус пользователя

    current_time = datetime.datetime.now().strftime("%H:%M:%S")  # Получаем текущее время
    print(f"Статус пользователя обновлен в {current_time}")

    update_user_status(user_id, "Новый статус пользователя")

    # Вам нужно подключиться к базе данных и выполнить соответствующие запросы
    engine = create_engine('database://username:password@hostname/database_name')
    # Replace 'database://username:password@hostname/database_name' with your database information
    
    # Ниже приведён пример использования SQLAlchemy
    # update_query = f"UPDATE {db_table} SET status = 'status', status_updated_at = '{datetime.now()}' WHERE id = {user_id}"
    # db_connection.execute(update_query)

# Функция для проверки, является ли сообщение триггером для отмены отправки
def is_cancel_trigger(text):
    # Проверяем наличие слов "прекрасно" или "ожидать" в сообщении
    return "прекрасно" in text or "ожидать" in text 

# Функция для обработки воронки
async def handler_funnel():
    while True:
        # Получаем список готовых для получения сообщений пользователей из базы данных
        messages = await get_ready_messages()
        
        # Вам нужно подключиться к базе данных и выполнить соответствующие запросы
        # Replace 'database://username:password@hostname/database_name' with your database information
        engine = create_engine('database://username:password@hostname/database_name')
        # Ниже приведён пример использования SQLAlchemy
        # select_query = f"SELECT id FROM {db_table} WHERE status = 'alive'"
        # result = db_connection.execute(select_query)
        # users = rusult.fetchall()
        users = [1, 2, 3, 4] # Пример списка пользователей, полученных из базы данных

        for user in users:
            user_id = user[0]

            # Отправляем первое сообщение "Текст1"
            await send_message(user_id, "Текст1")

            # Обновляем статус пользователя в базе данных
            update_user_status(user_id, "blocked")

            # Проверяем, является ли сообщение триггером для отмены отправки
            if is_cancel_trigger("Текст2"):

                # Обновляем статус пользователя в базе данных
                update_user_status(user_id, "finished")
                continue

                # Ожидаем указанное время перед отправкой следующего сообщения (39 минут)
                await asyncio.sleep(39 * 60)

                # Отправляем второе сообщение "Текст2"
                await send_massage(user_id, "Текст2")

                # Обновляем статус пользователя в базе данных 
                update_user_status(user_id, " finished")

                # Проверяем, является ли сообщение триггером для отправки
                if is_cancel_trigger("Текст3"):
                    continue

                # Ожидаем указанное время перед отправкой следующего сообщения (1 день 2 часа)
                await asyncio.sleep(26 * 60 * 60)

                # Отпраляем третье сообщение "Текст3"
                await send_massage(user_id, "Текст3")
                # Обновляем статус пользователя в базе данных
                update_user_status(user_id, "finished")

                # Ожидаем указанное время перед повторной проверкой готовых пользователей (например, 10 минут)
                await asyncio.sleep(10 * 60)

# Запускаем воронку вебинара 
async def start_funnel():
    while True:
        # Запускаем воронку вебинара
        await handler_funnel()

# Запускаем клиента Pyrogram и начинаем воронку 
with app:
    asyncio.run(start_funnel())                            
