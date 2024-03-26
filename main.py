from fastapi import FastAPI, UploadFile, File

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    # 指定文件保存的路径
    file_location = f"./uploaded_files/{file.filename}"
    # 使用异步写入，以'wb'模式打开文件，意味着以二进制写模式打开
    # 这对于大多数文件类型都是必需的
    with open(file_location, "wb") as file_object:
        # 读取上传的文件内容
        contents = await file.read()
        # 将内容写入到本地文件
        file_object.write(contents)
    # 返回保存文件的路径和文件名作为确认
    return {"info": f"file '{file.filename}' saved at '{file_location}'"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
