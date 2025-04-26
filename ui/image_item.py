#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QGraphicsItem
from PyQt5.QtCore import Qt, QRectF, QPointF
from PyQt5.QtGui import QPixmap, QPainter, QPen, QColor, QBrush

class ImageItem(QGraphicsItem):
    """
    贴图项类，继承自QGraphicsItem，
    用于管理单个贴图的状态和行为。
    """
    
    def __init__(self, filepath, name="", parent=None):
        super(ImageItem, self).__init__(parent)
        # 贴图基本属性
        self.id = id(self)  # 使用对象id作为唯一标识符
        self.name = name or filepath.split("/")[-1]
        self.filepath = filepath
        self.pixmap = QPixmap(filepath)
        
        # 位置和大小
        self.width = self.pixmap.width()
        self.height = self.pixmap.height()
        
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
        
    def boundingRect(self):
        """
        返回贴图项的边界矩形
        """
        return QRectF(0, 0, self.width * self.scale_x, self.height * self.scale_y)
    
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
        
        # 如果被选中，绘制边框
        if self.isSelected():
            pen = QPen(QColor(0, 120, 215), 1, Qt.DashLine)
            painter.setPen(pen)
            painter.setBrush(QBrush(Qt.transparent))
            painter.drawRect(self.boundingRect())
            
    def mousePressEvent(self, event):
        """
        鼠标按下事件处理
        """
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.drag_start = event.pos()
        super(ImageItem, self).mousePressEvent(event)
        
    def mouseMoveEvent(self, event):
        """
        鼠标移动事件处理
        """
        if self.dragging:
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
        
    def mouseReleaseEvent(self, event):
        """
        鼠标释放事件处理
        """
        if event.button() == Qt.LeftButton:
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
        将贴图项转换为字典，用于序列化
        """
        return {
            "id": str(self.id),
            "name": self.name,
            "filepath": self.filepath,
            "position": {
                "x": self.pos().x(),
                "y": self.pos().y()
            },
            "size": {
                "width": self.width,
                "height": self.height
            },
            "scale": {
                "x": self.scale_x,
                "y": self.scale_y
            },
            "rotation": self.rotation_angle,
            "zIndex": self.zValue(),
            "visible": self.visible
        }