import cv2
import mediapipe as mp
import threading
import math
from collections import deque

from utils.mouse_actions import *
from classes.gesture_controller import GestureController


class Recognition:
    def __init__(self, astra, ui):
        self.ui = ui
        self.astra = astra
        self.gesture_controller = None

    def launch_astra(self):
        pyautogui.FAILSAFE = False
        self.gesture_controller = GestureController()
        cap = cv2.VideoCapture(self.astra.camera_id)

        mpHands = mp.solutions.hands
        hands = mpHands.Hands(static_image_mode=False,
                              max_num_hands=1,
                              min_tracking_confidence=0.7,
                              min_detection_confidence=0.7)
        mpDraw = mp.solutions.drawing_utils
        width, height = pyautogui.size()

        border = self.astra.border
        alpha = self.astra.alpha
        smooth = self.astra.smooth
        camera_was_enabled = self.astra.camera

        adj_width = width - 2 * border
        adj_height = height - 2 * border

        cursor = {"x": 0, "y": 0}
        is_hand = False

        lock = threading.Lock()

        dqx = deque([0] * smooth, maxlen=smooth)
        dqy = deque([0] * smooth, maxlen=smooth)

        def move_cursor(cursor, lock):
            while self.astra.is_running:
                with lock:
                    cursor_x, cursor_y = cursor["x"], cursor["y"]
                if is_hand:
                    pyautogui.moveTo(width - border - cursor_x, cursor_y + border, duration=0)

        thread = threading.Thread(target=move_cursor, args=(cursor, lock))
        thread.start()

        fingers_positions = {}
        fingers_distances = [[0] * 21 for _ in range(21)]

        self.ui.label_status.setText("Запущено!")
        while True:
            success, image = cap.read()

            imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = hands.process(imageRGB)

            if results.multi_hand_landmarks:
                is_hand = True
                handLm = results.multi_hand_landmarks[0].landmark
                for id, lm in enumerate(handLm):
                    h, w, _ = image.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)

                    fingers_positions[id] = (cx, cy)

                    if id == 8 and self.gesture_controller.mouse:
                        cv2.circle(image, (cx, cy), 25, (255, 0, 255), cv2.FILLED)
                        with lock:
                            cx_adjusted = ((cx - border) * adj_width / (w - 2 * border))
                            cy_adjusted = ((cy - border) * adj_height / (h - 2 * border))
                            dqx.append(cx_adjusted)
                            dqy.append(cy_adjusted)

                            med_cx_adjusted = sorted(list(dqx))[smooth // 2]
                            med_cy_adjusted = sorted(list(dqy))[smooth // 2]

                            cursor["x"] = alpha * med_cx_adjusted + (1 - alpha) * cursor["x"]
                            cursor["y"] = alpha * med_cy_adjusted + (1 - alpha) * cursor["y"]

                mpDraw.draw_landmarks(image, results.multi_hand_landmarks[0], mpHands.HAND_CONNECTIONS)

                for i in range(21):
                    for j in range(21):
                        distance = math.sqrt((fingers_positions[i][0] - fingers_positions[j][0]) ** 2 + (
                                    fingers_positions[i][1] - fingers_positions[j][1]) ** 2)
                        fingers_distances[i][j] = distance

                self.gesture_controller.handle_activation(fingers_distances)
                self.gesture_controller.handle_actions()

            else:
                is_hand = False
                pyautogui.keyUp('alt')
            if self.astra.camera:
                cv2.imshow("ASTRA GESTURE CONTROL", image)
                camera_was_enabled = True
            if camera_was_enabled and not self.astra.camera:
                cv2.destroyAllWindows()
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            if not self.astra.is_running:
                break
        self.ui.label_status.setText("Не активно.")

        cap.release()
        cv2.destroyAllWindows()
