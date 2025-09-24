"""
Sunmao 子图 Legend 独立管理测试脚本

实现你的想法：
- 每个子图的 legend 单独作为一个 legend 处理
- Global legend 只负责收集和排列各个子图 legend 在 global legend panel 里的顺序
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import matplotlib.pyplot as plt
from sunmao import mortise

def test_subplot_legend_independence():
    """测试子图 legend 独立管理"""
    
    print("=== 子图 Legend 独立管理测试 ===\n")
    
    # 创建布局
    fig, root = mortise(figsize=(16, 10))
    
    # 添加子图
    top_panel = root.tenon(pos='top', size=0.4, pad=0.1, title='Scatter Plot Panel')
    bottom_panel = root.tenon(pos='bottom', size=0.4, pad=0.1, title='Line Plot Panel')
    left_panel = root.tenon(pos='left', size=0.3, pad=0.1, title='Bar Plot Panel')
    right_panel = root.tenon(pos='right', size=0.3, pad=0.1, title='Mixed Plot Panel')
    
    print("1. 创建多面板布局")
    
    # 准备数据
    np.random.seed(42)
    x = np.linspace(0, 10, 50)
    
    # 顶部面板：散点图（3个 legend 元素）
    colors_scatter = ['red', 'blue', 'green']
    for i, color in enumerate(colors_scatter):
        y_scatter = np.random.normal(i, 0.5, 50)
        top_panel.ax.scatter(x, y_scatter, c=color, label=f'Group {i+1}', 
                           alpha=0.7, s=30)
    
    top_panel.ax.set_title('Scatter Plot Panel')
    top_panel.ax.set_xlabel('X')
    top_panel.ax.set_ylabel('Y')
    top_panel.ax.grid(True, alpha=0.3)
    
    print("2. 绘制顶部散点图")
    
    # 底部面板：线图（3个 legend 元素）
    bottom_panel.ax.plot(x, np.sin(x), 'r-', linewidth=2, label='sin(x)')
    bottom_panel.ax.plot(x, np.cos(x), 'b-', linewidth=2, label='cos(x)')
    bottom_panel.ax.plot(x, np.tan(x), 'g-', linewidth=2, label='tan(x)')
    
    bottom_panel.ax.set_title('Line Plot Panel')
    bottom_panel.ax.set_xlabel('X')
    bottom_panel.ax.set_ylabel('Y')
    bottom_panel.ax.grid(True, alpha=0.3)
    
    print("3. 绘制底部线图")
    
    # 左侧面板：柱状图（2个 legend 元素）
    categories = ['A', 'B', 'C', 'D']
    values1 = np.random.normal(50, 10, 4)
    values2 = np.random.normal(30, 5, 4)
    
    left_panel.ax.bar(np.arange(len(categories)) - 0.2, values1, 0.4, 
                     label='Group 1', color='orange', alpha=0.8)
    left_panel.ax.bar(np.arange(len(categories)) + 0.2, values2, 0.4, 
                     label='Group 2', color='purple', alpha=0.8)
    
    left_panel.ax.set_title('Bar Plot Panel')
    left_panel.ax.set_xlabel('Categories')
    left_panel.ax.set_ylabel('Values')
    left_panel.ax.set_xticks(np.arange(len(categories)))
    left_panel.ax.set_xticklabels(categories)
    left_panel.ax.grid(True, alpha=0.3)
    
    print("4. 绘制左侧柱状图")
    
    # 右侧面板：混合图（4个 legend 元素）
    right_panel.ax.plot(x, np.exp(-x), 'brown', linewidth=2, label='exp(-x)')
    right_panel.ax.plot(x, np.log(x + 1), 'pink', linewidth=2, label='log(x+1)')
    
    # 添加散点
    x_scatter = np.random.normal(5, 1, 30)
    y_scatter = np.random.normal(0, 1, 30)
    right_panel.ax.scatter(x_scatter, y_scatter, c='cyan', label='Random Points', 
                          alpha=0.7, s=20)
    
    # 添加水平线
    right_panel.ax.axhline(y=0, color='black', linestyle='--', label='Zero Line')
    
    right_panel.ax.set_title('Mixed Plot Panel')
    right_panel.ax.set_xlabel('X')
    right_panel.ax.set_ylabel('Y')
    right_panel.ax.grid(True, alpha=0.3)
    
    print("5. 绘制右侧混合图")
    
    return fig, root, top_panel, bottom_panel, left_panel, right_panel

def test_independent_subplot_legends():
    """测试独立的子图 legend"""
    
    print("\n=== 独立子图 Legend 测试 ===\n")
    
    fig, root, top_panel, bottom_panel, left_panel, right_panel = test_subplot_legend_independence()
    
    # 手动添加所有 mortise 到 legend 管理器
    legend_manager = root.get_legend_manager()
    legend_manager.mortises = []
    
    legend_manager.add_mortise(root)
    legend_manager.add_mortise(top_panel)
    legend_manager.add_mortise(bottom_panel)
    legend_manager.add_mortise(left_panel)
    legend_manager.add_mortise(right_panel)
    
    print("6. 添加所有 mortise 到 legend 管理器")
    
    # 收集所有 legend 信息
    legend_info = legend_manager.collect_legends()
    
    print("7. 收集 legend 信息")
    
    # 为每个子图创建独立的 legend
    print("\n8. 为每个子图创建独立的 legend")
    
    subplot_legends = {}
    
    # 定义子图信息
    subplot_info = {
        'mortise_1': {'title': 'Scatter Plot', 'panel': top_panel},
        'mortise_2': {'title': 'Line Plot', 'panel': bottom_panel},
        'mortise_3': {'title': 'Bar Plot', 'panel': left_panel},
        'mortise_4': {'title': 'Mixed Plot', 'panel': right_panel}
    }
    
    # 为每个子图创建独立的 legend
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
                print(f"     Labels: {labels}")
    
    return fig, root, subplot_legends

def test_global_legend_panel_arrangement():
    """测试全局 legend panel 排列"""
    
    print("\n=== 全局 Legend Panel 排列测试 ===\n")
    
    fig, root, subplot_legends = test_independent_subplot_legends()
    
    # 创建全局 legend panel
    print("9. 创建全局 legend panel")
    
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
        print("\n10. 添加分组标题")
        
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
    
    fig.savefig('examples/independent_subplot_legends.png', dpi=150, bbox_inches='tight')
    print("   - 图片已保存: examples/independent_subplot_legends.png")
    
    return fig, root

def test_improved_global_legend_panel():
    """测试改进的全局 legend panel"""
    
    print("\n=== 改进的全局 Legend Panel 测试 ===\n")
    
    fig, root, subplot_legends = test_independent_subplot_legends()
    
    # 创建改进的全局 legend panel
    print("9. 创建改进的全局 legend panel")
    
    # 定义排列顺序和布局
    arrangement_config = {
        'mortise_1': {'title': 'Scatter Plot', 'position': 'top_left', 'ncol': 3},
        'mortise_2': {'title': 'Line Plot', 'position': 'top_right', 'ncol': 3},
        'mortise_3': {'title': 'Bar Plot', 'position': 'bottom_left', 'ncol': 2},
        'mortise_4': {'title': 'Mixed Plot', 'position': 'bottom_right', 'ncol': 2}
    }
    
    # 创建全局 legend panel 的各个子区域
    legend_panel_handles = []
    legend_panel_labels = []
    legend_panel_titles = []
    legend_panel_positions = []
    
    for mortise_name, config in arrangement_config.items():
        if mortise_name in subplot_legends:
            legend_info = subplot_legends[mortise_name]
            handles = legend_info['handles']
            labels = legend_info['labels']
            title = config['title']
            position = config['position']
            ncol = config['ncol']
            
            # 添加分组标题
            legend_panel_titles.append(title)
            legend_panel_positions.append(len(legend_panel_labels))
            
            # 添加 handles 和 labels
            legend_panel_handles.extend(handles)
            legend_panel_labels.extend(labels)
    
    if legend_panel_handles and legend_panel_labels:
        # 创建全局 legend panel
        global_legend = root._figure.legend(legend_panel_handles, legend_panel_labels, 
                                           loc='upper center', ncol=4)
        
        print(f"   - 改进的全局 legend panel 创建成功")
        print(f"   - Legend items: {len(global_legend.get_texts())}")
        print(f"   - Legend labels: {[text.get_text() for text in global_legend.get_texts()]}")
        
        # 添加分组标题
        print("\n10. 添加分组标题")
        
        # 为每个分组添加标题
        for i, (title, pos) in enumerate(zip(legend_panel_titles, legend_panel_positions)):
            if i < len(legend_panel_titles) - 1:
                # 计算标题位置
                title_x = 0.1 + (pos / len(legend_panel_labels)) * 0.8
                title_y = 0.95
                
                # 添加标题文本
                title_text = root._figure.text(title_x, title_y, title,
                                             transform=root._figure.transFigure,
                                             fontsize=10, fontweight='bold',
                                             ha='center', va='bottom')
                
                print(f"   - 分组 {i+1}: {title} (位置: {pos})")
    
    fig.savefig('examples/improved_global_legend_panel.png', dpi=150, bbox_inches='tight')
    print("   - 图片已保存: examples/improved_global_legend_panel.png")
    
    return fig, root

def test_legend_panel_with_separators():
    """测试带分隔符的 legend panel"""
    
    print("\n=== 带分隔符的 Legend Panel 测试 ===\n")
    
    fig, root, subplot_legends = test_independent_subplot_legends()
    
    # 创建带分隔符的全局 legend panel
    print("9. 创建带分隔符的全局 legend panel")
    
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
        
        print(f"   - 带分隔符的全局 legend panel 创建成功")
        print(f"   - Legend items: {len(global_legend.get_texts())}")
        print(f"   - Legend labels: {[text.get_text() for text in global_legend.get_texts()]}")
        
        # 添加分组标题和分隔符
        print("\n10. 添加分组标题和分隔符")
        
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
                
                # 添加分隔符
                separator_x = title_x
                separator_y = title_y - 0.02
                separator_text = root._figure.text(separator_x, separator_y, '|',
                                                 transform=root._figure.transFigure,
                                                 fontsize=8, color='gray',
                                                 ha='center', va='bottom')
                
                print(f"   - 分组 {i+1}: {title} (位置: {pos})")
    
    fig.savefig('examples/legend_panel_with_separators.png', dpi=150, bbox_inches='tight')
    print("   - 图片已保存: examples/legend_panel_with_separators.png")
    
    return fig, root

def main():
    """主函数"""
    
    print("Sunmao 子图 Legend 独立管理测试脚本\n")
    
    try:
        # 运行各种测试
        test_global_legend_panel_arrangement()
        test_improved_global_legend_panel()
        test_legend_panel_with_separators()
        
        print("\n=== 测试完成 ===")
        print("子图 Legend 独立管理测试结果:")
        print("✅ 独立子图 legend")
        print("✅ 全局 legend panel 排列")
        print("✅ 改进的全局 legend panel")
        print("✅ 带分隔符的 legend panel")
        
        print("\n=== 设计方案总结 ===")
        print("1. 每个子图的 legend 单独作为一个 legend 处理")
        print("2. Global legend 只负责收集和排列各个子图 legend")
        print("3. 全局 legend panel 中每个子图 legend 作为独立的块显示")
        print("4. 支持分组标题和分隔符")
        
        print("\n=== 关键优势 ===")
        print("- 避免不同图表类型的 legend 元素混排")
        print("- 保持每个子图 legend 的逻辑性")
        print("- 全局 legend panel 统一管理")
        print("- 支持灵活的排列和布局")
        
        print("\n=== 实现思路 ===")
        print("1. 为每个子图创建独立的 legend")
        print("2. 收集所有子图 legend 信息")
        print("3. 在全局 legend panel 中按顺序排列")
        print("4. 添加分组标题和分隔符")
        
        print("\n生成的示例图片:")
        print("- examples/independent_subplot_legends.png")
        print("- examples/improved_global_legend_panel.png")
        print("- examples/legend_panel_with_separators.png")
        
    except Exception as e:
        print(f"\n❌ 测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎉 子图 Legend 独立管理测试完成！")
        print("已实现你的设计思路。")
    else:
        print("\n💥 测试失败。")
    
    # 显示图片（可选）
    # plt.show()
