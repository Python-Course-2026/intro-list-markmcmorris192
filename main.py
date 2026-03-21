from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Shop API")


class Item(BaseModel):
    name: str
    price: float


class ItemInDB(Item):
    id: int


db: list[ItemInDB] = [
    ItemInDB(id=1, name="Ноутбук", price=89900),
    ItemInDB(id=2, name="Мышь", price=1200),
]


@app.get("/")
def healthcheck():
   return {"status": "ok"}


@app.get("/items", response_model=list[ItemInDB])
def list_items():
    # TODO: верни весь список db
    pass


@app.get("/items/{item_id}", response_model=ItemInDB)
def get_item(item_id: int):
    # TODO: найди элемент по id в db и верни его
    # если не найден - raise HTTPException(status_code=404, detail="Item not found")
    pass


@app.post("/items", response_model=ItemInDB, status_code=201)
def create_item(item: Item):
    # TODO: сгенерируй новый id (max по db + 1)
    # создай ItemInDB и добавь в db
    # верни созданный объект
    pass


@app.delete("/items/{item_id}", status_code=204)
def delete_item(item_id: int):
    # TODO: найди элемент по id и удали его из db
    # если не найден - raise HTTPException(status_code=404, detail="Item not found")
    pass
