import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                           QHBoxLayout, QTextEdit, QComboBox, QLabel, QPushButton)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QTextCharFormat, QTextCursor
from pyfiglet import Figlet, FigletFont
from colorama import Fore, Back, Style, init

# 初始化colorama
init()

class FigletGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Figlet 艺术字生成器  V1.0     by:yoruaki 公众号:夜秋的小屋")
        self.setMinimumSize(800, 600)
        
        # 创建主窗口部件
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        
        # 创建顶部控制区域
        controls_layout = QHBoxLayout()
        
        # 创建字体选择区域
        font_label = QLabel("选择字体:")
        self.font_combo = QComboBox()
        self.load_fonts()
        controls_layout.addWidget(font_label)
        controls_layout.addWidget(self.font_combo)
        
        # 创建颜色选择区域
        color_label = QLabel("文字颜色:")
        self.color_combo = QComboBox()
        self.load_colors()
        controls_layout.addWidget(color_label)
        controls_layout.addWidget(self.color_combo)
        
        # 创建背景色选择区域
        bg_color_label = QLabel("背景颜色:")
        self.bg_color_combo = QComboBox()
        self.load_bg_colors()
        controls_layout.addWidget(bg_color_label)
        controls_layout.addWidget(self.bg_color_combo)
        controls_layout.addStretch()
        
        # 创建第二行控制区域
        controls_layout2 = QHBoxLayout()
        
        # 添加文本方向选择
        direction_label = QLabel("文本方向:")
        self.direction_combo = QComboBox()
        self.direction_combo.addItems(["auto", "left-to-right", "right-to-left"])
        controls_layout2.addWidget(direction_label)
        controls_layout2.addWidget(self.direction_combo)
        
        # 添加对齐方式选择
        justify_label = QLabel("对齐方式:")
        self.justify_combo = QComboBox()
        self.justify_combo.addItems(["auto", "left", "center", "right"])
        controls_layout2.addWidget(justify_label)
        controls_layout2.addWidget(self.justify_combo)
        
        controls_layout2.addStretch()
        
        # 创建输入区域
        input_label = QLabel("输入文本:")
        self.input_text = QTextEdit()
        self.input_text.setMaximumHeight(100)
        self.input_text.setPlaceholderText("在这里输入要转换的文本...")
        
        # 创建输出区域
        output_label = QLabel("生成结果:")
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setFont(self.get_monospace_font())
        
        # 创建生成按钮
        self.generate_btn = QPushButton("生成艺术字")
        self.generate_btn.clicked.connect(self.generate_art)
        
        # 添加所有部件到布局
        layout.addLayout(controls_layout)
        layout.addLayout(controls_layout2)
        layout.addWidget(input_label)
        layout.addWidget(self.input_text)
        layout.addWidget(self.generate_btn)
        layout.addWidget(output_label)
        layout.addWidget(self.output_text)
        
        # 连接信号
        self.font_combo.currentTextChanged.connect(self.generate_art)
        self.input_text.textChanged.connect(self.generate_art)
        self.color_combo.currentTextChanged.connect(self.generate_art)
        self.bg_color_combo.currentTextChanged.connect(self.generate_art)
        self.direction_combo.currentTextChanged.connect(self.generate_art)
        self.justify_combo.currentTextChanged.connect(self.generate_art)
    
    def load_fonts(self):
        """加载所有可用的 Figlet 字体"""
        fonts = FigletFont.getFonts()
        self.font_combo.addItems(sorted(fonts))
        # 设置默认字体
        default_index = self.font_combo.findText("standard")
        if default_index >= 0:
            self.font_combo.setCurrentIndex(default_index)
    
    def load_colors(self):
        """加载所有可用的前景色"""
        self.colors = {
            "默认": (None, None),  # (QColor, Fore.COLOR)
            "黑色": (QColor(0, 0, 0), Fore.BLACK),
            "红色": (QColor(255, 0, 0), Fore.RED),
            "绿色": (QColor(0, 255, 0), Fore.GREEN),
            "黄色": (QColor(255, 255, 0), Fore.YELLOW),
            "蓝色": (QColor(0, 0, 255), Fore.BLUE),
            "品红": (QColor(255, 0, 255), Fore.MAGENTA),
            "青色": (QColor(0, 255, 255), Fore.CYAN),
            "白色": (QColor(255, 255, 255), Fore.WHITE),
            "亮黑色": (QColor(100, 100, 100), Fore.LIGHTBLACK_EX),
            "亮红色": (QColor(255, 100, 100), Fore.LIGHTRED_EX),
            "亮绿色": (QColor(100, 255, 100), Fore.LIGHTGREEN_EX),
            "亮黄色": (QColor(255, 255, 100), Fore.LIGHTYELLOW_EX),
            "亮蓝色": (QColor(100, 100, 255), Fore.LIGHTBLUE_EX),
            "亮品红": (QColor(255, 100, 255), Fore.LIGHTMAGENTA_EX),
            "亮青色": (QColor(100, 255, 255), Fore.LIGHTCYAN_EX),
            "亮白色": (QColor(255, 255, 255, 200), Fore.LIGHTWHITE_EX)
        }
        self.color_combo.addItems(self.colors.keys())
    
    def load_bg_colors(self):
        """加载所有可用的背景色"""
        self.bg_colors = {
            "默认": (None, None),  # (QColor, Back.COLOR)
            "黑色": (QColor(0, 0, 0), Back.BLACK),
            "红色": (QColor(255, 0, 0), Back.RED),
            "绿色": (QColor(0, 255, 0), Back.GREEN),
            "黄色": (QColor(255, 255, 0), Back.YELLOW),
            "蓝色": (QColor(0, 0, 255), Back.BLUE),
            "品红": (QColor(255, 0, 255), Back.MAGENTA),
            "青色": (QColor(0, 255, 255), Back.CYAN),
            "白色": (QColor(255, 255, 255), Back.WHITE),
            "亮黑色": (QColor(100, 100, 100), Back.LIGHTBLACK_EX),
            "亮红色": (QColor(255, 100, 100), Back.LIGHTRED_EX),
            "亮绿色": (QColor(100, 255, 100), Back.LIGHTGREEN_EX),
            "亮黄色": (QColor(255, 255, 100), Back.LIGHTYELLOW_EX),
            "亮蓝色": (QColor(100, 100, 255), Back.LIGHTBLUE_EX),
            "亮品红": (QColor(255, 100, 255), Back.LIGHTMAGENTA_EX),
            "亮青色": (QColor(100, 255, 255), Back.LIGHTCYAN_EX),
            "亮白色": (QColor(255, 255, 255, 200), Back.LIGHTWHITE_EX)
        }
        self.bg_color_combo.addItems(self.bg_colors.keys())
    
    def get_monospace_font(self):
        """获取等宽字体用于显示艺术字"""
        from PyQt6.QtGui import QFont
        font = QFont("Courier New")
        font.setStyleHint(QFont.StyleHint.Monospace)
        return font
    
    def generate_art(self):
        """生成艺术字"""
        text = self.input_text.toPlainText()
        if not text:
            self.output_text.clear()
            return
        
        try:
            # 获取选择的颜色
            qt_color, term_color = self.colors[self.color_combo.currentText()]
            qt_bg_color, term_bg_color = self.bg_colors[self.bg_color_combo.currentText()]
            
            # 生成艺术字
            selected_font = self.font_combo.currentText()
            f = Figlet(
                font=selected_font,
                direction=self.direction_combo.currentText(),
                justify=self.justify_combo.currentText(),
                width=120  # 设置一个合理的宽度
            )
            result = f.renderText(text)
            
            # 在GUI中显示
            self.output_text.clear()
            fmt = QTextCharFormat()
            if qt_color:
                fmt.setForeground(qt_color)
            if qt_bg_color:
                fmt.setBackground(qt_bg_color)
            cursor = self.output_text.textCursor()
            cursor.insertText(result, fmt)
            
            # 在终端中显示
            terminal_output = ""
            for line in result.split('\n'):
                if line.strip():
                    colored_line = ""
                    if term_color:
                        colored_line += term_color
                    if term_bg_color:
                        colored_line += term_bg_color
                    colored_line += line + Style.RESET_ALL
                    terminal_output += colored_line + '\n'
                else:
                    terminal_output += line + '\n'
            print(terminal_output)
            
        except Exception as e:
            error_msg = f"生成出错: {str(e)}"
            self.output_text.setText(error_msg)
            print(error_msg)

def main():
    app = QApplication(sys.argv)
    window = FigletGUI()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 