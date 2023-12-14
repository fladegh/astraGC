import json


def remove_gesture(gesture_name):
    with open('gestures.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    for gesture in data["gestures"]:
        if gesture["name"] == gesture_name:
            data["gestures"].remove(gesture)

    with open('gestures.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False)


def get_gesture_names_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        gesture_data = data["gestures"]
        gesture_names = [gesture["name"] for gesture in gesture_data]
        return gesture_names


def load_data(gesture_name):
    with open('gestures.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
        for gesture in data["gestures"]:
            if gesture["name"] == gesture_name:
                return gesture
    return None


def update_gesture_data(gesture_data):
    with open('gestures.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    for gesture in data["gestures"]:
        if gesture["name"] == gesture_data["name"]:
            gesture.update(gesture_data)
            break

    with open('gestures.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False)


def save_gesture_data(new_gesture_data):
    try:
        with open('gestures.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {"gestures": []}

    data["gestures"].append(new_gesture_data)

    with open('gestures.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False)
