from typing import Union
from fastapi import FastAPI, Path, Body
from pydantic import BaseModel
from typing_extensions import Annotated

app = FastAPI()

class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None

class User(BaseModel):
    username: str
    full_name: Union[str, None] = None

@app.put("/items/{item_id}")
async def update_item(
    item_id: Annotated[int, Path(title="the ID of the item to get", ge=0, le=1000)],
    q: Union[str, None] = None,
    item: Union[Item, None] = None
):
    result = {"item_id": item_id}
    if q:
        result.update({"q": q})
    if item:
        result.update({"item": item})
    
    return result

@app.put("/body/{item_id}")
async def update_body(
    item_id: int, item: Item, user: User, importance: Annotated[str, Body()], q: Union[str, None] = None
):
    results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
    if q:
        results.update({"q": q})
    return results