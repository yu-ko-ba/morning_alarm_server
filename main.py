# モーニングアラームのアラームリストを管理するサーバー
from flask import Flask, jsonify
import os
import json
import time


alarm_list_file_path = "./json/alarm_list.json"

flask = Flask(__name__)


def main(debug=False):
    # 日本語で文字化けしないようにする
    flask.config["JSON_AS_ASCII"] = False
    # 勝手にソートしないようにする
    flask.config["JSON_SORT_KEYS"] = False

    # JSONファイルが無かったら作る
    create_json_file()

    # サーバーを起動する
    flask.run(host="192.168.128.207", port=5000, debug=debug)


def print_line(line_length=100):
    line = ""
    for i in range(0, line_length + 1):
        line += "-"
    print(line)


# アラームのリストを記録するJSONファイルが存在しなかったら作る、ディレクトリも無かったら作る
def create_json_file(force=False):
    # JSONファイルを入れるディレクトリが存在しなかったら作る
    os.makedirs("./json", exist_ok=True)

    # JSONファイルが存在しなかったら作る
    if not os.path.isfile(alarm_list_file_path) or force:
        with open(alarm_list_file_path, "w", encoding="UTF-8") as file:
            data = {
                    "last_updated": time.time(),
                    "data": {
                        }
                    }
            json.dump(data, file, indent=4)


# file_pathの中身をJSONデータに変換して返す
def load_json(file_path, encoding="UTF-8"):
    return json.load(open(file_path, "r", encoding=encoding))


# file_pathにJSONデータを上書きする
def write_json(data, file_path, indent=4):
    # 最終更新日時を更新する
    data["last_updated"] = time.time()
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=indent)


# アラームリストのJSONを返す
def get_alarm_list():
    return load_json(alarm_list_file_path)


# アラームリストをJSONファイルに上書き保存する
def set_alarm_list(data):
    write_json(data, alarm_list_file_path)


@flask.route("/")
def hello_world():
    return "Hello World!"


# アラームリストを返すAPI
@flask.route("/show")
@flask.route("/get")
@flask.route("/get_alarm_list")
def get_alarm_list_api():
    return jsonify(get_alarm_list())


# アラームリストにアラームの時間を追加する
def add_alarm(add_time, debug=False):
    # JSONのデータを取得する
    data = get_alarm_list()
    # アラームにIDを割り当てる
    # '00'から'99'までで空いてる一番若い番号を割り当てる
    for i in range(100):
        # iの値を文字列型に変換する、ついでに0埋め2ケタ表示にする
        i = str(i).zfill(2)
        # IDにiの値が使われていなかったらそれを使う
        if i not in data["data"]:
            data["data"][i] = add_time

            # JSONファイルに書き込む
            set_alarm_list(data)

            if debug:
                print("ID: " + i + "を割り当てました")

            # IDを割り振れたらこの関数を終了する
            return

    # IDが'00'から'99'まですべて割り振られていたらメッセージを出力する
    if debug:
        print("新しく追加することができませんでした。")


# アラームリストにアラームを追加するためのAPI
@flask.route("/add/<time>")
def add_alarm_api(time=None):
    add_alarm(time)
    return jsonify(get_alarm_list())


# アラームを削除する関数
def delete_alarm(id):
    # JSONファイルからデータを読み込む
    data = get_alarm_list()

    # 指定されたIDのアラームを削除する
    del data["data"][id]

    # JSONファイルに書き込む
    set_alarm_list(data)


# アラームを削除するAPI
@flask.route("/remove/<id>")
@flask.route("/delete/<id>")
def delete_alarm_api(id=None):
    delete_alarm(id)
    return jsonify(get_alarm_list())


# アラームの時間を変更する関数
def change_the_alarm_time(id, new_time, debug=False):
    # アラームリストを読み込む
    data = get_alarm_list()

    if debug:
        print("old")
        print(data)
        print_line()

    # 指定されたIDの時間を変更する
    data["data"][id] = new_time

    if debug:
        print("new")
        print(data)
        print_line()

    # 変更を保存する
    set_alarm_list(data)


# アラームの時間を変更するAPI
@flask.route("/change/<id>/<new_time>")
def change_the_alarm_time_api(id=None, new_time=None):
    change_the_alarm_time(id, new_time)
    return jsonify(get_alarm_list())


# main関数を実行する
if __name__ == '__main__':
    main()
