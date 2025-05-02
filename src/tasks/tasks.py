import asyncio
from time import sleep
from PIL import Image
import os

from src.database import async_session_maker_null_pool
from src.tasks.celery_app import celery_instance
from src.utils.db_manager import DBManager


@celery_instance.task
def test_tasks():
    sleep(5)
    print("Я сделал!")


@celery_instance.task
def resize_image(input_path: str, output_dir="src/static/images"):
    try:
        # Открываем изображение
        with Image.open(input_path) as img:
            # Создаем директорию, если она не существует
            os.makedirs(output_dir, exist_ok=True)

            # Получаем имя файла без расширения
            filename = os.path.splitext(os.path.basename(input_path))[0]

            # Размеры для сжатия
            sizes = {"1000": 1000, "500": 500, "200": 200}

            # Обрабатываем каждыи размер
            for name, width in sizes.items():
                # Вычисляем новую высоту, сохраняя пропорции
                w_percent = width / float(img.size[0])
                height = int(float(img.size[1]) * float(w_percent))

                # Изменяем размер изображения
                resized_img = img.resize((width, height), Image.LANCZOS)

                # Формируем имя выходного файла
                output_path = os.path.join(output_dir, f"{filename}_{name}.jpg")

                # Сохраняем сжатое изображение в формате JPEG с качеством 85%
                resized_img.save(output_path, "JPEG", quality=85)

            print(f"Изображения успешно сохранены в {output_dir}")

    except Exception as e:
        print(f"Ошибка при обработке изображения: {e}")


async def get_bookings_with_today_checkin_helper():
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        bookings = await db.bookings.get_bookings_with_checkin()
        print(f"{bookings}")


@celery_instance.task(name="booking_today_checkin")
def send_emails_to_user_with_today_checkin():
    asyncio.run(get_bookings_with_today_checkin_helper())
