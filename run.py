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

        # 設定整體配色
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#f0f8ff"))  # 背景淺藍
        palette.setColor(QPalette.ColorRole.WindowText, QColor("#000080"))  # 深藍文字
        self.setPalette(palette)

        # 設定字體
        self.setFont(QFont("Microsoft YaHei", 10))

        # 標籤字體與顏色
        label_style = "font-size: 14px; color: #2f4f4f;"
        result_style = "font-size: 16px; font-weight: bold; color: #8b0000;"

        # 距離選單
        self.distance_label = QLabel("選擇距離 (公里):", self)
        self.distance_label.setStyleSheet(label_style)
        self.distance_combo = QComboBox(self)
        self.distance_combo.addItems(["5", "10", "21.1", "42.2"])

        # 時間選單
        self.time_label = QLabel("選擇完成時間:", self)
        self.time_label.setStyleSheet(label_style)
        self.hour_combo = QComboBox(self)
        self.hour_combo.addItems([f"{i:02}" for i in range(0, 6)])
        self.minute_combo = QComboBox(self)
        self.minute_combo.addItems([f"{i:02}" for i in range(0, 60)])
        self.second_combo = QComboBox(self)
        self.second_combo.addItems([f"{i:02}" for i in range(0, 60)])

        # 計算按鈕
        self.calculate_button = QPushButton("計算配速", self)
        self.calculate_button.setStyleSheet("background-color: #4682b4; color: white; font-size: 14px; padding: 6px; border-radius: 5px;")
        self.calculate_button.clicked.connect(self.calculate_pace)

        # 結果顯示
        self.result_label = QLabel("配速: 尚未計算", self)
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.result_label.setStyleSheet(result_style)

        # 配速建議
        self.easy_run_label = QLabel("Easy Run 配速: 尚未計算", self)
        self.easy_run_label.setStyleSheet(label_style)
        self.tempo_run_label = QLabel("Tempo Run 配速: 尚未計算", self)
        self.tempo_run_label.setStyleSheet(label_style)
        self.lsd_run_label = QLabel("LSD 配速: 尚未計算", self)
        self.lsd_run_label.setStyleSheet(label_style)
        self.interval_run_label = QLabel("Interval Run 配速: 尚未計算", self)
        self.interval_run_label.setStyleSheet(label_style)

        # 激勵語錄
        self.motivation_label = QLabel("激勵語: ""跑步讓你更強大！加油！", self)
        self.motivation_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.motivation_label.setStyleSheet("font-size: 14px; color: #2e8b57; font-style: italic;")

        # 訓練計劃標籤
        self.training_plan_label = QLabel("16 週訓練計劃", self)
        self.training_plan_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.training_plan_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #8b0000;")

        # 訓練計劃內容
        self.training_plan_text = QTextEdit(self)
        self.training_plan_text.setReadOnly(True)
        self.training_plan_text.setStyleSheet("font-size: 12px; background-color: #f5f5f5; border: 1px solid #ccc; padding: 5px;")
        self.training_plan_text.setText(self.generate_training_plan())

        # 設定佈局
        layout = QVBoxLayout()

        input_layout1 = QHBoxLayout()
        input_layout1.addWidget(self.distance_label)
        input_layout1.addWidget(self.distance_combo)

        input_layout2 = QHBoxLayout()
        input_layout2.addWidget(self.time_label)
        input_layout2.addWidget(self.hour_combo)
        input_layout2.addWidget(QLabel(":", self))
        input_layout2.addWidget(self.minute_combo)
        input_layout2.addWidget(QLabel(":", self))
        input_layout2.addWidget(self.second_combo)

        layout.addLayout(input_layout1)
        layout.addLayout(input_layout2)
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

    def calculate_pace(self):
        try:
            # 獲取距離與時間
            distance = float(self.distance_combo.currentText())
            h = int(self.hour_combo.currentText())
            m = int(self.minute_combo.currentText())
            s = int(self.second_combo.currentText())

            # 將時間轉換為總秒數
            total_seconds = h * 3600 + m * 60 + s

            # 計算配速 (每公里秒數)
            pace_seconds = total_seconds / distance

            # 格式化配速為 mm:ss
            pace_minutes = int(pace_seconds // 60)
            pace_seconds = int(pace_seconds % 60)
            self.result_label.setText(f"配速: {pace_minutes:02}:{pace_seconds:02} 分/公里")

            # 計算不同類型跑步的建議配速
            easy_pace_seconds = total_seconds / distance * 1.2
            tempo_pace_seconds = total_seconds / distance * 0.9
            lsd_pace_seconds = total_seconds / distance * 1.3
            interval_pace_seconds = total_seconds / distance * 0.8

            self.easy_run_label.setText(self.format_pace("Easy Run 配速", easy_pace_seconds))
            self.tempo_run_label.setText(self.format_pace("Tempo Run 配速", tempo_pace_seconds))
            self.lsd_run_label.setText(self.format_pace("LSD 配速", lsd_pace_seconds))
            self.interval_run_label.setText(self.format_pace("Interval Run 配速", interval_pace_seconds))

        except Exception as e:
            self.result_label.setText("輸入有誤，請重新選擇！")
            self.easy_run_label.setText("Easy Run 配速: 尚未計算")
            self.tempo_run_label.setText("Tempo Run 配速: 尚未計算")
            self.lsd_run_label.setText("LSD 配速: 尚未計算")
            self.interval_run_label.setText("Interval Run 配速: 尚未計算")

    def format_pace(self, label, pace_seconds):
        pace_minutes = int(pace_seconds // 60)
        pace_seconds = int(pace_seconds % 60)
        return f"{label}: {pace_minutes:02}:{pace_seconds:02} 分/公里"

    def generate_training_plan(self):
        motivation_phrases = [
            "跑步讓你更強大！加油！",
            "每一步都是一種進步！",
            "你比昨天的自己更強！",
            "堅持就是勝利！",
            "相信自己，你可以做到！",
            "每一次的挑戰都是一種成長！",
            "越過極限，成為更好的自己！",
            "你正在為你的目標而努力！",
            "無論多困難，不要放棄！",
            "跑步教會我們堅持的力量！",
            "今天的努力是為了明天的成功！",
            "勇敢地面對每一天的挑戰！",
            "熱愛跑步，熱愛生活！",
            "每一次奔跑都是一次心靈的釋放！",
            "跑步改變的不只是體能，還有心態！",
            "你的努力將會被看到！",
            "持之以恆，夢想成真！",
            "跑步是最好的自我投資！",
            "快樂地跑起來吧！",
            "每一次流汗都是進步的證明！"
        ]

        training_plan = ""
        week_motivation = random.sample(motivation_phrases, 4)

        for week in range(1, 17):
            training_plan += f"第 {week} 週:\n"
            week_index = (week - 1) // 4
            if (week - 1) % 4 == 0:
                training_plan += f"激勵語: {week_motivation[week_index]}\n"

            if week <= 4:
                training_plan += (
                    "  - 週一: Easy Run 5 公里 配速 6:30 分/公里\n"
                    "  - 週二: 間休\n"
                    "  - 週三: Tempo Run 6 公里 配速 5:45 分/公里\n"
                    "  - 週四: 間休\n"
                    "  - 週五: Easy Run 5 公里 配速 6:30 分/公里\n"
                    "  - 週六: LSD 10 公里 配速 7:15 分/公里\n"
                    "  - 週日: 間休\n"
                )
            elif week <= 8:
                training_plan += (
                    "  - 週一: Easy Run 6 公里 配速 6:30 分/公里\n"
                    "  - 週二: 間休\n"
                    "  - 週三: Tempo Run 7 公里 配速 5:45 分/公里\n"
                    "  - 週四: 間休\n"
                    "  - 週五: Easy Run 6 公里 配速 6:30 分/公里\n"
                    "  - 週六: LSD 12 公里 配速 7:15 分/公里\n"
                    "  - 週日: 間休\n"
                )
            elif week <= 12:
                training_plan += (
                    "  - 週一: Easy Run 7 公里 配速 6:20 分/公里\n"
                    "  - 週二: 間休\n"
                    "  - 週三: Tempo Run 8 公里 配速 5:40 分/公里\n"
                    "  - 週四: 間休\n"
                    "  - 週五: Easy Run 7 公里 配速 6:20 分/公里\n"
                    "  - 週六: LSD 15 公里 配速 7:10 分/公里\n"
                    "  - 週日: 間休\n"
                )
            else:
                training_plan += (
                    "  - 週一: Easy Run 8 公里 配速 6:10 分/公里\n"
                    "  - 週二: 間休\n"
                    "  - 週三: Tempo Run 9 公里 配速 5:35 分/公里\n"
                    "  - 週四: 間休\n"
                    "  - 週五: Easy Run 8 公里 配速 6:10 分/公里\n"
                    "  - 週六: LSD 18 公里 配速 7:00 分/公里\n"
                    "  - 週日: 間休\n"
                )

        return training_plan

# 主程式入口
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PaceCalculator()
    window.show()
    sys.exit(app.exec())
