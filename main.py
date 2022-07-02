from fastapi import FastAPI, Path, Query, HTTPException
import uvicorn
from typing import Optional
from pydantic import BaseModel
import json
from model_rout.model_part import router

app = FastAPI()
app.include_router(router)


class Item(BaseModel):
    name: str
    price: float
    brand: Optional[str] = None


class UpdateItem(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    brand: Optional[str] = None


def save_json():
    """
    serialize data to json for saving
    """
    print(products)
    json_object = json.dumps(products, indent=4)
    with open("prod.json", "w") as outfile:
        outfile.write(json_object)


def load_json():
    """
    load and deserialize data
    """
    a = open('prod.json')
    return json.load(a)


@app.get('/')
async def root():
    """
    starting page with greetings
    :return: greets
    """
    return {'say': 'hello'}


@app.get('/get-item/{item_id}')
def get_item(item_id: str = Path(None, description="There is some description of endpoint")):
    """
    return product by id
    :param item_id:
    :return: dict with name, price, brand
    """
    return products[item_id]


@app.get('/show-all')
def show_all():
    return products


@app.get('/get-by-name')
def get_item(name: str = Query(None)):
    for product_id in products:
        if products[product_id]['name'] == name:
            return products[product_id]
    raise HTTPException(status_code=400)


@app.post("/create-item/{item_id}")
def create_item(item_id: str, item: Item):
    if item_id in products:
        return {'Error': 'product with this id is already exist'}
    products[item_id] = {"name": item.name, "price": item.price, "brand": item.brand}
    save_json()
    return "product added"


@app.put("/update-item/{item_id}")
def update_item(item_id: str, item: UpdateItem):
    if item_id not in products:
        raise HTTPException(status_code=404)

    if item.name != None:
        products[item_id]['name'] = item.name

    if item.price != None:
        products[item_id]['price'] = item.price

    if item.brand != None:
        products[item_id]['brand'] = item.brand

    save_json()
    return products[item_id]


@app.delete("/delete-item")
def delete_item(item_id: str = Query(None)):
    if item_id not in products:
        raise HTTPException(status_code=404)
    del products[item_id]
    save_json()
    return {"Success": "Item deleted!"}


products = load_json()
if __name__ == '__main__':
    uvicorn.run("main:app", port=8000, host="0.0.0.0",  reload=True)