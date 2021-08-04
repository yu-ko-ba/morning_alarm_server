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


# アラームリストのJSONを返す
def get_alarm_list():
    return json.load(open("./json/alarm_list.json", "r", encoding="UTF-8"))


# アラームリストを返すAPI
@flask.route("/get_alarm_list")
def alarm_list():
    return jsonify(get_alarm_list())


# アラームリストに時間を追加する
def add_to_json(add_time, debug=False):
    file = open("./json/alarm_list.json", 'r', encoding="UTF-8")
    data = json.load(file)
    # アラームにIDを割り当てる
    # '00'から'99'までで空いてる一番若い番号を割り当てる
    for i in range(100):
        i = str(i).zfill(2)
        if i not in data["data"]:
            data["data"][i] = add_time
            # 最終更新日時を更新する
            data["last_updated"] = time.time()
            # JSONファイルに書き込む
            with open("./json/alarm_list.json", 'w', encoding="UTF-8") as f:
                json.dump(data, f, indent=4)
            # IDを割り振れたらこの関数を終了する
            if debug:
                print("ID: " + i + "を割り当てました")
            return

    # IDが'00'から'99'まですべて割り振られていたらメッセージを出力する
    if debug:
        print("新しく追加することができませんでした。")


# アラームリストにアラームを追加するためのAPI
@flask.route("/add/<time>")
def add_alarm(time=None):
    add_to_json(time)
    return jsonify(get_alarm_list())


# アラームを削除する関数
def remove_alarm_from_json(id):
    # JSONファイルからデータを読み込む
    file = open("./json/alarm_list.json", 'r', encoding="UTF-8")
    # 読み込んだデータをJSON形式に変換する
    data = json.load(file)
    # 指定されたIDのアラームを削除する
    del data["data"][id]
    # 最終更新日時を更新する
    data["last_updated"] = time.time()
    # JSONファイルに書き込む
    with open("./json/alarm_list.json", 'w', encoding="UTF-8") as f:
        json.dump(data, f, indent=4)


# アラームを削除するAPI
@flask.route("/remove/<id>")
def remove_alarm(id=None):
    remove_alarm_from_json(id)
    return jsonify(get_alarm_list())


# アラームの時間を変更する関数
def change_the_alarm_time(id, new_time, debug=False):
    json_data = get_alarm_list()

    if debug:
        print("old")
        print(json_data)
        print("---------------------------------------------------------")

    json_data["data"][id] = new_time
    if debug:
        print("new")
        print(json_data)

    json_data["last_updated"] = time.time()
    with open("./json/alarm_list.json", 'w', encoding="UTF-8") as f:
        json.dump(json_data, f, indent=4)


# アラームの時間を変更するAPI
@flask.route("/change/<id>/<new_time>")
def change_alarm(id=None, new_time=None):
    change_the_alarm_time(id, new_time)
    return jsonify(get_alarm_list())


# main関数を実行する
if __name__ == '__main__':
    main()
