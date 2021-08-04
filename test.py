from flask import Flask, jsonify
import main, os, json, time

main.add_to_json("23:59", True)

# main.main(True)

# main.create_json_file(True)
# main.add_to_json("12:34")


# alarm_list = json.load(open("./json/alarm_list.json", "r", encoding="UTF-8"))

# print(type(alarm_list))
# print(type({"hoge": "fuga"}))
# main.get_alarm_list()

# main.create_json_file(False)

# for i in range(0, 101):
    # main.add_to_json("12:34", debug=True)

# main.add_to_json("12:34", debug=True)
# main.remove_alarm_from_json("01")
# print(main.get_alarm_list())
