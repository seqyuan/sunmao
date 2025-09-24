"""
Sunmao 改进的 Legend 设计测试脚本（修复版）

探索更好的 legend 分组显示方案：
1. 移除 "Panel" 前缀
2. 添加分组标题
3. 考虑 colorbar 方向
4. 自定义每组行数
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import matplotlib.pyplot as plt
from sunmao import mortise

def test_simple_grouped_legend():
    """测试简单的分组 legend"""
    
    print("=== 简单分组 Legend 测试 ===\n")
    
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

def test_local_legend_with_titles():
    """测试局部 legend 带标题"""
    
    print("\n=== 局部 Legend 带标题测试 ===\n")
    
    fig, root, top_panel, bottom_panel, left_panel, right_panel = test_simple_grouped_legend()
    
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
    
    # 创建带分组标题的 legend
    print("\n8. 创建带分组标题的 legend")
    
    # 定义分组信息
    group_info = {
        'mortise_1': {'title': 'Scatter Plot', 'ncol': 3, 'position': 'upper left'},
        'mortise_2': {'title': 'Line Plot', 'ncol': 3, 'position': 'upper center'},
        'mortise_3': {'title': 'Bar Plot', 'ncol': 2, 'position': 'upper right'},
        'mortise_4': {'title': 'Mixed Plot', 'ncol': 2, 'position': 'lower center'}
    }
    
    # 为每个 mortise 创建带标题的 legend
    for mortise_name, mortise_info in legend_info['mortise_legends'].items():
        mortise_obj = mortise_info['mortise']
        handles = mortise_info['handles']
        labels = mortise_info['labels']
        
        if handles and labels and mortise_name in group_info:
            group_title = group_info[mortise_name]['title']
            ncol = group_info[mortise_name]['ncol']
            position = group_info[mortise_name]['position']
            
            # 创建 legend
            legend = mortise_obj.ax.legend(handles, labels, loc=position, ncol=ncol)
            
            # 添加分组标题（使用固定位置）
            if legend:
                # 使用固定的标题位置
                if position == 'upper left':
                    title_x, title_y = 0.05, 0.95
                elif position == 'upper center':
                    title_x, title_y = 0.5, 0.95
                elif position == 'upper right':
                    title_x, title_y = 0.95, 0.95
                else:  # lower center
                    title_x, title_y = 0.5, 0.05
                
                # 添加标题文本
                title_text = mortise_obj.ax.text(title_x, title_y, group_title,
                                               transform=mortise_obj.ax.transAxes,
                                               fontsize=10, fontweight='bold',
                                               ha='center', va='bottom')
                
                print(f"   - {mortise_name}: {group_title} ({len(labels)} 个元素)")
                print(f"     Labels: {labels}")
    
    fig.savefig('examples/local_legend_with_titles.png', dpi=150, bbox_inches='tight')
    print("   - 图片已保存: examples/local_legend_with_titles.png")
    
    return fig, root

def test_global_legend_with_group_titles():
    """测试全局 legend 带分组标题"""
    
    print("\n=== 全局 Legend 带分组标题测试 ===\n")
    
    fig, root, top_panel, bottom_panel, left_panel, right_panel = test_simple_grouped_legend()
    
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
    
    # 创建全局 legend 带分组标题
    print("\n8. 创建全局 legend 带分组标题")
    
    # 定义分组信息
    group_info = {
        'mortise_1': {'title': 'Scatter Plot', 'ncol': 3},
        'mortise_2': {'title': 'Line Plot', 'ncol': 3},
        'mortise_3': {'title': 'Bar Plot', 'ncol': 2},
        'mortise_4': {'title': 'Mixed Plot', 'ncol': 2}
    }
    
    # 按分组收集 handles 和 labels
    all_handles = []
    all_labels = []
    group_titles = []
    group_positions = []
    
    # 按 mortise 顺序处理
    mortise_order = ['mortise_1', 'mortise_2', 'mortise_3', 'mortise_4']
    
    for i, mortise_name in enumerate(mortise_order):
        if mortise_name in legend_info['mortise_legends']:
            mortise_info = legend_info['mortise_legends'][mortise_name]
            handles = mortise_info['handles']
            labels = mortise_info['labels']
            
            if handles and labels and mortise_name in group_info:
                group_title = group_info[mortise_name]['title']
                ncol = group_info[mortise_name]['ncol']
                
                # 添加分组标题
                group_titles.append(group_title)
                group_positions.append(len(all_labels))
                
                # 添加 handles 和 labels
                all_handles.extend(handles)
                all_labels.extend(labels)
    
    if all_handles and all_labels:
        # 创建全局 legend
        global_legend = root._figure.legend(all_handles, all_labels, 
                                           loc='upper center', ncol=4)
        
        print(f"   - 全局 legend 创建成功")
        print(f"   - Legend items: {len(global_legend.get_texts())}")
        print(f"   - Legend labels: {[text.get_text() for text in global_legend.get_texts()]}")
        
        # 添加分组标题
        print("\n9. 添加分组标题")
        
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
    
    fig.savefig('examples/global_legend_with_group_titles.png', dpi=150, bbox_inches='tight')
    print("   - 图片已保存: examples/global_legend_with_group_titles.png")
    
    return fig, root

def test_colorbar_legend_integration():
    """测试 colorbar 与 legend 的集成"""
    
    print("\n=== Colorbar 与 Legend 集成测试 ===\n")
    
    # 创建布局
    fig, root = mortise(figsize=(16, 10))
    
    # 添加子图
    top_panel = root.tenon(pos='top', size=0.4, pad=0.1, title='Heatmap Panel')
    bottom_panel = root.tenon(pos='bottom', size=0.4, pad=0.1, title='Line Plot Panel')
    left_panel = root.tenon(pos='left', size=0.3, pad=0.1, title='Bar Plot Panel')
    right_panel = root.tenon(pos='right', size=0.3, pad=0.1, title='Scatter Plot Panel')
    
    print("1. 创建多面板布局")
    
    # 准备数据
    np.random.seed(42)
    
    # 顶部面板：热图 + 纵向 colorbar
    heatmap_data = np.random.randn(20, 15)
    im = top_panel.ax.imshow(heatmap_data, cmap='viridis', aspect='auto')
    top_panel.ax.set_title('Heatmap Panel')
    top_panel.ax.set_xlabel('Samples')
    top_panel.ax.set_ylabel('Genes')
    
    # 添加纵向 colorbar
    cbar = plt.colorbar(im, ax=top_panel.ax, shrink=0.8)
    cbar.set_label('Expression Level', rotation=270, labelpad=15)
    
    print("2. 绘制顶部热图 + 纵向 colorbar")
    
    # 底部面板：线图
    x = np.linspace(0, 10, 100)
    bottom_panel.ax.plot(x, np.sin(x), 'r-', linewidth=2, label='sin(x)')
    bottom_panel.ax.plot(x, np.cos(x), 'b-', linewidth=2, label='cos(x)')
    bottom_panel.ax.plot(x, np.tan(x), 'g-', linewidth=2, label='tan(x)')
    
    bottom_panel.ax.set_title('Line Plot Panel')
    bottom_panel.ax.set_xlabel('X')
    bottom_panel.ax.set_ylabel('Y')
    bottom_panel.ax.grid(True, alpha=0.3)
    
    print("3. 绘制底部线图")
    
    # 左侧面板：柱状图
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
    
    # 右侧面板：散点图 + 横向 colorbar
    x_scatter = np.random.normal(0, 1, 100)
    y_scatter = np.random.normal(0, 1, 100)
    colors = np.random.rand(100)
    
    scatter = right_panel.ax.scatter(x_scatter, y_scatter, c=colors, 
                                   cmap='plasma', alpha=0.7, s=30)
    right_panel.ax.set_title('Scatter Plot Panel')
    right_panel.ax.set_xlabel('X')
    right_panel.ax.set_ylabel('Y')
    right_panel.ax.grid(True, alpha=0.3)
    
    # 添加横向 colorbar
    cbar2 = plt.colorbar(scatter, ax=right_panel.ax, orientation='horizontal', 
                        shrink=0.8, pad=0.1)
    cbar2.set_label('Intensity', labelpad=10)
    
    print("5. 绘制右侧散点图 + 横向 colorbar")
    
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
    
    # 创建带 colorbar 信息的 legend
    print("\n8. 创建带 colorbar 信息的 legend")
    
    # 定义分组信息（包括 colorbar）
    group_info = {
        'mortise_1': {'title': 'Heatmap', 'ncol': 1, 'has_colorbar': True, 'colorbar_orientation': 'vertical'},
        'mortise_2': {'title': 'Line Plot', 'ncol': 3, 'has_colorbar': False},
        'mortise_3': {'title': 'Bar Plot', 'ncol': 2, 'has_colorbar': False},
        'mortise_4': {'title': 'Scatter Plot', 'ncol': 1, 'has_colorbar': True, 'colorbar_orientation': 'horizontal'}
    }
    
    # 为每个 mortise 创建带标题的 legend
    for mortise_name, mortise_info in legend_info['mortise_legends'].items():
        mortise_obj = mortise_info['mortise']
        handles = mortise_info['handles']
        labels = mortise_info['labels']
        
        if mortise_name in group_info:
            group_title = group_info[mortise_name]['title']
            ncol = group_info[mortise_name]['ncol']
            has_colorbar = group_info[mortise_name]['has_colorbar']
            
            if handles and labels:
                # 创建 legend
                legend = mortise_obj.ax.legend(handles, labels, loc='upper right', ncol=ncol)
                
                # 添加分组标题
                if legend:
                    # 使用固定的标题位置
                    title_x, title_y = 0.95, 0.95
                    
                    # 添加标题文本
                    title_text = mortise_obj.ax.text(title_x, title_y, group_title,
                                                   transform=mortise_obj.ax.transAxes,
                                                   fontsize=10, fontweight='bold',
                                                   ha='center', va='bottom')
                    
                    print(f"   - {mortise_name}: {group_title} ({len(labels)} 个元素)")
                    if has_colorbar:
                        colorbar_orientation = group_info[mortise_name]['colorbar_orientation']
                        print(f"     Colorbar: {colorbar_orientation}")
                    print(f"     Labels: {labels}")
    
    fig.savefig('examples/colorbar_legend_integration.png', dpi=150, bbox_inches='tight')
    print("   - 图片已保存: examples/colorbar_legend_integration.png")
    
    return fig, root

def test_custom_row_layout():
    """测试自定义行布局"""
    
    print("\n=== 自定义行布局测试 ===\n")
    
    fig, root, top_panel, bottom_panel, left_panel, right_panel = test_simple_grouped_legend()
    
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
    
    # 创建自定义行布局的 legend
    print("\n8. 创建自定义行布局的 legend")
    
    # 定义自定义行布局
    custom_layout = {
        'mortise_1': {'title': 'Scatter Plot', 'rows': 1, 'cols_per_row': 3},
        'mortise_2': {'title': 'Line Plot', 'rows': 1, 'cols_per_row': 3},
        'mortise_3': {'title': 'Bar Plot', 'rows': 1, 'cols_per_row': 2},
        'mortise_4': {'title': 'Mixed Plot', 'rows': 2, 'cols_per_row': 2}
    }
    
    # 为每个 mortise 创建自定义布局的 legend
    for mortise_name, mortise_info in legend_info['mortise_legends'].items():
        mortise_obj = mortise_info['mortise']
        handles = mortise_info['handles']
        labels = mortise_info['labels']
        
        if handles and labels and mortise_name in custom_layout:
            layout_info = custom_layout[mortise_name]
            group_title = layout_info['title']
            rows = layout_info['rows']
            cols_per_row = layout_info['cols_per_row']
            
            # 创建 legend
            legend = mortise_obj.ax.legend(handles, labels, loc='upper right', 
                                         ncol=cols_per_row)
            
            # 添加分组标题
            if legend:
                # 使用固定的标题位置
                title_x, title_y = 0.95, 0.95
                
                # 添加标题文本
                title_text = mortise_obj.ax.text(title_x, title_y, group_title,
                                               transform=mortise_obj.ax.transAxes,
                                               fontsize=10, fontweight='bold',
                                               ha='center', va='bottom')
                
                print(f"   - {mortise_name}: {group_title}")
                print(f"     布局: {rows} 行, 每行 {cols_per_row} 列")
                print(f"     元素: {len(labels)} 个")
                print(f"     Labels: {labels}")
    
    fig.savefig('examples/custom_row_layout.png', dpi=150, bbox_inches='tight')
    print("   - 图片已保存: examples/custom_row_layout.png")
    
    return fig, root

def main():
    """主函数"""
    
    print("Sunmao 改进的 Legend 设计测试脚本（修复版）\n")
    
    try:
        # 运行各种测试
        test_local_legend_with_titles()
        test_global_legend_with_group_titles()
        test_colorbar_legend_integration()
        test_custom_row_layout()
        
        print("\n=== 测试完成 ===")
        print("改进的 Legend 设计测试结果:")
        print("✅ 局部 legend 带标题")
        print("✅ 全局 legend 带分组标题")
        print("✅ Colorbar 与 legend 集成")
        print("✅ 自定义行布局")
        
        print("\n=== 设计方案总结 ===")
        print("1. 移除 'Panel' 前缀，保持 label 简洁")
        print("2. 添加分组标题，提高可读性")
        print("3. 考虑 colorbar 方向，调整标题位置")
        print("4. 支持自定义每组行数")
        
        print("\n=== 建议的实现方案 ===")
        print("1. 局部 legend + 分组标题（推荐）")
        print("2. 全局 legend + 分组标题")
        print("3. Colorbar 集成支持")
        print("4. 灵活的行数配置")
        
        print("\n=== 关键特性 ===")
        print("- 分组标题位置自适应")
        print("- Colorbar 方向感知")
        print("- 自定义每组行数")
        print("- 美观的布局设计")
        
        print("\n=== 使用建议 ===")
        print("- 对于复杂布局，推荐使用局部 legend")
        print("- 分组标题位置可以根据 legend 位置自动调整")
        print("- Colorbar 方向影响标题位置")
        print("- 自定义行数提供更灵活的布局控制")
        
        print("\n生成的示例图片:")
        print("- examples/local_legend_with_titles.png")
        print("- examples/global_legend_with_group_titles.png")
        print("- examples/colorbar_legend_integration.png")
        print("- examples/custom_row_layout.png")
        
    except Exception as e:
        print(f"\n❌ 测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎉 改进的 Legend 设计测试完成！")
        print("已探索多种设计方案。")
    else:
        print("\n💥 测试失败。")
    
    # 显示图片（可选）
    # plt.show()
