import sys
from pathlib import Path
from PyQt6.QtGui import QAction, QPalette, QColor, QTextFormat, QCursor
from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout,
                             QWidget, QMenu)
from PyQt6.QtCore import Qt, QSize, QTimer
from datetime import datetime
from text_check import TextCheck


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.check_tool = TextCheck()
        self.start_time = None  # if None game is not started

        self.setWindowTitle("Typing Speed Test")
        self.setFixedSize(QSize(700, 500))

        main_vertical_layout = QVBoxLayout()
        main_vertical_layout.setContentsMargins(100, 0, 100, 0)

        # main widgets

        title_label = QLabel()
        title_label.setObjectName("title_label")
        title_label.setText("Typing Speed Test")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # score board

        self.score_board = QLabel()
        self.score_board.setObjectName("score_board")
        self.score_board.setText("Words Per Minute: ?")

        self.time_left = QLabel()
        self.time_left.setObjectName("time_left")
        self.update_time_left()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time_left)
        self.timer.start(100)

        self.restart_button = QPushButton()
        self.restart_button.clicked.connect(self.restart_game)
        self.restart_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.restart_button.setText("Restart")
        self.restart_button.setObjectName("restart")

        score_layout = QHBoxLayout()
        score_layout.addWidget(self.score_board)
        score_layout.addWidget(self.time_left)
        score_layout.addWidget(self.restart_button)
        score_layout_widget = QWidget()
        score_layout_widget.setObjectName("score_layout")
        score_layout_widget.setLayout(score_layout)

        # target text box

        self.target_text_label = QLabel()
        self.target_text_label.setObjectName("target_text_label")
        self.target_text_label.setText(self.check_tool.get_formatted_text(''))
        self.target_text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # self.target_text_label.setMinimumHeight(4 * self.target_text_label.fontMetrics().lineSpacing())

        self.text_input_field = QLineEdit()
        self.text_input_field.setObjectName("text_input_field")
        self.text_input_field.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.text_input_field.setPlaceholderText("type your words here")
        self.text_input_field.textEdited.connect(self.text_edited)

        # layout

        main_vertical_layout.addStretch()
        main_vertical_layout.addWidget(title_label, alignment=Qt.AlignmentFlag.AlignCenter)
        main_vertical_layout.addWidget(score_layout_widget, alignment=Qt.AlignmentFlag.AlignCenter)
        main_vertical_layout.addWidget(self.target_text_label, alignment=Qt.AlignmentFlag.AlignCenter)
        main_vertical_layout.addWidget(self.text_input_field, alignment=Qt.AlignmentFlag.AlignCenter)
        main_vertical_layout.addStretch()

        widget = QWidget()
        widget.setLayout(main_vertical_layout)
        widget.setFixedWidth(700)
        self.setCentralWidget(widget)

    def text_edited(self, word: str):
        if self.start_time is None:
            self.start_time = datetime.now()

        if word != '' and word.count(' ') < len(word) and word[-1] == ' ':
            # space was printed (word submitted)
            self.check_tool.next_word(word[:-1])
            self.text_input_field.setText('')
            self.target_text_label.setText(self.check_tool.get_formatted_text(''))

            elapsed_seconds = (datetime.now() - self.start_time).seconds
            # check words per minute
            if elapsed_seconds > 5:
                wpm = int(self.check_tool.correct_characters / 5 * 60 / elapsed_seconds)
                self.score_board.setText(f"Words Per Minute: {wpm}")

            # stop game if 60 seconds passed
            if elapsed_seconds >= 60:
                self.text_input_field.setReadOnly(True)
                self.target_text_label.setText(f"Your typing speed is<br>{wpm} words per minute")
        else:
            self.target_text_label.setText(self.check_tool.get_formatted_text(word))

    def update_time_left(self):
        if self.start_time is None:
            self.time_left.setText("Time Left: 60")
        else:
            elapsed_seconds = (datetime.now() - self.start_time).seconds
            time_left = 60 - elapsed_seconds if elapsed_seconds <= 60 else 0
            self.time_left.setText(f"Time Left: {time_left}")

    def restart_game(self):
        self.start_time = None
        self.check_tool.restart()
        self.target_text_label.setText(self.check_tool.get_formatted_text(""))
        self.score_board.setText("Words Per Minute: ?")
        self.text_input_field.setReadOnly(False)
        self.text_input_field.setText('')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(Path('style.qss').read_text())

    window = MainWindow()
    window.show()

    app.exec()
