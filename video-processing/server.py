from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/video_url', methods=["GET"])
def hello():
    return "https://storage.googleapis.com/hlt_project/Off_Topic_SA/testvideo.mp4"


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3000)
