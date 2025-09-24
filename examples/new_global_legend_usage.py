"""
Sunmao 新 Global Legend 用法示例

展示新的 global legend 设计的使用方法：
- 每个子图的 legend 单独处理
- Global legend 只负责收集和排列各个子图 legend
- 支持分组标题和分隔符
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import matplotlib.pyplot as plt
from sunmao import mortise

def example_basic_usage():
    """示例：基本用法"""
    
    print("=== 新 Global Legend 基本用法示例 ===\n")
    
    # 1. 创建多面板布局
    fig, root = mortise(figsize=(14, 10))
    
    # 添加子图
    top_panel = root.tenon(pos='top', size=0.4, pad=0.1, title='Scatter Plot')
    bottom_panel = root.tenon(pos='bottom', size=0.4, pad=0.1, title='Line Plot')
    left_panel = root.tenon(pos='left', size=0.3, pad=0.1, title='Bar Plot')
    right_panel = root.tenon(pos='right', size=0.3, pad=0.1, title='Mixed Plot')
    
    print("1. 创建多面板布局")
    
    # 2. 绘制数据（确保有 label 参数）
    np.random.seed(42)
    x = np.linspace(0, 10, 50)
    
    # 顶部面板：散点图
    colors_scatter = ['red', 'blue', 'green']
    for i, color in enumerate(colors_scatter):
        y_scatter = np.random.normal(i, 0.5, 50)
        top_panel.ax.scatter(x, y_scatter, c=color, label=f'Group {i+1}', 
                           alpha=0.7, s=30)
    
    # 底部面板：线图
    bottom_panel.ax.plot(x, np.sin(x), 'r-', linewidth=2, label='sin(x)')
    bottom_panel.ax.plot(x, np.cos(x), 'b-', linewidth=2, label='cos(x)')
    bottom_panel.ax.plot(x, np.tan(x), 'g-', linewidth=2, label='tan(x)')
    
    # 左侧面板：柱状图
    categories = ['A', 'B', 'C', 'D']
    values1 = np.random.normal(50, 10, 4)
    values2 = np.random.normal(30, 5, 4)
    
    left_panel.ax.bar(np.arange(len(categories)) - 0.2, values1, 0.4, 
                     label='Group 1', color='orange', alpha=0.8)
    left_panel.ax.bar(np.arange(len(categories)) + 0.2, values2, 0.4, 
                     label='Group 2', color='purple', alpha=0.8)
    
    # 右侧面板：混合图
    right_panel.ax.plot(x, np.exp(-x), 'brown', linewidth=2, label='exp(-x)')
    right_panel.ax.plot(x, np.log(x + 1), 'pink', linewidth=2, label='log(x+1)')
    
    x_scatter = np.random.normal(5, 1, 30)
    y_scatter = np.random.normal(0, 1, 30)
    right_panel.ax.scatter(x_scatter, y_scatter, c='cyan', label='Random Points', 
                          alpha=0.7, s=20)
    
    right_panel.ax.axhline(y=0, color='black', linestyle='--', label='Zero Line')
    
    print("2. 绘制数据并添加 labels")
    
    # 3. 手动添加所有 mortise 到 legend 管理器
    legend_manager = root.get_legend_manager()
    legend_manager.mortises = []
    
    legend_manager.add_mortise(root)
    legend_manager.add_mortise(top_panel)
    legend_manager.add_mortise(bottom_panel)
    legend_manager.add_mortise(left_panel)
    legend_manager.add_mortise(right_panel)
    
    print("3. 添加所有 mortise 到 legend 管理器")
    
    # 4. 收集所有 legend 信息
    legend_info = legend_manager.collect_legends()
    
    print("4. 收集 legend 信息")
    
    # 5. 创建新的 global legend
    print("\n5. 创建新的 global legend")
    
    # 定义子图信息
    subplot_info = {
        'mortise_1': {'title': 'Scatter Plot', 'panel': top_panel},
        'mortise_2': {'title': 'Line Plot', 'panel': bottom_panel},
        'mortise_3': {'title': 'Bar Plot', 'panel': left_panel},
        'mortise_4': {'title': 'Mixed Plot', 'panel': right_panel}
    }
    
    # 为每个子图创建独立的 legend
    subplot_legends = {}
    
    for mortise_name, mortise_info in legend_info['mortise_legends'].items():
        mortise_obj = mortise_info['mortise']
        handles = mortise_info['handles']
        labels = mortise_info['labels']
        
        if handles and labels and mortise_name in subplot_info:
            subplot_title = subplot_info[mortise_name]['title']
            panel = subplot_info[mortise_name]['panel']
            
            # 创建独立的 legend
            legend = panel.ax.legend(handles, labels, loc='upper right', ncol=1)
            
            if legend:
                subplot_legends[mortise_name] = {
                    'legend': legend,
                    'title': subplot_title,
                    'handles': handles,
                    'labels': labels,
                    'panel': panel
                }
                
                print(f"   - {mortise_name}: {subplot_title} ({len(labels)} 个元素)")
    
    # 6. 创建全局 legend panel
    print("\n6. 创建全局 legend panel")
    
    # 定义排列顺序
    arrangement_order = ['mortise_1', 'mortise_2', 'mortise_3', 'mortise_4']
    
    # 收集所有子图 legend 信息
    all_handles = []
    all_labels = []
    group_titles = []
    group_positions = []
    
    for i, mortise_name in enumerate(arrangement_order):
        if mortise_name in subplot_legends:
            legend_info = subplot_legends[mortise_name]
            handles = legend_info['handles']
            labels = legend_info['labels']
            title = legend_info['title']
            
            # 添加分组标题
            group_titles.append(title)
            group_positions.append(len(all_labels))
            
            # 添加 handles 和 labels
            all_handles.extend(handles)
            all_labels.extend(labels)
    
    if all_handles and all_labels:
        # 创建全局 legend panel
        global_legend = root._figure.legend(all_handles, all_labels, 
                                           loc='upper center', ncol=4)
        
        print(f"   - 全局 legend panel 创建成功")
        print(f"   - Legend items: {len(global_legend.get_texts())}")
        print(f"   - Legend labels: {[text.get_text() for text in global_legend.get_texts()]}")
        
        # 添加分组标题
        print("\n7. 添加分组标题")
        
        # 为每个分组添加标题
        for i, (title, pos) in enumerate(zip(group_titles, group_positions)):
            if i < len(group_titles) - 1:
                # 计算标题位置
                title_x = 0.1 + (pos / len(all_labels)) * 0.8
                title_y = 0.95
                
                # 添加标题文本
                title_text = root._figure.text(title_x, title_y, title,
                                             transform=root._figure.transFigure,
                                             fontsize=10, fontweight='bold',
                                             ha='center', va='bottom')
                
                print(f"   - 分组 {i+1}: {title} (位置: {pos})")
    
    # 保存图片
    fig.savefig('examples/new_global_legend_basic.png', dpi=150, bbox_inches='tight')
    print("   - 图片已保存: examples/new_global_legend_basic.png")
    
    return fig, root

def example_advanced_usage():
    """示例：高级用法"""
    
    print("\n=== 新 Global Legend 高级用法示例 ===\n")
    
    # 1. 创建复杂布局
    fig, root = mortise(figsize=(16, 12))
    
    # 添加子图
    top_panel = root.tenon(pos='top', size=0.4, pad=0.1, title='Heatmap')
    bottom_panel = root.tenon(pos='bottom', size=0.4, pad=0.1, title='Time Series')
    left_panel = root.tenon(pos='left', size=0.3, pad=0.1, title='Statistics')
    right_panel = root.tenon(pos='right', size=0.3, pad=0.1, title='Clustering')
    
    print("1. 创建复杂布局")
    
    # 2. 绘制复杂数据
    np.random.seed(42)
    
    # 顶部面板：热图 + 纵向 colorbar
    heatmap_data = np.random.randn(20, 15)
    im = top_panel.ax.imshow(heatmap_data, cmap='viridis', aspect='auto')
    top_panel.ax.set_title('Heatmap')
    top_panel.ax.set_xlabel('Samples')
    top_panel.ax.set_ylabel('Genes')
    
    # 添加纵向 colorbar
    cbar = plt.colorbar(im, ax=top_panel.ax, shrink=0.8)
    cbar.set_label('Expression Level', rotation=270, labelpad=15)
    
    # 底部面板：时间序列
    time_points = np.linspace(0, 24, 100)
    
    bottom_panel.ax.plot(time_points, np.sin(time_points/4) + 1, 'b-', linewidth=2, label='Gene A')
    bottom_panel.ax.plot(time_points, np.cos(time_points/3) + 1, 'r-', linewidth=2, label='Gene B')
    bottom_panel.ax.plot(time_points, np.sin(time_points/2) + 1, 'g-', linewidth=2, label='Gene C')
    bottom_panel.ax.plot(time_points, np.cos(time_points/5) + 1, 'm-', linewidth=2, label='Gene D')
    
    bottom_panel.ax.set_title('Time Series')
    bottom_panel.ax.set_xlabel('Time (hours)')
    bottom_panel.ax.set_ylabel('Expression Level')
    bottom_panel.ax.grid(True, alpha=0.3)
    
    # 左侧面板：统计图
    categories = ['High', 'Medium', 'Low', 'Very Low']
    values = [45, 30, 20, 5]
    colors = ['red', 'orange', 'yellow', 'green']
    
    bars = left_panel.ax.bar(categories, values, color=colors, alpha=0.8)
    left_panel.ax.set_title('Statistics')
    left_panel.ax.set_ylabel('Number of Genes')
    left_panel.ax.set_xlabel('Expression Level')
    left_panel.ax.grid(True, alpha=0.3)
    
    # 右侧面板：聚类图
    n_points = 100
    x_cluster = np.random.normal(0, 1, n_points)
    y_cluster = np.random.normal(0, 1, n_points)
    cluster_labels = np.random.choice(['Cluster 1', 'Cluster 2', 'Cluster 3'], n_points)
    
    colors_cluster = {'Cluster 1': 'red', 'Cluster 2': 'blue', 'Cluster 3': 'green'}
    
    for cluster in ['Cluster 1', 'Cluster 2', 'Cluster 3']:
        mask = cluster_labels == cluster
        right_panel.ax.scatter(x_cluster[mask], y_cluster[mask], 
                              c=colors_cluster[cluster], label=cluster, 
                              alpha=0.7, s=30)
    
    right_panel.ax.set_title('Clustering')
    right_panel.ax.set_xlabel('PC1')
    right_panel.ax.set_ylabel('PC2')
    right_panel.ax.grid(True, alpha=0.3)
    
    print("2. 绘制复杂数据")
    
    # 3. 手动添加所有 mortise 到 legend 管理器
    legend_manager = root.get_legend_manager()
    legend_manager.mortises = []
    
    legend_manager.add_mortise(root)
    legend_manager.add_mortise(top_panel)
    legend_manager.add_mortise(bottom_panel)
    legend_manager.add_mortise(left_panel)
    legend_manager.add_mortise(right_panel)
    
    print("3. 添加所有 mortise 到 legend 管理器")
    
    # 4. 收集所有 legend 信息
    legend_info = legend_manager.collect_legends()
    
    print("4. 收集 legend 信息")
    
    # 5. 创建高级 global legend
    print("\n5. 创建高级 global legend")
    
    # 定义子图信息（包括 colorbar 信息）
    subplot_info = {
        'mortise_1': {'title': 'Heatmap', 'panel': top_panel, 'has_colorbar': True, 'colorbar_orientation': 'vertical'},
        'mortise_2': {'title': 'Time Series', 'panel': bottom_panel, 'has_colorbar': False},
        'mortise_3': {'title': 'Statistics', 'panel': left_panel, 'has_colorbar': False},
        'mortise_4': {'title': 'Clustering', 'panel': right_panel, 'has_colorbar': False}
    }
    
    # 为每个子图创建独立的 legend
    subplot_legends = {}
    
    for mortise_name, mortise_info in legend_info['mortise_legends'].items():
        mortise_obj = mortise_info['mortise']
        handles = mortise_info['handles']
        labels = mortise_info['labels']
        
        if handles and labels and mortise_name in subplot_info:
            subplot_title = subplot_info[mortise_name]['title']
            panel = subplot_info[mortise_name]['panel']
            has_colorbar = subplot_info[mortise_name]['has_colorbar']
            
            # 创建独立的 legend
            legend = panel.ax.legend(handles, labels, loc='upper right', ncol=1)
            
            if legend:
                subplot_legends[mortise_name] = {
                    'legend': legend,
                    'title': subplot_title,
                    'handles': handles,
                    'labels': labels,
                    'panel': panel,
                    'has_colorbar': has_colorbar
                }
                
                print(f"   - {mortise_name}: {subplot_title} ({len(labels)} 个元素)")
                if has_colorbar:
                    colorbar_orientation = subplot_info[mortise_name]['colorbar_orientation']
                    print(f"     Colorbar: {colorbar_orientation}")
    
    # 6. 创建全局 legend panel（带分隔符）
    print("\n6. 创建全局 legend panel（带分隔符）")
    
    # 定义排列顺序
    arrangement_order = ['mortise_1', 'mortise_2', 'mortise_3', 'mortise_4']
    
    # 收集所有子图 legend 信息
    all_handles = []
    all_labels = []
    group_titles = []
    group_positions = []
    
    for i, mortise_name in enumerate(arrangement_order):
        if mortise_name in subplot_legends:
            legend_info = subplot_legends[mortise_name]
            handles = legend_info['handles']
            labels = legend_info['labels']
            title = legend_info['title']
            
            # 添加分组标题
            group_titles.append(title)
            group_positions.append(len(all_labels))
            
            # 添加 handles 和 labels
            all_handles.extend(handles)
            all_labels.extend(labels)
    
    if all_handles and all_labels:
        # 创建全局 legend panel
        global_legend = root._figure.legend(all_handles, all_labels, 
                                           loc='upper center', ncol=4)
        
        print(f"   - 全局 legend panel 创建成功")
        print(f"   - Legend items: {len(global_legend.get_texts())}")
        print(f"   - Legend labels: {[text.get_text() for text in global_legend.get_texts()]}")
        
        # 添加分组标题和分隔符
        print("\n7. 添加分组标题和分隔符")
        
        # 为每个分组添加标题和分隔符
        for i, (title, pos) in enumerate(zip(group_titles, group_positions)):
            if i < len(group_titles) - 1:
                # 计算标题位置
                title_x = 0.1 + (pos / len(all_labels)) * 0.8
                title_y = 0.95
                
                # 添加标题文本
                title_text = root._figure.text(title_x, title_y, title,
                                             transform=root._figure.transFigure,
                                             fontsize=10, fontweight='bold',
                                             ha='center', va='bottom')
                
                # 添加分隔符
                separator_x = title_x
                separator_y = title_y - 0.02
                separator_text = root._figure.text(separator_x, separator_y, '|',
                                                 transform=root._figure.transFigure,
                                                 fontsize=8, color='gray',
                                                 ha='center', va='bottom')
                
                print(f"   - 分组 {i+1}: {title} (位置: {pos})")
    
    # 保存图片
    fig.savefig('examples/new_global_legend_advanced.png', dpi=150, bbox_inches='tight')
    print("   - 图片已保存: examples/new_global_legend_advanced.png")
    
    return fig, root

def example_custom_layout():
    """示例：自定义布局"""
    
    print("\n=== 新 Global Legend 自定义布局示例 ===\n")
    
    # 1. 创建自定义布局
    fig, root = mortise(figsize=(18, 10))
    
    # 添加子图
    top_panel = root.tenon(pos='top', size=0.4, pad=0.1, title='Main Plot')
    bottom_panel = root.tenon(pos='bottom', size=0.4, pad=0.1, title='Secondary Plot')
    left_panel = root.tenon(pos='left', size=0.3, pad=0.1, title='Supporting Plot')
    right_panel = root.tenon(pos='right', size=0.3, pad=0.1, title='Additional Plot')
    
    print("1. 创建自定义布局")
    
    # 2. 绘制数据
    np.random.seed(42)
    x = np.linspace(0, 10, 100)
    
    # 顶部面板：主图
    top_panel.ax.plot(x, np.sin(x), 'r-', linewidth=2, label='sin(x)')
    top_panel.ax.plot(x, np.cos(x), 'b-', linewidth=2, label='cos(x)')
    top_panel.ax.plot(x, np.tan(x), 'g-', linewidth=2, label='tan(x)')
    top_panel.ax.plot(x, np.exp(-x), 'm-', linewidth=2, label='exp(-x)')
    
    # 底部面板：次图
    bottom_panel.ax.scatter(x[::5], np.sin(x[::5]), c='red', s=20, label='sin points')
    bottom_panel.ax.scatter(x[::5], np.cos(x[::5]), c='blue', s=20, label='cos points')
    bottom_panel.ax.scatter(x[::5], np.tan(x[::5]), c='green', s=20, label='tan points')
    
    # 左侧面板：支持图
    left_panel.ax.plot(x, np.log(x + 1), 'purple', linewidth=2, label='log(x+1)')
    left_panel.ax.plot(x, np.sqrt(x), 'orange', linewidth=2, label='sqrt(x)')
    
    # 右侧面板：附加图
    right_panel.ax.plot(x, np.sin(x) + np.cos(x), 'brown', linewidth=2, label='sin+cos')
    right_panel.ax.plot(x, np.sin(x) - np.cos(x), 'pink', linewidth=2, label='sin-cos')
    right_panel.ax.plot(x, np.sin(x) * np.cos(x), 'cyan', linewidth=2, label='sin*cos')
    
    print("2. 绘制数据")
    
    # 3. 手动添加所有 mortise 到 legend 管理器
    legend_manager = root.get_legend_manager()
    legend_manager.mortises = []
    
    legend_manager.add_mortise(root)
    legend_manager.add_mortise(top_panel)
    legend_manager.add_mortise(bottom_panel)
    legend_manager.add_mortise(left_panel)
    legend_manager.add_mortise(right_panel)
    
    print("3. 添加所有 mortise 到 legend 管理器")
    
    # 4. 收集所有 legend 信息
    legend_info = legend_manager.collect_legends()
    
    print("4. 收集 legend 信息")
    
    # 5. 创建自定义布局的 global legend
    print("\n5. 创建自定义布局的 global legend")
    
    # 定义自定义布局配置
    custom_layout_config = {
        'mortise_1': {'title': 'Main Plot', 'position': 'top_left', 'ncol': 2, 'priority': 1},
        'mortise_2': {'title': 'Secondary Plot', 'position': 'top_right', 'ncol': 3, 'priority': 2},
        'mortise_3': {'title': 'Supporting Plot', 'position': 'bottom_left', 'ncol': 2, 'priority': 3},
        'mortise_4': {'title': 'Additional Plot', 'position': 'bottom_right', 'ncol': 3, 'priority': 4}
    }
    
    # 为每个子图创建独立的 legend
    subplot_legends = {}
    
    for mortise_name, mortise_info in legend_info['mortise_legends'].items():
        mortise_obj = mortise_info['mortise']
        handles = mortise_info['handles']
        labels = mortise_info['labels']
        
        if handles and labels and mortise_name in custom_layout_config:
            config = custom_layout_config[mortise_name]
            subplot_title = config['title']
            panel = mortise_obj
            ncol = config['ncol']
            priority = config['priority']
            
            # 创建独立的 legend
            legend = panel.ax.legend(handles, labels, loc='upper right', ncol=ncol)
            
            if legend:
                subplot_legends[mortise_name] = {
                    'legend': legend,
                    'title': subplot_title,
                    'handles': handles,
                    'labels': labels,
                    'panel': panel,
                    'ncol': ncol,
                    'priority': priority
                }
                
                print(f"   - {mortise_name}: {subplot_title} ({len(labels)} 个元素, {ncol} 列)")
    
    # 6. 创建自定义布局的全局 legend panel
    print("\n6. 创建自定义布局的全局 legend panel")
    
    # 按优先级排序
    sorted_mortises = sorted(custom_layout_config.items(), key=lambda x: x[1]['priority'])
    
    # 收集所有子图 legend 信息
    all_handles = []
    all_labels = []
    group_titles = []
    group_positions = []
    
    for mortise_name, config in sorted_mortises:
        if mortise_name in subplot_legends:
            legend_info = subplot_legends[mortise_name]
            handles = legend_info['handles']
            labels = legend_info['labels']
            title = config['title']
            
            # 添加分组标题
            group_titles.append(title)
            group_positions.append(len(all_labels))
            
            # 添加 handles 和 labels
            all_handles.extend(handles)
            all_labels.extend(labels)
    
    if all_handles and all_labels:
        # 创建全局 legend panel
        global_legend = root._figure.legend(all_handles, all_labels, 
                                           loc='upper center', ncol=5)
        
        print(f"   - 自定义布局的全局 legend panel 创建成功")
        print(f"   - Legend items: {len(global_legend.get_texts())}")
        print(f"   - Legend labels: {[text.get_text() for text in global_legend.get_texts()]}")
        
        # 添加分组标题
        print("\n7. 添加分组标题")
        
        # 为每个分组添加标题
        for i, (title, pos) in enumerate(zip(group_titles, group_positions)):
            if i < len(group_titles) - 1:
                # 计算标题位置
                title_x = 0.1 + (pos / len(all_labels)) * 0.8
                title_y = 0.95
                
                # 添加标题文本
                title_text = root._figure.text(title_x, title_y, title,
                                             transform=root._figure.transFigure,
                                             fontsize=10, fontweight='bold',
                                             ha='center', va='bottom')
                
                print(f"   - 分组 {i+1}: {title} (位置: {pos})")
    
    # 保存图片
    fig.savefig('examples/new_global_legend_custom.png', dpi=150, bbox_inches='tight')
    print("   - 图片已保存: examples/new_global_legend_custom.png")
    
    return fig, root

def main():
    """主函数"""
    
    print("Sunmao 新 Global Legend 用法示例\n")
    
    try:
        # 运行各种示例
        example_basic_usage()
        example_advanced_usage()
        example_custom_layout()
        
        print("\n=== 示例完成 ===")
        print("新 Global Legend 用法示例:")
        print("✅ 基本用法")
        print("✅ 高级用法")
        print("✅ 自定义布局")
        
        print("\n=== 使用方法总结 ===")
        print("1. 创建多面板布局")
        print("2. 绘制数据并添加 labels")
        print("3. 手动添加所有 mortise 到 legend 管理器")
        print("4. 收集 legend 信息")
        print("5. 为每个子图创建独立的 legend")
        print("6. 创建全局 legend panel")
        print("7. 添加分组标题和分隔符")
        
        print("\n=== 关键代码 ===")
        print("""
# 1. 手动添加所有 mortise 到 legend 管理器
legend_manager = root.get_legend_manager()
legend_manager.mortises = []

legend_manager.add_mortise(root)
legend_manager.add_mortise(panel1)
legend_manager.add_mortise(panel2)
# ... 添加所有面板

# 2. 收集 legend 信息
legend_info = legend_manager.collect_legends()

# 3. 为每个子图创建独立的 legend
subplot_legends = {}
for mortise_name, mortise_info in legend_info['mortise_legends'].items():
    handles = mortise_info['handles']
    labels = mortise_info['labels']
    
    if handles and labels:
        legend = panel.ax.legend(handles, labels, loc='upper right', ncol=1)
        subplot_legends[mortise_name] = {
            'legend': legend,
            'title': subplot_title,
            'handles': handles,
            'labels': labels,
            'panel': panel
        }

# 4. 创建全局 legend panel
all_handles = []
all_labels = []
group_titles = []
group_positions = []

for mortise_name in arrangement_order:
    if mortise_name in subplot_legends:
        legend_info = subplot_legends[mortise_name]
        handles = legend_info['handles']
        labels = legend_info['labels']
        title = legend_info['title']
        
        group_titles.append(title)
        group_positions.append(len(all_labels))
        
        all_handles.extend(handles)
        all_labels.extend(labels)

# 5. 创建全局 legend
global_legend = root._figure.legend(all_handles, all_labels, 
                                   loc='upper center', ncol=4)

# 6. 添加分组标题
for i, (title, pos) in enumerate(zip(group_titles, group_positions)):
    if i < len(group_titles) - 1:
        title_x = 0.1 + (pos / len(all_labels)) * 0.8
        title_y = 0.95
        
        title_text = root._figure.text(title_x, title_y, title,
                                     transform=root._figure.transFigure,
                                     fontsize=10, fontweight='bold',
                                     ha='center', va='bottom')
        """)
        
        print("\n=== 关键特性 ===")
        print("- 每个子图的 legend 独立处理")
        print("- 全局 legend panel 统一管理")
        print("- 支持分组标题和分隔符")
        print("- 避免不同图表类型的 legend 混排")
        print("- 支持自定义布局和排列顺序")
        print("- 支持 colorbar 集成")
        
        print("\n=== 优势 ===")
        print("- 美观：移除 'Panel' 前缀")
        print("- 可读：添加分组标题")
        print("- 灵活：支持自定义布局")
        print("- 智能：考虑 colorbar 方向")
        print("- 统一：全局 legend panel 管理")
        
        print("\n生成的示例图片:")
        print("- examples/new_global_legend_basic.png")
        print("- examples/new_global_legend_advanced.png")
        print("- examples/new_global_legend_custom.png")
        
    except Exception as e:
        print(f"\n❌ 示例运行过程中出现错误: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎉 新 Global Legend 用法示例运行成功！")
        print("已展示新的 global legend 设计的使用方法。")
    else:
        print("\n💥 示例运行失败。")
    
    # 显示图片（可选）
    # plt.show()
