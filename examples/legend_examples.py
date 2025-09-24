"""
Sunmao Legend 系统使用示例

展示如何使用 sunmao 的 LegendManager 系统
包括四种模式：global、local、mixed、auto
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import matplotlib.pyplot as plt
from sunmao import mortise

def example_global_legend():
    """示例：全局 legend 模式"""
    
    print("=== 全局 Legend 模式示例 ===")
    
    # 创建布局
    fig, root = mortise(figsize=(10, 8))
    
    # 添加子图
    top_panel = root.tenon(pos='top', size=0.4, pad=0.1, title='Top Panel')
    bottom_panel = root.tenon(pos='bottom', size=0.4, pad=0.1, title='Bottom Panel')
    
    # 绘制数据
    x = np.linspace(0, 10, 100)
    
    # 主图
    root.ax.plot(x, np.sin(x), 'b-', linewidth=2, label='sin(x)')
    root.ax.plot(x, np.cos(x), 'r-', linewidth=2, label='cos(x)')
    root.ax.set_title('Main Plot')
    root.ax.grid(True)
    
    # 子图
    top_panel.ax.plot(x, np.tan(x), 'g-', linewidth=2, label='tan(x)')
    top_panel.ax.set_title('Top Panel')
    top_panel.ax.grid(True)
    
    bottom_panel.ax.scatter(x[::5], np.sin(x[::5]), c='blue', s=20, label='sin points')
    bottom_panel.ax.scatter(x[::5], np.cos(x[::5]), c='red', s=20, label='cos points')
    bottom_panel.ax.set_title('Bottom Panel')
    bottom_panel.ax.grid(True)
    
    # 创建全局 legend
    global_legend = root.create_legend(mode='global', position='upper center', ncol=3)
    
    print(f"✅ 全局 legend 创建成功: {global_legend is not None}")
    print(f"   - Legend 项目数: {len(global_legend.get_texts())}")
    print(f"   - Legend 标签: {[text.get_text() for text in global_legend.get_texts()]}")
    
    fig.savefig('examples/example_global_legend.png', dpi=150, bbox_inches='tight')
    print("   - 图片已保存: examples/example_global_legend.png")
    
    return fig, root

def example_local_legend():
    """示例：局部 legend 模式"""
    
    print("\n=== 局部 Legend 模式示例 ===")
    
    # 创建布局
    fig, root = mortise(figsize=(10, 8))
    
    # 添加子图
    top_panel = root.tenon(pos='top', size=0.4, pad=0.1, title='Top Panel')
    bottom_panel = root.tenon(pos='bottom', size=0.4, pad=0.1, title='Bottom Panel')
    
    # 绘制数据
    x = np.linspace(0, 10, 100)
    
    # 主图
    root.ax.plot(x, np.sin(x), 'b-', linewidth=2, label='sin(x)')
    root.ax.plot(x, np.cos(x), 'r-', linewidth=2, label='cos(x)')
    root.ax.set_title('Main Plot')
    root.ax.grid(True)
    
    # 子图
    top_panel.ax.plot(x, np.tan(x), 'g-', linewidth=2, label='tan(x)')
    top_panel.ax.set_title('Top Panel')
    top_panel.ax.grid(True)
    
    bottom_panel.ax.scatter(x[::5], np.sin(x[::5]), c='blue', s=20, label='sin points')
    bottom_panel.ax.scatter(x[::5], np.cos(x[::5]), c='red', s=20, label='cos points')
    bottom_panel.ax.set_title('Bottom Panel')
    bottom_panel.ax.grid(True)
    
    # 创建局部 legend
    local_legends = root.create_legend(mode='local')
    
    print(f"✅ 局部 legend 创建成功: {len(local_legends)} 个")
    for mortise_name, legend in local_legends.items():
        print(f"   - {mortise_name}: {len(legend.get_texts())} 个项目")
        print(f"     标签: {[text.get_text() for text in legend.get_texts()]}")
    
    fig.savefig('examples/example_local_legend.png', dpi=150, bbox_inches='tight')
    print("   - 图片已保存: examples/example_local_legend.png")
    
    return fig, root

def example_mixed_legend():
    """示例：混合 legend 模式"""
    
    print("\n=== 混合 Legend 模式示例 ===")
    
    # 创建布局
    fig, root = mortise(figsize=(10, 8))
    
    # 添加子图
    top_panel = root.tenon(pos='top', size=0.4, pad=0.1, title='Top Panel')
    bottom_panel = root.tenon(pos='bottom', size=0.4, pad=0.1, title='Bottom Panel')
    
    # 绘制数据
    x = np.linspace(0, 10, 100)
    
    # 主图
    root.ax.plot(x, np.sin(x), 'b-', linewidth=2, label='sin(x)')
    root.ax.plot(x, np.cos(x), 'r-', linewidth=2, label='cos(x)')
    root.ax.set_title('Main Plot')
    root.ax.grid(True)
    
    # 子图
    top_panel.ax.plot(x, np.tan(x), 'g-', linewidth=2, label='tan(x)')
    top_panel.ax.set_title('Top Panel')
    top_panel.ax.grid(True)
    
    bottom_panel.ax.scatter(x[::5], np.sin(x[::5]), c='blue', s=20, label='sin points')
    bottom_panel.ax.scatter(x[::5], np.cos(x[::5]), c='red', s=20, label='cos points')
    bottom_panel.ax.set_title('Bottom Panel')
    bottom_panel.ax.grid(True)
    
    # 创建混合 legend
    global_legend, local_legends = root.create_legend(mode='mixed', 
                                                     global_position='upper center',
                                                     global_ncol=2)
    
    print(f"✅ 混合 legend 创建成功")
    print(f"   - 全局 legend: {global_legend is not None}")
    print(f"   - 局部 legend: {len(local_legends)} 个")
    
    if global_legend:
        print(f"   - 全局 legend 项目: {len(global_legend.get_texts())}")
    
    for mortise_name, legend in local_legends.items():
        print(f"   - {mortise_name}: {len(legend.get_texts())} 个项目")
    
    fig.savefig('examples/example_mixed_legend.png', dpi=150, bbox_inches='tight')
    print("   - 图片已保存: examples/example_mixed_legend.png")
    
    return fig, root

def example_auto_legend():
    """示例：自动 legend 模式"""
    
    print("\n=== 自动 Legend 模式示例 ===")
    
    # 创建布局
    fig, root = mortise(figsize=(10, 8))
    
    # 添加子图
    top_panel = root.tenon(pos='top', size=0.4, pad=0.1, title='Top Panel')
    bottom_panel = root.tenon(pos='bottom', size=0.4, pad=0.1, title='Bottom Panel')
    
    # 绘制数据
    x = np.linspace(0, 10, 100)
    
    # 主图
    root.ax.plot(x, np.sin(x), 'b-', linewidth=2, label='sin(x)')
    root.ax.plot(x, np.cos(x), 'r-', linewidth=2, label='cos(x)')
    root.ax.set_title('Main Plot')
    root.ax.grid(True)
    
    # 子图
    top_panel.ax.plot(x, np.tan(x), 'g-', linewidth=2, label='tan(x)')
    top_panel.ax.set_title('Top Panel')
    top_panel.ax.grid(True)
    
    bottom_panel.ax.scatter(x[::5], np.sin(x[::5]), c='blue', s=20, label='sin points')
    bottom_panel.ax.scatter(x[::5], np.cos(x[::5]), c='red', s=20, label='cos points')
    bottom_panel.ax.set_title('Bottom Panel')
    bottom_panel.ax.grid(True)
    
    # 创建自动 legend
    auto_result = root.create_legend(mode='auto')
    
    print(f"✅ 自动 legend 创建成功")
    print(f"   - 结果类型: {type(auto_result)}")
    
    if isinstance(auto_result, tuple):
        global_legend, local_legends = auto_result
        print(f"   - 全局 legend: {global_legend is not None}")
        print(f"   - 局部 legend: {len(local_legends) if local_legends else 0}")
    elif isinstance(auto_result, dict):
        print(f"   - 局部 legend: {len(auto_result)}")
    else:
        print(f"   - 单一 legend: {auto_result is not None}")
    
    fig.savefig('examples/example_auto_legend.png', dpi=150, bbox_inches='tight')
    print("   - 图片已保存: examples/example_auto_legend.png")
    
    return fig, root

def example_legend_management():
    """示例：Legend 管理功能"""
    
    print("\n=== Legend 管理功能示例 ===")
    
    # 创建布局
    fig, root = mortise(figsize=(10, 8))
    
    # 添加子图
    top_panel = root.tenon(pos='top', size=0.4, pad=0.1, title='Top Panel')
    
    # 绘制数据
    x = np.linspace(0, 10, 100)
    
    root.ax.plot(x, np.sin(x), 'b-', linewidth=2, label='sin(x)')
    root.ax.plot(x, np.cos(x), 'r-', linewidth=2, label='cos(x)')
    root.ax.set_title('Main Plot')
    root.ax.grid(True)
    
    top_panel.ax.plot(x, np.tan(x), 'g-', linewidth=2, label='tan(x)')
    top_panel.ax.set_title('Top Panel')
    top_panel.ax.grid(True)
    
    # 获取 legend 管理器
    legend_manager = root.get_legend_manager()
    print(f"✅ Legend 管理器获取成功: {legend_manager is not None}")
    print(f"   - 管理的 mortise 数量: {len(legend_manager.mortises)}")
    
    # 收集 legend 信息
    legend_info = legend_manager.collect_legends()
    print(f"✅ Legend 信息收集成功")
    print(f"   - 总 handles: {len(legend_info['handles'])}")
    print(f"   - 总 labels: {len(legend_info['labels'])}")
    print(f"   - 唯一 labels: {len(legend_info['unique_labels'])}")
    print(f"   - Mortise legends: {len(legend_info['mortise_legends'])}")
    
    # 创建和清除 legend
    root.create_legend(mode='global')
    print("✅ 创建 legend 成功")
    
    root.clear_legends()
    print("✅ 清除 legend 成功")
    
    return fig, root

def main():
    """主函数"""
    
    print("Sunmao Legend 系统使用示例\n")
    
    try:
        # 运行各种示例
        example_global_legend()
        example_local_legend()
        example_mixed_legend()
        example_auto_legend()
        example_legend_management()
        
        print("\n=== 示例完成 ===")
        print("Sunmao Legend 系统使用示例:")
        print("✅ 全局 legend 模式")
        print("✅ 局部 legend 模式")
        print("✅ 混合 legend 模式")
        print("✅ 自动 legend 模式")
        print("✅ Legend 管理功能")
        
        print("\n=== 使用方法总结 ===")
        print("1. 创建布局: fig, root = mortise(figsize=(10, 8))")
        print("2. 添加子图: panel = root.tenon(pos='top', size=0.4)")
        print("3. 绘制数据: root.ax.plot(x, y, label='data')")
        print("4. 创建 legend: root.create_legend(mode='global')")
        
        print("\n=== 四种模式 ===")
        print("- global: 全局统一 legend")
        print("- local: 各子图独立 legend")
        print("- mixed: 全局 + 局部混合")
        print("- auto: 自动选择最佳模式")
        
        print("\n生成的示例图片:")
        print("- examples/example_global_legend.png")
        print("- examples/example_local_legend.png")
        print("- examples/example_mixed_legend.png")
        print("- examples/example_auto_legend.png")
        
    except Exception as e:
        print(f"\n❌ 示例运行过程中出现错误: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎉 所有示例运行成功！Sunmao Legend 系统完全可用。")
    else:
        print("\n💥 示例运行失败，需要检查 Legend 系统实现。")
    
    # 显示图片（可选）
    # plt.show()
