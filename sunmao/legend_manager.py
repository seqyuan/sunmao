"""
Sunmao 统一 Legend 管理架构设计

设计理念：
1. 统一管理：可以在整个图形级别统一管理所有 legend
2. 灵活布局：每个子图可以单独在图周围布局 legend
3. 自动优化：根据布局自动调整 legend 位置和大小
4. 多种模式：支持全局 legend、局部 legend、混合模式
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.legend import Legend
from typing import Dict, List, Tuple, Optional, Union, Any
import numpy as np


class LegendManager:
    """
    统一的 Legend 管理器
    
    功能：
    1. 收集所有 mortise 的 legend 信息
    2. 统一管理 legend 位置和样式
    3. 支持全局、局部、混合三种模式
    4. 自动优化 legend 布局
    """
    
    def __init__(self, figure: plt.Figure):
        """
        初始化 Legend 管理器
        
        Args:
            figure: matplotlib Figure 对象
        """
        self.figure = figure
        self.mortises = []  # 存储所有 mortise 对象
        self.legends = {}   # 存储 legend 信息
        self.global_legend = None  # 全局 legend
        self.legend_mode = 'auto'  # legend 模式：'global', 'local', 'mixed', 'auto'
        
    def add_mortise(self, mortise: 'mortise'):
        """添加 mortise 到管理器"""
        self.mortises.append(mortise)
        
    def collect_legends(self) -> Dict[str, Any]:
        """
        收集所有 mortise 的 legend 信息
        
        Returns:
            dict: 包含所有 legend 信息的字典
        """
        legend_info = {
            'handles': [],
            'labels': [],
            'mortise_legends': {},
            'unique_labels': set()
        }
        
        for i, mortise in enumerate(self.mortises):
            if mortise.axes is not None:
                handles, labels = mortise.axes.get_legend_handles_labels()
                if handles and labels:
                    legend_info['handles'].extend(handles)
                    legend_info['labels'].extend(labels)
                    legend_info['mortise_legends'][f'mortise_{i}'] = {
                        'handles': handles,
                        'labels': labels,
                        'mortise': mortise
                    }
                    legend_info['unique_labels'].update(labels)
        
        return legend_info
    
    def create_global_legend(self, position: str = 'upper center', 
                           ncol: int = None, **kwargs) -> Legend:
        """
        创建全局 legend
        
        Args:
            position: legend 位置
            ncol: legend 列数
            **kwargs: 其他 legend 参数
            
        Returns:
            Legend: 创建的 legend 对象
        """
        legend_info = self.collect_legends()
        
        if not legend_info['handles']:
            return None
            
        # 去重处理
        by_label = dict(zip(legend_info['labels'], legend_info['handles']))
        
        # 自动确定列数
        if ncol is None:
            ncol = min(len(by_label), 4)
            
        # 创建全局 legend
        self.global_legend = self.figure.legend(
            by_label.values(), 
            by_label.keys(),
            loc=position,
            ncol=ncol,
            **kwargs
        )
        
        return self.global_legend
    
    def create_local_legends(self, positions: Dict[str, str] = None, **kwargs) -> Dict[str, Legend]:
        """
        为每个 mortise 创建局部 legend
        
        Args:
            positions: mortise 名称到位置的映射
            **kwargs: 其他 legend 参数
            
        Returns:
            dict: mortise 名称到 Legend 对象的映射
        """
        local_legends = {}
        
        for i, mortise in enumerate(self.mortises):
            if mortise.axes is not None:
                handles, labels = mortise.axes.get_legend_handles_labels()
                if handles and labels:
                    mortise_name = f'mortise_{i}'
                    position = positions.get(mortise_name, 'upper right') if positions else 'upper right'
                    
                    legend = mortise.axes.legend(
                        handles, labels,
                        loc=position,
                        **kwargs
                    )
                    local_legends[mortise_name] = legend
                    
        return local_legends
    
    def create_mixed_legends(self, global_position: str = 'upper center',
                           local_positions: Dict[str, str] = None,
                           global_ncol: int = None, **kwargs) -> Tuple[Legend, Dict[str, Legend]]:
        """
        创建混合模式 legend（全局 + 局部）
        
        Args:
            global_position: 全局 legend 位置
            local_positions: 局部 legend 位置映射
            global_ncol: 全局 legend 列数
            **kwargs: 其他 legend 参数
            
        Returns:
            tuple: (全局 legend, 局部 legend 字典)
        """
        # 创建全局 legend
        global_legend = self.create_global_legend(global_position, global_ncol, **kwargs)
        
        # 创建局部 legend
        local_legends = self.create_local_legends(local_positions, **kwargs)
        
        return global_legend, local_legends
    
    def auto_layout_legends(self, mode: str = 'auto', **kwargs) -> Union[Legend, Dict[str, Legend], Tuple]:
        """
        自动布局 legend
        
        Args:
            mode: 布局模式 ('global', 'local', 'mixed', 'auto')
            **kwargs: 其他参数
            
        Returns:
            legend 对象或对象集合
        """
        if mode == 'auto':
            # 自动选择模式
            legend_info = self.collect_legends()
            unique_count = len(legend_info['unique_labels'])
            mortise_count = len(self.mortises)
            
            if unique_count <= 3 and mortise_count <= 2:
                mode = 'global'
            elif unique_count > 6 or mortise_count > 4:
                mode = 'local'
            else:
                mode = 'mixed'
        
        if mode == 'global':
            return self.create_global_legend(**kwargs)
        elif mode == 'local':
            return self.create_local_legends(**kwargs)
        elif mode == 'mixed':
            return self.create_mixed_legends(**kwargs)
        else:
            raise ValueError(f"Unknown mode: {mode}")
    
    def optimize_legend_layout(self, legend: Legend, margin: float = 0.05):
        """
        优化 legend 布局，避免遮挡
        
        Args:
            legend: legend 对象
            margin: 边距
        """
        if legend is None:
            return
            
        # 获取 legend 的边界框
        bbox = legend.get_window_extent()
        
        # 检查是否与 mortise 重叠
        for mortise in self.mortises:
            if mortise.axes is not None:
                mortise_bbox = mortise.axes.get_window_extent()
                
                # 如果重叠，调整 legend 位置
                if bbox.overlaps(mortise_bbox):
                    # 简单的避让策略：移动到右上角
                    legend.set_bbox_to_anchor((1 + margin, 1 + margin))
                    legend.set_loc('upper left')

    def clear_all_legends(self):
        """清除所有 legend"""
        # 清除全局 legend
        if self.global_legend:
            self.global_legend.remove()
            self.global_legend = None

        # 清除局部 legend
        for mortise in self.mortises:
            if mortise.axes is not None:
                legend = mortise.axes.get_legend()
                if legend:
                    legend.remove()


class LegendPosition:
    """
    Legend 位置管理器

    提供预定义的 legend 位置和自动计算功能
    """
    # 预定义位置
    POSITIONS = {
        'top_left': (0.02, 0.98),
        'top_center': (0.5, 0.98),
        'top_right': (0.98, 0.98),
        'center_left': (0.02, 0.5),
        'center': (0.5, 0.5),
        'center_right': (0.98, 0.5),
        'bottom_left': (0.02, 0.02),
        'bottom_center': (0.5, 0.02),
        'bottom_right': (0.98, 0.02),
        'outside_top': (0.5, 1.05),
        'outside_bottom': (0.5, -0.05),
        'outside_left': (-0.05, 0.5),
        'outside_right': (1.05, 0.5)
    }

    @classmethod
    def get_position(cls, position_name: str) -> Tuple[float, float]:
        """获取预定义位置"""
        return cls.POSITIONS.get(position_name, (0.98, 0.98))

    @classmethod
    def calculate_optimal_position(cls, mortises: List['mortise'],
                                  legend_size: Tuple[float, float]) -> str:
        """
        计算最优 legend 位置

        Args:
            mortises: mortise 列表
            legend_size: legend 大小 (width, height)

        Returns:
            str: 最优位置名称
        """
        if not mortises:
            return 'top_right'

        # 简单的启发式算法
        # 统计 mortise 的分布
        positions = []
        for mortise in mortises:
            if mortise.position:
                positions.append(mortise.position)

        if not positions:
            return 'top_right'

        # 计算中心点
        center_x = np.mean([pos[0] + pos[2]/2 for pos in positions])
        center_y = np.mean([pos[1] + pos[3]/2 for pos in positions])

        # 根据中心点选择位置
        if center_y > 0.7:
            return 'bottom_center'
        elif center_y < 0.3:
            return 'top_center'
        elif center_x > 0.7:
            return 'outside_left'
        elif center_x < 0.3:
            return 'outside_right'
        else:
            return 'outside_top'
