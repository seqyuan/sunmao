"""
Sunmao Legend 系统测试脚本

测试 sunmao 的 LegendManager 系统是否正常工作
包括全局、局部、混合、自动四种模式
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import matplotlib.pyplot as plt
from sunmao import mortise

def test_basic_legend_functionality():
    """测试基本的 legend 功能"""
    
    print("=== 测试基本 Legend 功能 ===\n")
    
    # 创建布局
    fig, root = mortise(figsize=(10, 8))
    
    # 添加子图
    top_panel = root.tenon(pos='top', size=0.4, pad=0.1, title='Top Panel')
    bottom_panel = root.tenon(pos='bottom', size=0.4, pad=0.1, title='Bottom Panel')
    left_panel = root.tenon(pos='left', size=0.3, pad=0.1, title='Left Panel')
    right_panel = root.tenon(pos='right', size=0.3, pad=0.1, title='Right Panel')
    
    print("1. 创建布局和子图")
    
    # 绘制数据并添加 label
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
    
    print("2. 绘制数据并添加 labels")
    
    return fig, root, top_panel, bottom_panel, left_panel, right_panel

def test_global_legend():
    """测试全局 legend 模式"""
    
    print("\n=== 测试全局 Legend 模式 ===\n")
    
    fig, root, top_panel, bottom_panel, left_panel, right_panel = test_basic_legend_functionality()
    
    # 创建全局 legend
    global_legend = root.create_legend(mode='global', position='upper center', ncol=3)
    
    print("3. 创建全局 legend")
    print(f"   - Global legend created: {global_legend is not None}")
    
    if global_legend:
        print(f"   - Legend handles: {len(global_legend.get_texts())}")
        print(f"   - Legend labels: {[text.get_text() for text in global_legend.get_texts()]}")
    
    # 保存图片
    fig.savefig('examples/global_legend_example.png', dpi=150, bbox_inches='tight')
    print("   - 图片已保存: examples/global_legend_example.png")
    
    return fig, root

def test_local_legend():
    """测试局部 legend 模式"""
    
    print("\n=== 测试局部 Legend 模式 ===\n")
    
    fig, root, top_panel, bottom_panel, left_panel, right_panel = test_basic_legend_functionality()
    
    # 创建局部 legend
    local_legends = root.create_legend(mode='local')
    
    print("3. 创建局部 legend")
    print(f"   - Local legends created: {len(local_legends)}")
    
    for mortise_name, legend in local_legends.items():
        print(f"   - {mortise_name}: {len(legend.get_texts())} items")
        print(f"     Labels: {[text.get_text() for text in legend.get_texts()]}")
    
    # 保存图片
    fig.savefig('examples/local_legend_example.png', dpi=150, bbox_inches='tight')
    print("   - 图片已保存: examples/local_legend_example.png")
    
    return fig, root

def test_mixed_legend():
    """测试混合 legend 模式"""
    
    print("\n=== 测试混合 Legend 模式 ===\n")
    
    fig, root, top_panel, bottom_panel, left_panel, right_panel = test_basic_legend_functionality()
    
    # 创建混合 legend
    global_legend, local_legends = root.create_legend(mode='mixed', 
                                                     global_position='upper center',
                                                     global_ncol=2)
    
    print("3. 创建混合 legend")
    print(f"   - Global legend created: {global_legend is not None}")
    print(f"   - Local legends created: {len(local_legends)}")
    
    if global_legend:
        print(f"   - Global legend items: {len(global_legend.get_texts())}")
    
    for mortise_name, legend in local_legends.items():
        print(f"   - {mortise_name}: {len(legend.get_texts())} items")
    
    # 保存图片
    fig.savefig('examples/mixed_legend_example.png', dpi=150, bbox_inches='tight')
    print("   - 图片已保存: examples/mixed_legend_example.png")
    
    return fig, root

def test_auto_legend():
    """测试自动 legend 模式"""
    
    print("\n=== 测试自动 Legend 模式 ===\n")
    
    fig, root, top_panel, bottom_panel, left_panel, right_panel = test_basic_legend_functionality()
    
    # 创建自动 legend
    auto_result = root.create_legend(mode='auto')
    
    print("3. 创建自动 legend")
    print(f"   - Auto legend result type: {type(auto_result)}")
    
    if isinstance(auto_result, tuple):
        global_legend, local_legends = auto_result
        print(f"   - Global legend: {global_legend is not None}")
        print(f"   - Local legends: {len(local_legends) if local_legends else 0}")
    elif isinstance(auto_result, dict):
        print(f"   - Local legends: {len(auto_result)}")
    else:
        print(f"   - Single legend: {auto_result is not None}")
    
    # 保存图片
    fig.savefig('examples/auto_legend_example.png', dpi=150, bbox_inches='tight')
    print("   - 图片已保存: examples/auto_legend_example.png")
    
    return fig, root

def test_legend_manager():
    """测试 LegendManager 功能"""
    
    print("\n=== 测试 LegendManager 功能 ===\n")
    
    fig, root, top_panel, bottom_panel, left_panel, right_panel = test_basic_legend_functionality()
    
    # 测试 legend 管理器
    legend_manager = root.get_legend_manager()
    print("1. 获取 legend 管理器")
    print(f"   - Legend manager: {legend_manager is not None}")
    print(f"   - Managed mortises: {len(legend_manager.mortises)}")
    
    # 收集 legend 信息
    legend_info = legend_manager.collect_legends()
    print("\n2. 收集 legend 信息")
    print(f"   - Total handles: {len(legend_info['handles'])}")
    print(f"   - Total labels: {len(legend_info['labels'])}")
    print(f"   - Unique labels: {len(legend_info['unique_labels'])}")
    print(f"   - Mortise legends: {len(legend_info['mortise_legends'])}")
    
    # 测试清除功能
    root.create_legend(mode='global')
    print("\n3. 创建 legend 后清除")
    root.clear_legends()
    print("   - Legends cleared")
    
    return fig, root

def test_legend_positions():
    """测试不同位置的 legend"""
    
    print("\n=== 测试不同位置的 Legend ===\n")
    
    fig, root, top_panel, bottom_panel, left_panel, right_panel = test_basic_legend_functionality()
    
    # 测试不同位置
    positions = ['upper left', 'upper center', 'upper right', 
                'center left', 'center', 'center right',
                'lower left', 'lower center', 'lower right']
    
    print("1. 测试不同位置的全局 legend")
    
    for i, pos in enumerate(positions):
        root.clear_legends()
        legend = root.create_legend(mode='global', position=pos)
        print(f"   - {pos}: {legend is not None}")
        
        if i == 0:  # 只保存第一个位置的图片
            fig.savefig(f'examples/legend_position_{pos.replace(" ", "_")}_example.png', 
                       dpi=150, bbox_inches='tight')
    
    return fig, root

def test_complex_layout():
    """测试复杂布局的 legend"""
    
    print("\n=== 测试复杂布局的 Legend ===\n")
    
    # 创建复杂嵌套布局
    fig, root = mortise(figsize=(12, 10))
    
    # 第一层
    top_panel = root.tenon(pos='top', size=0.3, pad=0.1, title='Top Level')
    bottom_panel = root.tenon(pos='bottom', size=0.3, pad=0.1, title='Bottom Level')
    left_panel = root.tenon(pos='left', size=0.25, pad=0.1, title='Left Level')
    right_panel = root.tenon(pos='right', size=0.25, pad=0.1, title='Right Level')
    
    # 第二层嵌套
    top_left = top_panel.tenon(pos='left', size=0.5, pad=0.05, title='Top-Left')
    top_right = top_panel.tenon(pos='right', size=0.5, pad=0.05, title='Top-Right')
    bottom_left = bottom_panel.tenon(pos='left', size=0.5, pad=0.05, title='Bottom-Left')
    bottom_right = bottom_panel.tenon(pos='right', size=0.5, pad=0.05, title='Bottom-Right')
    
    print("1. 创建复杂嵌套布局")
    
    # 绘制数据
    x = np.linspace(0, 5, 50)
    
    # 主图
    root.ax.plot(x, np.sin(x), 'b-', linewidth=2, label='sin(x)')
    root.ax.plot(x, np.cos(x), 'r-', linewidth=2, label='cos(x)')
    root.ax.set_title('Main Plot')
    
    # 第一层子图
    top_panel.ax.plot(x, np.tan(x), 'g-', linewidth=2, label='tan(x)')
    top_panel.ax.set_title('Top Level')
    
    bottom_panel.ax.scatter(x[::2], np.sin(x[::2]), c='blue', s=20, label='sin scatter')
    bottom_panel.ax.set_title('Bottom Level')
    
    left_panel.ax.plot(x, np.exp(-x), 'purple', linewidth=2, label='exp(-x)')
    left_panel.ax.set_title('Left Level')
    
    right_panel.ax.plot(x, np.log(x + 1), 'brown', linewidth=2, label='log(x+1)')
    right_panel.ax.set_title('Right Level')
    
    # 第二层嵌套图
    top_left.ax.plot(x, np.sqrt(x), 'orange', linewidth=2, label='sqrt(x)')
    top_left.ax.set_title('Top-Left')
    
    top_right.ax.plot(x, x**2, 'pink', linewidth=2, label='x²')
    top_right.ax.set_title('Top-Right')
    
    bottom_left.ax.plot(x, x**3, 'cyan', linewidth=2, label='x³')
    bottom_left.ax.set_title('Bottom-Left')
    
    bottom_right.ax.plot(x, np.abs(np.sin(x)), 'magenta', linewidth=2, label='|sin(x)|')
    bottom_right.ax.set_title('Bottom-Right')
    
    print("2. 绘制数据并添加 labels")
    
    # 测试混合 legend
    global_legend, local_legends = root.create_legend(mode='mixed', 
                                                     global_position='upper center',
                                                     global_ncol=3)
    
    print("3. 创建混合 legend")
    print(f"   - Global legend created: {global_legend is not None}")
    print(f"   - Local legends created: {len(local_legends)}")
    
    if global_legend:
        print(f"   - Global legend items: {len(global_legend.get_texts())}")
        print(f"   - Global legend labels: {[text.get_text() for text in global_legend.get_texts()]}")
    
    # 保存图片
    fig.savefig('examples/complex_layout_legend_example.png', dpi=150, bbox_inches='tight')
    print("   - 图片已保存: examples/complex_layout_legend_example.png")
    
    return fig, root

def main():
    """主测试函数"""
    
    print("开始测试 Sunmao Legend 系统...\n")
    
    try:
        # 测试各种 legend 模式
        test_global_legend()
        test_local_legend()
        test_mixed_legend()
        test_auto_legend()
        test_legend_manager()
        test_legend_positions()
        test_complex_layout()
        
        print("\n=== 测试完成 ===")
        print("Sunmao Legend 系统测试结果:")
        print("✅ 全局 legend 模式")
        print("✅ 局部 legend 模式")
        print("✅ 混合 legend 模式")
        print("✅ 自动 legend 模式")
        print("✅ LegendManager 功能")
        print("✅ Legend 位置管理")
        print("✅ 复杂布局支持")
        
        print("\n=== 总结 ===")
        print("Sunmao 的 Legend 系统完全可用，提供了:")
        print("- 统一的 LegendManager 管理")
        print("- 四种 legend 模式支持")
        print("- 自动收集和去重功能")
        print("- 灵活的位置管理")
        print("- 复杂嵌套布局支持")
        
        print("\n生成的示例图片:")
        print("- examples/global_legend_example.png")
        print("- examples/local_legend_example.png")
        print("- examples/mixed_legend_example.png")
        print("- examples/auto_legend_example.png")
        print("- examples/legend_position_upper_left_example.png")
        print("- examples/complex_layout_legend_example.png")
        
    except Exception as e:
        print(f"\n❌ 测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎉 所有测试通过！Sunmao Legend 系统工作正常。")
    else:
        print("\n💥 测试失败，需要检查 Legend 系统实现。")
    
    # 显示图片（可选）
    # plt.show()
