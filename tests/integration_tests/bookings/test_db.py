from datetime import date, timedelta

from src.schemas.booking import BookingCreateDB, BookingUpdateDB


async def test_bookings_crud(db):
    """Тест CRUD операций для бронирований."""

    # Проверяем наличие тестовых данных
    users = await db.users.get_all()
    rooms = await db.rooms.get_all()
    assert len(users) > 0, "No users found in database for testing"
    assert len(rooms) > 0, "No rooms found in database for testing"

    user = users[0]
    room = rooms[0]

    # Используем относительные даты
    today = date.today()
    date_from = today + timedelta(days=30)  # Бронирование через месяц
    date_to = date_from + timedelta(days=1)
    price = 5000

    # Очистка возможных существующих бронирований
    await db.bookings.delete(user_id=user.id, room_id=room.id)

    # CREATE - Создание бронирования
    booking_data = BookingCreateDB(
        user_id=user.id,
        room_id=room.id,
        date_from=date_from,
        date_to=date_to,
        price=price,
    )

    # Проверка бизнес-логики
    assert booking_data.date_to > booking_data.date_from, "date_to должен быть больше date_from"
    assert booking_data.price > 0, "Цена должна быть положительной"

    # Добавляем бронирование
    created_booking = await db.bookings.add(booking_data)
    assert created_booking is not None, "Бронирование не было создано"

    # READ - Чтение созданного бронирования
    booking = await db.bookings.get_one_or_none(
        user_id=user.id,
        room_id=room.id,
    )

    assert booking is not None, "Созданное бронирование не найдено"
    assert booking.user_id == user.id
    assert booking.room_id == room.id
    assert booking.date_from == date_from
    assert booking.date_to == date_to
    assert booking.price == price

    # UPDATE - Обновление бронирования
    new_date_from = today + timedelta(days=35)
    new_date_to = new_date_from + timedelta(days=2)
    new_price = 10000

    update_data = BookingUpdateDB(
        user_id=user.id,
        room_id=room.id,
        date_from=new_date_from,
        date_to=new_date_to,
        price=new_price,
    )

    # Проверка новых данных
    assert update_data.date_to > update_data.date_from, "Новый date_to должен быть больше date_from"
    assert update_data.price > 0, "Новая цена должна быть положительной"

    await db.bookings.edit(
        update_data,
        user_id=user.id,
        room_id=room.id,
    )

    # Проверяем обновленное бронирование
    updated_booking = await db.bookings.get_one_or_none(
        user_id=user.id,
        room_id=room.id,
    )

    assert updated_booking is not None, "Обновленное бронирование не найдено"
    assert updated_booking.user_id == user.id
    assert updated_booking.room_id == room.id
    assert updated_booking.date_from == new_date_from
    assert updated_booking.date_to == new_date_to
    assert updated_booking.price == new_price

    # DELETE - Удаление бронирования
    await db.bookings.delete(
        user_id=user.id,
        room_id=room.id,
    )

    # Проверяем, что бронирование удалено
    deleted_booking = await db.bookings.get_one_or_none(
        user_id=user.id,
        room_id=room.id,
    )

    assert deleted_booking is None, "Бронирование не было удалено"

    # Коммитим изменения
    await db.commit()
