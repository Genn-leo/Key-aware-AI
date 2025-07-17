import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import threading
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QTextEdit, QVBoxLayout, QMessageBox
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from core.monitor import main as start_monitoring
from core.retrain_model import retrain_model
from scanner.api_detector import scan_api_usage
from scanner.file_checker import scan_files
from scanner.process_scanner import scan_processes
from scanner.registry_scanner import scan_registry

LOG_FILE = "data/detection_log.txt"

class KeyAwareAIWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("KeyAwareAI - Keylogger Detection")
        self.setGeometry(300, 200, 800, 500)
        self.setStyleSheet("background-color: #1e1e1e; color: white;")

        self.running = False
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        title = QLabel(" KeyAwareAI")
        title.setFont(QFont("Segoe UI", 20))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        self.start_btn = QPushButton(" Start Scanner")
        self.start_btn.setStyleSheet("background-color: #00af91; color: white; font-weight: bold;")
        self.start_btn.clicked.connect(self.toggle_scan)
        layout.addWidget(self.start_btn)

        retrain_btn = QPushButton(" Retrain AI")
        retrain_btn.setStyleSheet("background-color: #7d5fff; color: white; font-weight: bold;")
        retrain_btn.clicked.connect(self.retrain_model)
        layout.addWidget(retrain_btn)

        scan_btn = QPushButton(" Run Full System Scan")
        scan_btn.setStyleSheet("background-color: #ff6b6b; color: white; font-weight: bold;")
        scan_btn.clicked.connect(self.run_full_scan)
        layout.addWidget(scan_btn)

        refresh_btn = QPushButton(" Refresh Logs")
        refresh_btn.setStyleSheet("background-color: #ffb142; color: black; font-weight: bold;")
        refresh_btn.clicked.connect(self.refresh_logs)
        layout.addWidget(refresh_btn)

        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        self.log_area.setStyleSheet("background-color: #2d2d2d; color: #ffffff;")
        layout.addWidget(self.log_area)

        self.setLayout(layout)
        self.refresh_logs()

    def toggle_scan(self):
        if not self.running:
            self.running = True
            self.start_btn.setText(" Scanner Running...")
            self.start_btn.setStyleSheet("background-color: #ff3f34; color: white; font-weight: bold;")
            threading.Thread(target=start_monitoring, daemon=True).start()
        else:
            QMessageBox.information(self, "Running", "Scanner is already running in the background.")

    def retrain_model(self):
        retrain_model()
        QMessageBox.information(self, "Retrain", " AI model retrained successfully!")

    def refresh_logs(self):
        self.log_area.clear()
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r") as f:
                self.log_area.setPlainText(f.read())
        else:
            self.log_area.setPlainText(" No logs found yet...")

    def run_full_scan(self):
        results = []

        try:
            api_results = scan_api_usage()
            if api_results:
                results.append(" API Scan:\n" + "\n".join(api_results))
        except Exception as e:
            results.append(f" API Scan Error: {e}")

        try:
            file_results = scan_files()
            if file_results:
                results.append(" File Scan:\n" + "\n".join(file_results))
        except Exception as e:
            results.append(f" File Scan Error: {e}")

        try:
            process_results = scan_processes()
            if process_results:
                results.append(" Process Scan:\n" + "\n".join(process_results))
        except Exception as e:
            results.append(f" Process Scan Error: {e}")

        try:
            reg_results = scan_registry()
            if reg_results:
                results.append(" Registry Scan:\n" + "\n".join(reg_results))
        except Exception as e:
            results.append(f" Registry Scan Error: {e}")

        if results:
            full_report = "\n\n".join(results)
            self.log_area.append("\n\n Full Scan Results:\n" + full_report)
            QMessageBox.warning(self, "Suspicious Activity Found!", full_report)
        else:
            self.log_area.append("\n Full Scan: No suspicious activity found.")
            QMessageBox.information(self, "System Clean", "No suspicious behavior detected.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = KeyAwareAIWindow()
    window.show()
    sys.exit(app.exec_())
