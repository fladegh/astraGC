import json
from utils.mouse_actions import *
from classes.gesture import Gesture


class GestureController:
    def __init__(self):
        self.gestures = {}
        self.mouse = False
        self.load_gestures_from_file("gestures.json")

    def load_gestures_from_file(self, file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
            if 'gestures' in data:
                for gesture_data in data['gestures']:
                    key_or_mouse_button = gesture_data['key_or_mouse_button']
                    if isinstance(key_or_mouse_button, list):
                        key_or_mouse_button = list(key_or_mouse_button)
                    gesture = Gesture(gesture_data['name'], key_or_mouse_button,
                                      gesture_data['delay_after_gesture'], gesture_data['type'],
                                      gesture_data['requirement'], gesture_data['block_if'],
                                      gesture_data['distances'])
                    self.gestures[gesture_data['name']] = gesture

    def handle_activation(self, distances):
        for gesture in self.gestures.values():
            gesture.activated = True
            for points, distance in gesture.distances.items():
                point1, point2 = map(int, points.split("-"))

                if not distances[point1][point2] * (120 / distances[0][5]) < distance:
                    gesture.activated = False

    def action(self, action):
        if not action:
            return
        if action == ["left"]:
            click_left()
        elif action == ["right"]:
            click_right()
        else:
            pyautogui.hotkey(*action)

    def action_start(self, action):
        if not action:
            return
        if action == ["left"]:
            press_left()
        elif action == ["right"]:
            press_right()
        else:
            pyautogui.keyDown(*action)

    def action_stop(self, action):
        if not action:
            return
        if action == ["left"]:
            release_left()
        elif action == ["right"]:
            release_right()
        else:
            pyautogui.keyUp(*action)

    def handle_actions(self):
        for gesture in self.gestures.values():
            if gesture.activated and not gesture.requirement or gesture.activated and \
                    self.gestures[gesture.requirement].activated:  # Блокируем жест если нет requirement
                if not gesture.block_if or not self.gestures[gesture.block_if].activated:  # Блокируем жест если block
                    if gesture.type == "once" and not gesture.was_done:
                        self.action(gesture.key_or_mouse_button)
                        gesture.was_done = True
                    elif gesture.type == "drag" and not gesture.was_done:
                        self.action_start(gesture.key_or_mouse_button)
                        gesture.was_done = True
                        if gesture.name == "MOUSE":
                            self.mouse = True
                    elif gesture.type == "spam":
                        self.action(gesture.key_or_mouse_button)
            else:
                if gesture.type == "drag" and gesture.was_done:
                    self.action_stop(gesture.key_or_mouse_button)
                    if gesture.name == "MOUSE":
                        self.mouse = False
                gesture.was_done = False
