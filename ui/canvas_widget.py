#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QPainter, QColor

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
        self.scene.addItem(image_item)
        
    def clear_scene(self):
        """
        清空场景
        """
        self.scene.clear()
        self.scene.setSceneRect(QRectF(0, 0, 800, 600))