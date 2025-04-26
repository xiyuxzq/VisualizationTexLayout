#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
from PyQt5.QtWidgets import (QMainWindow, QAction, QFileDialog, QSplitter, 
                             QStatusBar, QMessageBox, QToolBar, QWidget,
                             QVBoxLayout)
from PyQt5.QtCore import Qt, QSettings
from PyQt5.QtGui import QIcon

from ui.canvas_widget import CanvasWidget
from ui.tool_panel import ToolPanel
from ui.image_item import ImageItem

class MainWindow(QMainWindow):
    """
    主窗口类，整合画布和工具面板，
    并添加菜单栏、工具栏和状态栏。
    """
    
    def __init__(self):
        super(MainWindow, self).__init__()
        self.init_ui()
        self.current_file = None
        self.init_settings()
        
    def init_ui(self):
        """
        初始化界面
        """
        # 设置窗口属性
        self.setWindowTitle("贴图可视化布局工具")
        self.setGeometry(100, 100, 1200, 800)
        
        # 创建中央部件
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setCentralWidget(central_widget)
        
        # 创建分割器
        self.splitter = QSplitter(Qt.Horizontal)
        
        # 创建画布
        self.canvas = CanvasWidget()
        
        # 创建工具面板
        self.tool_panel = ToolPanel()
        
        # 添加组件到分割器
        self.splitter.addWidget(self.canvas)
        self.splitter.addWidget(self.tool_panel)
        
        # 设置默认大小比例
        self.splitter.setSizes([800, 400])
        
        # 添加分割器到主布局
        main_layout.addWidget(self.splitter)
        
        # 创建菜单栏
        self.create_menu_bar()
        
        # 创建状态栏
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("就绪")
        
        # 连接信号和槽
        self.connect_signals()
        
    def create_menu_bar(self):
        """
        创建菜单栏
        """
        # 文件菜单
        file_menu = self.menuBar().addMenu("文件")
        
        new_action = QAction("新建", self)
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(self.new_file)
        file_menu.addAction(new_action)
        
        open_action = QAction("打开", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)
        
        save_action = QAction("保存", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)
        
        save_as_action = QAction("另存为", self)
        save_as_action.setShortcut("Ctrl+Shift+S")
        save_as_action.triggered.connect(self.save_file_as)
        file_menu.addAction(save_as_action)
        
        file_menu.addSeparator()
        
        export_action = QAction("导出", self)
        export_action.setShortcut("Ctrl+E")
        export_action.triggered.connect(self.export_layout)
        file_menu.addAction(export_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("退出", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # 编辑菜单
        edit_menu = self.menuBar().addMenu("编辑")
        
        # 后续实现编辑菜单
        
        # 视图菜单
        view_menu = self.menuBar().addMenu("视图")
        
        zoom_in_action = QAction("放大", self)
        zoom_in_action.setShortcut("Ctrl++")
        zoom_in_action.triggered.connect(lambda: self.canvas.scale(1.2, 1.2))
        view_menu.addAction(zoom_in_action)
        
        zoom_out_action = QAction("缩小", self)
        zoom_out_action.setShortcut("Ctrl+-")
        zoom_out_action.triggered.connect(lambda: self.canvas.scale(1/1.2, 1/1.2))
        view_menu.addAction(zoom_out_action)
        
        reset_view_action = QAction("重置视图", self)
        reset_view_action.setShortcut("Ctrl+0")
        reset_view_action.triggered.connect(self.canvas.reset_view)
        view_menu.addAction(reset_view_action)
        
        fit_view_action = QAction("适应视图", self)
        fit_view_action.setShortcut("Ctrl+F")
        fit_view_action.triggered.connect(self.canvas.fit_in_view)
        view_menu.addAction(fit_view_action)
        
        view_menu.addSeparator()
        
        show_grid_action = QAction("显示网格", self)
        show_grid_action.setCheckable(True)
        show_grid_action.setChecked(True)
        show_grid_action.triggered.connect(lambda checked: self.canvas.set_grid_visible(checked))
        view_menu.addAction(show_grid_action)
        
        snap_to_grid_action = QAction("网格吸附", self)
        snap_to_grid_action.setCheckable(True)
        snap_to_grid_action.setChecked(True)
        snap_to_grid_action.triggered.connect(lambda checked: self.canvas.set_snap_to_grid(checked))
        view_menu.addAction(snap_to_grid_action)
        
        # 贴图菜单
        image_menu = self.menuBar().addMenu("贴图")
        
        add_image_action = QAction("添加贴图", self)
        add_image_action.triggered.connect(self.tool_panel.on_add_image_clicked)
        image_menu.addAction(add_image_action)
        
        # 后续实现贴图菜单
        
        # 帮助菜单
        help_menu = self.menuBar().addMenu("帮助")
        
        about_action = QAction("关于", self)
        about_action.triggered.connect(self.show_about_dialog)
        help_menu.addAction(about_action)
        
    def connect_signals(self):
        """
        连接信号和槽
        """
        # 连接添加贴图信号
        self.tool_panel.add_image_signal.connect(self.add_image)
        
        # 连接网格设置信号
        self.tool_panel.grid_visible_changed.connect(self.canvas.set_grid_visible)
        self.tool_panel.grid_size_changed.connect(self.canvas.set_grid_size)
        self.tool_panel.snap_to_grid_changed.connect(self.canvas.set_snap_to_grid)
        self.tool_panel.grid_color_changed.connect(self.canvas.set_grid_color)
        self.tool_panel.grid_width_changed.connect(self.canvas.set_grid_width)
        self.tool_panel.border_color_changed.connect(self.canvas.set_border_color)
        self.tool_panel.border_width_changed.connect(self.canvas.set_border_width)
        
        # 连接画布大小设置信号
        self.tool_panel.canvas_size_changed.connect(self.canvas.set_canvas_size)
        
        # 连接右侧主操作按钮
        self.tool_panel.new_btn.clicked.connect(self.new_file)
        self.tool_panel.open_btn.clicked.connect(self.open_file)
        self.tool_panel.save_btn.clicked.connect(self.save_file)
        self.tool_panel.zoom_in_btn.clicked.connect(lambda: self.canvas.scale(1.2, 1.2))
        self.tool_panel.zoom_out_btn.clicked.connect(lambda: self.canvas.scale(1/1.2, 1/1.2))
        self.tool_panel.reset_view_btn.clicked.connect(self.canvas.reset_view)
        self.tool_panel.fit_view_btn.clicked.connect(self.canvas.fit_in_view)
        
    def init_settings(self):
        """
        初始化应用设置
        """
        self.settings = QSettings("VisualizationTexLayout", "TextureLayoutTool")
        
        # 读取上次窗口位置和大小
        if self.settings.contains("window/geometry"):
            self.restoreGeometry(self.settings.value("window/geometry"))
        if self.settings.contains("window/state"):
            self.restoreState(self.settings.value("window/state"))
        
        # 读取上次的网格设置
        if self.settings.contains("grid/visible"):
            visible = self.settings.value("grid/visible", type=bool)
            self.canvas.set_grid_visible(visible)
            self.tool_panel.grid_visible_check.setChecked(visible)
        
        if self.settings.contains("grid/size"):
            size = self.settings.value("grid/size", type=float)
            self.canvas.set_grid_size(size)
            self.tool_panel.set_grid_settings({"size": size})
            
        if self.settings.contains("grid/snap_enabled"):
            enabled = self.settings.value("grid/snap_enabled", type=bool)
            self.canvas.set_snap_to_grid(enabled)
            self.tool_panel.snap_to_grid_check.setChecked(enabled)
        
        # 读取上次的画布大小
        if self.settings.contains("canvas/width") and self.settings.contains("canvas/height"):
            width = self.settings.value("canvas/width", type=int)
            height = self.settings.value("canvas/height", type=int)
            self.canvas.set_canvas_size(width, height)
            self.tool_panel.set_canvas_size(width, height)
            
    def closeEvent(self, event):
        """
        关闭事件处理，保存应用设置
        """
        # 保存窗口位置和大小
        self.settings.setValue("window/geometry", self.saveGeometry())
        self.settings.setValue("window/state", self.saveState())
        
        # 保存网格设置
        grid_settings = self.canvas.get_grid_settings()
        self.settings.setValue("grid/visible", grid_settings["visible"])
        self.settings.setValue("grid/size", grid_settings["size"])
        self.settings.setValue("grid/snap_enabled", grid_settings["snap_enabled"])
        
        # 保存画布大小
        canvas_rect = self.canvas.scene.sceneRect()
        self.settings.setValue("canvas/width", int(canvas_rect.width()))
        self.settings.setValue("canvas/height", int(canvas_rect.height()))
        
        event.accept()
    
    def add_image(self, filepath):
        """
        添加贴图到画布
        """
        if os.path.exists(filepath):
            image_item = ImageItem(filepath)
            # 设置网格吸附属性
            image_item.set_snap_to_grid(self.canvas.snap_to_grid, self.canvas.grid_size)
            self.canvas.add_image(image_item)
            self.status_bar.showMessage(f"已添加贴图: {filepath}")
            return image_item
        else:
            self.status_bar.showMessage(f"文件不存在: {filepath}")
            return None
    
    def new_file(self):
        """
        新建文件
        """
        # 清空画布
        self.canvas.clear_scene()
        self.current_file = None
        self.canvas.set_canvas_size(1024, 1024)
        self.tool_panel.set_canvas_size(1024, 1024)
        self.status_bar.showMessage("已创建新文件")
    
    def open_file(self):
        """
        打开文件
        """
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(
            self, "打开布局", "", "布局文件 (*.json)"
        )
        
        if file_path:
            try:
                with open(file_path, 'r') as f:
                    layout_data = json.load(f)
                
                # 清空当前画布
                self.canvas.clear_scene()
                
                # 设置画布大小
                if "canvas" in layout_data:
                    width = layout_data["canvas"].get("width", 1024)
                    height = layout_data["canvas"].get("height", 1024)
                    self.canvas.set_canvas_size(width, height)
                    self.tool_panel.set_canvas_size(width, height)
                
                # 设置网格属性
                if "grid" in layout_data:
                    grid_settings = layout_data["grid"]
                    self.canvas.set_grid_settings(grid_settings)
                    self.tool_panel.set_grid_settings(grid_settings)
                
                # 加载贴图
                if "images" in layout_data:
                    for img_data in layout_data["images"]:
                        filepath = img_data.get("filepath", "")
                        if os.path.exists(filepath):
                            image_item = self.add_image(filepath)
                            if image_item:
                                # 设置位置
                                pos = img_data.get("position", {})
                                x = pos.get("x", 0)
                                y = pos.get("y", 0)
                                image_item.setPos(x, y)
                                
                                # 设置缩放
                                scale = img_data.get("scale", {})
                                scale_x = scale.get("x", 1.0)
                                scale_y = scale.get("y", 1.0)
                                image_item.set_scale(scale_x, scale_y)
                                
                                # 设置旋转
                                rotation = img_data.get("rotation", 0)
                                image_item.setRotation(rotation)
                                
                                # 设置层级
                                z_index = img_data.get("zIndex", 0)
                                image_item.setZValue(z_index)
                                
                                # 设置可见性
                                visible = img_data.get("visible", True)
                                image_item.setVisible(visible)
                
                self.current_file = file_path
                self.status_bar.showMessage(f"已打开文件: {file_path}")
                
            except Exception as e:
                QMessageBox.critical(self, "错误", f"打开文件失败: {str(e)}")
    
    def save_file(self):
        """
        保存文件
        """
        if self.current_file:
            self.save_layout_to_file(self.current_file)
        else:
            self.save_file_as()
    
    def save_file_as(self):
        """
        另存为文件
        """
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getSaveFileName(
            self, "保存布局", "", "布局文件 (*.json)"
        )
        
        if file_path:
            if not file_path.endswith(".json"):
                file_path += ".json"
            
            self.save_layout_to_file(file_path)
            self.current_file = file_path
    
    def save_layout_to_file(self, filepath):
        """
        将当前布局保存到文件
        """
        try:
            layout_data = {
                "version": "1.0",
                "canvas": {
                    "width": self.canvas.scene.width(),
                    "height": self.canvas.scene.height()
                },
                "grid": self.canvas.get_grid_settings(),
                "images": []
            }
            
            # 收集所有贴图项
            for item in self.canvas.scene.items():
                if isinstance(item, ImageItem):
                    layout_data["images"].append(item.to_dict())
            
            with open(filepath, 'w') as f:
                json.dump(layout_data, f, indent=2)
            
            self.status_bar.showMessage(f"已保存文件: {filepath}")
            
        except Exception as e:
            QMessageBox.critical(self, "错误", f"保存文件失败: {str(e)}")
    
    def export_layout(self):
        """
        导出布局数据
        """
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getSaveFileName(
            self, "导出布局", "", "布局数据 (*.json)"
        )
        
        if file_path:
            if not file_path.endswith(".json"):
                file_path += ".json"
            
            self.save_layout_to_file(file_path)
            QMessageBox.information(self, "导出成功", f"布局数据已导出到: {file_path}")
    
    def show_about_dialog(self):
        """
        显示关于对话框
        """
        QMessageBox.about(
            self,
            "关于贴图可视化布局工具",
            "贴图可视化布局工具 v1.0\n\n"
            "一个用于可视化调整贴图布局并生成合并数据的工具。\n\n"
            "© 2023 VisualizationTexLayout"
        )