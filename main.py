from fastapi import FastAPI, Query, Body
import uvicorn

app = FastAPI()

hotels = [
    {'id': 1, 'name': 'Sochi'},
    {'id': 2, 'name': 'Dubai'},
]

@app.get("/")
def main():
    return "Hello World!"

@app.get("/hotels")
def get_hotels(
        id: int | None = Query(None, description="Hotel ID"),
        name: str | None = Query(None, description="Hotel Name"),
):
    hotels_ = []

    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if name and hotel["name"] != name:
            continue
        hotels_.append(hotel)
    return hotels_


@app.post("/hotels")
def create_hotel(
        name: str = Body(embed=True, description="Hotel Name"),
):
    global hotels

    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "name": name,
    })

    return {
        "success": "true",
    }

@app.delete("/hotels/{hotel_id}")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"success": "true"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True )
