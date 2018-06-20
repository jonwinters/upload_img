from flask import request, Flask, send_file
import base64, hashlib, time, secrets, os

app = Flask(__name__)

path_prefix = "/root/pic/"

url = "https://temp_url"

token = secrets.token_hex(16)


@app.route("/upload/<auth_token>", methods=['POST'])
def upload(auth_token):
    if auth_token != token:
        return "error"
    print("file: text")
    md5sum = hashlib.md5(request.data).hexdigest()
    file_path = md5sum + "-" + str(int(time.time())) + ".png"
    with open(path_prefix + file_path, "w+b") as file:
        file.write(base64.b64decode(request.data))
    return url + file_path


@app.route("/<file_path>", methods=['GET'])
def pic(file_path):
    return send_file(path_prefix + file_path, mimetype='image/png')


if __name__ == '__main__':
    print("token: " + token)
    os.system("echo " + token + "> /tmp/pic_token")
    app.run(host='127.0.0.1', port=8090)
