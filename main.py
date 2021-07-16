# モーニングアラームのアラームリストを管理するサーバー
from flask import Flask, jsonify
import os, json, time


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
            data = {
                    "last_updated" : time.time(),
                    "data" : {
                        }
                    }
            json.dump(data, file, indent=4)


@flask.route("/")
def hello_world():
    return "Hello World!"


def get_alarm_list():
    return json.load(open("./json/alarm_list.json", "r", encoding="UTF-8"))


@flask.route("/get_alarm_list")
def alarm_list():
    return jsonify(get_alarm_list())


def add_to_json(time, debug=False):
    file = open("./json/alarm_list.json", 'r', encoding="UTF-8")
    data = json.load(file)
    for i in range(100):
        i = str(i).zfill(2)
        if i not in data["data"]:
            data["data"][i] = time

            with open("./json/alarm_list.json", 'w', encoding="UTF-8") as f:
                json.dump(data, f, indent=4)

            break

    if debug:
        print("新しく追加することができませんでした。")


@flask.route("/add/<time>")
def add_alarm(time=None):
    add_to_json(time)
    return jsonify(get_alarm_list())


# main関数を実行する
if __name__ == '__main__':
    main();
