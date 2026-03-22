from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Shop API")


class Item(BaseModel):
    name: str
    price: int


class ItemInDB(Item):
    id: int


db: list[ItemInDB] = [
    ItemInDB(id=1, name="Ноутбук", price=89900),
    ItemInDB(id=2, name="Мышь", price=1200),
    ItemInDB(id=3, name="Телефон", price=150000),
]


@app.get("/")
def healthcheck():
   return {"status": "ok"}


@app.get("/items", response_model=list[ItemInDB])
def list_items():
    # TODO: верни весь список db
    return db


@app.get("/items/{item_id}", response_model=ItemInDB)
def get_item(item_id: int):
    # TODO: найди элемент по id в db и верни его
    # если не найден - raise HTTPException(status_code=404, detail="Item not found")
    for item in db:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")


@app.post("/items", response_model=ItemInDB, status_code=201)
def create_item(item: Item):
    # TODO: сгенерируй новый id (max по db + 1)
    # создай ItemInDB и добавь в db
    # верни созданный объект
    if db:
        new_id = max(i.id for i in db) + 1
    else:
        new_id = 1
    new_item = ItemInDB(id=new_id, name=item.name, price=item.price)
    db.append(new_item)
    return new_item


@app.delete("/items/{item_id}", status_code=204)
def delete_item(item_id: int):
    # TODO: найди элемент по id и удали его из db
    # если не найден - raise HTTPException(status_code=404, detail="Item not found")
    for i, item in enumerate(db):
        if item.id == item_id:
            db.pop(i)
            return
    raise HTTPException(status_code=404, detail="Item not found")
