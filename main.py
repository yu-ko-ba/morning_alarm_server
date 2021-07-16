# モーニングアラームのアラームリストを管理するサーバー
from flask import Flask, jsonify
import os, json


flask = Flask(__name__)


def main(debug=False):
    # 日本語で文字化けしないようにする
    flask.config["JSON_AS_ASCII"] = False
    # 勝手にソートしないようにする
    flask.config["JSON_SORT_KEYS"] = False

    # JSONファイルが無かったら作る
    create_json_file()

    # サーバーを起動する
    flask.run(debug=debug)


# アラームのリストを記録するJSONファイルが存在しなかったら作る、ディレクトリも無かったら作る
def create_json_file(force=False):
    # JSONファイルを入れるディレクトリが存在しなかったら作る
    os.makedirs("./json", exist_ok=True)

    # JSONファイルが存在しなかったら作る
    path = "./json/alarm_list.json"
    if not os.path.isfile(path) or force:
        with open(path, "w", encoding="UTF-8") as file:
            file.write("{}")


@flask.route("/")
def hello_world():
    return "Hello World!"


def get_alarm_list():
    return json.load(open("./json/alarm_list.json", "r", encoding="UTF-8"))


@flask.route("/get_alarm_list")
def alarm_list():
    return jsonify(get_alarm_list())


@flask.route("/set/<time>")
def set_alarm(time=None):
    return time


# main関数を実行する
if __name__ == '__main__':
    main()
