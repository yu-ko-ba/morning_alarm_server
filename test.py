from flask import Flask, jsonify
import main, os, json, time

# main.main(True)

# main.create_json_file(True)
main.add_to_json("12:34")


# alarm_list = json.load(open("./json/alarm_list.json", "r", encoding="UTF-8"))

# print(type(alarm_list))
# print(type({"hoge": "fuga"}))
# main.get_alarm_list()
