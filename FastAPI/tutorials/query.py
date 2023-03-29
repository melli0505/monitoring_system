from fastapi import FastAPI

app = FastAPI()

item_db = [{'itemname' : "va"}, {'itemname' : "mr"}, {'itemname' : "lk"}, {'itemname' : "ie"}, {'itemname' : "sy"}]

@app.get('/')
async def root():
    return 'Hello World'

@app.get('/items/')
async def read_item(skip: int, limit: int = 10):
    return item_db[skip: skip + limit]