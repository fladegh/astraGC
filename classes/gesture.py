class Gesture:
    def __init__(self, name, key_or_mouse_button, delay_after_gesture, type, requirement, block_if, distances):
        self.name = name
        self.key_or_mouse_button = key_or_mouse_button
        self.delay_after_gesture = delay_after_gesture
        self.type = type
        self.requirement = requirement
        self.block_if = block_if
        self.distances = distances
        self.activated = False
        self.was_done = False
