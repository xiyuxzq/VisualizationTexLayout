#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QTabWidget, QPushButton, 
                            QFileDialog, QLabel, QGridLayout, QSpinBox, 
                            QDoubleSpinBox, QCheckBox, QListWidget, QHBoxLayout,
                            QGroupBox, QFrame, QSizePolicy, QComboBox, QColorDialog,
                            QLineEdit, QMessageBox, QApplication, QDialog, QFormLayout)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap, QColor
import os

from ui.image_item import ImageItem

class ToolPanel(QWidget):
    """
    工具面板类，包含添加贴图和属性编辑等功能
    """
    
    # 自定义信号
    add_image_signal = pyqtSignal(str, str, int, int)  # 添加贴图信号，参数为文件路径、材质球名称、宽度、高度
    grid_visible_changed = pyqtSignal(bool)  # 网格可见性变更信号
    grid_size_changed = pyqtSignal(float)  # 网格大小变更信号
    canvas_size_changed = pyqtSignal(int, int)  # 画布大小变更信号，参数为宽度和高度
    snap_to_grid_changed = pyqtSignal(bool)  # 网格吸附变更信号
    grid_color_changed = pyqtSignal(QColor)  # 网格颜色变更信号
    grid_width_changed = pyqtSignal(int)     # 网格线宽度变更信号
    border_color_changed = pyqtSignal(QColor) # 边界颜色变更信号
    border_width_changed = pyqtSignal(int)    # 边界线宽度变更信号
    handle_color_changed = pyqtSignal(QColor)  # 新增：缩放手柄颜色变更信号
    handle_size_changed = pyqtSignal(int)      # 新增：缩放手柄大小变更信号
    export_signal = pyqtSignal(str, str)  # 导出信号，参数为PresetID和导出路径
    
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
        self.tab_widget.addTab(self.add_image_tab, "工具")
        
        # 视图设置面板
        self.view_settings_tab = QWidget()
        self.init_view_settings_tab()
        self.tab_widget.addTab(self.view_settings_tab, "视图设置")
        
        # 细节属性面板
        self.detail_property_tab = QWidget()
        self.init_detail_property_tab()
        self.tab_widget.addTab(self.detail_property_tab, "细节属性")
        
        # 导出面板
        self.export_tab = QWidget()
        self.init_export_tab()
        self.tab_widget.addTab(self.export_tab, "导出")
        
        layout.addWidget(self.tab_widget)
        self.setLayout(layout)
        
    def init_add_image_tab(self):
        """
        初始化添加贴图面板
        """
        layout = QVBoxLayout(self.add_image_tab)

        # 主操作按钮区放入GroupBox
        op_group = QGroupBox("常用操作")
        op_layout = QGridLayout()
        self.new_btn = QPushButton("新建")
        self.open_btn = QPushButton("打开")
        self.zoom_in_btn = QPushButton("放大选中图片")
        self.zoom_out_btn = QPushButton("缩小选中图片")
        self.fit_view_btn = QPushButton("适应视图")
        self.delete_btn = QPushButton("删除选中贴图")
        self.add_image_btn = QPushButton("添加贴图")
        # 两行布局
        op_layout.addWidget(self.new_btn, 0, 0)
        op_layout.addWidget(self.open_btn, 0, 1)
        op_layout.addWidget(self.fit_view_btn, 0, 2)
        op_layout.addWidget(self.zoom_in_btn, 1, 0)
        op_layout.addWidget(self.zoom_out_btn, 1, 1)
        op_layout.addWidget(self.add_image_btn, 1, 2)
        op_layout.addWidget(self.delete_btn, 1, 3)
        
        op_group.setLayout(op_layout)
        layout.addWidget(op_group)

        # 连接信号（槽函数待主窗口绑定）
        self.add_image_btn.clicked.connect(self.on_add_image_clicked)

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
        self.canvas_width_spin.setValue(1024)
        self.canvas_width_spin.setSingleStep(100)
        self.canvas_width_spin.setSuffix(" 像素")
        canvas_layout.addWidget(self.canvas_width_spin, 1, 1)
        
        canvas_layout.addWidget(QLabel("高度:"), 2, 0)
        self.canvas_height_spin = QSpinBox()
        self.canvas_height_spin.setRange(100, 10000)
        self.canvas_height_spin.setValue(1024)
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
        
        
        # 网格颜色
        grid_layout.addWidget(QLabel("网格颜色:"), 5, 0)
        self.grid_color_btn = QPushButton()
        self.grid_color_btn.setStyleSheet("background-color: #646464;")
        self.grid_color_btn.clicked.connect(self.on_grid_color_clicked)
        grid_layout.addWidget(self.grid_color_btn, 5, 1)
        
        # 网格线宽
        grid_layout.addWidget(QLabel("网格线宽:"), 6, 0)
        self.grid_width_spin = QSpinBox()
        self.grid_width_spin.setRange(1, 20)
        self.grid_width_spin.setValue(2)
        self.grid_width_spin.valueChanged.connect(self.on_grid_width_changed)
        grid_layout.addWidget(self.grid_width_spin, 6, 1)
        
        # 边界颜色
        grid_layout.addWidget(QLabel("边界颜色:"), 7, 0)
        self.border_color_btn = QPushButton()
        self.border_color_btn.setStyleSheet("background-color: #ff0000;")
        self.border_color_btn.clicked.connect(self.on_border_color_clicked)
        grid_layout.addWidget(self.border_color_btn, 7, 1)
        
        # 边界线宽
        grid_layout.addWidget(QLabel("边界线宽:"), 8, 0)
        self.border_width_spin = QSpinBox()
        self.border_width_spin.setRange(1, 20)
        self.border_width_spin.setValue(4)
        self.border_width_spin.valueChanged.connect(self.on_border_width_changed)
        grid_layout.addWidget(self.border_width_spin, 8, 1)

        grid_group.setLayout(grid_layout)
        layout.addWidget(grid_group)
        
        grid_group = QGroupBox("图片缩放手柄设置")
        grid_layout = QGridLayout()

        # 新增：缩放手柄颜色
        grid_layout.addWidget(QLabel("缩放手柄颜色:"), 9, 0)
        self.handle_color_btn = QPushButton()
        self.handle_color_btn.setStyleSheet("background-color: #0078d7;")
        self.handle_color_btn.clicked.connect(self.on_handle_color_clicked)
        grid_layout.addWidget(self.handle_color_btn, 9, 1)

        # 新增：缩放手柄大小
        grid_layout.addWidget(QLabel("缩放手柄大小:"), 10, 0)
        self.handle_size_spin = QSpinBox()
        self.handle_size_spin.setRange(8, 32)
        self.handle_size_spin.setValue(12)
        self.handle_size_spin.valueChanged.connect(self.on_handle_size_changed)
        grid_layout.addWidget(self.handle_size_spin, 10, 1)
        
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
        
    def init_detail_property_tab(self):
        """
        初始化细节属性面板
        """
        layout = QVBoxLayout(self.detail_property_tab)
        
        # 贴图属性组
        property_group = QGroupBox("贴图属性")
        property_layout = QGridLayout()
        
        # 名称
        property_layout.addWidget(QLabel("名称:"), 0, 0)
        self.name_label = QLabel("未选择贴图")
        property_layout.addWidget(self.name_label, 0, 1)
        
        # 文件路径
        property_layout.addWidget(QLabel("文件路径:"), 1, 0)
        path_layout = QHBoxLayout()
        self.path_label = QLabel("未选择贴图")
        self.path_label.setToolTip("完整文件路径")  # 添加工具提示，鼠标悬停时显示完整路径
        path_layout.addWidget(self.path_label)
        
        # 添加复制按钮
        self.copy_path_btn = QPushButton("复制")
        self.copy_path_btn.setEnabled(False)  # 默认禁用
        self.copy_path_btn.clicked.connect(self.on_copy_path_clicked)
        path_layout.addWidget(self.copy_path_btn)
        
        property_layout.addLayout(path_layout, 1, 1)
        
        # 材质球名称
        property_layout.addWidget(QLabel("材质球名称:"), 2, 0)
        self.material_edit = QLineEdit()
        self.material_edit.setPlaceholderText("请输入材质球名称")
        self.material_edit.setEnabled(False)  # 默认禁用，只有在选中贴图时启用
        self.material_edit.textChanged.connect(self.on_material_name_changed)
        property_layout.addWidget(self.material_edit, 2, 1)
        
        property_group.setLayout(property_layout)
        layout.addWidget(property_group)
        
        # 添加占位空间
        layout.addStretch()
        
    def init_export_tab(self):
        """
        初始化导出面板
        """
        layout = QVBoxLayout(self.export_tab)
        
        # PresetID设置组
        preset_group = QGroupBox("PresetID设置")
        preset_layout = QGridLayout()
        
        # PresetID输入
        preset_layout.addWidget(QLabel("PresetID:"), 0, 0)
        self.preset_id_edit = QLineEdit()
        self.preset_id_edit.setPlaceholderText("请输入PresetID")
        preset_layout.addWidget(self.preset_id_edit, 0, 1)
        
        preset_group.setLayout(preset_layout)
        layout.addWidget(preset_group)
        
        # 导出路径设置组
        path_group = QGroupBox("导出路径设置")
        path_layout = QGridLayout()
        
        # 导出路径输入
        path_layout.addWidget(QLabel("导出路径:"), 0, 0)
        self.export_path_edit = QLineEdit()
        self.export_path_edit.setPlaceholderText("请选择导出路径")
        path_layout.addWidget(self.export_path_edit, 0, 1)
        
        # 浏览按钮
        self.browse_btn = QPushButton("浏览...")
        self.browse_btn.clicked.connect(self.on_browse_export_path)
        path_layout.addWidget(self.browse_btn, 0, 2)
        
        path_group.setLayout(path_layout)
        layout.addWidget(path_group)
        
        # 导出按钮
        self.export_btn = QPushButton("导出")
        self.export_btn.clicked.connect(self.on_export_clicked)
        layout.addWidget(self.export_btn)
        
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
        添加图片按钮点击事件处理
        """
        filepath, _ = QFileDialog.getOpenFileName(
            self,
            "选择图片",
            "",
            "图片文件 (*.png *.jpg *.jpeg *.bmp *.gif *.tga)"
        )
        
        if filepath:
            dialog = MaterialNameDialog(self, filepath)
            if dialog.exec_() == QDialog.Accepted:
                material_name = dialog.get_material_name()
                width, height = dialog.get_resize_dimensions()
                self.add_image_signal.emit(filepath, material_name, width, height)
    
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
    
    def on_grid_color_clicked(self):
        color = QColorDialog.getColor(QColor(100, 100, 100), self, "选择网格颜色")
        if color.isValid():
            self.grid_color_btn.setStyleSheet(f"background-color: {color.name()};")
            self.grid_color_changed.emit(color)
    
    def on_grid_width_changed(self, value):
        self.grid_width_changed.emit(value)
    
    def on_border_color_clicked(self):
        color = QColorDialog.getColor(QColor(255, 0, 0), self, "选择边界颜色")
        if color.isValid():
            self.border_color_btn.setStyleSheet(f"background-color: {color.name()};")
            self.border_color_changed.emit(color)
    
    def on_border_width_changed(self, value):
        self.border_width_changed.emit(value)
    
    def on_handle_color_clicked(self):
        color = QColorDialog.getColor(QColor(0, 120, 215), self, "选择缩放手柄颜色")
        if color.isValid():
            self.handle_color_btn.setStyleSheet(f"background-color: {color.name()};")
            self.handle_color_changed.emit(color)

    def on_handle_size_changed(self, value):
        self.handle_size_changed.emit(value)
    
    def clear_preview(self):
        """
        清除预览图
        """
        self.preview_label.setText("未选择贴图")
        self.preview_label.setPixmap(QPixmap())
    
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

    def on_browse_export_path(self):
        """
        浏览导出路径按钮点击事件处理
        """
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getSaveFileName(
            self, "选择导出路径", "", "布局数据 (*.json)"
        )
        
        if file_path:
            if not file_path.endswith(".json"):
                file_path += ".json"
            self.export_path_edit.setText(file_path)
            
    def on_export_clicked(self):
        """
        处理导出按钮点击事件
        """
        preset_id = self.preset_id_edit.text().strip()
        export_path = self.export_path_edit.text().strip()
        
        if not preset_id:
            QMessageBox.warning(self, "警告", "请输入PresetID")
            return
            
        if not export_path:
            QMessageBox.warning(self, "警告", "请选择导出路径")
            return
            
        # 发出导出信号
        self.export_signal.emit(preset_id, export_path)
        
        # 复制导出路径到剪贴板
        clipboard = QApplication.clipboard()
        clipboard.setText(export_path)
        
        # 通过主窗口显示状态栏消息
        main_window = self.window()
        if main_window:
            main_window.statusBar().showMessage(f"导出成功！导出路径已复制到剪贴板：{export_path}")
        
    def update_detail_property(self, image_item):
        """
        更新细节属性面板的值
        """
        if image_item:
            self.name_label.setText(image_item.name)
            
            # 优化文件路径显示，显示完整路径但限制长度
            filepath = image_item.filepath
            if filepath:
                # 显示完整路径，但限制长度为20个字符
                if len(filepath) > 20:
                    display_text = filepath[:20] + "..."
                else:
                    display_text = filepath
                self.path_label.setText(display_text)
                self.path_label.setToolTip(filepath)  # 设置工具提示为完整路径
                self.copy_path_btn.setEnabled(True)  # 启用复制按钮
            else:
                self.path_label.setText("未设置")
                self.path_label.setToolTip("")
                self.copy_path_btn.setEnabled(False)  # 禁用复制按钮
            
            # 设置材质球名称
            material_name = getattr(image_item, "material_name", "")
            self.material_edit.setText(material_name)
            self.material_edit.setEnabled(True)  # 启用编辑
        else:
            self.name_label.setText("未选择贴图")
            self.path_label.setText("未选择贴图")
            self.path_label.setToolTip("")
            self.copy_path_btn.setEnabled(False)  # 禁用复制按钮
            self.material_edit.setText("")
            self.material_edit.setEnabled(False)  # 禁用编辑
            
    def on_material_name_changed(self, text):
        """
        材质球名称变更事件处理
        """
        # 获取主窗口
        main_window = self.window()
        if not main_window:
            return
            
        # 获取画布
        canvas = main_window.canvas
        if not canvas:
            return
            
        # 获取选中的贴图项
        selected_items = [item for item in canvas.scene.selectedItems() 
                         if isinstance(item, ImageItem)]
        
        if len(selected_items) == 1:
            # 更新材质球名称
            selected_items[0].material_name = text
            
    def on_copy_path_clicked(self):
        """
        复制文件路径按钮点击事件处理
        """
        # 获取主窗口
        main_window = self.window()
        if not main_window:
            return
            
        # 获取画布
        canvas = main_window.canvas
        if not canvas:
            return
            
        # 获取选中的贴图项
        selected_items = [item for item in canvas.scene.selectedItems() 
                         if isinstance(item, ImageItem)]
        
        if len(selected_items) == 1:
            # 获取完整文件路径
            filepath = selected_items[0].filepath
            if filepath:
                # 复制到剪贴板
                clipboard = QApplication.clipboard()
                clipboard.setText(filepath)
                
                # 显示提示信息
                main_window.statusBar().showMessage(f"已复制文件路径: {filepath}", 3000)

class MaterialNameDialog(QDialog):
    """
    材质球名称输入对话框
    """
    def __init__(self, parent=None, filepath=""):
        super(MaterialNameDialog, self).__init__(parent)
        self.filepath = filepath
        self.material_name = ""
        self.resize_width = 0
        self.resize_height = 0
        self.original_width = 0
        self.original_height = 0
        self.init_ui()
        
    def init_ui(self):
        """
        初始化界面
        """
        self.setWindowTitle("输入材质球名称")
        self.setMinimumWidth(400)
        
        layout = QVBoxLayout(self)
        
        # 文件名显示（不显示完整路径）
        if self.filepath:
            filename = os.path.basename(self.filepath)
            file_layout = QHBoxLayout()
            file_layout.addWidget(QLabel("文件名:"))
            file_label = QLabel(filename)
            file_label.setWordWrap(True)
            file_layout.addWidget(file_label)
            layout.addLayout(file_layout)
        
        # 材质球名称输入
        form_layout = QFormLayout()
        self.material_edit = QLineEdit()
        self.material_edit.setPlaceholderText("请输入材质球名称")
        # 尝试从文件名生成默认材质球名称
        if self.filepath:
            filename = os.path.basename(self.filepath)
            name_without_ext = os.path.splitext(filename)[0]
            self.material_edit.setText(name_without_ext)
        form_layout.addRow("材质球名称:", self.material_edit)
        layout.addLayout(form_layout)
        
        # 图片大小设置
        size_group = QGroupBox("图片大小设置")
        size_layout = QVBoxLayout()
        
        # 原始大小显示
        if self.filepath:
            pixmap = QPixmap(self.filepath)
            if not pixmap.isNull():
                self.original_width = pixmap.width()
                self.original_height = pixmap.height()
                original_size_label = QLabel(f"原始大小: {self.original_width} x {self.original_height}")
                size_layout.addWidget(original_size_label)
        
        # 调整大小选项
        resize_checkbox = QCheckBox("调整图片大小")
        resize_checkbox.setChecked(False)
        size_layout.addWidget(resize_checkbox)
        
        # 宽度和高度输入
        size_input_layout = QHBoxLayout()
        self.width_edit = QSpinBox()
        self.width_edit.setRange(1, 8192)
        self.width_edit.setValue(self.original_width)
        self.width_edit.setEnabled(False)
        
        self.height_edit = QSpinBox()
        self.height_edit.setRange(1, 8192)
        self.height_edit.setValue(self.original_height)
        self.height_edit.setEnabled(False)
        
        size_input_layout.addWidget(QLabel("宽度:"))
        size_input_layout.addWidget(self.width_edit)
        size_input_layout.addWidget(QLabel("高度:"))
        size_input_layout.addWidget(self.height_edit)
        size_layout.addLayout(size_input_layout)
        
        # 保持宽高比选项
        self.keep_aspect_ratio = QCheckBox("保持宽高比")
        self.keep_aspect_ratio.setChecked(True)
        size_layout.addWidget(self.keep_aspect_ratio)
        
        # 连接信号
        resize_checkbox.toggled.connect(lambda checked: self.width_edit.setEnabled(checked))
        resize_checkbox.toggled.connect(lambda checked: self.height_edit.setEnabled(checked))
        resize_checkbox.toggled.connect(lambda checked: self.keep_aspect_ratio.setEnabled(checked))
        
        self.width_edit.valueChanged.connect(self.on_width_changed)
        self.height_edit.valueChanged.connect(self.on_height_changed)
        self.keep_aspect_ratio.toggled.connect(self.on_keep_aspect_ratio_changed)
        
        size_group.setLayout(size_layout)
        layout.addWidget(size_group)
        
        # 按钮
        button_layout = QHBoxLayout()
        self.ok_button = QPushButton("确定")
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button = QPushButton("取消")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)
        
        # 设置默认按钮
        self.ok_button.setDefault(True)
        
    def on_width_changed(self, value):
        """
        宽度变化时，如果保持宽高比，则同步更新高度
        """
        if self.keep_aspect_ratio.isChecked() and self.original_width > 0:
            ratio = self.original_height / self.original_width
            new_height = int(value * ratio)
            self.height_edit.blockSignals(True)
            self.height_edit.setValue(new_height)
            self.height_edit.blockSignals(False)
            
    def on_height_changed(self, value):
        """
        高度变化时，如果保持宽高比，则同步更新宽度
        """
        if self.keep_aspect_ratio.isChecked() and self.original_height > 0:
            ratio = self.original_width / self.original_height
            new_width = int(value * ratio)
            self.width_edit.blockSignals(True)
            self.width_edit.setValue(new_width)
            self.width_edit.blockSignals(False)
            
    def on_keep_aspect_ratio_changed(self, checked):
        """
        保持宽高比选项变化时，如果选中，则根据当前宽度更新高度
        """
        if checked:
            self.on_width_changed(self.width_edit.value())
        
    def get_material_name(self):
        """
        获取输入的材质球名称
        """
        return self.material_edit.text().strip()
        
    def get_resize_dimensions(self):
        """
        获取调整后的图片尺寸
        """
        if self.width_edit.isEnabled():
            return self.width_edit.value(), self.height_edit.value()
        return 0, 0
        
    def accept(self):
        """
        确认按钮点击事件处理
        """
        self.material_name = self.get_material_name()
        if not self.material_name:
            QMessageBox.warning(self, "警告", "请输入材质球名称")
            return
            
        # 获取调整后的尺寸
        self.resize_width, self.resize_height = self.get_resize_dimensions()
            
        super(MaterialNameDialog, self).accept()