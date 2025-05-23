#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QGraphicsItem
from PyQt5.QtCore import Qt, QRectF, QPointF
from PyQt5.QtGui import QPixmap, QPainter, QPen, QColor, QBrush
import os

class ImageItem(QGraphicsItem):
    """
    贴图项类，继承自QGraphicsItem，
    用于管理单个贴图的状态和行为。
    """
    
    HANDLE_SIZE = 12  # 手柄大小
    HANDLE_MARGIN = 2  # 手柄边缘间距
    HANDLE_NONE = -1
    HANDLE_TOP_LEFT = 0
    HANDLE_TOP_RIGHT = 1
    HANDLE_BOTTOM_LEFT = 2
    HANDLE_BOTTOM_RIGHT = 3
    
    def __init__(self, filepath, name="", parent=None):
        super(ImageItem, self).__init__(parent)
        # 贴图基本属性
        self.id = id(self)  # 使用对象id作为唯一标识符
        self.name = name or filepath.split("/")[-1]
        self.filepath = filepath
        self.pixmap = QPixmap(filepath)
        self.material_name = name or os.path.splitext(os.path.basename(filepath))[0]  # 使用不带扩展名的文件名作为默认值
        self.mesh_index = 0  # 添加mesh_index属性，默认为0
        
        # 位置和大小
        self.width = self.pixmap.width()
        self.height = self.pixmap.height()
        
        # 用户设置的初始尺寸（默认为原始尺寸）
        self.initial_width = self.width
        self.initial_height = self.height
        
        # 缩放因子
        self.scale_x = 1.0
        self.scale_y = 1.0
        
        # 旋转角度
        self.rotation_angle = 0
        
        # 可见性
        self.visible = True
        
        # 设置贴图项可移动、可选择
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)
        
        # 设置接受悬停事件
        self.setAcceptHoverEvents(True)
        
        # 拖拽状态
        self.dragging = False
        self.drag_start = QPointF()
        
        # 网格吸附设置
        self.snap_to_grid = True
        self.grid_size = 50
        
        self.resizing = False
        self.resize_handle = self.HANDLE_NONE
        self.resize_start_pos = QPointF()
        self.resize_start_rect = QRectF()
        
        self.handle_color = QColor(0, 120, 215)  # 新增：手柄颜色
        self.handle_size = 12                   # 新增：手柄大小
        
    def boundingRect(self):
        """
        返回贴图项的边界矩形
        """
        margin = self.handle_size + self.HANDLE_MARGIN
        return QRectF(0, 0, self.width * self.scale_x, self.height * self.scale_y).adjusted(-margin, -margin, margin, margin)
    
    def paint(self, painter, option, widget):
        """
        绘制贴图项
        """
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)
        
        # 绘制贴图
        if self.visible:
            target_rect = QRectF(0, 0, self.width * self.scale_x, self.height * self.scale_y)
            source_rect = QRectF(0, 0, self.width, self.height)
            painter.drawPixmap(target_rect, self.pixmap, source_rect)
        
        # 如果被选中，绘制边框和手柄
        if self.isSelected():
            pen = QPen(self.handle_color, 2, Qt.DashLine)
            painter.setPen(pen)
            painter.setBrush(QBrush(Qt.transparent))
            painter.drawRect(QRectF(0, 0, self.width * self.scale_x, self.height * self.scale_y))
            # 绘制四角手柄
            for rect in self.handleRects():
                painter.setBrush(QBrush(self.handle_color))
                painter.setPen(Qt.NoPen)
                painter.drawRect(rect)
            
    def handleRects(self):
        # 返回四个手柄的QRectF列表
        w = self.width * self.scale_x
        h = self.height * self.scale_y
        s = self.handle_size
        m = self.HANDLE_MARGIN
        return [
            QRectF(-s/2 + m, -s/2 + m, s, s),  # 左上
            QRectF(w - s/2 - m, -s/2 + m, s, s),  # 右上
            QRectF(-s/2 + m, h - s/2 - m, s, s),  # 左下
            QRectF(w - s/2 - m, h - s/2 - m, s, s),  # 右下
        ]

    def handleAt(self, pos):
        # 判断pos是否在某个手柄内，返回手柄编号，否则-1
        for i, rect in enumerate(self.handleRects()):
            if rect.contains(pos):
                return i
        return self.HANDLE_NONE

    def mousePressEvent(self, event):
        """
        鼠标按下事件处理
        """
        if event.button() == Qt.LeftButton:
            handle = self.handleAt(event.pos())
            if handle != self.HANDLE_NONE:
                self.resizing = True
                self.resize_handle = handle
                self.resize_start_pos = event.scenePos()
                self.resize_start_rect = QRectF(0, 0, self.width * self.scale_x, self.height * self.scale_y)
                event.accept()
                return
            else:
                self.dragging = True
                self.drag_start = event.pos()
        super(ImageItem, self).mousePressEvent(event)
        
    def mouseMoveEvent(self, event):
        """
        鼠标移动事件处理
        """
        if self.resizing:
            # 计算缩放
            delta = event.scenePos() - self.resize_start_pos
            rect = QRectF(self.resize_start_rect)
            if self.resize_handle == self.HANDLE_TOP_LEFT:
                new_left = rect.left() + delta.x()
                new_top = rect.top() + delta.y()
                rect.setLeft(new_left)
                rect.setTop(new_top)
            elif self.resize_handle == self.HANDLE_TOP_RIGHT:
                new_right = rect.right() + delta.x()
                new_top = rect.top() + delta.y()
                rect.setRight(new_right)
                rect.setTop(new_top)
            elif self.resize_handle == self.HANDLE_BOTTOM_LEFT:
                new_left = rect.left() + delta.x()
                new_bottom = rect.bottom() + delta.y()
                rect.setLeft(new_left)
                rect.setBottom(new_bottom)
            elif self.resize_handle == self.HANDLE_BOTTOM_RIGHT:
                new_right = rect.right() + delta.x()
                new_bottom = rect.bottom() + delta.y()
                rect.setRight(new_right)
                rect.setBottom(new_bottom)
            rect = rect.normalized()
            # 限制最小尺寸
            min_size = 10
            rect.setWidth(max(rect.width(), min_size))
            rect.setHeight(max(rect.height(), min_size))
            # 网格吸附
            if self.snap_to_grid:
                rect.setWidth(round(rect.width() / self.grid_size) * self.grid_size)
                rect.setHeight(round(rect.height() / self.grid_size) * self.grid_size)
            # 计算缩放因子
            scale_x = rect.width() / self.width if self.width else 1.0
            scale_y = rect.height() / self.height if self.height else 1.0
            self.set_scale(scale_x, scale_y)
            self.update()
            event.accept()
            return
        elif self.dragging:
            # 让基类处理移动
            super(ImageItem, self).mouseMoveEvent(event)
            
            # 如果启用了网格吸附，将位置吸附到网格
            if self.snap_to_grid:
                # 获取当前位置
                current_pos = self.pos()
                # 计算吸附位置
                snapped_pos = self.snap_position(current_pos)
                # 设置吸附后的位置
                self.setPos(snapped_pos)
        else:
            super(ImageItem, self).mouseMoveEvent(event)
        
    def mouseReleaseEvent(self, event):
        """
        鼠标释放事件处理
        """
        if event.button() == Qt.LeftButton:
            if self.resizing:
                self.resizing = False
                self.resize_handle = self.HANDLE_NONE
                event.accept()
                return
            self.dragging = False
            
            # 如果启用了网格吸附，确保最终位置吸附到网格
            if self.snap_to_grid:
                current_pos = self.pos()
                snapped_pos = self.snap_position(current_pos)
                self.setPos(snapped_pos)
                
        super(ImageItem, self).mouseReleaseEvent(event)
        
    def resize(self, width, height):
        """
        调整贴图大小
        """
        self.prepareGeometryChange()
        # 记录用户设置的初始尺寸
        self.initial_width = width
        self.initial_height = height
        # 更新缩放比例
        self.scale_x = width / self.width if self.width else 1.0
        self.scale_y = height / self.height if self.height else 1.0
        self.update()
        
    def set_scale(self, scale_x, scale_y):
        """
        设置缩放因子
        """
        self.prepareGeometryChange()
        self.scale_x = scale_x
        self.scale_y = scale_y
        self.update()
        
    def set_snap_to_grid(self, enabled, grid_size=None):
        """
        设置网格吸附
        """
        old_grid_size = self.grid_size
        self.snap_to_grid = enabled
        if grid_size is not None:
            self.grid_size = grid_size
        # 如果正在拖拽且网格间距发生变化，立即吸附到新网格
        if self.dragging and self.snap_to_grid and (grid_size is not None and old_grid_size != grid_size):
            self.setPos(self.snap_position(self.pos()))
            
    def snap_position(self, pos):
        """
        将位置吸附到网格
        """
        if not self.snap_to_grid:
            return pos
        
        # 计算最近的网格点
        x = round(pos.x() / self.grid_size) * self.grid_size
        y = round(pos.y() / self.grid_size) * self.grid_size
        
        return QPointF(x, y)
        
    def to_dict(self):
        """
        将图片项转换为字典数据
        """
        # 获取场景（画布）大小
        scene = self.scene()
        if not scene:
            return {}
            
        scene_width = scene.width()
        scene_height = scene.height()
        
        # 获取图片当前的实际尺寸（不包含手柄区域）
        current_width = self.width * self.scale_x
        current_height = self.height * self.scale_y
        
        # 计算最终尺寸相对于画布的占比
        scale_x = current_width / scene_width
        scale_y = current_height / scene_height
        
        # 获取图片在画布中的位置（百分比）
        pos = self.pos()
        x_percent = pos.x() / scene_width
        y_percent = pos.y() / scene_height
        
        return {
            "filepath": self.filepath,
            "material_name": self.material_name,
            "mesh_index": self.mesh_index,
            "position": {
                "x": x_percent,
                "y": y_percent
            },
            "scale": {
                "x": scale_x,
                "y": scale_y
            },
            "rotation": self.rotation_angle,
            "zIndex": self.zValue(),
            "visible": self.visible
        }

    def set_handle_color(self, color):
        """
        设置缩放手柄颜色
        """
        self.handle_color = color
        self.update()

    def set_handle_size(self, size):
        """
        设置缩放手柄大小
        """
        self.handle_size = size
        self.update()

    def set_border_width(self, width):
        """
        设置边界线宽度
        """
        self.border_width = width
        self.update()
