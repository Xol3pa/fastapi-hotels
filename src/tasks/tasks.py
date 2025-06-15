import os
import asyncio
from time import sleep
from pathlib import Path
from PIL import Image

from src.database import async_session_maker_null_pull
from src.tasks.celery_app import celery_instance
from src.utils.db_manager import DBManager


@celery_instance.task()
def test_task():
    sleep(5)
    print("Конец")


@celery_instance.task()
def resize_image(image_path):
    sizes = [1000, 500, 200]
    output_dir = "src/static/images"

    # Открываем изображение
    try:
        with Image.open(image_path) as img:
            # Получаем имя файла без расширения и расширение
            file_path = Path(image_path)
            filename_stem = file_path.stem
            file_extension = file_path.suffix

            saved_files = []

            # Ресайзим для каждого размера
            for size in sizes:
                # Вычисляем пропорциональную высоту
                original_width, original_height = img.size
                aspect_ratio = original_height / original_width
                new_height = int(size * aspect_ratio)

                # Ресайзим изображение
                resized_img = img.resize((size, new_height), Image.Resampling.LANCZOS)

                # Формируем имя файла с указанием размера
                output_filename = f"{filename_stem}_{size}w{file_extension}"
                output_path = os.path.join(output_dir, output_filename)

                # Сохраняем
                resized_img.save(output_path, quality=95, optimize=True)
                saved_files.append(output_path)

                print(f"Сохранено: {output_path} ({size}x{new_height})")

            return saved_files

    except FileNotFoundError:
        print(f"Ошибка: Файл {image_path} не найден")
        return []
    except Exception as e:
        print(f"Ошибка при обработке изображения: {e}")
        return []


async def get_bookings_with_today_checkin_helper():
    print("enter")
    async with DBManager(session_factory=async_session_maker_null_pull) as db:
        await db.bookings.get_bookings_with_today_checkin()
        print("result")
    print("exit")


@celery_instance.task(name="bookings_from_today")
def send_emails_to_users_with_today_bookings():
    asyncio.run(get_bookings_with_today_checkin_helper())
