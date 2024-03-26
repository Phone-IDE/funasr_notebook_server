import os

from fastapi import FastAPI, UploadFile, File

from funclipper.videoclipper import runner

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

        res_text=runner(stage=1, file=file_location, output_dir="./output", dest_text=None,
               dest_spk=None, start_ost=0, end_ost=0, sd_switch="not",
               output_file=None)
        os.remove(file_location)
        if res_text is None:
            return {"info": "file uploaded successfully", "filename": file.filename, "res_text": "No text found"}
    return {"info": "file uploaded successfully", "filename": file.filename, "res_text": res_text}

if __name__ == '__main__':
    #启动
    import uvicorn
    print("Starting server...")
    uvicorn.run(app=app,
                host="0.0.0.0",
                port=8000)
    print("Server started!")