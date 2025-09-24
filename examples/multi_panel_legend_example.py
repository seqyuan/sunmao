"""
Sunmao 多图 Legend 使用示例

展示如何正确使用 sunmao 的多面板 legend 功能
包括热图、统计图等多种图表类型的 legend 统一管理
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import matplotlib.pyplot as plt
from sunmao import mortise

def example_multi_panel_legend():
    """示例：多面板 legend 使用"""
    
    print("=== 多面板 Legend 使用示例 ===\n")
    
    # 1. 创建布局
    fig, root = mortise(figsize=(15, 10))
    
    # 中间热图
    heatmap_panel = root.tenon(pos='top', size=0.6, pad=0.1, title='Gene Expression Heatmap')
    
    # 左边统计图
    left_stats = root.tenon(pos='left', size=0.35, pad=0.1, title='Expression Statistics')
    
    # 右边聚类图
    right_cluster = root.tenon(pos='right', size=0.35, pad=0.1, title='Cluster Analysis')
    
    # 底部时间序列
    bottom_time = root.tenon(pos='bottom', size=0.3, pad=0.1, title='Time Series')
    
    print("1. 创建多面板布局")
    
    # 2. 绘制数据
    np.random.seed(42)
    
    # 热图
    heatmap_data = np.random.randn(20, 15)
    im = heatmap_panel.ax.imshow(heatmap_data, cmap='RdBu_r', aspect='auto')
    heatmap_panel.ax.set_title('Gene Expression Heatmap')
    heatmap_panel.ax.set_xlabel('Samples')
    heatmap_panel.ax.set_ylabel('Genes')
    
    # 添加颜色条
    cbar = plt.colorbar(im, ax=heatmap_panel.ax, shrink=0.8)
    cbar.set_label('Log2 Fold Change', rotation=270, labelpad=15)
    
    # 左边统计图
    categories = ['High', 'Medium', 'Low', 'Very Low']
    values = [45, 30, 20, 5]
    colors = ['red', 'orange', 'yellow', 'green']
    
    bars = left_stats.ax.bar(categories, values, color=colors, alpha=0.8)
    left_stats.ax.set_title('Expression Level Distribution')
    left_stats.ax.set_ylabel('Number of Genes')
    left_stats.ax.set_xlabel('Expression Level')
    left_stats.ax.grid(True, alpha=0.3)
    
    # 右边聚类图
    n_points = 100
    x_cluster = np.random.normal(0, 1, n_points)
    y_cluster = np.random.normal(0, 1, n_points)
    cluster_labels = np.random.choice(['Cluster 1', 'Cluster 2', 'Cluster 3'], n_points)
    
    colors_cluster = {'Cluster 1': 'red', 'Cluster 2': 'blue', 'Cluster 3': 'green'}
    
    for cluster in ['Cluster 1', 'Cluster 2', 'Cluster 3']:
        mask = cluster_labels == cluster
        right_cluster.ax.scatter(x_cluster[mask], y_cluster[mask], 
                                c=colors_cluster[cluster], label=cluster, 
                                alpha=0.7, s=30)
    
    right_cluster.ax.set_title('Gene Clustering')
    right_cluster.ax.set_xlabel('PC1')
    right_cluster.ax.set_ylabel('PC2')
    right_cluster.ax.grid(True, alpha=0.3)
    
    # 底部时间序列
    time_points = np.linspace(0, 24, 100)
    
    bottom_time.ax.plot(time_points, np.sin(time_points/4) + 1, 'b-', linewidth=2, label='Gene A')
    bottom_time.ax.plot(time_points, np.cos(time_points/3) + 1, 'r-', linewidth=2, label='Gene B')
    bottom_time.ax.plot(time_points, np.sin(time_points/2) + 1, 'g-', linewidth=2, label='Gene C')
    bottom_time.ax.plot(time_points, np.cos(time_points/5) + 1, 'm-', linewidth=2, label='Gene D')
    
    bottom_time.ax.set_title('Time Series Expression')
    bottom_time.ax.set_xlabel('Time (hours)')
    bottom_time.ax.set_ylabel('Expression Level')
    bottom_time.ax.grid(True, alpha=0.3)
    
    print("2. 绘制数据并添加 labels")
    
    # 3. 关键步骤：手动添加所有 mortise 到 legend 管理器
    legend_manager = root.get_legend_manager()
    
    # 清空现有的 mortise 列表
    legend_manager.mortises = []
    
    # 重新添加所有 mortise
    legend_manager.add_mortise(root)
    legend_manager.add_mortise(heatmap_panel)
    legend_manager.add_mortise(left_stats)
    legend_manager.add_mortise(right_cluster)
    legend_manager.add_mortise(bottom_time)
    
    print("3. 手动添加所有 mortise 到 legend 管理器")
    print(f"   - 管理的 mortise 数量: {len(legend_manager.mortises)}")
    
    # 4. 创建全局 legend
    global_legend = root.create_legend(mode='global', position='upper center', ncol=4)
    
    print("4. 创建全局 legend")
    print(f"   - Global legend created: {global_legend is not None}")
    
    if global_legend:
        print(f"   - Legend items: {len(global_legend.get_texts())}")
        print(f"   - Legend labels: {[text.get_text() for text in global_legend.get_texts()]}")
    
    # 保存图片
    fig.savefig('examples/multi_panel_legend_example.png', dpi=150, bbox_inches='tight')
    print("   - 图片已保存: examples/multi_panel_legend_example.png")
    
    return fig, root

def example_mixed_legend():
    """示例：混合 legend 模式"""
    
    print("\n=== 混合 Legend 模式示例 ===\n")
    
    # 创建布局
    fig, root = mortise(figsize=(12, 8))
    
    # 添加子图
    top_panel = root.tenon(pos='top', size=0.4, pad=0.1, title='Top Panel')
    bottom_panel = root.tenon(pos='bottom', size=0.4, pad=0.1, title='Bottom Panel')
    left_panel = root.tenon(pos='left', size=0.3, pad=0.1, title='Left Panel')
    right_panel = root.tenon(pos='right', size=0.3, pad=0.1, title='Right Panel')
    
    print("1. 创建布局")
    
    # 绘制数据
    x = np.linspace(0, 10, 100)
    
    # 主图
    root.ax.plot(x, np.sin(x), 'b-', linewidth=2, label='sin(x)')
    root.ax.plot(x, np.cos(x), 'r-', linewidth=2, label='cos(x)')
    root.ax.set_title('Main Plot')
    root.ax.grid(True)
    
    # 子图
    top_panel.ax.plot(x, np.tan(x), 'g-', linewidth=2, label='tan(x)')
    top_panel.ax.plot(x, np.sqrt(x), 'orange', linewidth=2, label='sqrt(x)')
    top_panel.ax.set_title('Top Panel')
    top_panel.ax.grid(True)
    
    bottom_panel.ax.scatter(x[::5], np.sin(x[::5]), c='blue', s=20, label='sin points')
    bottom_panel.ax.scatter(x[::5], np.cos(x[::5]), c='red', s=20, label='cos points')
    bottom_panel.ax.set_title('Bottom Panel')
    bottom_panel.ax.grid(True)
    
    left_panel.ax.plot(x, np.exp(-x), 'purple', linewidth=2, label='exp(-x)')
    left_panel.ax.set_title('Left Panel')
    left_panel.ax.grid(True)
    
    right_panel.ax.plot(x, np.log(x + 1), 'brown', linewidth=2, label='log(x+1)')
    right_panel.ax.set_title('Right Panel')
    right_panel.ax.grid(True)
    
    print("2. 绘制数据")
    
    # 手动添加所有 mortise 到 legend 管理器
    legend_manager = root.get_legend_manager()
    legend_manager.mortises = []
    
    legend_manager.add_mortise(root)
    legend_manager.add_mortise(top_panel)
    legend_manager.add_mortise(bottom_panel)
    legend_manager.add_mortise(left_panel)
    legend_manager.add_mortise(right_panel)
    
    print("3. 添加所有 mortise 到 legend 管理器")
    
    # 创建混合 legend
    global_legend, local_legends = root.create_legend(mode='mixed', 
                                                     global_position='upper center',
                                                     global_ncol=3)
    
    print("4. 创建混合 legend")
    print(f"   - Global legend created: {global_legend is not None}")
    print(f"   - Local legends created: {len(local_legends)}")
    
    if global_legend:
        print(f"   - Global legend items: {len(global_legend.get_texts())}")
        print(f"   - Global legend labels: {[text.get_text() for text in global_legend.get_texts()]}")
    
    for mortise_name, legend in local_legends.items():
        print(f"   - {mortise_name}: {len(legend.get_texts())} items")
        print(f"     Labels: {[text.get_text() for text in legend.get_texts()]}")
    
    # 保存图片
    fig.savefig('examples/mixed_legend_example.png', dpi=150, bbox_inches='tight')
    print("   - 图片已保存: examples/mixed_legend_example.png")
    
    return fig, root

def main():
    """主函数"""
    
    print("Sunmao 多图 Legend 使用示例\n")
    
    try:
        # 运行示例
        example_multi_panel_legend()
        example_mixed_legend()
        
        print("\n=== 示例完成 ===")
        print("多图 Legend 使用示例:")
        print("✅ 多面板全局 legend")
        print("✅ 混合 legend 模式")
        
        print("\n=== 使用方法总结 ===")
        print("1. 创建多面板布局")
        print("2. 在各面板绘制数据，确保有 label 参数")
        print("3. 手动添加所有 mortise 到 legend 管理器")
        print("4. 创建 legend: root.create_legend(mode='global')")
        
        print("\n=== 关键代码 ===")
        print("""
# 手动添加所有 mortise 到 legend 管理器
legend_manager = root.get_legend_manager()
legend_manager.mortises = []

legend_manager.add_mortise(root)
legend_manager.add_mortise(panel1)
legend_manager.add_mortise(panel2)
# ... 添加所有面板

# 创建 legend
global_legend = root.create_legend(mode='global')
        """)
        
        print("\n=== 注意事项 ===")
        print("- 只有带有 label 参数的图表元素才会被收集")
        print("- 颜色条（colorbar）不会自动被收集")
        print("- 需要手动添加所有 mortise 到管理器")
        print("- 支持 global、local、mixed、auto 四种模式")
        
        print("\n生成的示例图片:")
        print("- examples/multi_panel_legend_example.png")
        print("- examples/mixed_legend_example.png")
        
    except Exception as e:
        print(f"\n❌ 示例运行过程中出现错误: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎉 多图 Legend 示例运行成功！")
        print("Sunmao 完全支持多面板 legend 统一管理。")
    else:
        print("\n💥 示例运行失败。")
    
    # 显示图片（可选）
    # plt.show()
