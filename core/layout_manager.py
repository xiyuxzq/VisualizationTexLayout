#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
from PyQt5.QtCore import QObject, pyqtSignal

class LayoutManager(QObject):
    """
    布局管理器类，负责保存、加载和导出布局数据
    """
    
    # 自定义信号
    layout_loaded = pyqtSignal(dict)  # 布局加载完成信号，参数为布局数据
    layout_saved = pyqtSignal(str)    # 布局保存完成信号，参数为文件路径
    
    def __init__(self):
        super(LayoutManager, self).__init__()
        self.current_file = None
        
    def new_layout(self, width=800, height=600):
        """
        创建新的布局
        """
        layout_data = {
            "version": "1.0",
            "canvas": {
                "width": width,
                "height": height
            },
            "images": []
        }
        
        self.current_file = None
        return layout_data
        
    def load_layout(self, filepath):
        """
        从文件加载布局
        """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"文件不存在: {filepath}")
        
        try:
            with open(filepath, 'r') as f:
                layout_data = json.load(f)
            
            self.current_file = filepath
            self.layout_loaded.emit(layout_data)
            return layout_data
            
        except json.JSONDecodeError:
            raise ValueError(f"无效的JSON格式: {filepath}")
        except Exception as e:
            raise Exception(f"加载布局失败: {str(e)}")
    
    def save_layout(self, layout_data, filepath=None):
        """
        保存布局到文件
        """
        save_path = filepath or self.current_file
        
        if not save_path:
            raise ValueError("未指定保存路径")
        
        try:
            with open(save_path, 'w') as f:
                json.dump(layout_data, f, indent=2)
            
            self.current_file = save_path
            self.layout_saved.emit(save_path)
            return True
            
        except Exception as e:
            raise Exception(f"保存布局失败: {str(e)}")
    
    def export_layout(self, layout_data, filepath):
        """
        导出布局数据
        """
        try:
            with open(filepath, 'w') as f:
                json.dump(layout_data, f, indent=2)
            return True
            
        except Exception as e:
            raise Exception(f"导出布局失败: {str(e)}")
    
    def get_current_file(self):
        """
        获取当前文件路径
        """
        return self.current_file