from flask import Flask, jsonify
import main, os, json

main.create_json_file(True)

# alarm_list = json.load(open("./json/alarm_list.json", "r", encoding="UTF-8"))

# print(type(alarm_list))
# print(type({"hoge": "fuga"}))
# main.get_alarm_list()
