#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QTabWidget, QPushButton, 
                            QFileDialog, QLabel, QGridLayout, QSpinBox, 
                            QDoubleSpinBox, QCheckBox, QListWidget, QHBoxLayout,
                            QGroupBox, QFrame, QSizePolicy, QComboBox)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap

from ui.image_item import ImageItem

class ToolPanel(QWidget):
    """
    工具面板类，包含添加贴图和属性编辑等功能
    """
    
    # 自定义信号
    add_image_signal = pyqtSignal(str)  # 添加贴图信号，参数为文件路径
    grid_visible_changed = pyqtSignal(bool)  # 网格可见性变更信号
    grid_size_changed = pyqtSignal(float)  # 网格大小变更信号
    canvas_size_changed = pyqtSignal(int, int)  # 画布大小变更信号，参数为宽度和高度
    snap_to_grid_changed = pyqtSignal(bool)  # 网格吸附变更信号
    
    def __init__(self, parent=None):
        super(ToolPanel, self).__init__(parent)
        self.init_ui()
        
    def init_ui(self):
        """
        初始化界面
        """
        layout = QVBoxLayout(self)
        
        # 创建选项卡
        self.tab_widget = QTabWidget()
        
        # 添加贴图面板
        self.add_image_tab = QWidget()
        self.init_add_image_tab()
        self.tab_widget.addTab(self.add_image_tab, "添加贴图")
        
        # 属性编辑面板
        self.property_tab = QWidget()
        self.init_property_tab()
        self.tab_widget.addTab(self.property_tab, "属性编辑")
        
        # 层级管理面板
        self.layer_tab = QWidget()
        self.init_layer_tab()
        self.tab_widget.addTab(self.layer_tab, "层级管理")
        
        # 视图设置面板
        self.view_settings_tab = QWidget()
        self.init_view_settings_tab()
        self.tab_widget.addTab(self.view_settings_tab, "视图设置")
        
        layout.addWidget(self.tab_widget)
        self.setLayout(layout)
        
    def init_add_image_tab(self):
        """
        初始化添加贴图面板
        """
        layout = QVBoxLayout(self.add_image_tab)
        
        # 添加贴图按钮
        self.add_image_btn = QPushButton("添加贴图")
        self.add_image_btn.clicked.connect(self.on_add_image_clicked)
        layout.addWidget(self.add_image_btn)
        
        # 最近添加的贴图预览
        self.preview_group = QGroupBox("贴图预览")
        preview_layout = QVBoxLayout()
        self.preview_label = QLabel("未选择贴图")
        self.preview_label.setAlignment(Qt.AlignCenter)
        self.preview_label.setMinimumHeight(150)
        preview_layout.addWidget(self.preview_label)
        self.preview_group.setLayout(preview_layout)
        layout.addWidget(self.preview_group)
        
        # 添加占位空间
        layout.addStretch()
        
    def init_property_tab(self):
        """
        初始化属性编辑面板
        """
        layout = QGridLayout(self.property_tab)
        
        # 位置编辑
        layout.addWidget(QLabel("X 坐标:"), 0, 0)
        self.x_spin = QSpinBox()
        self.x_spin.setRange(-10000, 10000)
        layout.addWidget(self.x_spin, 0, 1)
        
        layout.addWidget(QLabel("Y 坐标:"), 1, 0)
        self.y_spin = QSpinBox()
        self.y_spin.setRange(-10000, 10000)
        layout.addWidget(self.y_spin, 1, 1)
        
        # 大小编辑
        layout.addWidget(QLabel("宽度:"), 2, 0)
        self.width_spin = QSpinBox()
        self.width_spin.setRange(1, 10000)
        layout.addWidget(self.width_spin, 2, 1)
        
        layout.addWidget(QLabel("高度:"), 3, 0)
        self.height_spin = QSpinBox()
        self.height_spin.setRange(1, 10000)
        layout.addWidget(self.height_spin, 3, 1)
        
        # 缩放编辑
        layout.addWidget(QLabel("X 缩放:"), 4, 0)
        self.scale_x_spin = QDoubleSpinBox()
        self.scale_x_spin.setRange(0.1, 10.0)
        self.scale_x_spin.setSingleStep(0.1)
        layout.addWidget(self.scale_x_spin, 4, 1)
        
        layout.addWidget(QLabel("Y 缩放:"), 5, 0)
        self.scale_y_spin = QDoubleSpinBox()
        self.scale_y_spin.setRange(0.1, 10.0)
        self.scale_y_spin.setSingleStep(0.1)
        layout.addWidget(self.scale_y_spin, 5, 1)
        
        # 旋转编辑
        layout.addWidget(QLabel("旋转:"), 6, 0)
        self.rotation_spin = QSpinBox()
        self.rotation_spin.setRange(0, 359)
        layout.addWidget(self.rotation_spin, 6, 1)
        
        # 可见性编辑
        layout.addWidget(QLabel("可见:"), 7, 0)
        self.visible_check = QCheckBox()
        self.visible_check.setChecked(True)
        layout.addWidget(self.visible_check, 7, 1)
        
        # 添加占位空间
        layout.setRowStretch(8, 1)
        
    def init_layer_tab(self):
        """
        初始化层级管理面板
        """
        layout = QVBoxLayout(self.layer_tab)
        
        # 层级列表
        self.layer_list = QListWidget()
        layout.addWidget(self.layer_list)
        
        # 层级操作按钮
        btn_layout = QHBoxLayout()
        self.move_up_btn = QPushButton("上移")
        self.move_down_btn = QPushButton("下移")
        self.move_top_btn = QPushButton("置顶")
        self.move_bottom_btn = QPushButton("置底")
        
        btn_layout.addWidget(self.move_up_btn)
        btn_layout.addWidget(self.move_down_btn)
        btn_layout.addWidget(self.move_top_btn)
        btn_layout.addWidget(self.move_bottom_btn)
        
        layout.addLayout(btn_layout)
        
    def init_view_settings_tab(self):
        """
        初始化视图设置面板
        """
        layout = QVBoxLayout(self.view_settings_tab)
        
        # 画布大小设置组
        canvas_size_group = QGroupBox("画布大小")
        canvas_layout = QGridLayout()
        
        # 预设尺寸选择
        canvas_layout.addWidget(QLabel("预设尺寸:"), 0, 0)
        self.canvas_size_combo = QComboBox()
        self.canvas_size_combo.addItem("自定义")
        self.canvas_size_combo.addItem("512 x 512")
        self.canvas_size_combo.addItem("1024 x 1024")
        self.canvas_size_combo.addItem("2048 x 2048")
        self.canvas_size_combo.addItem("4096 x 4096")
        self.canvas_size_combo.currentIndexChanged.connect(self.on_canvas_size_preset_changed)
        canvas_layout.addWidget(self.canvas_size_combo, 0, 1)
        
        # 自定义宽度和高度
        canvas_layout.addWidget(QLabel("宽度:"), 1, 0)
        self.canvas_width_spin = QSpinBox()
        self.canvas_width_spin.setRange(100, 10000)
        self.canvas_width_spin.setValue(800)
        self.canvas_width_spin.setSingleStep(100)
        self.canvas_width_spin.setSuffix(" 像素")
        canvas_layout.addWidget(self.canvas_width_spin, 1, 1)
        
        canvas_layout.addWidget(QLabel("高度:"), 2, 0)
        self.canvas_height_spin = QSpinBox()
        self.canvas_height_spin.setRange(100, 10000)
        self.canvas_height_spin.setValue(600)
        self.canvas_height_spin.setSingleStep(100)
        self.canvas_height_spin.setSuffix(" 像素")
        canvas_layout.addWidget(self.canvas_height_spin, 2, 1)
        
        # 应用按钮
        self.apply_canvas_size_btn = QPushButton("应用画布大小")
        self.apply_canvas_size_btn.clicked.connect(self.on_apply_canvas_size)
        canvas_layout.addWidget(self.apply_canvas_size_btn, 3, 0, 1, 2)
        
        canvas_size_group.setLayout(canvas_layout)
        layout.addWidget(canvas_size_group)
        
        # 添加一个分隔线
        line1 = QFrame()
        line1.setFrameShape(QFrame.HLine)
        line1.setFrameShadow(QFrame.Sunken)
        layout.addWidget(line1)
        
        # 网格设置组
        grid_group = QGroupBox("网格设置")
        grid_layout = QGridLayout()
        
        # 网格可见性
        grid_layout.addWidget(QLabel("显示网格:"), 0, 0)
        self.grid_visible_check = QCheckBox()
        self.grid_visible_check.setChecked(True)
        self.grid_visible_check.stateChanged.connect(self.on_grid_visible_changed)
        grid_layout.addWidget(self.grid_visible_check, 0, 1)
        
        # 网格大小
        grid_layout.addWidget(QLabel("网格间距:"), 1, 0)
        self.grid_size_combo = QComboBox()
        self.grid_size_combo.addItem("10%")
        self.grid_size_combo.addItem("20%")
        self.grid_size_combo.addItem("25%")
        self.grid_size_combo.addItem("50%")
        self.grid_size_combo.setCurrentIndex(0)  # 默认选择10%
        self.grid_size_combo.currentIndexChanged.connect(self.on_grid_size_changed)
        grid_layout.addWidget(self.grid_size_combo, 1, 1)
        
        # 网格吸附
        grid_layout.addWidget(QLabel("网格吸附:"), 2, 0)
        self.snap_to_grid_check = QCheckBox()
        self.snap_to_grid_check.setChecked(True)
        self.snap_to_grid_check.stateChanged.connect(self.on_snap_to_grid_changed)
        grid_layout.addWidget(self.snap_to_grid_check, 2, 1)
        
        # 网格示例
        grid_layout.addWidget(QLabel("网格示例:"), 3, 0, 1, 2)
        self.grid_example = QFrame()
        self.grid_example.setMinimumHeight(100)
        self.grid_example.setFrameShape(QFrame.StyledPanel)
        self.grid_example.setStyleSheet("background-color: #f0f0f0;")
        grid_layout.addWidget(self.grid_example, 4, 0, 1, 2)
        
        grid_group.setLayout(grid_layout)
        layout.addWidget(grid_group)
        
        # 添加一个分隔线
        line2 = QFrame()
        line2.setFrameShape(QFrame.HLine)
        line2.setFrameShadow(QFrame.Sunken)
        layout.addWidget(line2)
        
        # 其他视图设置（未来可以添加）
        
        # 添加占位空间
        layout.addStretch()
        
    def on_canvas_size_preset_changed(self, index):
        """
        预设画布大小改变事件处理
        """
        if index == 0:  # 自定义
            return
        
        # 根据预设值设置宽度和高度
        if index == 1:  # 512 x 512
            width = height = 512
        elif index == 2:  # 1024 x 1024
            width = height = 1024
        elif index == 3:  # 2048 x 2048
            width = height = 2048
        elif index == 4:  # 4096 x 4096
            width = height = 4096
        
        self.canvas_width_spin.setValue(width)
        self.canvas_height_spin.setValue(height)
        
    def on_apply_canvas_size(self):
        """
        应用画布大小按钮点击事件处理
        """
        width = self.canvas_width_spin.value()
        height = self.canvas_height_spin.value()
        self.canvas_size_changed.emit(width, height)
        
    def on_add_image_clicked(self):
        """
        添加贴图按钮点击事件处理
        """
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(
            self, "选择贴图", "", "图片文件 (*.png *.jpg *.jpeg *.bmp *.gif)"
        )
        
        if file_path:
            # 更新预览
            pixmap = QPixmap(file_path)
            if not pixmap.isNull():
                # 设置预览图片，保持比例
                self.preview_label.setPixmap(
                    pixmap.scaled(
                        self.preview_label.width(), 
                        self.preview_label.height(),
                        Qt.KeepAspectRatio,
                        Qt.SmoothTransformation
                    )
                )
            
            # 发送添加贴图信号
            self.add_image_signal.emit(file_path)
    
    def on_grid_visible_changed(self, state):
        """
        网格可见性改变事件处理
        """
        visible = state == Qt.Checked
        self.grid_visible_changed.emit(visible)
    
    def on_grid_size_changed(self, index):
        """
        网格间距改变事件处理
        """
        # 根据索引确定百分比值
        if index == 0:
            grid_size = 10.0  # 10%
        elif index == 1:
            grid_size = 20.0  # 20%
        elif index == 2:
            grid_size = 25.0  # 25%
        elif index == 3:
            grid_size = 50.0  # 50%
        else:
            grid_size = 10.0  # 默认10%
        
        self.grid_size_changed.emit(grid_size)
        
    def on_snap_to_grid_changed(self, state):
        """
        网格吸附改变事件处理
        """
        enabled = state == Qt.Checked
        self.snap_to_grid_changed.emit(enabled)
    
    def update_property_values(self, image_item):
        """
        更新属性编辑面板的值
        """
        if image_item:
            self.x_spin.setValue(int(image_item.pos().x()))
            self.y_spin.setValue(int(image_item.pos().y()))
            self.width_spin.setValue(int(image_item.width * image_item.scale_x))
            self.height_spin.setValue(int(image_item.height * image_item.scale_y))
            self.scale_x_spin.setValue(image_item.scale_x)
            self.scale_y_spin.setValue(image_item.scale_y)
            self.rotation_spin.setValue(int(image_item.rotation_angle))
            self.visible_check.setChecked(image_item.visible)
    
    def update_layer_list(self, items):
        """
        更新层级列表
        """
        self.layer_list.clear()
        for item in items:
            self.layer_list.addItem(item.name)
            
    def set_grid_settings(self, settings):
        """
        设置网格属性控件
        """
        if "visible" in settings:
            self.grid_visible_check.setChecked(settings["visible"])
        if "size" in settings:
            size_value = settings["size"]
            # 根据百分比值设置选择项
            if abs(size_value - 10.0) < 0.001:
                self.grid_size_combo.setCurrentIndex(0)  # 10%
            elif abs(size_value - 20.0) < 0.001:
                self.grid_size_combo.setCurrentIndex(1)  # 20%
            elif abs(size_value - 25.0) < 0.001:
                self.grid_size_combo.setCurrentIndex(2)  # 25%
            elif abs(size_value - 50.0) < 0.001:
                self.grid_size_combo.setCurrentIndex(3)  # 50%
            else:
                # 如果没有匹配项，默认选择10%
                self.grid_size_combo.setCurrentIndex(0)
        if "snap_enabled" in settings:
            self.snap_to_grid_check.setChecked(settings["snap_enabled"])
            
    def set_canvas_size(self, width, height):
        """
        设置画布大小控件
        """
        self.canvas_width_spin.setValue(width)
        self.canvas_height_spin.setValue(height)
        
        # 尝试匹配预设值
        if width == height:
            if width == 512:
                self.canvas_size_combo.setCurrentIndex(1)
            elif width == 1024:
                self.canvas_size_combo.setCurrentIndex(2)
            elif width == 2048:
                self.canvas_size_combo.setCurrentIndex(3)
            elif width == 4096:
                self.canvas_size_combo.setCurrentIndex(4)
            else:
                self.canvas_size_combo.setCurrentIndex(0)
        else:
            self.canvas_size_combo.setCurrentIndex(0)