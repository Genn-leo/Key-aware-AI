from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QColor, QFont

def status_label(text, color="green"):
    label = QLabel(text)
    label.setFont(QFont("Segoe UI", 11, QFont.Bold))
    label.setStyleSheet(f"color: {color};")
    return label
