from fastapi import FastAPI, Query, Body
import uvicorn
import threading

app = FastAPI()

hotels = [
    {'id': 1, 'title': 'Sochi', "name": "sochi"},
    {'id': 2, 'title': 'Dubai', 'name': 'dubai'}
]


import time
import asyncio

@app.get('/async/{id}')
async def get_async(id: int):
    print(f"Потоки: {threading.active_count()}")
    print(f"async. Начал {id}: {time.time()}")
    await asyncio.sleep(3)
    print(f"async. Закончил {id}: {time.time()}")


@app.get('/sync/{id}')
def get_sync(id: int):
    print(f"Потоки: {threading.active_count()}")
    print(f"sync. Начал {id}: {time.time()}")
    time.sleep(3)
    print(f"sync. Закончил {id}: {time.time()}")

@app.get(
    "/",
    summary='Главная страница',
    description='<h1>Главная страница api</h1>'
)
def main():
    return "Hello World!"

@app.get("/hotels")
def get_hotels(
        hotel_id: int | None = Query(None, description="Hotel ID"),
        title: str | None = Query(None, description="Hotel title"),
):
    hotels_ = []

    for hotel in hotels:
        if hotel_id and hotel["id"] != hotel_id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)
    return hotels_


@app.post("/hotels")
def create_hotel(
        title: str = Body(embed=True, description="Hotel title"),
):
    global hotels

    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": title,
    })

    return {
        "success": "true",
    }

@app.delete("/hotels/{hotel_id}")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"success": "true"}


@app.put("/hotels/{hotel_id}")
def update_hotel(
        hotel_id: int,
        title: str = Body(embed=True, description="Hotel title"),
        name: str = Body(embed=True, description="Hotel name"),
):
    global hotels

    hotel_to_update = next((hotel for hotel in hotels if hotel['id'] == hotel_id), None)

    if not hotel_to_update:
        return {'error': 'Hotel not found'}

    hotel_to_update["title"] = title
    hotel_to_update["name"] = name

    return {"success": "true"}

@app.patch("/hotels/{hotel_id}")
def change_hotel(
        hotel_id: int,
        title: str | None = Body(None, embed=True, description="Hotel title"),
        name: str | None = Body(None, embed=True, description="Hotel name"),
):
    global hotels

    hotel_to_update = next((hotel for hotel in hotels if hotel['id'] == hotel_id), None)

    if not hotel_to_update:
        return {'error': 'Hotel not found'}

    if title and hotel_to_update["title"] != title:
        hotel_to_update["title"] = title
    if name and hotel_to_update["name"] != name:
        hotel_to_update["name"] = name

    return {"success": "true"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=8000)
