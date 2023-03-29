from typing import Union, List
from typing_extensions import Annotated
from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/items/")
async def read_items(q: Annotated[Union[List[str], None], Query()] = ["hello", "darling"]):
	query_items = {"q": q}
	return query_items