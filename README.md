# 贴图可视化布局工具

一个用于可视化调整贴图布局并生成合并数据的工具。

## 功能特点

- 通过右侧面板添加多个贴图到左侧画布
- 在左侧画布上拖拽移动贴图
- 在左侧画布上调整贴图大小
- 保存和加载布局配置
- 导出布局数据（JSON格式）给合并工具使用

## 安装依赖

```bash
pip install -r requirements.txt
```

## 运行程序

```bash
python main.py
```

## 使用说明

1. 启动程序后，界面分为左侧画布和右侧工具面板
2. 在右侧工具面板的"添加贴图"标签页，点击"添加贴图"按钮选择图片文件
3. 在左侧画布上，可以拖拽移动贴图，选中贴图后可以在右侧属性面板调整其属性
4. 使用顶部菜单栏或工具栏的功能按钮保存、加载或导出布局配置

## 文件格式

本工具使用JSON格式保存和导出布局数据，格式示例：

```json
{
    "version": "1.0",
    "canvas": {
        "width": 800,
        "height": 600
    },
    "images": [
        {
            "id": "img1",
            "name": "背景",
            "filepath": "path/to/image1.png",
            "position": {"x": 0, "y": 0},
            "size": {"width": 800, "height": 600},
            "scale": {"x": 1.0, "y": 1.0},
            "rotation": 0,
            "zIndex": 0,
            "visible": true
        }
    ]
}
```

## 版权信息

© 2023 VisualizationTexLayout