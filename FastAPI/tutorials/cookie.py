from typing import Union
from fastapi import FastAPI, Cookie
from typing_extensions import Annotated

app = FastAPI()

@app.get("/items/")
async def read_items(ads_ids: Annotated[Union[str, None], Cookie()] = None):
    return {"ads_id": ads_ids}