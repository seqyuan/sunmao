"""
Sunmao Legend 混排问题测试脚本

测试多子图 legend 混排时的问题
验证不同图表类型的 legend 元素被混排的情况
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import matplotlib.pyplot as plt
from sunmao import mortise

def test_legend_mixing_problem():
    """测试 legend 混排问题"""
    
    print("=== Legend 混排问题测试 ===\n")
    
    # 创建布局
    fig, root = mortise(figsize=(14, 8))
    
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
        top_panel.ax.scatter(x, y_scatter, c=color, label=f'Scatter Group {i+1}', 
                           alpha=0.7, s=30)
    
    top_panel.ax.set_title('Scatter Plot Panel')
    top_panel.ax.set_xlabel('X')
    top_panel.ax.set_ylabel('Y')
    top_panel.ax.grid(True, alpha=0.3)
    
    print("2. 绘制顶部散点图（3个 legend 元素）")
    
    # 底部面板：线图（3个 legend 元素）
    bottom_panel.ax.plot(x, np.sin(x), 'r-', linewidth=2, label='sin(x)')
    bottom_panel.ax.plot(x, np.cos(x), 'b-', linewidth=2, label='cos(x)')
    bottom_panel.ax.plot(x, np.tan(x), 'g-', linewidth=2, label='tan(x)')
    
    bottom_panel.ax.set_title('Line Plot Panel')
    bottom_panel.ax.set_xlabel('X')
    bottom_panel.ax.set_ylabel('Y')
    bottom_panel.ax.grid(True, alpha=0.3)
    
    print("3. 绘制底部线图（3个 legend 元素）")
    
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
    
    print("4. 绘制左侧柱状图（2个 legend 元素）")
    
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
    
    print("5. 绘制右侧混合图（4个 legend 元素）")
    
    return fig, root, top_panel, bottom_panel, left_panel, right_panel

def test_global_legend_mixing():
    """测试全局 legend 混排问题"""
    
    print("\n=== 全局 Legend 混排问题测试 ===\n")
    
    fig, root, top_panel, bottom_panel, left_panel, right_panel = test_legend_mixing_problem()
    
    # 手动添加所有 mortise 到 legend 管理器
    legend_manager = root.get_legend_manager()
    legend_manager.mortises = []
    
    legend_manager.add_mortise(root)
    legend_manager.add_mortise(top_panel)
    legend_manager.add_mortise(bottom_panel)
    legend_manager.add_mortise(left_panel)
    legend_manager.add_mortise(right_panel)
    
    print("6. 添加所有 mortise 到 legend 管理器")
    print(f"   - 管理的 mortise 数量: {len(legend_manager.mortises)}")
    
    # 创建全局 legend（每行2个元素）
    global_legend = root.create_legend(mode='global', position='upper center', ncol=2)
    
    print("7. 创建全局 legend（每行2个元素）")
    print(f"   - Global legend created: {global_legend is not None}")
    
    if global_legend:
        print(f"   - Legend items: {len(global_legend.get_texts())}")
        print(f"   - Legend labels: {[text.get_text() for text in global_legend.get_texts()]}")
        
        # 分析混排问题
        print("\n8. 分析混排问题:")
        labels = [text.get_text() for text in global_legend.get_texts()]
        
        print("   - 散点图 legend 元素:")
        scatter_labels = [label for label in labels if 'Scatter' in label]
        print(f"     {scatter_labels}")
        
        print("   - 线图 legend 元素:")
        line_labels = [label for label in labels if any(func in label for func in ['sin', 'cos', 'tan'])]
        print(f"     {line_labels}")
        
        print("   - 柱状图 legend 元素:")
        bar_labels = [label for label in labels if 'Group' in label]
        print(f"     {bar_labels}")
        
        print("   - 混合图 legend 元素:")
        mixed_labels = [label for label in labels if label in ['exp(-x)', 'log(x+1)', 'Random Points', 'Zero Line']]
        print(f"     {mixed_labels}")
        
        # 检查混排情况
        print("\n9. 检查混排情况:")
        print("   - 按顺序显示所有 legend 元素:")
        for i, label in enumerate(labels):
            print(f"     {i+1}. {label}")
        
        print("\n   - 混排分析:")
        print("     * 散点图有3个元素，线图有3个元素")
        print("     * 如果每行2个元素，散点图的第3个元素会和线图的第1个元素在同一行")
        print("     * 这会导致不同图表类型的 legend 元素混排")
    
    fig.savefig('examples/legend_mixing_problem.png', dpi=150, bbox_inches='tight')
    print("   - 图片已保存: examples/legend_mixing_problem.png")
    
    return fig, root

def test_grouped_legend_solution():
    """测试分组 legend 解决方案"""
    
    print("\n=== 分组 Legend 解决方案测试 ===\n")
    
    fig, root, top_panel, bottom_panel, left_panel, right_panel = test_legend_mixing_problem()
    
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
    print(f"   - 总 handles: {len(legend_info['handles'])}")
    print(f"   - 总 labels: {len(legend_info['labels'])}")
    print(f"   - Mortise legends: {len(legend_info['mortise_legends'])}")
    
    # 按 mortise 分组创建 legend
    print("\n8. 按 mortise 分组创建 legend")
    
    # 为每个 mortise 创建独立的 legend
    for mortise_name, mortise_info in legend_info['mortise_legends'].items():
        mortise_obj = mortise_info['mortise']
        handles = mortise_info['handles']
        labels = mortise_info['labels']
        
        if handles and labels:
            # 创建局部 legend
            legend = mortise_obj.ax.legend(handles, labels, loc='upper right', 
                                         bbox_to_anchor=(1, 1))
            print(f"   - {mortise_name}: {len(labels)} 个 legend 元素")
            print(f"     Labels: {labels}")
    
    # 创建全局 legend（按组分组）
    print("\n9. 创建分组全局 legend")
    
    # 按 mortise 分组收集 handles 和 labels
    grouped_handles = []
    grouped_labels = []
    
    for mortise_name, mortise_info in legend_info['mortise_legends'].items():
        handles = mortise_info['handles']
        labels = mortise_info['labels']
        
        if handles and labels:
            # 添加分组标识
            group_name = mortise_name.replace('mortise_', 'Panel ')
            grouped_handles.extend(handles)
            grouped_labels.extend([f"{group_name}: {label}" for label in labels])
    
    if grouped_handles and grouped_labels:
        # 创建全局 legend
        global_legend = root._figure.legend(grouped_handles, grouped_labels, 
                                           loc='upper center', ncol=2)
        
        print(f"   - 分组全局 legend 创建成功")
        print(f"   - Legend items: {len(global_legend.get_texts())}")
        print(f"   - Legend labels: {[text.get_text() for text in global_legend.get_texts()]}")
    
    fig.savefig('examples/grouped_legend_solution.png', dpi=150, bbox_inches='tight')
    print("   - 图片已保存: examples/grouped_legend_solution.png")
    
    return fig, root

def test_improved_legend_manager():
    """测试改进的 legend 管理器"""
    
    print("\n=== 改进的 Legend 管理器测试 ===\n")
    
    fig, root, top_panel, bottom_panel, left_panel, right_panel = test_legend_mixing_problem()
    
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
    
    # 按 mortise 分组，每组内部保持顺序
    print("\n8. 按 mortise 分组创建 legend")
    
    # 为每个 mortise 创建独立的 legend
    for mortise_name, mortise_info in legend_info['mortise_legends'].items():
        mortise_obj = mortise_info['mortise']
        handles = mortise_info['handles']
        labels = mortise_info['labels']
        
        if handles and labels:
            # 创建局部 legend
            legend = mortise_obj.ax.legend(handles, labels, loc='upper right', 
                                         bbox_to_anchor=(1, 1))
            print(f"   - {mortise_name}: {len(labels)} 个 legend 元素")
            print(f"     Labels: {labels}")
    
    # 创建全局 legend（保持分组顺序）
    print("\n9. 创建保持分组顺序的全局 legend")
    
    # 按 mortise 顺序收集 handles 和 labels
    ordered_handles = []
    ordered_labels = []
    
    # 按 mortise 顺序处理
    mortise_order = ['mortise_0', 'mortise_1', 'mortise_2', 'mortise_3', 'mortise_4']
    
    for mortise_name in mortise_order:
        if mortise_name in legend_info['mortise_legends']:
            mortise_info = legend_info['mortise_legends'][mortise_name]
            handles = mortise_info['handles']
            labels = mortise_info['labels']
            
            if handles and labels:
                ordered_handles.extend(handles)
                ordered_labels.extend(labels)
    
    if ordered_handles and ordered_labels:
        # 创建全局 legend
        global_legend = root._figure.legend(ordered_handles, ordered_labels, 
                                           loc='upper center', ncol=3)
        
        print(f"   - 保持分组顺序的全局 legend 创建成功")
        print(f"   - Legend items: {len(global_legend.get_texts())}")
        print(f"   - Legend labels: {[text.get_text() for text in global_legend.get_texts()]}")
        
        # 分析分组效果
        print("\n10. 分析分组效果:")
        labels = [text.get_text() for text in global_legend.get_texts()]
        
        print("   - 按顺序显示所有 legend 元素:")
        for i, label in enumerate(labels):
            print(f"     {i+1}. {label}")
        
        print("\n   - 分组效果分析:")
        print("     * 散点图元素: 1-3")
        print("     * 线图元素: 4-6")
        print("     * 柱状图元素: 7-8")
        print("     * 混合图元素: 9-12")
        print("     * 每行3个元素，同类型元素更可能在同一行")
    
    fig.savefig('examples/improved_legend_manager.png', dpi=150, bbox_inches='tight')
    print("   - 图片已保存: examples/improved_legend_manager.png")
    
    return fig, root

def main():
    """主函数"""
    
    print("Sunmao Legend 混排问题测试脚本\n")
    
    try:
        # 运行各种测试
        test_global_legend_mixing()
        test_grouped_legend_solution()
        test_improved_legend_manager()
        
        print("\n=== 测试完成 ===")
        print("Legend 混排问题测试结果:")
        print("✅ 全局 legend 混排问题识别")
        print("✅ 分组 legend 解决方案")
        print("✅ 改进的 legend 管理器")
        
        print("\n=== 问题总结 ===")
        print("1. 问题：不同图表类型的 legend 元素被混排")
        print("2. 原因：全局 legend 按顺序排列，不考虑图表类型")
        print("3. 影响：降低图例的可读性和逻辑性")
        
        print("\n=== 解决方案 ===")
        print("1. 按 mortise 分组创建局部 legend")
        print("2. 保持分组顺序创建全局 legend")
        print("3. 使用分组标识区分不同图表类型")
        print("4. 调整 ncol 参数优化布局")
        
        print("\n=== 建议 ===")
        print("- 对于复杂布局，建议使用局部 legend")
        print("- 如果需要全局 legend，考虑按图表类型分组")
        print("- 使用合适的 ncol 参数避免混排")
        print("- 考虑添加分组标识提高可读性")
        
        print("\n生成的示例图片:")
        print("- examples/legend_mixing_problem.png")
        print("- examples/grouped_legend_solution.png")
        print("- examples/improved_legend_manager.png")
        
    except Exception as e:
        print(f"\n❌ 测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎉 Legend 混排问题测试完成！")
        print("已识别问题并提供解决方案。")
    else:
        print("\n💥 测试失败。")
    
    # 显示图片（可选）
    # plt.show()
