#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QTabWidget, QPushButton, 
                            QFileDialog, QLabel, QGridLayout, QSpinBox, 
                            QDoubleSpinBox, QCheckBox, QListWidget, QHBoxLayout,
                            QGroupBox)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap

from ui.image_item import ImageItem

class ToolPanel(QWidget):
    """
    工具面板类，包含添加贴图和属性编辑等功能
    """
    
    # 自定义信号
    add_image_signal = pyqtSignal(str)  # 添加贴图信号，参数为文件路径
    
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