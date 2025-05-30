#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsItem
from PyQt5.QtCore import Qt, QRectF, QPointF, QLineF, QSizeF
from PyQt5.QtGui import QPainter, QColor, QPen, QBrush, QTransform
import math

from ui.image_item import ImageItem  # 添加ImageItem的导入

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
        self.setDragMode(QGraphicsView.NoDrag)  # 默认不启用拖拽
        
        # 启用鼠标跟踪
        self.setMouseTracking(True)
        
        # 设置视图属性
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        
        # 初始化缩放比例
        self.scale_factor = 1.0
        
        # 网格设置
        self.show_grid = True
        self.grid_size = 256.0  # 默认网格间距为256像素
        self.grid_color = QColor(100, 100, 100, 200)  # 浅灰色，半透明
        self.grid_width = 2  # 新增：网格线宽度
        self.border_color = QColor(255, 0, 0, 200)  # 红色，稍微透明
        self.border_width = 4  # 新增：边界线宽度
        
        # 网格吸附设置
        self.snap_to_grid = True
        
        # 添加鼠标中键拖拽相关变量
        self._panning = False
        self._last_mouse_pos = None
        
    def get_actual_grid_size(self):
        """
        返回网格大小（像素）
        """
        return self.grid_size
        
    def drawBackground(self, painter, rect):
        """
        重写背景绘制方法，添加网格和边界
        """
        super(CanvasWidget, self).drawBackground(painter, rect)
        
        # 保存当前的画笔设置
        old_pen = painter.pen()
        
        # 获取场景矩形
        scene_rect = self.scene.sceneRect()
        
        # 绘制网格
        if self.show_grid:
            # 设置网格线的画笔
            grid_pen = QPen(self.grid_color)
            grid_pen.setWidth(self.grid_width)  # 使用可设置的宽度
            painter.setPen(grid_pen)
            
            # 根据像素间距绘制网格线
            grid_spacing = self.grid_size  # 网格间距（像素）
            
            # 绘制垂直线
            x = scene_rect.left()
            while x <= scene_rect.right():
                painter.drawLine(QLineF(x, rect.top(), x, rect.bottom()))
                x += grid_spacing
            
            # 绘制水平线
            y = scene_rect.top()
            while y <= scene_rect.bottom():
                painter.drawLine(QLineF(rect.left(), y, rect.right(), y))
                y += grid_spacing
        
        # 绘制场景边界红色框
        border_pen = QPen(self.border_color)
        border_pen.setWidth(self.border_width)  # 使用可设置的宽度
        painter.setPen(border_pen)
        painter.drawRect(scene_rect)
        
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
        actual_grid_size = self.get_actual_grid_size()
        image_item.set_snap_to_grid(self.snap_to_grid, actual_grid_size)
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
        
    def set_grid_size(self, pixels):
        """
        设置网格尺寸（像素）
        """
        # 确保像素值为正数且在合理范围内
        if pixels > 0:
            self.grid_size = pixels
            # 计算实际网格大小（像素）
            actual_grid_size = self.get_actual_grid_size()
            # 更新所有贴图项的网格尺寸
            for item in self.scene.items():
                from ui.image_item import ImageItem
                if isinstance(item, ImageItem):
                    item.set_snap_to_grid(self.snap_to_grid, actual_grid_size)
            self.viewport().update()  # 更新视图
            
    def set_snap_to_grid(self, enabled):
        """
        设置网格吸附
        """
        self.snap_to_grid = enabled
        # 计算实际网格大小
        actual_grid_size = self.get_actual_grid_size()
        # 更新所有贴图项的网格吸附设置
        for item in self.scene.items():
            from ui.image_item import ImageItem
            if isinstance(item, ImageItem):
                item.set_snap_to_grid(enabled, actual_grid_size)
    
    def set_canvas_size(self, width, height):
        """
        设置画布大小
        """
        # 设置场景大小
        self.scene.setSceneRect(0, 0, width, height)
        # 由于画布大小变了，网格的实际像素大小也需要更新
        actual_grid_size = self.get_actual_grid_size()
        # 更新所有贴图项的网格设置
        for item in self.scene.items():
            from ui.image_item import ImageItem
            if isinstance(item, ImageItem):
                item.set_snap_to_grid(self.snap_to_grid, actual_grid_size)
        # 更新视图
        self.fit_in_view()
            
    def get_grid_settings(self):
        """
        获取当前网格设置
        """
        return {
            "visible": self.show_grid,
            "size": self.grid_size,  # 现在是像素值
            "snap_enabled": self.snap_to_grid
        }
        
    def set_grid_settings(self, settings):
        """
        设置网格属性
        """
        if "visible" in settings:
            self.show_grid = settings["visible"]
        if "size" in settings:
            # 确保像素值在有效范围内
            size_value = settings["size"]
            self.grid_size = max(1, size_value)
        if "snap_enabled" in settings:
            self.snap_to_grid = settings["snap_enabled"]
            
        # 计算实际网格大小
        actual_grid_size = self.get_actual_grid_size()
        
        # 更新所有贴图项的网格吸附设置
        for item in self.scene.items():
            from ui.image_item import ImageItem
            if isinstance(item, ImageItem):
                item.set_snap_to_grid(self.snap_to_grid, actual_grid_size)
                
        self.viewport().update()  # 更新视图
        
    def snap_position_to_grid(self, pos):
        """
        将位置吸附到网格
        """
        if not self.snap_to_grid:
            return pos
        
        # 计算实际网格大小
        actual_grid_size = self.get_actual_grid_size()
        
        # 计算最近的网格点
        x = round(pos.x() / actual_grid_size) * actual_grid_size
        y = round(pos.y() / actual_grid_size) * actual_grid_size
        
        return QPointF(x, y)

    def set_grid_color(self, color):
        """
        设置网格颜色
        """
        self.grid_color = color
        self.viewport().update()

    def set_grid_width(self, width):
        """
        设置网格线宽度
        """
        self.grid_width = width
        self.viewport().update()

    def set_border_color(self, color):
        """
        设置边界颜色
        """
        self.border_color = color
        self.viewport().update()

    def set_border_width(self, width):
        """
        设置所有贴图项的边界线宽度
        """
        for item in self.scene.items():
            if isinstance(item, ImageItem):
                item.set_border_width(width)
                
    def set_handle_color(self, color):
        """
        设置所有贴图项的缩放手柄颜色
        """
        for item in self.scene.items():
            if isinstance(item, ImageItem):
                item.set_handle_color(color)
                
    def set_handle_size(self, size):
        """
        设置所有贴图项的缩放手柄大小
        """
        for item in self.scene.items():
            if isinstance(item, ImageItem):
                item.set_handle_size(size)

    def mousePressEvent(self, event):
        """
        处理鼠标按下事件
        """
        if event.button() == Qt.MiddleButton:
            self._panning = True
            self._last_mouse_pos = event.pos()
            self.setCursor(Qt.ClosedHandCursor)
            event.accept()  # 接受事件，防止事件继续传播
            return
        super(CanvasWidget, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        """
        处理鼠标释放事件
        """
        if event.button() == Qt.MiddleButton:
            self._panning = False
            self.setCursor(Qt.ArrowCursor)
            event.accept()  # 接受事件，防止事件继续传播
            return
        super(CanvasWidget, self).mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        """
        处理鼠标移动事件
        """
        if self._panning and self._last_mouse_pos is not None:
            # 计算鼠标移动的距离
            delta = event.pos() - self._last_mouse_pos
            # 移动视图
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - delta.x())
            self.verticalScrollBar().setValue(self.verticalScrollBar().value() - delta.y())
            self._last_mouse_pos = event.pos()
            event.accept()  # 接受事件，防止事件继续传播
            return
        super(CanvasWidget, self).mouseMoveEvent(event)