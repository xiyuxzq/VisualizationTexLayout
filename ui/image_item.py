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
            super(ImageItem, self).mouseMoveEvent(event)
        
    def mouseReleaseEvent(self, event):
        """
        鼠标释放事件处理
        """
        if event.button() == Qt.LeftButton:
            self.dragging = False
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