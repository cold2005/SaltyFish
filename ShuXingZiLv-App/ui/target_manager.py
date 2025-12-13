import sys
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                             QTreeWidget, QTreeWidgetItem, QDialog, QFormLayout,
                             QLineEdit, QDateEdit, QSpinBox, QMessageBox, QHeaderView)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont, QColor
from utils.data_handler import read_data, write_data
from datetime import datetime
import uuid

class TargetDialog(QDialog):
    """添加/编辑目标的对话框"""
    def __init__(self, initial_data=None, parent_data=None, is_sub=False):
        super().__init__()
        self.initial_data = initial_data
        self.parent_data = parent_data  # 父任务数据（用于子任务继承）
        self.is_sub = is_sub  # 是否为子任务
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("编辑目标" if self.initial_data else "添加目标")
        layout = QFormLayout(self)
        self.setFixedSize(350, 220)  # 固定窗口大小

        # 目标名称
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("请输入目标名称")
        if self.is_sub and self.parent_data:
            parent_name = self.parent_data.get("name", "子任务")
            children_count = self._get_parent_children_count()
            self.name_edit.setText(f"{parent_name}-子任务{children_count + 1}")

        # 截止时间
        self.deadline_edit = QDateEdit(QDate.currentDate().addDays(7))
        self.deadline_edit.setDisplayFormat("yyyy-MM-dd")
        self.deadline_edit.setMinimumDate(QDate.currentDate())
        if self.is_sub and self.parent_data:
            try:
                parent_deadline = QDate.fromString(self.parent_data["deadline"], "yyyy-MM-dd")
                self.deadline_edit.setDate(parent_deadline)
                self.deadline_edit.setMaximumDate(parent_deadline)
            except:
                pass  # 兼容无效日期

        # 奖励积分
        self.points_edit = QSpinBox()
        self.points_edit.setRange(0, 1000)
        self.points_edit.setSuffix(" 分")
        if self.is_sub and self.parent_data:
            parent_points = self.parent_data.get("points", 10)
            default_points = max(1, int(parent_points / 3))
            self.points_edit.setValue(default_points)
        else:
            self.points_edit.setValue(10)

        # 填充初始数据（编辑模式）
        if self.initial_data:
            self.name_edit.setText(self.initial_data.get("name", ""))
            try:
                deadline = QDate.fromString(self.initial_data["deadline"], "yyyy-MM-dd")
                self.deadline_edit.setDate(deadline)
            except:
                pass
            self.points_edit.setValue(self.initial_data.get("points", 0))

        # 添加控件到布局
        layout.addRow("目标名称：", self.name_edit)
        layout.addRow("截止时间：", self.deadline_edit)
        layout.addRow("奖励积分：", self.points_edit)

        # 确认/取消按钮
        btn_layout = QHBoxLayout()
        self.ok_btn = QPushButton("确认")
        self.cancel_btn = QPushButton("取消")
        self.ok_btn.clicked.connect(self._on_confirm)
        self.cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(self.ok_btn)
        btn_layout.addWidget(self.cancel_btn)
        layout.addRow(btn_layout)

    def _get_parent_children_count(self):
        """获取父任务的子任务数量"""
        if not self.parent_data or "id" not in self.parent_data:
            return 0
        parent_id = self.parent_data["id"]
        data = read_data()
        targets = data.get("targets", [])
        return len([t for t in targets if t.get("parent_id") == parent_id])

    def _on_confirm(self):
        """确认按钮验证"""
        name = self.name_edit.text().strip()
        if not name:
            QMessageBox.warning(self, "输入错误", "目标名称不能为空！")
            return
        self.accept()

    def get_data(self):
        """返回对话框数据"""
        return {
            "name": self.name_edit.text().strip(),
            "deadline": self.deadline_edit.date().toString("yyyy-MM-dd"),
            "points": self.points_edit.value()
        }



class TargetManager(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.load_targets()  # 加载数据

    def init_ui(self):
        # 主布局（确保绑定到当前窗口）
        main_layout = QVBoxLayout(self)
        self.setLayout(main_layout)  # 显式设置布局，避免控件不显示

        # 1. 顶部区域：标题+按钮
        top_layout = QHBoxLayout()
        self.title = QLabel("目标管理")
        self.title.setFont(QFont("Microsoft YaHei", 14, QFont.Weight.Bold))
        self.add_btn = QPushButton("添加目标")
        self.add_sub_btn = QPushButton("添加子任务")
        self.refresh_btn = QPushButton("刷新列表")
        self.add_sub_btn.setEnabled(False)  # 初始置灰

        top_layout.addWidget(self.title)
        top_layout.addStretch()
        top_layout.addWidget(self.add_btn)
        top_layout.addWidget(self.add_sub_btn)
        top_layout.addWidget(self.refresh_btn)
        main_layout.addLayout(top_layout)

        # 2. 中间区域：树形控件（核心修复：列宽和布局）
        self.tree_widget = QTreeWidget()
        self.tree_widget.setHeaderLabels(["目标名称", "截止时间", "完成状态", "奖励积分"])
        # 修复列宽设置：确保"完成状态"列（索引2）不被拉伸挤压
        self.tree_widget.setColumnWidth(0, 250)    # 目标名称
        self.tree_widget.setColumnWidth(1, 120)    # 截止时间
        self.tree_widget.setColumnWidth(2, 100)    # 完成状态（按钮宽度）
        self.tree_widget.setColumnWidth(3, 100)    # 奖励积分
        # 禁止列宽自动拉伸导致按钮不可见
        self.tree_widget.header().setSectionResizeMode(0, QHeaderView.ResizeMode.Interactive)
        self.tree_widget.header().setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)
        self.tree_widget.header().setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)  # 固定完成状态列宽
        self.tree_widget.header().setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        # 其他属性
        self.tree_widget.setSelectionMode(QTreeWidget.SelectionMode.SingleSelection)
        self.tree_widget.setDragEnabled(True)
        self.tree_widget.setAcceptDrops(True)
        self.tree_widget.setDropIndicatorShown(True)
        self.tree_widget.itemSelectionChanged.connect(self.on_item_selected)
        main_layout.addWidget(self.tree_widget)  # 添加到主布局

        # 3. 底部区域：编辑/删除按钮
        bottom_layout = QHBoxLayout()
        self.edit_btn = QPushButton("编辑")
        self.delete_btn = QPushButton("删除")
        self.edit_btn.setEnabled(False)
        self.delete_btn.setEnabled(False)
        bottom_layout.addStretch()
        bottom_layout.addWidget(self.edit_btn)
        bottom_layout.addWidget(self.delete_btn)
        main_layout.addLayout(bottom_layout)

        # 绑定按钮事件
        self.add_btn.clicked.connect(lambda: self.show_add_dialog())
        self.add_sub_btn.clicked.connect(self.show_add_sub_dialog)
        self.refresh_btn.clicked.connect(self.load_targets)
        self.edit_btn.clicked.connect(self.edit_target)
        self.delete_btn.clicked.connect(self.delete_target)

        # 设置窗口最小尺寸，避免控件挤压
        self.setMinimumSize(800, 600)

    def load_targets(self):
        """加载目标数据（增强兼容性处理）"""
        self.tree_widget.clear()
        try:
            data = read_data()
            # 确保targets字段存在
            if "targets" not in data:
                data["targets"] = []
            # 为旧数据补充必要字段（防止缺失字段导致崩溃）
            for target in data["targets"]:
                # 补充parent_id（默认为root）
                if "parent_id" not in target:
                    target["parent_id"] = "root"
                # 补充status（默认为未开始）
                if "status" not in target:
                    target["status"] = "未开始"
                # 补充id（防止无id导致后续操作崩溃）
                if "id" not in target:
                    target["id"] = str(uuid.uuid4())
            write_data(data)  # 保存修复后的数据

            # 构建树形结构
            targets = data["targets"]
            root_items = [t for t in targets if t["parent_id"] == "root"]
            for root in root_items:
                root_item = self.create_tree_item(root)
                self.tree_widget.addTopLevelItem(root_item)
                self.add_children(root_item, root["id"], targets)
        except Exception as e:
            QMessageBox.critical(self, "加载失败", f"数据加载出错：{str(e)}")

    def create_tree_item(self, target):
        """创建树形节点（确保按钮显示及事件绑定正确）"""
        item = QTreeWidgetItem([
            target["name"],
            target["deadline"],
            "",  # 完成状态由按钮控制
            str(target["points"])
        ])
        item.setData(0, Qt.ItemDataRole.UserRole, target["id"])  # 存储任务ID

        # 创建完成/已完成按钮
        status_btn = QPushButton(self.tree_widget)  # 显式设置父控件
        if target["status"] == "已完成":
            status_btn.setText("已完成")
            status_btn.setStyleSheet("""
                QPushButton { 
                    background-color: #f0f0f0; 
                    color: #666; 
                    border: 1px solid #ccc; 
                    border-radius: 3px;
                    padding: 2px 8px;
                    min-width: 60px;
                }
            """)
        else:
            status_btn.setText("完成")
            status_btn.setStyleSheet("""
                QPushButton { 
                    background-color: #e6f7ff; 
                    color: #1890ff; 
                    border: 1px solid #91d5ff; 
                    border-radius: 3px;
                    padding: 2px 8px;
                    min-width: 60px;
                }
                QPushButton:hover {
                    background-color: #bae7ff;
                }
            """)

        # 关键修复：显式获取并处理目标ID，避免引用错误
        target_id = target.get("id", "")  # 安全获取ID，不存在则返回空字符串
        if not target_id:  # 若ID缺失，自动生成新ID（兜底处理）
            target_id = str(uuid.uuid4())
            # 同步更新target的id（确保数据一致性）
            target["id"] = target_id

        # 绑定按钮点击事件（使用处理后的target_id）
        status_btn.clicked.connect(
            lambda checked, tid=target_id: self.on_button_status_toggle(tid)
        )

        # 将按钮添加到第3列
        self.tree_widget.setItemWidget(item, 2, status_btn)

        # 已完成任务文字变灰
        if target["status"] == "已完成":
            for col in range(4):
                item.setForeground(col, QColor(128, 128, 128))

        return item

    def add_children(self, parent_item, parent_id, targets):
        """递归添加子节点（增加异常捕获）"""
        try:
            children = [t for t in targets if t["parent_id"] == parent_id]
            for child in children:
                child_item = self.create_tree_item(child)
                parent_item.addChild(child_item)
                self.add_children(child_item, child["id"], targets)
        except Exception as e:
            QMessageBox.warning(self, "添加子节点失败", f"错误：{str(e)}")

    def on_item_selected(self):
        """选中节点时启用按钮（增加空值判断）"""
        try:
            selected_items = self.tree_widget.selectedItems()
            if selected_items and len(selected_items) > 0:
                self.add_sub_btn.setEnabled(True)
                self.edit_btn.setEnabled(True)
                self.delete_btn.setEnabled(True)
            else:
                self.add_sub_btn.setEnabled(False)
                self.edit_btn.setEnabled(False)
                self.delete_btn.setEnabled(False)
        except Exception as e:
            QMessageBox.warning(self, "选择失败", f"错误：{str(e)}")

    def show_add_dialog(self, parent_id="root", parent_data=None):
        """显示添加对话框（增加异常处理）"""
        try:
            dialog = TargetDialog(parent_data=parent_data, is_sub=parent_id != "root")
            if dialog.exec():
                target_data = dialog.get_data()
                # 验证数据有效性
                if not target_data["name"].strip():
                    QMessageBox.warning(self, "输入错误", "目标名称不能为空")
                    return
                # 补充必要字段
                target_data["id"] = str(uuid.uuid4())
                target_data["parent_id"] = parent_id
                target_data["status"] = "未开始"
                # 保存数据
                data = read_data()
                if "targets" not in data:
                    data["targets"] = []
                data["targets"].append(target_data)
                write_data(data)
                self.load_targets()
        except Exception as e:
            QMessageBox.critical(self, "添加失败", f"错误：{str(e)}")

    def show_add_sub_dialog(self):
        """添加子任务（增加选中项验证）"""
        try:
            selected_items = self.tree_widget.selectedItems()
            if not selected_items:
                return
            selected_item = selected_items[0]
            parent_id = selected_item.data(0, Qt.ItemDataRole.UserRole)
            data = read_data()
            parent_data = next((t for t in data["targets"] if t["id"] == parent_id), None)
            if parent_data:
                self.show_add_dialog(parent_id=parent_id, parent_data=parent_data)
        except Exception as e:
            QMessageBox.warning(self, "添加子任务失败", f"错误：{str(e)}")

    def on_button_status_toggle(self, target_id):
        """处理完成按钮点击（增强数据验证）"""
        try:
            data = read_data()
            target = next((t for t in data["targets"] if t["id"] == target_id), None)
            if not target:
                QMessageBox.warning(self, "错误", "未找到该任务数据")
                return

            # 切换状态（其余逻辑与原代码一致）
            new_status = "未开始" if target["status"] == "已完成" else "已完成"
            old_status = target["status"]
            target["status"] = new_status

            # 积分处理
            if "points_account" not in data:
                data["points_account"] = {"total": 0, "records": []}
            if old_status != "已完成" and new_status == "已完成":
                data["points_account"]["total"] += target["points"]
                data["points_account"]["records"].append({
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "reason": f"完成任务：{target['name']}",
                    "points": target["points"]
                })
            elif old_status == "已完成" and new_status != "已完成":
                data["points_account"]["total"] -= target["points"]
                data["points_account"]["records"].append({
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "reason": f"取消完成任务：{target['name']}",
                    "points": -target["points"]
                })

            # 父子任务联动
            parent_id = target["parent_id"]
            if parent_id != "root":
                self.check_parent_complete(parent_id, data)
            if new_status == "未开始":
                self.reset_children_status(target_id, data)

            write_data(data)
            self.load_targets()
        except Exception as e:
            QMessageBox.critical(self, "状态更新失败", f"错误：{str(e)}")

    def check_parent_complete(self, parent_id, data):
        """检查父任务是否自动完成"""
        try:
            parent = next((t for t in data["targets"] if t["id"] == parent_id), None)
            if not parent:
                return
            children = [t for t in data["targets"] if t["parent_id"] == parent_id]
            if all(child["status"] == "已完成" for child in children):
                parent["status"] = "已完成"
                grandparent_id = parent["parent_id"]
                if grandparent_id != "root":
                    self.check_parent_complete(grandparent_id, data)
            else:
                parent["status"] = "未开始"
        except Exception as e:
            QMessageBox.warning(self, "联动失败", f"父任务状态更新错误：{str(e)}")

    def reset_children_status(self, parent_id, data):
        """重置子任务状态"""
        try:
            children = [t for t in data["targets"] if t["parent_id"] == parent_id]
            for child in children:
                child["status"] = "未开始"
                self.reset_children_status(child["id"], data)
        except Exception as e:
            QMessageBox.warning(self, "联动失败", f"子任务状态重置错误：{str(e)}")

    def edit_target(self):
        """编辑目标（修复闪退问题：增加完整异常处理）"""
        try:
            selected_items = self.tree_widget.selectedItems()
            if not selected_items:
                return
            selected_item = selected_items[0]
            target_id = selected_item.data(0, Qt.ItemDataRole.UserRole)
            if not target_id:
                QMessageBox.warning(self, "错误", "未找到任务ID")
                return

            data = read_data()
            target = next((t for t in data["targets"] if t["id"] == target_id), None)
            if not target:
                QMessageBox.warning(self, "错误", "未找到该任务数据")
                return

            # 显示编辑对话框（传入完整的初始数据）
            dialog = TargetDialog(initial_data=target)
            if dialog.exec():
                new_data = dialog.get_data()
                # 验证新数据
                if not new_data["name"].strip():
                    QMessageBox.warning(self, "输入错误", "目标名称不能为空")
                    return
                # 更新数据
                target["name"] = new_data["name"]
                target["deadline"] = new_data["deadline"]
                target["points"] = new_data["points"]
                write_data(data)
                self.load_targets()
        except Exception as e:
            # 捕获所有异常，避免闪退并显示错误信息
            QMessageBox.critical(self, "编辑失败", f"错误：{str(e)}")

    def delete_target(self):
        """删除目标（增加异常处理）"""
        try:
            selected_items = self.tree_widget.selectedItems()
            if not selected_items:
                return
            selected_item = selected_items[0]
            target_id = selected_item.data(0, Qt.ItemDataRole.UserRole)
            if not target_id:
                QMessageBox.warning(self, "错误", "未找到任务ID")
                return

            # 二次确认
            if QMessageBox.question(self, "确认删除",
                                    "确定要删除该目标及所有子任务吗？") != QMessageBox.StandardButton.Yes:
                return

            data = read_data()

            # 递归删除子任务
            def delete_children(parent_id):
                children = [t for t in data["targets"] if t["parent_id"] == parent_id]
                for child in children:
                    delete_children(child["id"])
                    data["targets"].remove(child)

            delete_children(target_id)
            # 删除自身
            target = next((t for t in data["targets"] if t["id"] == target_id), None)
            if target:
                data["targets"].remove(target)
            write_data(data)
            self.load_targets()
        except Exception as e:
            QMessageBox.critical(self, "删除失败", f"错误：{str(e)}")