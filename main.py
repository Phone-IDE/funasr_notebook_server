import subprocess

from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os

from funclipper.videoclipper import runner

app = Flask(__name__)


# 为上传的文件设置一个保存路径
UPLOAD_FOLDER = './uploaded_files'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def root():
    return {"message": "Hello World"}

@app.route("/uploadfile/", methods=["POST"])
def create_upload_file():
    if 'file' not in request.files:
        return jsonify(error="No file part"), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify(error="No selected file"), 400
    if file:
        filename = secure_filename(file.filename)
        file_location = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_location)

        res_text = runner(stage=1, file=file_location, output_dir="./output", dest_text=None,
                          dest_spk=None, start_ost=0, end_ost=0, sd_switch="not",
                          output_file=None)
        os.remove(file_location)
        if res_text is None:
            return jsonify(info="file uploaded successfully", filename=file.filename, res_text="No text found")
        return jsonify(info="file uploaded successfully", filename=file.filename, res_text=res_text)


def create_frpc_config_toml(local_port, remote_port, server_ip='your_server_ip', server_port=7000):
    """
    生成 TOML 格式的 FRP 客户端配置文件。
    """
    config = f"""
    serverAddr = "124.156.230.199"
    serverPort = 7000
    auth.method = "token"
    auth.token = "password"

    [[proxies]]
    name = "{str(uuid.uuid4())}"
    type = "tcp"
    remotePort = {remote_port}
    localPort = {local_port}
    """
    return config

def main():
    # 解析命令行参数

    # 生成 TOML 格式的 FRP 客户端配置

    # 保存配置到文件
    config_file_path = 'frpc.toml'
    with open(config_file_path, 'w') as config_file:
        config_file.write(create_frpc_config_toml(8000, 8005))

    # 修改为你的 FRP 可执行文件路径
    frpc_executable_path = "./frpc"

    # 启动 FRP 客户端，并将输出重定向到日志文件
    with open("logs.txt", "w") as logs:
        subprocess.Popen([frpc_executable_path, "-c", config_file_path], stdout=logs, stderr=logs)
    print(f"FRP 客户端已启动，配置文件路径: {config_file_path}")
    
if __name__ == "__main__":
    main()
    app.run(host="127.0.0.1", port=8000)
