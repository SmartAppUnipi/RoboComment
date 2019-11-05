from flask import Flask

app = Flask(__name__)


@app.route('/video_url', methods=["GET"])
def hello():
    return "https://b2ushds2-vh.akamaihd.net/i/Italy/podcastcdn/raidue/Nazionali_Raisport/10639147_,800,1800,.mp4.csmil/segment100_1_av.ts?null=0"


if __name__ == '__main__':
    app.run()
