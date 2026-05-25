import sys
import json
import aigrep_core
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLineEdit, QCheckBox, 
                             QPushButton, QTextEdit, QGridLayout, QGroupBox)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class AIGrepWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AIGrep - AI Destekli Kod Operasyon Aracı")
        self.resize(850, 650)
        self.setStyleSheet("""
            QMainWindow { background-color: #1e1e1e; color: #ffffff; }
            QLabel { color: #cccccc; font-weight: bold; }
            QLineEdit, QTextEdit { background-color: #2d2d2d; color: #ffffff; border: 1px solid #3d3d3d; border-radius: 5px; padding: 5px; }
            QGroupBox { color: #ffffff; border: 1px solid #3d3d3d; border-radius: 5px; margin-top: 10px; font-weight: bold; }
            QPushButton { background-color: #0e639c; color: white; border-radius: 5px; padding: 10px; font-weight: bold; }
            QPushButton#aiButton { background-color: #4CAF50; }
        """)
        self.current_results = []
        self.initUI()

    def initUI(self):
        central_widget = QWidget()
        main_layout = QVBoxLayout()

        # Girişler
        input_layout = QGridLayout()
        self.pattern_input = QLineEdit("def")
        self.path_input = QLineEdit(".")
        self.type_input = QLineEdit("py")
        input_layout.addWidget(QLabel("Arama deseni:"), 0, 0); input_layout.addWidget(self.pattern_input, 0, 1)
        input_layout.addWidget(QLabel("Klasör yolu:"), 1, 0); input_layout.addWidget(self.path_input, 1, 1)
        input_layout.addWidget(QLabel("Dosya tipi:"), 2, 0); input_layout.addWidget(self.type_input, 2, 1)
        main_layout.addLayout(input_layout)

        # Bayraklar
        flags_group = QGroupBox("Bayraklar")
        flags_layout = QGridLayout()
        self.flags = {
            "-i": QCheckBox("-i (Büyük/Küçük Harf)"), "-n": QCheckBox("-n (Satır No)"),
            "-w": QCheckBox("-w (Tam Kelime)"), "-l": QCheckBox("-l (Sadece Dosya)"),
            "--stats": QCheckBox("--stats (İstatistik)"), "-U": QCheckBox("-U (Çok Satır)")
        }
        row, col = 0, 0
        for key, cb in self.flags.items():
            flags_layout.addWidget(cb, row, col)
            col += 1
            if col > 2: col = 0; row += 1
        flags_group.setLayout(flags_layout)
        main_layout.addWidget(flags_group)

        # Komut Önizleme
        self.command_output = QLineEdit(); self.command_output.setReadOnly(True)
        self.command_output.setStyleSheet("background-color: #1a1a1a; color: #569cd6; border: 1px solid #4CAF50;")
        main_layout.addWidget(QLabel("Oluşturulan Komut (Canlı):")); main_layout.addWidget(self.command_output)

        # Butonlar
        btn_layout = QHBoxLayout()
        self.btn_run = QPushButton("▶ Arama Yap")
        self.btn_ai = QPushButton("✨ AI ile Analiz Et")
        self.btn_ai.setObjectName("aiButton")
        btn_layout.addWidget(self.btn_run); btn_layout.addWidget(self.btn_ai)
        main_layout.addLayout(btn_layout)

        # Sonuç
        self.result_area = QTextEdit()
        self.result_area.setReadOnly(True)
        main_layout.addWidget(self.result_area)

        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Bağlantılar
        self.btn_run.clicked.connect(self.run_search)
        self.btn_ai.clicked.connect(self.export_to_json)
        self.pattern_input.textChanged.connect(self.update_command)
        for cb in self.flags.values(): cb.stateChanged.connect(self.update_command)
        self.update_command()

    def update_command(self):
        active_flags = [f for f, cb in self.flags.items() if cb.isChecked()]
        cmd = f"rg {' '.join(active_flags)} --type {self.type_input.text()} '{self.pattern_input.text()}' {self.path_input.text()}"
        self.command_output.setText(cmd)

    def run_search(self):
        self.current_results = aigrep_core.arama_yap(self.pattern_input.text(), self.path_input.text(), ext_list=[f".{self.type_input.text()}"])
        self.result_area.clear()
        for res in self.current_results:
            self.result_area.append(f"[{res['file']}:{res['line_number']}] -> {res['original_content']}")
        self.result_area.append(f"\n✅ Toplam {len(self.current_results)} eşleşme bulundu.")

    def export_to_json(self):
        if not self.current_results:
            self.result_area.append("❌ Önce arama yapmalısın!")
            return
        with open('analysis.json', 'w', encoding='utf-8') as f:
            json.dump(self.current_results, f, indent=4)
        self.result_area.append(f"\n✨ Analiz verileri 'analysis.json' dosyasına başarıyla yazıldı!")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AIGrepWindow()
    window.show()
    sys.exit(app.exec_())