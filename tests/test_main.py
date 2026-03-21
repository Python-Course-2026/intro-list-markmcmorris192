from fastapi.testclient import TestClient
from main import app, db, ItemInDB

client = TestClient(app)


def setup_function():
    db.clear()
    db.append(ItemInDB(id=1, name="Ноутбук", price=89900))
    db.append(ItemInDB(id=2, name="Мышь", price=1200))


# --- healthcheck ---

def test_healthcheck():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


# --- list_items ---

def test_list_items_returns_all():
    response = client.get("/items")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_list_items_structure():
    response = client.get("/items")
    item = response.json()[0]
    assert "id" in item
    assert "name" in item
    assert "price" in item


# --- get_item ---

def test_get_item_exists():
    response = client.get("/items/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Ноутбук"


def test_get_item_not_found():
    response = client.get("/items/999")
    assert response.status_code == 404


# --- create_item ---

def test_create_item_status_code():
    response = client.post("/items", json={"name": "Клавиатура", "price": 3500})
    assert response.status_code == 201


def test_create_item_returns_created_object():
    response = client.post("/items", json={"name": "Клавиатура", "price": 3500})
    data = response.json()
    assert data["name"] == "Клавиатура"
    assert data["price"] == 3500
    assert "id" in data


def test_create_item_appears_in_list():
    client.post("/items", json={"name": "Клавиатура", "price": 3500})
    response = client.get("/items")
    names = [i["name"] for i in response.json()]
    assert "Клавиатура" in names


def test_create_item_id_is_unique():
    r1 = client.post("/items", json={"name": "Товар 1", "price": 100})
    r2 = client.post("/items", json={"name": "Товар 2", "price": 200})
    assert r1.json()["id"] != r2.json()["id"]


def test_create_item_missing_field():
    response = client.post("/items", json={"name": "Без цены"})
    assert response.status_code == 422


# --- delete_item ---

def test_delete_item_status_code():
    response = client.delete("/items/1")
    assert response.status_code == 204


def test_delete_item_removed_from_list():
    client.delete("/items/1")
    response = client.get("/items/1")
    assert response.status_code == 404


def test_delete_item_not_found():
    response = client.delete("/items/999")
    assert response.status_code == 404


def test_delete_item_others_remain():
    client.delete("/items/1")
    response = client.get("/items/2")
    assert response.status_code == 200