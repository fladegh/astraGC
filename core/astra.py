import threading
from PyQt5.QtWidgets import QMainWindow, QPushButton
from utils.loading_gestures import *
from ui.main_window import Ui_MainWindow
from ui.gesture_editor import GestureEditor
from core.recognition import Recognition


class Astra(QMainWindow):
    def __init__(self, main_window):
        super(Astra, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(main_window)
        self.update_gestures()
        self.recognition = Recognition(self, self.ui)
        self.gesture_editor = None

        self.border = 30
        self.alpha = 0.1
        self.smooth = 5
        self.is_running = False
        self.camera = False
        self.camera_id = 0

        self.ui.horizontalSlider_alpha.valueChanged.connect(self.horizontalSlider_alpha_changed)
        self.ui.horizontalSlider_smooth.valueChanged.connect(self.horizontalSlider_smooth_changed)
        self.ui.horizontalSlider_border.valueChanged.connect(self.horizontalSlider_border_changed)

        self.ui.pushButton_launch.clicked.connect(self.call_launch_astra)
        self.ui.pushButton_stop.clicked.connect(self.call_shutdown_astra)
        self.ui.checkBox_camera.stateChanged.connect(self.manage_camera)
        self.ui.spinBox_camera.valueChanged.connect(self.camera_changed)

    def update_gestures(self):
        # Удаляем все существующие кнопки из вертикального макета
        for i in reversed(range(self.ui.verticalLayout.count())):
            widget = self.ui.verticalLayout.itemAt(i).widget()
            if widget:
                self.ui.verticalLayout.removeWidget(widget)
                widget.setParent(None)

        # Получаем обновленный список жестов
        gestures = get_gesture_names_from_file("gestures.json")

        # Переназначаем вертикальный макет для scrollAreaWidgetContents
        self.ui.scrollAreaWidgetContents.setLayout(self.ui.verticalLayout)

        # Добавляем кнопки для каждого жеста в вертикальный макет
        for gesture in gestures:
            button = QPushButton(f"{gesture}")
            button.setStyleSheet("color: rgb(255, 255, 255);")
            button.clicked.connect(lambda checked, idx=gesture: self.on_gesture_button_clicked(load_data(idx)))
            self.ui.verticalLayout.addWidget(button)

        self.ui.verticalLayout.addWidget(self.ui.pushButton_new_gesture)
        self.ui.pushButton_new_gesture.clicked.connect(self.on_create_gesture_button_clicked)

        # Обновляем размеры scrollArea
        self.ui.scrollArea.setWidgetResizable(True)
        self.ui.scrollArea.setWidget(self.ui.scrollAreaWidgetContents)

    def horizontalSlider_border_changed(self):
        self.ui.label_border_value.setText(str(self.ui.horizontalSlider_border.value()))
        self.border = self.ui.horizontalSlider_border.value()

    def horizontalSlider_alpha_changed(self):
        self.ui.label_alpha_value.setText(str(self.ui.horizontalSlider_alpha.value() / 100))
        self.alpha = self.ui.horizontalSlider_alpha.value() / 100

    def horizontalSlider_smooth_changed(self):
        self.ui.label_smooth_value.setText(str(self.ui.horizontalSlider_smooth.value()))
        self.smooth = self.ui.horizontalSlider_smooth.value()

    def camera_changed(self):
        self.camera_id = self.ui.spinBox_camera.value() - 1

    def on_create_gesture_button_clicked(self):
        new_gesture_data = {
            "name": "NEW_GESTURE",
            "key_or_mouse_button": "",
            "delay_after_gesture": 0,
            "type": "",
            "requirement": "",
            "block_if": "",
            "distances": {}
        }
        self.gesture_editor = GestureEditor(new_gesture_data, self)
        self.gesture_editor.save_button.clicked.connect(self.gesture_editor.save_new_gesture)
        self.gesture_editor.delete_button.setVisible(False)
        self.gesture_editor.name_input.setReadOnly(False)
        self.gesture_editor.show()

    def on_gesture_button_clicked(self, gesture_data):
        if gesture_data is None:
            print(f"Gesture was not found")
            return
        self.gesture_editor = GestureEditor(gesture_data, self)
        self.gesture_editor.show()

    def call_launch_astra(self):
        self.is_running = True
        thread = threading.Thread(target=self.recognition.launch_astra)
        thread.start()
        self.ui.label_status.setText("Запускается...")

    def call_shutdown_astra(self):
        self.is_running = False
        self.ui.label_status.setText("Останавливается...")

    def manage_camera(self):
        if self.ui.checkBox_camera.isChecked():
            self.camera = True
        else:
            self.camera = False
