#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene
from PyQt5.QtCore import Qt, QRectF, QPointF, QLineF
from PyQt5.QtGui import QPainter, QColor, QPen
import math

class CanvasWidget(QGraphicsView):
    """
    画布组件，用于显示和编辑贴图。
    继承自QGraphicsView，管理QGraphicsScene。
    """
    
    def __init__(self, parent=None):
        super(CanvasWidget, self).__init__(parent)
        self.setRenderHint(QPainter.Antialiasing, True)
        self.setRenderHint(QPainter.SmoothPixmapTransform, True)
        self.setRenderHint(QPainter.TextAntialiasing, True)
        
        # 设置场景大小
        self.scene = QGraphicsScene(self)
        self.scene.setSceneRect(QRectF(0, 0, 800, 600))
        self.setScene(self.scene)
        
        # 设置背景颜色
        self.setBackgroundBrush(QColor(240, 240, 240))
        
        # 设置拖拽模式
        self.setDragMode(QGraphicsView.RubberBandDrag)
        
        # 启用鼠标跟踪
        self.setMouseTracking(True)
        
        # 初始化缩放比例
        self.scale_factor = 1.0
        
        # 适应视图大小
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        
        # 网格设置
        self.show_grid = True
        self.grid_size = 50  # 默认网格尺寸为50像素
        self.grid_color = QColor(200, 200, 200, 120)  # 浅灰色，半透明
        
        # 网格吸附设置
        self.snap_to_grid = True
        
    def drawBackground(self, painter, rect):
        """
        重写背景绘制方法，添加网格
        """
        super(CanvasWidget, self).drawBackground(painter, rect)
        
        if not self.show_grid:
            return
        
        # 保存当前的画笔设置
        old_pen = painter.pen()
        
        # 设置网格线的画笔
        grid_pen = QPen(self.grid_color)
        grid_pen.setWidth(1)
        painter.setPen(grid_pen)
        
        # 计算可见区域的边界
        left = math.floor(rect.left() / self.grid_size) * self.grid_size
        top = math.floor(rect.top() / self.grid_size) * self.grid_size
        
        # 绘制垂直线
        x = left
        while x < rect.right():
            painter.drawLine(QLineF(x, rect.top(), x, rect.bottom()))
            x += self.grid_size
        
        # 绘制水平线
        y = top
        while y < rect.bottom():
            painter.drawLine(QLineF(rect.left(), y, rect.right(), y))
            y += self.grid_size
        
        # 恢复之前的画笔设置
        painter.setPen(old_pen)
        
    def wheelEvent(self, event):
        """
        鼠标滚轮事件处理，用于缩放视图
        """
        factor = 1.2
        if event.angleDelta().y() < 0:
            factor = 1.0 / factor
        
        self.scale(factor, factor)
        self.scale_factor *= factor
        
    def resizeEvent(self, event):
        """
        窗口大小改变时，调整视图
        """
        super(CanvasWidget, self).resizeEvent(event)
        self.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)
        self.scale_factor = 1.0
        
    def reset_view(self):
        """
        重置视图到原始大小
        """
        self.resetTransform()
        self.scale_factor = 1.0
        
    def fit_in_view(self):
        """
        适应场景内容到视图
        """
        self.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)
        
    def add_image(self, image_item):
        """
        添加贴图项到场景
        """
        # 设置网格吸附属性
        image_item.set_snap_to_grid(self.snap_to_grid, self.grid_size)
        self.scene.addItem(image_item)
        
    def clear_scene(self):
        """
        清空场景
        """
        self.scene.clear()
        self.scene.setSceneRect(QRectF(0, 0, 800, 600))
        
    def set_grid_visible(self, visible):
        """
        设置网格可见性
        """
        self.show_grid = visible
        self.viewport().update()  # 更新视图
        
    def set_grid_size(self, size):
        """
        设置网格尺寸
        """
        # 确保网格尺寸为正数
        if size > 0:
            self.grid_size = size
            # 更新所有贴图项的网格尺寸
            for item in self.scene.items():
                from ui.image_item import ImageItem
                if isinstance(item, ImageItem):
                    item.set_snap_to_grid(self.snap_to_grid, self.grid_size)
            self.viewport().update()  # 更新视图
            
    def set_snap_to_grid(self, enabled):
        """
        设置网格吸附
        """
        self.snap_to_grid = enabled
        # 更新所有贴图项的网格吸附设置
        for item in self.scene.items():
            from ui.image_item import ImageItem
            if isinstance(item, ImageItem):
                item.set_snap_to_grid(enabled, self.grid_size)
    
    def set_canvas_size(self, width, height):
        """
        设置画布大小
        """
        # 设置场景大小
        self.scene.setSceneRect(0, 0, width, height)
        # 更新视图
        self.fit_in_view()
            
    def get_grid_settings(self):
        """
        获取当前网格设置
        """
        return {
            "visible": self.show_grid,
            "size": self.grid_size,
            "snap_enabled": self.snap_to_grid
        }
        
    def set_grid_settings(self, settings):
        """
        设置网格属性
        """
        if "visible" in settings:
            self.show_grid = settings["visible"]
        if "size" in settings:
            self.grid_size = settings["size"]
        if "snap_enabled" in settings:
            self.snap_to_grid = settings["snap_enabled"]
            
        # 更新所有贴图项的网格吸附设置
        for item in self.scene.items():
            from ui.image_item import ImageItem
            if isinstance(item, ImageItem):
                item.set_snap_to_grid(self.snap_to_grid, self.grid_size)
                
        self.viewport().update()  # 更新视图
        
    def snap_position_to_grid(self, pos):
        """
        将位置吸附到网格
        """
        if not self.snap_to_grid:
            return pos
        
        # 计算最近的网格点
        x = round(pos.x() / self.grid_size) * self.grid_size
        y = round(pos.y() / self.grid_size) * self.grid_size
        
        return QPointF(x, y)