from PyQt5 import QtWidgets
from utils.loading_gestures import *


class GestureEditor(QtWidgets.QWidget):
    def __init__(self, gesture_data, ui, parent=None):
        super(GestureEditor, self).__init__(parent)
        self.ui = ui

        self.setWindowTitle(f"Редактировать {gesture_data['name']}")
        self.gesture_data = gesture_data

        name_label = QtWidgets.QLabel("Имя жеста:")
        self.name_input = QtWidgets.QLineEdit()
        self.name_input.setText(gesture_data["name"])
        self.name_input.setReadOnly(True)  # Отключаем редактирование

        button_label = QtWidgets.QLabel("Кнопка/клавиша:")
        self.button_edit = QtWidgets.QLineEdit()
        button_text = ', '.join(gesture_data["key_or_mouse_button"])
        self.button_edit.setText(button_text)

        delay_label = QtWidgets.QLabel("Задержка после жеста (сек):")
        self.delay_spinbox = QtWidgets.QDoubleSpinBox()
        self.delay_spinbox.setValue(gesture_data["delay_after_gesture"])

        type_label = QtWidgets.QLabel("Тип жеста:")
        self.type_edit = QtWidgets.QLineEdit()
        self.type_edit.setText(gesture_data["type"])

        requirement_label = QtWidgets.QLabel("Требование:")
        self.requirement_edit = QtWidgets.QLineEdit()
        self.requirement_edit.setText(gesture_data.get("requirement", ""))

        block_if_label = QtWidgets.QLabel("Блокировать если:")
        self.block_if_edit = QtWidgets.QLineEdit()
        self.block_if_edit.setText(gesture_data.get("block_if", ""))

        distances_label = QtWidgets.QLabel("Дистанции:")
        add_distance_button = QtWidgets.QPushButton("Добавить дистанцию")
        add_distance_button.clicked.connect(self.add_distance_field)

        self.distances_layout = QtWidgets.QVBoxLayout()
        self.distances_widgets = []

        self.distances_layout.addWidget(distances_label)
        self.distances_layout.addWidget(add_distance_button)

        self.delete_button = QtWidgets.QPushButton("Удалить жест")
        self.delete_button.clicked.connect(self.delete_gesture)

        for key, value in gesture_data["distances"].items():
            self.add_distance_field(key, value)

        layout = QtWidgets.QFormLayout()
        layout.addRow(name_label, self.name_input)
        layout.addRow(button_label, self.button_edit)
        layout.addRow(delay_label, self.delay_spinbox)
        layout.addRow(type_label, self.type_edit)
        layout.addRow(requirement_label, self.requirement_edit)
        layout.addRow(block_if_label, self.block_if_edit)

        layout.addRow(self.distances_layout)
        layout.addRow(self.delete_button)

        self.save_button = QtWidgets.QPushButton("Сохранить")
        self.save_button.clicked.connect(self.save_and_close)
        layout.addRow(self.save_button)

        self.setLayout(layout)

    def add_distance_field(self, key="", value=""):
        distance_widget = QtWidgets.QWidget()
        distance_layout = QtWidgets.QHBoxLayout()
        if not key or not value:
            key, value = "0-1", 30
        key_edit = QtWidgets.QLineEdit()
        key_edit.setText(key)
        value_edit = QtWidgets.QLineEdit()
        value_edit.setText(str(value))
        remove_button = QtWidgets.QPushButton("Удалить")
        remove_button.clicked.connect(lambda: self.remove_distance_field(distance_widget))

        distance_layout.addWidget(key_edit)
        distance_layout.addWidget(value_edit)
        distance_layout.addWidget(remove_button)

        distance_widget.setLayout(distance_layout)

        self.distances_layout.insertWidget(self.distances_layout.count() - 1, distance_widget)
        self.distances_widgets.append(distance_widget)

    def remove_distance_field(self, widget):
        self.distances_layout.removeWidget(widget)
        widget.deleteLater()
        self.distances_widgets.remove(widget)

    def delete_gesture(self):
        confirm_dialog = QtWidgets.QMessageBox(self)
        confirm_dialog.setIcon(QtWidgets.QMessageBox.Question)
        confirm_dialog.setText("Вы уверены, что хотите удалить этот жест?")
        confirm_dialog.setWindowTitle("Подтверждение удаления")
        confirm_dialog.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)

        if confirm_dialog.exec() == QtWidgets.QMessageBox.Yes:
            remove_gesture(self.gesture_data['name'])
            self.ui.update_gestures()
            self.close()

    def save_new_gesture(self):
        save_gesture_data(self.gesture_data)
        self.ui.update_gestures()
        self.close()

    def save_and_close(self):
        self.gesture_data["name"] = self.name_input.text()
        button_text = self.button_edit.text()
        self.gesture_data["key_or_mouse_button"] = button_text.split(", ")
        self.gesture_data["delay_after_gesture"] = self.delay_spinbox.value()
        self.gesture_data["type"] = self.type_edit.text()
        self.gesture_data["requirement"] = self.requirement_edit.text()
        self.gesture_data["block_if"] = self.block_if_edit.text()

        self.gesture_data["distances"] = {}
        for widget in self.distances_widgets:
            key_edit = widget.layout().itemAt(0).widget()
            value_edit = widget.layout().itemAt(1).widget()
            key = key_edit.text().strip()
            value = int(value_edit.text().strip())
            self.gesture_data["distances"][key] = value

        update_gesture_data(self.gesture_data)
        self.close()
