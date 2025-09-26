"""
测试修正后的 legend 布局
使用正确的 Figure 坐标系，参考 PyComplexHeatmap 的实现
"""

import sys
import os
sys.path.insert(0, '/Users/yuanzan/Documents/github/seqyuan/sunmao')
import numpy as np
import matplotlib.pyplot as plt
from sunmao import create_whiteLayer

# 1. 创建 whiteLayer
fig, wl = create_whiteLayer(figsize=(12, 8))
root_panel = wl.mortise

# 2. 添加子面板
panel1 = root_panel.tenon(pos='top', size=0.4, pad=0.1, title='Panel 1')
panel2 = root_panel.tenon(pos='bottom', size=0.4, pad=0.1, title='Panel 2')
panel3 = root_panel.tenon(pos='left', size=0.3, pad=0.1, title='Panel 3')
panel4 = root_panel.tenon(pos='right', size=0.3, pad=0.1, title='Panel 4')

# 3. 绘制数据（确保有 label 参数）
np.random.seed(42)
x = np.linspace(0, 10, 50)

# 面板1：散点图
colors1 = ['red', 'blue', 'green']
for i, color in enumerate(colors1):
    y1 = np.random.normal(i, 0.5, 50)
    panel1.ax.scatter(x, y1, c=color, label=f'Group {i+1}', alpha=0.7, s=30)

# 面板2：线图
panel2.ax.plot(x, np.sin(x), 'r-', linewidth=2, label='sin(x)')
panel2.ax.plot(x, np.cos(x), 'b-', linewidth=2, label='cos(x)')
panel2.ax.plot(x, np.tan(x), 'g-', linewidth=2, label='tan(x)')

# 面板3：柱状图
categories = ['A', 'B', 'C', 'D']
values1 = np.random.normal(50, 10, 4)
values2 = np.random.normal(30, 5, 4)

panel3.ax.bar(np.arange(len(categories)) - 0.2, values1, 0.4, 
             label='Group 1', color='orange', alpha=0.8)
panel3.ax.bar(np.arange(len(categories)) + 0.2, values2, 0.4, 
             label='Group 2', color='purple', alpha=0.8)

# 面板4：混合图
panel4.ax.plot(x, np.exp(-x), 'brown', linewidth=2, label='exp(-x)')
panel4.ax.plot(x, np.log(x + 1), 'pink', linewidth=2, label='log(x+1)')

x_scatter = np.random.normal(5, 1, 30)
y_scatter = np.random.normal(0, 1, 30)
panel4.ax.scatter(x_scatter, y_scatter, c='cyan', label='Random Points', 
                 alpha=0.7, s=20)

panel4.ax.axhline(y=0, color='black', linestyle='--', label='Zero Line')

# 4. 配置 legend
# 选择要显示的 legend（面板索引）
wl.show_legends([0, 2, 3])  # 显示 Panel 1, Panel 3, Panel 4 的 legend

# 设置 legend 位置，使用正确的 Figure 坐标系
wl.set_legend_pos(
    loc='bottom', 
    orientation='horizontal', 
    ncol=3,  # 子图 legend 块的列数
    legend_hpad=0.005,  # 控制水平间距
    legend_vpad=0.005,  # 控制垂直间距
    legend_gap=0.02     # 控制 legend 之间的间距
)

# 保存图片
wl.savefig('examples/test_corrected_pycomplexheatmap_style.png', dpi=150, bbox_inches='tight')
