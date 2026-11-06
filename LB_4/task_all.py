import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QTabWidget, QVBoxLayout, QLabel, QPushButton,
    QLineEdit, QComboBox, QCheckBox, QSlider, QSpinBox, QMessageBox,
    QMainWindow, QTextEdit, QFileDialog, QToolBar, QListWidget, QDialog,
    QFormLayout, QInputDialog, QDialogButtonBox, QGroupBox, QHBoxLayout
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QAction, QKeySequence

class Task1Widget(QWidget):
    def __init__(self):
        super().__init__()
        main_layout = QVBoxLayout()
        form_group = QGroupBox("Форма введення даних")
        form_layout = QFormLayout()

        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Введіть ваше ім'я...")
        self.name_edit.setToolTip("Введіть повне ім'я користувача")
        form_layout.addRow(QLabel("Ім'я користувача:"), self.name_edit)

        self.role_combo = QComboBox()
        self.role_combo.addItems(["Студент", "Викладач", "Розробник", "Адміністратор"])
        self.role_combo.setToolTip("Оберіть вашу роль у системі")
        form_layout.addRow(QLabel("Роль:"), self.role_combo)

        self.age_slider = QSlider(Qt.Orientation.Horizontal)
        self.age_slider.setRange(16, 80)
        self.age_slider.setValue(20)
        self.age_slider.setToolTip("Оберіть вік за допомогою повзунка")
        form_layout.addRow(QLabel("Вік:"), self.age_slider)

        form_group.setLayout(form_layout)
        main_layout.addWidget(form_group)

        self.agree_check = QCheckBox("Я погоджуюся з умовами використання")
        self.agree_check.setChecked(True)
        main_layout.addWidget(self.agree_check)

        button_layout = QHBoxLayout()
        self.btn_reset = QPushButton("Скинути")
        self.btn_submit = QPushButton("Надіслати")
        self.btn_submit.setEnabled(False)

        button_layout.addWidget(self.btn_reset)
        button_layout.addWidget(self.btn_submit)
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

class Task2Widget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Введіть ім'я (мін. 2 символи)")

        self.score_spinbox = QSpinBox()
        self.score_spinbox.setRange(0, 100)
        self.score_spinbox.setValue(50)

        self.confirm_checkbox = QCheckBox("Підтверджую правильність даних")
        self.info_label = QLabel("Значення балу: 50")
        self.status_label = QLabel("Статус: Очікування введення")

        self.btn_submit = QPushButton("Підтвердити")
        self.btn_submit.setEnabled(False)
        self.btn_reset = QPushButton("Скинути")

        layout.addWidget(QLabel("Ім'я:"))
        layout.addWidget(self.name_input)
        layout.addWidget(QLabel("Бал:"))
        layout.addWidget(self.score_spinbox)
        layout.addWidget(self.info_label)
        layout.addWidget(self.confirm_checkbox)
        layout.addWidget(self.status_label)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.btn_reset)
        btn_layout.addWidget(self.btn_submit)
        layout.addLayout(btn_layout)
        self.setLayout(layout)

        
        self.score_spinbox.valueChanged.connect(lambda v: self.info_label.setText(f"Значення балу: {v}"))
        self.confirm_checkbox.toggled.connect(self.btn_submit.setEnabled)
        self.name_input.textChanged.connect(lambda text: self.status_label.setText(f"Введено символів: {len(text)}"))
        self.btn_submit.clicked.connect(self.validate_and_submit)
        self.btn_reset.clicked.connect(self.reset_form)

    def validate_and_submit(self):
        name = self.name_input.text().strip()
        if len(name) < 2:
            QMessageBox.warning(self, "Помилка", "Ім'я має містити щонайменше 2 символи!")
        elif self.score_spinbox.value() < 60:
            QMessageBox.warning(self, "Помилка", "Прохідний бал має бути не менше 60!")
        else:
            QMessageBox.information(self, "Успіх", f"Дані збережено!\nІм'я: {name}\nБал: {self.score_spinbox.value()}")

    def reset_form(self):
        self.name_input.clear()
        self.score_spinbox.setValue(50)
        self.confirm_checkbox.setChecked(False)
        self.status_label.setText("Статус: Форму скинуто")


class Task3Widget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.text_edit = QTextEdit()
        self.setCentralWidget(self.text_edit)
        self.text_edit.textChanged.connect(self.update_status_bar)

        self.statusBar().showMessage("Готовий до роботи")

        action_open = QAction("Відкрити", self)
        action_open.setShortcut(QKeySequence.StandardKey.Open)
        action_open.triggered.connect(self.open_file)

        action_clear = QAction("Очистити", self)
        action_clear.setShortcut(QKeySequence("Cmd+K"))
        action_clear.triggered.connect(self.text_edit.clear)

        action_about = QAction("Про програму", self)
        action_about.triggered.connect(lambda: QMessageBox.about(self, "Про програму", "Текстовий редактор (Завдання 3)"))

        menu_bar = self.menuBar()
        menu_bar.setNativeMenuBar(False) # Для macOS

        file_menu = menu_bar.addMenu("Файл")
        file_menu.addAction(action_open)
        file_menu.addAction(action_clear)

        help_menu = menu_bar.addMenu("Довідка")
        help_menu.addAction(action_about)

        toolbar = QToolBar("Панель")
        self.addToolBar(toolbar)
        toolbar.addAction(action_open)
        toolbar.addAction(action_clear)

    def update_status_bar(self):
        self.statusBar().showMessage(f"Кількість символів: {len(self.text_edit.toPlainText())}")

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Відкрити файл", "", "Text Files (*.txt);;All Files (*)")
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as f:
                self.text_edit.setText(f.read())


class InputComponent(QWidget):
    item_added = pyqtSignal(str)
    data_cleared = pyqtSignal(int, str)

    def __init__(self):
        super().__init__()
        layout = QHBoxLayout()
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Введіть елемент...")
        btn_add = QPushButton("Додати")
        btn_clear = QPushButton("Скинути все")

        btn_add.clicked.connect(self.emit_add)
        btn_clear.clicked.connect(lambda: self.data_cleared.emit(200, "Список очищено"))

        layout.addWidget(self.input_field)
        layout.addWidget(btn_add)
        layout.addWidget(btn_clear)
        self.setLayout(layout)

    def emit_add(self):
        text = self.input_field.text().strip()
        if text:
            self.item_added.emit(text)
            self.input_field.clear()

class DisplayComponent(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.list_widget = QListWidget()
        self.status_label = QLabel("Статус: Очікування")