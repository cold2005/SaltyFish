import sys
import numpy as np
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                             QListWidget, QListWidgetItem, QDialog, QDialogButtonBox,
                             QLineEdit, QSpinBox, QDoubleSpinBox, QFormLayout,
                             QInputDialog, QMessageBox, QSizePolicy, QApplication)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QColor
from PyQt6 import QtCore
from utils.data_handler import read_data, write_data
import uuid
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

# 设置Matplotlib中文显示
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题


class RadarChartCanvas(FigureCanvas):
    """Matplotlib雷达图画布（嵌入PyQt6）"""

    def __init__(self, parent=None):
        # 创建图形和子图
        self.fig = Figure(figsize=(8, 6), dpi=100, tight_layout=True)
        super().__init__(self.fig)
        self.setParent(parent)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # 初始化雷达图
        self.ax = self.fig.add_subplot(111, polar=True)
        self.ax.set_theta_zero_location('N')  # 角度0度在北方（上方）
        self.ax.set_theta_direction(-1)  # 角度顺时针增加
        self.ax.set_ylim(0, 100)  # 能力值范围固定0-100
        self.ax.set_yticks(range(0, 101, 20))  # Y轴刻度：0,20,...100
        self.ax.grid(True, alpha=0.3)  # 网格透明度

        # 存储当前数据
        self.abilities = []
        self.values = []

    def update_chart(self, abilities: list):
        """更新雷达图数据（添加线程安全处理）"""
        try:
            # 清空子图
            self.ax.clear()
            self.ax.set_theta_zero_location('N')
            self.ax.set_theta_direction(-1)
            self.ax.set_ylim(0, 100)
            self.ax.set_yticks(range(0, 101, 20))
            self.ax.grid(True, alpha=0.3)

            if not abilities:
                self.ax.text(0.5, 0.5, '暂无能力项数据\n请添加能力项',
                             horizontalalignment='center', verticalalignment='center',
                             transform=self.ax.transAxes, fontsize=14)
                self.draw()
                return

            # 提取能力名称和数值（过滤无效数据）
            self.abilities = [item['name'] for item in abilities if 'name' in item]
            self.values = []
            for item in abilities:
                val = item.get('value', 0.0)
                # 限制数值在0-100之间，避免异常值
                self.values.append(max(0.0, min(100.0, float(val))))

            n = len(self.abilities)
            if n == 0:
                self.draw()
                return

            # 计算角度（避免n=0的除零错误）
            angles = np.linspace(0, 2 * np.pi, n, endpoint=False).tolist()
            values_closed = self.values + [self.values[0]]
            angles_closed = angles + [angles[0]]

            # 绘制雷达图（添加异常捕获）
            self.ax.plot(angles_closed, values_closed, 'o-', linewidth=2, color='#2196F3')
            self.ax.fill(angles_closed, values_closed, alpha=0.25, color='#2196F3')
            self.ax.set_xticks(angles)
            self.ax.set_xticklabels(self.abilities, fontsize=11)

            # 刷新前处理所有UI事件（关键：避免线程阻塞）
            from PyQt6.QtWidgets import QApplication
            QApplication.processEvents()
            self.draw()

        except Exception as e:
            # 捕获所有异常，避免程序崩溃
            print(f"雷达图绘制错误：{str(e)}")
            QMessageBox.warning(None, "绘制错误", f"图表刷新失败：{str(e)}")


class RatingManager(QWidget):
    """能力评价主页面"""
    data_updated = pyqtSignal()  # 数据更新信号（触发雷达图刷新）

    def __init__(self):
        super().__init__()
        self.current_rating_system = None  # 当前评分系统（阶段一默认第一个）
        self.init_ui()
        self.load_rating_data()  # 加载数据
        self.data_updated.connect(self.refresh_radar_chart)  # 绑定数据更新→图表刷新

    def init_ui(self):
        """初始化UI布局"""
        # 主布局（垂直）
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # 1. 顶部区域：标题 + 功能按钮
        top_layout = QHBoxLayout()

        # 标题
        title_label = QLabel("综合能力评价")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title_label.setFont(title_font)
        top_layout.addWidget(title_label)

        # 功能按钮（居右）
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)

        # 添加能力项按钮
        self.add_ability_btn = QPushButton("添加能力项")
        self.add_ability_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        self.add_ability_btn.clicked.connect(self.add_ability)
        btn_layout.addWidget(self.add_ability_btn)

        # 编辑段位按钮
        self.edit_rank_btn = QPushButton("编辑段位")
        self.edit_rank_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #388E3C;
            }
        """)
        self.edit_rank_btn.clicked.connect(self.edit_rank_rules)
        btn_layout.addWidget(self.edit_rank_btn)

        # 刷新图表按钮
        self.refresh_chart_btn = QPushButton("刷新图表")
        self.refresh_chart_btn.setStyleSheet("""
            QPushButton {
                background-color: #f0f0f0;
                color: #333;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """)
        self.refresh_chart_btn.clicked.connect(self.refresh_radar_chart)
        btn_layout.addWidget(self.refresh_chart_btn)

        top_layout.addStretch()
        top_layout.addLayout(btn_layout)
        main_layout.addLayout(top_layout)

        # 2. 中间区域：左侧能力项列表 + 右侧雷达图（水平布局）
        middle_layout = QHBoxLayout()
        middle_layout.setSpacing(20)  # 左右区域间距20px
        middle_layout.setContentsMargins(0, 0, 0, 0)

        # 左侧：能力项列表（优化宽度和样式）
        self.ability_list = QListWidget()
        self.ability_list.setStyleSheet("""
                QListWidget {
                    border: 1px solid #e0e0e0;
                    border-radius: 6px;
                    background-color: white;
                    padding: 5px;
                }
                QListWidget::item {
                    border-bottom: 1px solid #f0f0f0;
                }
                QListWidget::item:hover {
                    background-color: #f5f9ff;
                    border-radius: 4px;
                }
            """)
        self.ability_list.setMinimumWidth(300)  # 最小宽度300px，确保可见
        middle_layout.addWidget(self.ability_list, stretch=1)  # 左侧权重1

        # 右侧：雷达图（占2/3宽度）
        chart_container = QWidget()
        chart_layout = QVBoxLayout(chart_container)
        chart_layout.setContentsMargins(0, 0, 0, 0)

        self.radar_canvas = RadarChartCanvas()
        self.toolbar = NavigationToolbar(self.radar_canvas, chart_container)
        chart_layout.addWidget(self.toolbar)
        chart_layout.addWidget(self.radar_canvas)

        middle_layout.addWidget(chart_container, stretch=2)  # 右侧权重2（左侧1:右侧2）

        main_layout.addLayout(middle_layout, stretch=1)

    def load_rating_data(self):
        """加载评分系统数据（核心数据交互）"""
        # 读取JSON数据
        data = read_data()
        rating_systems = data.get("rating_systems", [])

        # 阶段一默认使用第一个评分系统
        if rating_systems:
            self.current_rating_system = rating_systems[0]
            # 更新能力项列表
            self.update_ability_list()
            # 初始化雷达图
            self.refresh_radar_chart()
        else:
            # 无评分系统时创建默认（理论上不会触发，data_handler已初始化）
            self.create_default_rating_system()

    def delete_ability(self, ability_id: str, ability_name: str):
        """删除能力项"""
        # 二次确认
        reply = QMessageBox.question(
            self, "确认删除", f"是否确定删除能力项「{ability_name}」？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        if reply != QMessageBox.StandardButton.Yes:
            return

        # 1. 更新内存数据
        abilities = self.current_rating_system["abilities"]
        self.current_rating_system["abilities"] = [a for a in abilities if a["id"] != ability_id]

        # 2. 写入JSON
        data = read_data()
        for rs in data["rating_systems"]:
            if rs["id"] == self.current_rating_system["id"]:
                rs["abilities"] = self.current_rating_system["abilities"]
                break
        write_result = write_data(data)

        if write_result:
            QMessageBox.information(self, "成功", f"能力项「{ability_name}」已删除！")
            # 3. 刷新UI
            self.update_ability_list()
            self.data_updated.emit()
        else:
            QMessageBox.warning(self, "失败", "删除失败，请重试！")

    def update_ability_list(self):
        """更新能力项列表（优化UI显示，突出段位标签）"""
        self.ability_list.clear()
        abilities = self.current_rating_system.get("abilities", [])
        rank_rules = self.current_rating_system.get("rank_rules", [])

        # 统一设置字体（确保中文显示清晰）
        default_font = QFont("Microsoft YaHei", 10)  # 微软雅黑，10号字

        for ability in abilities:
            # 1. 创建列表项（固定足够高度，避免内容挤压）
            item = QListWidgetItem()
            item.setData(Qt.ItemDataRole.UserRole, ability["id"])
            item.setSizeHint(QtCore.QSize(0, 60))  # 高度60px，宽度自适应

            # 2. 列表项内容布局
            item_widget = QWidget()
            item_widget.setFont(default_font)  # 统一字体
            item_layout = QHBoxLayout(item_widget)
            item_layout.setContentsMargins(15, 10, 15, 10)  # 内边距：上下10，左右15
            item_layout.setSpacing(15)  # 控件间距15px

            # 能力名称（加宽标签，避免文字截断）
            name_label = QLabel(ability["name"])
            name_label.setFont(default_font)
            name_label.setFixedWidth(100)  # 加宽到100px，容纳更长名称
            name_label.setAlignment(Qt.AlignmentFlag.AlignVCenter)  # 垂直居中
            item_layout.addWidget(name_label)

            # 能力数值输入框（优化尺寸和字体）
            value_spin = QDoubleSpinBox()
            value_spin.setFont(default_font)
            value_spin.setRange(0.0, 100.0)
            value_spin.setSingleStep(1.0)  # 步长改为1，更易操作
            value_spin.setValue(ability["value"])
            value_spin.setFixedWidth(90)  # 加宽输入框
            value_spin.setAlignment(Qt.AlignmentFlag.AlignCenter)  # 数值居中
            value_spin.setReadOnly(False)
            # 绑定修改事件
            value_spin.editingFinished.connect(
                lambda aid=ability["id"], spin=value_spin: self.update_ability_value(aid, spin.value())
            )
            item_layout.addWidget(value_spin)

            # 段位标签（优化文字显示）

            rank = self.get_ability_rank(ability["value"])
            rank_label = QLabel(f"段位:{rank}")
            # 关键修复：调整字体和对齐方式

            rank_label.setFont(QFont("Microsoft YaHei", 11, QFont.Weight.Bold))  # 确保字体支持中文
            rank_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # 强制居中对齐
            rank_label.setStyleSheet(f"""
                QLabel {{
                    background-color: {self.get_rank_color(rank)};
                    color: white;
                    padding: 6px 16px;
                    border-radius: 8px;
                    min-width: 80px;
                    text-align: center;  # 确保文字水平居中
                    vertical-align: middle;  # 确保文字垂直居中
                    border: 2px solid {self.get_rank_border_color(rank)};
                    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
                    letter-spacing: 2px;  # 增加字间距，避免拥挤
                }}
            """)
            rank_label.setFixedHeight(36)
            # 新增：强制文本不换行
            rank_label.setWordWrap(False)
            item_layout.addWidget(rank_label)

            # 填充空白，将删除按钮推到最右侧
            item_layout.addStretch()

            # 删除按钮（保持原有样式，避免抢镜）
            delete_btn = QPushButton("删除")
            delete_btn.setFont(default_font)
            delete_btn.setFixedSize(70, 30)  # 加大按钮
            delete_btn.setStyleSheet("""
                QPushButton {
                    background-color: #F44336;
                    color: white;
                    border: none;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #D32F2F;
                    border: 1px solid #b71c1c;  # hover时加边框
                }
                QPushButton:pressed {
                    background-color: #c62828;
                }
            """)
            delete_btn.clicked.connect(
                lambda checked, aid=ability["id"], name=ability["name"]: self.delete_ability(aid, name)
            )
            item_layout.addWidget(delete_btn)

            # 3. 设置列表项
            self.ability_list.addItem(item)
            self.ability_list.setItemWidget(item, item_widget)

    # 新增：为段位标签添加边框颜色（与背景色协调，增强层次感）
    def get_rank_border_color(self, rank: str) -> str:
        """根据段位返回边框颜色（比背景色深一度）"""
        border_colors = {
            "S": "#C2185B",  # 深粉色
            "A": "#1565C0",  # 深蓝色
            "B": "#2E7D32",  # 深绿色
            "C": "#F57C00",  # 深黄色
            "D": "#E65100",  # 深橙色
            "E": "#616161",  # 深灰色
            "F": "#B71C1C"  # 深红色
        }
        return border_colors.get(rank, "#616161")

    def get_ability_rank(self, value: float) -> str:
        """根据能力值匹配段位（核心逻辑）"""
        rank_rules = self.current_rating_system.get("rank_rules", [])
        # 按最小值降序排序（确保高段位优先匹配）
        sorted_rules = sorted(rank_rules, key=lambda x: x["min"], reverse=True)

        for rule in sorted_rules:
            if rule["min"] <= value <= rule["max"]:
                return rule["rank"]
        return "F"  # 默认返回最低段位

    def get_rank_color(self, rank: str) -> str:
        """根据段位返回颜色（美化UI）"""
        rank_colors = {
            "S": "#FF4081",  # 粉色
            "A": "#2196F3",  # 蓝色
            "B": "#4CAF50",  # 绿色
            "C": "#FFC107",  # 黄色
            "D": "#FF9800",  # 橙色
            "E": "#9E9E9E",  # 灰色
            "F": "#F44336"  # 红色
        }
        return rank_colors.get(rank, "#9E9E9E")

    def update_ability_value(self, ability_id: str, new_value: float):
        """更新能力值（避免重复刷新）"""
        # 1. 限制数值范围并保留1位小数
        new_value = round(max(0.0, min(100.0, new_value)), 1)

        # 2. 查找并更新对应能力项
        abilities = self.current_rating_system["abilities"]
        target_ability = None
        for ab in abilities:
            if ab["id"] == ability_id:
                target_ability = ab
                break
        if not target_ability:
            return  # 未找到能力项，直接返回

        # 3. 数值未变化则不刷新
        if target_ability["value"] == new_value:
            return

        # 4. 更新数值并保存
        target_ability["value"] = new_value
        try:
            data = read_data()
            for rs in data["rating_systems"]:
                if rs["id"] == self.current_rating_system["id"]:
                    rs["abilities"] = abilities
                    break
            write_data(data)
        except Exception as e:
            QMessageBox.warning(self, "保存失败", f"数据写入错误：{str(e)}")
            return

        # 5. 刷新UI（分步刷新，减少压力）
        self.update_ability_list()  # 先更新列表
        # 延迟刷新图表，避免UI阻塞
        from PyQt6.QtCore import QTimer
        QTimer.singleShot(100, self.refresh_radar_chart)  # 100ms后刷新图表

    def add_ability(self):
        """添加能力项（弹窗交互）"""
        name, ok = QInputDialog.getText(self, "添加能力项", "请输入能力项名称：")
        if not ok or not name.strip():
            return

        # 1. 构造新能力项数据
        new_ability = {
            "id": f"ability_{uuid.uuid4().hex[:8]}",
            "name": name.strip(),
            "value": 0.0  # 默认值0
        }

        # 2. 更新内存数据
        self.current_rating_system["abilities"].append(new_ability)

        # 3. 写入JSON
        data = read_data()
        for rs in data["rating_systems"]:
            if rs["id"] == self.current_rating_system["id"]:
                rs["abilities"].append(new_ability)
                break
        write_result = write_data(data)

        if write_result:
            QMessageBox.information(self, "成功", f"能力项「{name}」添加成功！")
            # 4. 刷新UI
            self.update_ability_list()
            self.data_updated.emit()
        else:
            QMessageBox.warning(self, "失败", "能力项添加失败，请重试！")

    def edit_rank_rules(self):
        """编辑段位规则（弹窗交互）"""
        # 修复：将 rank_rules 作为第一个参数传递
        dialog = RankRuleDialog(self.current_rating_system["rank_rules"], self)
        if dialog.exec():
            # 1. 获取修改后的段位规则
            updated_rules = dialog.get_updated_rules()
            # 2. 验证规则合法性（区间不重叠、覆盖0-100）
            if self.validate_rank_rules(updated_rules):
                # 3. 更新数据
                self.current_rating_system["rank_rules"] = updated_rules
                data = read_data()
                for rs in data["rating_systems"]:
                    if rs["id"] == self.current_rating_system["id"]:
                        rs["rank_rules"] = updated_rules
                        break
                write_data(data)

                QMessageBox.information(self, "成功", "段位规则修改成功！")
                # 4. 刷新UI（段位标签会重新匹配）
                self.update_ability_list()
            else:
                QMessageBox.warning(self, "错误", "段位规则不合法（区间重叠或未覆盖0-100）！")

    def validate_rank_rules(self, rules: list) -> bool:
        """验证段位规则合法性"""
        if not rules:
            return False

        # 1. 按最小值升序排序
        sorted_rules = sorted(rules, key=lambda x: x["min"])
        # 2. 检查是否覆盖0-100
        if sorted_rules[0]["min"] > 0 or sorted_rules[-1]["max"] < 100:
            return False
        # 3. 检查区间是否连续不重叠
        for i in range(1, len(sorted_rules)):
            if sorted_rules[i]["min"] <= sorted_rules[i - 1]["max"]:
                return False
        return True

    def refresh_radar_chart(self):
        """刷新雷达图（添加异常捕获）"""
        try:
            if self.current_rating_system:
                abilities = self.current_rating_system.get("abilities", [])
                self.radar_canvas.update_chart(abilities)
        except Exception as e:
            QMessageBox.critical(self, "图表刷新失败", f"错误详情：{str(e)}")
            print(f"雷达图刷新错误：{e}")  # 控制台输出详细错误，便于调试

    def create_default_rating_system(self):
        """创建默认评分系统（容错处理）"""
        default_rank_rules = [
            {"rank": "S", "min": 90, "max": 100},
            {"rank": "A", "min": 80, "max": 89},
            {"rank": "B", "min": 70, "max": 79},
            {"rank": "C", "min": 60, "max": 69},
            {"rank": "D", "min": 50, "max": 59},
            {"rank": "E", "min": 40, "max": 49},
            {"rank": "F", "min": 0, "max": 39}
        ]
        default_abilities = [
            {"id": f"ability_{uuid.uuid4().hex[:8]}", "name": "学习能力", "value": 60},
            {"id": f"ability_{uuid.uuid4().hex[:8]}", "name": "执行能力", "value": 55},
            {"id": f"ability_{uuid.uuid4().hex[:8]}", "name": "自律能力", "value": 50},
            {"id": f"ability_{uuid.uuid4().hex[:8]}", "name": "创新能力", "value": 70}
        ]
        new_rating_system = {
            "id": f"rating_{uuid.uuid4().hex[:8]}",
            "name": "综合能力",
            "abilities": default_abilities,
            "rank_rules": default_rank_rules
        }

        # 写入JSON
        data = read_data()
        data["rating_systems"].append(new_rating_system)
        write_data(data)

        # 更新当前评分系统
        self.current_rating_system = new_rating_system
        self.update_ability_list()
        self.refresh_radar_chart()


class RankRuleDialog(QDialog):
    """编辑段位规则对话框"""

    def __init__(self, rank_rules: list, parent=None):
        super().__init__(parent)
        self.rank_rules = rank_rules.copy()  # 复制原始规则（避免直接修改）
        self.init_dialog_ui()

    def init_dialog_ui(self):
        """初始化对话框UI"""
        self.setWindowTitle("编辑段位规则")
        self.setFixedSize(400, 400)
        self.setModal(True)

        # 布局：滚动区域 + 按钮
        main_layout = QVBoxLayout(self)

        # 表单布局（显示每个段位的区间）
        self.form_layout = QFormLayout()
        self.form_layout.setSpacing(15)

        # 为每个段位创建输入框
        self.rank_inputs = []  # 存储（段位标签, 最小值输入框, 最大值输入框）
        for rule in self.rank_rules:
            rank_label = QLabel(f"{rule['rank']} 段位")
            # 最小值输入框
            min_spin = QSpinBox()
            min_spin.setRange(0, 100)
            min_spin.setValue(rule["min"])
            # 最大值输入框
            max_spin = QSpinBox()
            max_spin.setRange(0, 100)
            max_spin.setValue(rule["max"])

            self.rank_inputs.append((rule["rank"], min_spin, max_spin))
            self.form_layout.addRow(rank_label, self._create_range_widget(min_spin, max_spin))

        main_layout.addLayout(self.form_layout)

        # 确认/取消按钮
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel,
            Qt.Orientation.Horizontal, self
        )
        buttons.button(QDialogButtonBox.StandardButton.Ok).setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                padding: 6px 12px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        buttons.button(QDialogButtonBox.StandardButton.Cancel).setStyleSheet("""
            QPushButton {
                background-color: #f0f0f0;
                color: #333;
                border: none;
                padding: 6px 12px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        main_layout.addWidget(buttons)

    def _create_range_widget(self, min_spin: QSpinBox, max_spin: QSpinBox) -> QWidget:
        """创建「最小值-最大值」组合控件"""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        layout.addWidget(QLabel("最小值："))
        layout.addWidget(min_spin)
        layout.addWidget(QLabel("最大值："))
        layout.addWidget(max_spin)

        return widget

    def get_updated_rules(self) -> list:
        """获取修改后的段位规则"""
        updated_rules = []
        for rank, min_spin, max_spin in self.rank_inputs:
            updated_rules.append({
                "rank": rank,
                "min": min_spin.value(),
                "max": max_spin.value()
            })
        return updated_rules


# 测试代码（直接运行该文件可测试页面）
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RatingManager()
    window.setFixedSize(800, 600)
    window.setWindowTitle("能力评价测试")
    window.show()
    sys.exit(app.exec())