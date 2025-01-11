import sys
from PyQt6.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QComboBox, QHBoxLayout, QTextEdit
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette, QColor, QFont

import random

class PaceCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("跑步配速計算程式")
        self.resize(500, 600)

        # 配色與字體
        self.setPalette(self.create_palette())
        self.setFont(QFont("Microsoft YaHei", 10))

        # 元件初始化
        self.init_ui()

    def create_palette(self):
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#f0f8ff"))
        palette.setColor(QPalette.ColorRole.WindowText, QColor("#000080"))
        return palette

    def init_ui(self):
        label_style = "font-size: 14px; color: #2f4f4f;"
        result_style = "font-size: 16px; font-weight: bold; color: #8b0000;"

        # 配速輸入區域
        self.distance_label = self.create_label("選擇距離 (公里):", label_style)
        self.distance_combo = self.create_combo(["5", "10", "21.1", "42.2"])
        self.time_label = self.create_label("選擇完成時間:", label_style)
        self.hour_combo = self.create_combo([f"{i:02}" for i in range(6)])
        self.minute_combo = self.create_combo([f"{i:02}" for i in range(60)])
        self.second_combo = self.create_combo([f"{i:02}" for i in range(60)])

        # 計算按鈕
        self.calculate_button = QPushButton("計算配速", self)
        self.calculate_button.setStyleSheet("background-color: #4682b4; color: white; font-size: 14px; padding: 6px; border-radius: 5px;")
        self.calculate_button.clicked.connect(self.calculate_pace)

        # 結果與建議配速
        self.result_label = self.create_label("配速: 尚未計算", result_style, Qt.AlignmentFlag.AlignCenter)
        self.easy_run_label = self.create_label("Easy Run 配速: 尚未計算", label_style)
        self.tempo_run_label = self.create_label("Tempo Run 配速: 尚未計算", label_style)
        self.lsd_run_label = self.create_label("LSD 配速: 尚未計算", label_style)
        self.interval_run_label = self.create_label("Interval Run 配速: 尚未計算", label_style)

        # 激勵語與訓練計劃
        self.motivation_label = self.create_label("激勵語: 跑步讓你更強大！加油！", "font-size: 14px; color: #2e8b57; font-style: italic;", Qt.AlignmentFlag.AlignCenter)
        self.training_plan_label = self.create_label("16 週訓練計劃", "font-size: 16px; font-weight: bold; color: #8b0000;", Qt.AlignmentFlag.AlignCenter)
        self.training_plan_text = QTextEdit(self)
        self.training_plan_text.setReadOnly(True)
        self.training_plan_text.setStyleSheet("font-size: 12px; background-color: #f5f5f5; border: 1px solid #ccc; padding: 5px;")

        # 佈局
        layout = QVBoxLayout()
        layout.addLayout(self.create_input_layout())
        layout.addWidget(self.calculate_button)
        layout.addWidget(self.result_label)
        layout.addWidget(self.easy_run_label)
        layout.addWidget(self.tempo_run_label)
        layout.addWidget(self.lsd_run_label)
        layout.addWidget(self.interval_run_label)
        layout.addWidget(self.motivation_label)
        layout.addWidget(self.training_plan_label)
        layout.addWidget(self.training_plan_text)
        self.setLayout(layout)

    def create_label(self, text, style, alignment=None):
        label = QLabel(text, self)
        label.setStyleSheet(style)
        if alignment:
            label.setAlignment(alignment)
        return label

    def create_combo(self, items):
        combo = QComboBox(self)
        combo.addItems(items)
        return combo

    def create_input_layout(self):
        layout1 = QHBoxLayout()
        layout1.addWidget(self.distance_label)
        layout1.addWidget(self.distance_combo)

        layout2 = QHBoxLayout()
        layout2.addWidget(self.time_label)
        layout2.addWidget(self.hour_combo)
        layout2.addWidget(QLabel(":", self))
        layout2.addWidget(self.minute_combo)
        layout2.addWidget(QLabel(":", self))
        layout2.addWidget(self.second_combo)

        layout = QVBoxLayout()
        layout.addLayout(layout1)
        layout.addLayout(layout2)
        return layout

    def calculate_pace(self):
        try:
            distance = float(self.distance_combo.currentText())
            h, m, s = int(self.hour_combo.currentText()), int(self.minute_combo.currentText()), int(self.second_combo.currentText())
            total_seconds = h * 3600 + m * 60 + s
            pace_seconds = total_seconds / distance

            self.result_label.setText(f"配速: {int(pace_seconds // 60):02}:{int(pace_seconds % 60):02} 分/公里")

            self.easy_run_label.setText(self.format_pace("Easy Run 配速", pace_seconds * 1.2))
            self.tempo_run_label.setText(self.format_pace("Tempo Run 配速", pace_seconds * 0.9))
            self.lsd_run_label.setText(self.format_pace("LSD 配速", pace_seconds * 1.3))
            self.interval_run_label.setText(self.format_pace("Interval Run 配速", pace_seconds * 0.8))

            self.training_plan_text.setText(self.generate_training_plan(pace_seconds))
        except ValueError:
            self.result_label.setText("輸入有誤，請重新選擇！")

    def format_pace(self, label, pace_seconds):
        pace_minutes, pace_seconds = divmod(int(pace_seconds), 60)
        return f"{label}: {pace_minutes:02}:{pace_seconds:02} 分/公里"

    def generate_training_plan(self, base_pace):
        motivation_phrases = [
            "跑步讓你更強大！加油！", "每一步都是一種進步！", "你比昨天的自己更強！", "堅持就是勝利！", "相信自己，你可以做到！",
            "每一次的挑戰都是一種成長！", "越過極限，成為更好的自己！", "你正在為你的目標而努力！", "無論多困難，不要放棄！", "跑步教會我們堅持的力量！",
            "今天的努力是為了明天的成功！", "勇敢地面對每一天的挑戰！", "熱愛跑步，熱愛生活！", "每一次奔跑都是一次心靈的釋放！", "跑步改變的不只是體能，還有心態！",
            "你的努力將會被看到！", "持之以恆，夢想成真！", "跑步是最好的自我投資！", "快樂地跑起來吧！", "每一次流汗都是進步的證明！"
        ]

        weekly_motivation = random.sample(motivation_phrases, 4)
        plan = ""

        for week in range(1, 17):
            plan += f"第 {week} 週:\n"
            if (week - 1) % 4 == 0:
                plan += f"激勵語: {weekly_motivation[(week - 1) // 4]}\n"

            distances = [(5, 1.2), (6, 0.9), (10, 1.3), (5, 1.2)]
            weekdays = ["週一", "週三", "週五", "週六"]
            for i, (distance, multiplier) in enumerate(distances):
                pace = self.format_pace("", base_pace * multiplier)
                plan += f"  - {weekdays[i]}: 跑 {distance} 公里 配速 {pace}\n"

            plan += "  - 其他日: 間休\n"

        return plan

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PaceCalculator()
    window.show()
    sys.exit(app.exec())
