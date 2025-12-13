import sys
import warnings
import matplotlib

warnings.filterwarnings('ignore', category=DeprecationWarning, module='PyQt6.QtCore')
warnings.filterwarnings('ignore', category=UserWarning, module='matplotlib')

from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QStackedWidget)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette, QColor

# 集成 Matplotlib QT 后端
import matplotlib

matplotlib.use('QtAgg')

# 导入页面组件（新增RatingManager）
from ui.target_manager import TargetManager
from ui.rating_manager import RatingManager


class TreeSelfDisciplineApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # 1. 主窗口基础设置
        self.setWindowTitle("树行自律 - 个人评价与自律系统")
        self.setFixedSize(800, 600)
        self.center_window()

        # 2. 主容器与布局
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 3. 页面容器（QStackedWidget）
        self.stacked_widget = QStackedWidget()
        self.init_pages()  # 初始化页面（修改：添加能力评价页面）
        main_layout.addWidget(self.stacked_widget, stretch=1)

        # 4. 底部导航栏
        self.nav_buttons = []
        nav_layout = QHBoxLayout()
        nav_layout.setContentsMargins(0, 0, 0, 0)
        nav_layout.setSpacing(0)

        nav_items = [
            ("目标管理", 0),
            ("能力评价", 1),
            ("成长记录", 2),
            ("自律管控", 3)
        ]

        for text, index in nav_items:
            btn = self.create_nav_button(text, index)
            self.nav_buttons.append(btn)
            nav_layout.addWidget(btn, stretch=1)

        main_layout.addLayout(nav_layout)
        self.set_selected_button(0)

    def init_pages(self):
        """初始化页面（核心修改：添加实际功能页面）"""
        # 页面1：目标管理（已实现）
        self.target_page = TargetManager()
        self.stacked_widget.addWidget(self.target_page)

        # 页面2：能力评价（本次新增）
        self.rating_page = RatingManager()
        self.stacked_widget.addWidget(self.rating_page)

        # 页面3-4：空白占位页面（后续开发）
        page_colors = [
            QColor(242, 243, 244),  # 成长记录页面
            QColor(239, 240, 241)  # 自律管控页面
        ]

        for color in page_colors:
            page = QWidget()
            page.setAutoFillBackground(True)
            palette = QPalette()
            palette.setColor(QPalette.ColorRole.Window, color)
            page.setPalette(palette)
            self.stacked_widget.addWidget(page)

    def create_nav_button(self, text, index):
        btn = QPushButton(text)
        btn.setStyleSheet("""
            QPushButton {
                border: none;
                background-color: #ffffff;
                color: #333333;
                font-size: 14px;
                height: 50px;
                font-weight: 500;
                font-family: 'Microsoft YaHei', 'Segoe UI', sans-serif;
            }
            QPushButton:hover:!checked {
                background-color: #f0f0f0;
            }
            QPushButton:checked {
                background-color: #2196F3;
                color: #ffffff;
            }
        """)
        btn.clicked.connect(lambda _, idx=index: self.switch_page(idx))
        btn.setCheckable(True)
        btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        return btn

    def switch_page(self, index):
        self.stacked_widget.setCurrentIndex(index)
        self.set_selected_button(index)

    def set_selected_button(self, index):
        for i, btn in enumerate(self.nav_buttons):
            btn.setChecked(i == index)

    def center_window(self):
        screen_geometry = QApplication.primaryScreen().availableGeometry()
        window_geometry = self.frameGeometry()
        window_geometry.moveCenter(screen_geometry.center())
        self.move(window_geometry.topLeft())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TreeSelfDisciplineApp()
    window.show()
    sys.exit(app.exec())