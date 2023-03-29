from fastapi import FastAPI, File, UploadFile

app = FastAPI()

@app.post("/files/")
async def create_file(file: bytes = File()):
    return {"filesize": len(file)}

@app.post("/uploadfile/")
async def create_upload_file(file:UploadFile):
    return {"filename": file.filename}