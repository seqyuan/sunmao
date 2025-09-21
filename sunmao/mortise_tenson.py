"""
Mortise class - the main panel class for sunmao layout system.

This module provides the mortise class which is the main building block for
creating flexible subplot layouts. Each mortise can have child tenons in all
four directions (top, bottom, left, right).
"""

import matplotlib.pyplot as plt
from matplotlib.legend import Legend
from typing import Optional, Dict, Any, Tuple, List, Union
import numpy as np


class mortise:
    """
    A mortise that can contain a matplotlib axes and have child tenons in all
    directions.

    This class is inspired by traditional Chinese mortise-tenon joinery, where
    mortise is the main structure and tenons are the connecting pieces.

    Attributes:
        ax (matplotlib.axes.Axes): The matplotlib axes object for this mortise
        tenons (dict): Dictionary containing child tenons in each direction
        parent (mortise): Parent mortise that contains this mortise
        size (tuple): Size of the mortise as (width, height)
        position (tuple): Position of the mortise as (x, y, width, height)
        structure (str): String representation of the mortise structure
    """
    
    def __new__(cls, *args, **kwargs):
        """Override __new__ to support returning (fig, mortise) tuple."""
        instance = super().__new__(cls)
        # Initialize the instance
        instance.__init__(*args, **kwargs)
        # If this is a root mortise with auto_render, return (fig, mortise)
        if (instance.parent is None and instance.auto_render and
                hasattr(instance, '_fig')):
            return instance._fig, instance
        return instance
    
    def __init__(self, width: float = 1.0, height: float = 1.0,
                 axoff: bool = False,
                 cbar_pos: Optional[Tuple[float, float, float, float]] = None,
                 auto_render: bool = True,
                 figsize: Tuple[float, float] = (10, 8),
                 **kwargs):
        """
        Initialize a mortise.

        Args:
            width (float): Relative width of the mortise (default: 1.0)
            height (float): Relative height of the mortise (default: 1.0)
            axoff (bool): Whether to turn off axes display (default: False)
            cbar_pos (tuple): Colorbar position as (x, y, width, height)
                (default: None)
            auto_render (bool): Whether to automatically render the mortise
                (default: True)
            figsize (tuple): Figure size for auto-render (default: (10, 8))
            **kwargs: Additional arguments passed to matplotlib subplot creation
        """
        self.width = width
        self.height = height
        self.axoff = axoff
        self.cbar_pos = cbar_pos
        self.auto_render = auto_render
        self.figsize = figsize
        self.kwargs = kwargs
        
        # Child tenons in each direction
        self.tenons = {
            'top': [],
            'bottom': [], 
            'left': [],
            'right': []
        }
        
        # Parent mortise
        self.parent = None
        
        # Matplotlib objects
        self.axes = None
        self._figure = None
        
        # Create a property for ax access
        self._ax = None
        
        # Layout properties
        self.position = None  # Will be set during layout calculation
        self._calculated_size = None
        
        # Structure representation
        self._structure = None
        
        # Legend management
        self._legend_manager = None
        
        # Auto-render if this is a root mortise
        if auto_render and self.parent is None:
            self._fig = self._auto_render()
    
    @classmethod
    def create(cls, width: float = 1.0, height: float = 1.0, 
               axoff: bool = False, cbar_pos: Optional[Tuple[float, float, float, float]] = None,
               figsize: Tuple[float, float] = (10, 8), **kwargs):
        """
        Create a mortise and return both figure and mortise object.
        
        Args:
            width (float): Relative width of the mortise (default: 1.0)
            height (float): Relative height of the mortise (default: 1.0)
            axoff (bool): Whether to turn off axes display (default: False)
            cbar_pos (tuple): Colorbar position as (x, y, width, height) (default: None)
            figsize (tuple): Figure size for auto-render (default: (10, 8))
            **kwargs: Additional arguments passed to matplotlib subplot creation
            
        Returns:
            tuple: (figure, mortise) tuple
        """
        mortise_obj = cls(width=width, height=height, axoff=axoff, cbar_pos=cbar_pos,
                         auto_render=True, figsize=figsize, **kwargs)
        return mortise_obj._fig, mortise_obj
        
    def tenon(self, pos: str, size: float = 1.0, pad: float = 0.05,
              title: Optional[str] = None, title_pos: str = 'top',
              axoff: bool = False, cbar_pos: Optional[Tuple[float, float, float, float]] = None,
              auto_align: bool = True, **kwargs) -> 'mortise':
        """
        Add a tenon (child mortise) in the specified direction.
        
        Args:
            pos (str): Position to add tenon ('top', 'bottom', 'left', 'right')
            size (float): Size of the tenon (width for left/right, height for top/bottom)
            pad (float): Padding between tenons (default: 0.05)
            title (str): Title for the tenon (default: None)
            title_pos (str): Position of title ('top', 'bottom', 'left', 'right') (default: 'top')
            axoff (bool): Whether to turn off axes display (default: False)
            cbar_pos (tuple): Colorbar position as (x, y, width, height) (default: None)
            auto_align (bool): Whether to automatically align axes with parent (default: True)
            **kwargs: Additional arguments for tenon creation
            
        Returns:
            mortise: The created tenon
        """
        if pos not in ['top', 'bottom', 'left', 'right']:
            raise ValueError("pos must be one of 'top', 'bottom', 'left', 'right'")
            
        # Check if this position already has tenons
        if self.tenons[pos]:
            raise ValueError(f"Position '{pos}' already has tenons. Use get_tenon() to access existing tenons.")
            
        # Create new tenon
        if pos in ['top', 'bottom']:
            tenon_width = self.width
            tenon_height = size
        else:  # left, right
            tenon_width = size
            tenon_height = self.height
            
        new_tenon = mortise(width=tenon_width, height=tenon_height, 
                           axoff=axoff, cbar_pos=cbar_pos, auto_render=False, **kwargs)
        new_tenon.parent = self
        new_tenon.title = title
        new_tenon.title_pos = title_pos
        new_tenon.pad = pad
        
        # Add to tenons list
        self.tenons[pos].append(new_tenon)
        
        # Auto-align axes if requested and parent has axes
        if auto_align and self.axes is not None:
            # Ensure the new tenon is rendered first
            self._ensure_rendered()
            if new_tenon.axes is not None:
                self._auto_align_new_tenon(new_tenon, pos)
        
        return new_tenon
        
    def _auto_align_new_tenon(self, new_tenon: 'mortise', pos: str):
        """
        Automatically align the new tenon with the parent mortise.
        
        Args:
            new_tenon (mortise): The newly created tenon
            pos (str): Position of the tenon ('top', 'bottom', 'left', 'right')
        """
        if self.axes is None or new_tenon.axes is None:
            return
            
        # Determine which axis to align based on position
        if pos in ['top', 'bottom']:
            # For top/bottom tenons, align x-axis (horizontal alignment)
            x_lim = self.axes.get_xlim()
            new_tenon.axes.set_xlim(x_lim)
        elif pos in ['left', 'right']:
            # For left/right tenons, align y-axis (vertical alignment)
            y_lim = self.axes.get_ylim()
            new_tenon.axes.set_ylim(y_lim)
        
    def _auto_render(self):
        """Automatically render the mortise if it's a root mortise."""
        if self.parent is None and self.auto_render:
            # Create a simple figure and render this mortise
            fig = plt.figure(figsize=self.figsize)
            self.render(fig, 0.1, 0.1, 0.8, 0.8)
            return fig
        return None
            
    def _ensure_rendered(self):
        """Ensure the mortise is rendered before plotting."""
        if self.axes is None:
            # Get the root mortise
            root = self.get_root()
            if root.axes is None:
                # Render the root mortise
                root._fig = root._auto_render()
            # Only render if this mortise hasn't been rendered yet
            if self.axes is None and root._fig is not None:
                # Clear existing axes and re-render
                root._fig.clear()
                root.render(root._fig, 0.1, 0.1, 0.8, 0.8)
            
    def get_tenon(self, pos: str, index: int = 0) -> Optional['mortise']:
        """
        Get a tenon from the specified position and index.
        
        Args:
            pos (str): Position to get tenon from ('top', 'bottom', 'left', 'right')
            index (int): Index of the tenon (default: 0)
            
        Returns:
            mortise or None: The tenon at the specified position and index
        """
        if pos not in ['top', 'bottom', 'left', 'right']:
            raise ValueError("pos must be one of 'top', 'bottom', 'left', 'right'")
            
        tenons_list = self.tenons[pos]
        if not tenons_list:
            return None
            
        # Handle negative indexing
        if index < 0:
            index = len(tenons_list) + index
            
        if 0 <= index < len(tenons_list):
            return tenons_list[index]
        else:
            return None
            
    def get_root(self) -> 'mortise':
        """
        Get the root mortise of the hierarchy.
        
        Returns:
            mortise: The root mortise
        """
        if self.parent is None:
            return self
        return self.parent.get_root()
        
    def calculate_layout(self) -> Tuple[float, float, float, float]:
        """
        Calculate the total size needed for this mortise and all its tenons.
        
        Returns:
            tuple: (total_width, total_height, offset_x, offset_y)
        """
        # Start with this mortise's size
        total_width = self.width
        total_height = self.height
        
        # Add space for left and right tenons
        left_width = 0
        right_width = 0
        if self.tenons['left']:
            for tenon in self.tenons['left']:
                left_width += tenon.calculate_layout()[0]
        if self.tenons['right']:
            for tenon in self.tenons['right']:
                right_width += tenon.calculate_layout()[0]
                
        # Add space for top and bottom tenons
        top_height = 0
        bottom_height = 0
        if self.tenons['top']:
            for tenon in self.tenons['top']:
                top_height += tenon.calculate_layout()[1]
        if self.tenons['bottom']:
            for tenon in self.tenons['bottom']:
                bottom_height += tenon.calculate_layout()[1]
                
        total_width += left_width + right_width
        total_height += top_height + bottom_height
        
        # Calculate offset (where this mortise should be positioned)
        offset_x = left_width
        offset_y = bottom_height
        
        self._calculated_size = (total_width, total_height, offset_x, offset_y)
        return self._calculated_size
        
    def render(self, figure: plt.Figure, x: float = 0, y: float = 0, 
               width: float = 1, height: float = 1, **kwargs) -> None:
        """
        Render this mortise and all its tenons.
        
        Args:
            figure (matplotlib.figure.Figure): Figure to render into
            x (float): X position of this mortise (0-1)
            y (float): Y position of this mortise (0-1) 
            width (float): Width of this mortise (0-1)
            height (float): Height of this mortise (0-1)
            **kwargs: Additional arguments for subplot creation
        """
        # Calculate layout for all tenons
        total_width, total_height, offset_x, offset_y = self.calculate_layout()
        
        # Position of this mortise within the total layout
        mortise_x = x + (offset_x / total_width) * width
        mortise_y = y + (offset_y / total_height) * height
        mortise_width = (self.width / total_width) * width
        mortise_height = (self.height / total_height) * height
        
        # Create axes for this mortise
        rect = [mortise_x, mortise_y, mortise_width, mortise_height]
        self.axes = figure.add_axes(rect, **{**self.kwargs, **kwargs})
        self._ax = self.axes  # Set the ax property
        self._figure = figure
        self.position = rect
        
        # Set up axes
        if self.axoff:
            self.axes.set_xticks([])
            self.axes.set_yticks([])
            self.axes.spines['top'].set_visible(False)
            self.axes.spines['right'].set_visible(False)
            self.axes.spines['bottom'].set_visible(False)
            self.axes.spines['left'].set_visible(False)
            
        # Add title if specified
        if hasattr(self, 'title') and self.title:
            title_pos = getattr(self, 'title_pos', 'top')
            if title_pos == 'top':
                self.axes.set_title(self.title)
            elif title_pos == 'bottom':
                self.axes.text(0.5, -0.1, self.title, transform=self.axes.transAxes, 
                             ha='center', va='top')
            elif title_pos == 'left':
                self.axes.text(-0.1, 0.5, self.title, transform=self.axes.transAxes, 
                             ha='right', va='center', rotation=90)
            elif title_pos == 'right':
                self.axes.text(1.1, 0.5, self.title, transform=self.axes.transAxes, 
                             ha='left', va='center', rotation=90)
        
        # Add colorbar if specified
        if self.cbar_pos:
            # This would need to be implemented based on the plot content
            pass
            
        # Render tenons
        self._render_tenons(figure, x, y, width, height, total_width, total_height, offset_x, offset_y)
        
    def _render_tenons(self, figure: plt.Figure, x: float, y: float, 
                      width: float, height: float, total_width: float, total_height: float,
                      offset_x: float, offset_y: float) -> None:
        """Render all tenons."""
        
        # Render left tenons
        if self.tenons['left']:
            current_x = x
            for tenon in self.tenons['left']:
                tenon_width = tenon.calculate_layout()[0]
                tenon_height = tenon.calculate_layout()[1]
                tenon_x = current_x
                tenon_y = y + ((offset_y - tenon.calculate_layout()[2]) / total_height) * height
                tenon_panel_width = (tenon_width / total_width) * width
                tenon_panel_height = (tenon_height / total_height) * height
                tenon.render(figure, tenon_x, tenon_y, tenon_panel_width, tenon_panel_height)
                current_x += tenon_panel_width
                
        # Render right tenons
        if self.tenons['right']:
            current_x = x + ((offset_x + self.width) / total_width) * width
            for tenon in self.tenons['right']:
                tenon_width = tenon.calculate_layout()[0]
                tenon_height = tenon.calculate_layout()[1]
                tenon_x = current_x
                tenon_y = y + ((offset_y - tenon.calculate_layout()[2]) / total_height) * height
                tenon_panel_width = (tenon_width / total_width) * width
                tenon_panel_height = (tenon_height / total_height) * height
                tenon.render(figure, tenon_x, tenon_y, tenon_panel_width, tenon_panel_height)
                current_x += tenon_panel_width
                
        # Render top tenons
        if self.tenons['top']:
            current_y = y + ((offset_y + self.height) / total_height) * height
            for tenon in self.tenons['top']:
                tenon_width = tenon.calculate_layout()[0]
                tenon_height = tenon.calculate_layout()[1]
                tenon_x = x + ((offset_x - tenon.calculate_layout()[2]) / total_width) * width
                tenon_y = current_y
                tenon_panel_width = (tenon_width / total_width) * width
                tenon_panel_height = (tenon_height / total_height) * height
                tenon.render(figure, tenon_x, tenon_y, tenon_panel_width, tenon_panel_height)
                current_y += tenon_panel_height
                
        # Render bottom tenons
        if self.tenons['bottom']:
            current_y = y
            for tenon in self.tenons['bottom']:
                tenon_width = tenon.calculate_layout()[0]
                tenon_height = tenon.calculate_layout()[1]
                tenon_x = x + ((offset_x - tenon.calculate_layout()[2]) / total_width) * width
                tenon_y = current_y
                tenon_panel_width = (tenon_width / total_width) * width
                tenon_panel_height = (tenon_height / total_height) * height
                tenon.render(figure, tenon_x, tenon_y, tenon_panel_width, tenon_panel_height)
                current_y += tenon_panel_height
        
    @property
    def structure(self) -> str:
        """
        Get a string representation of the mortise structure.
        
        Returns:
            str: String representation of the structure
        """
        if self._structure is None:
            self._structure = self._build_structure()
        return self._structure
        
    def _build_structure(self, level: int = 0) -> str:
        """Build the structure string representation."""
        indent = "  " * level
        result = f"{indent}mortise(width={self.width}, height={self.height})"
        
        for pos in ['top', 'bottom', 'left', 'right']:
            if self.tenons[pos]:
                result += f"\n{indent}  {pos}:"
                for i, tenon in enumerate(self.tenons[pos]):
                    result += f"\n{tenon._build_structure(level + 2)}"
                    
        return result
        
    @property
    def ax(self):
        """Get the matplotlib axes object."""
        return self._ax
        
    def plot(self, *args, **kwargs):
        """
        Plot data on this mortise's axes.
        
        Args:
            *args: Arguments passed to matplotlib plot function
            **kwargs: Keyword arguments passed to matplotlib plot function
        """
        self._ensure_rendered()
        return self.axes.plot(*args, **kwargs)
        
    def scatter(self, *args, **kwargs):
        """
        Create a scatter plot on this mortise's axes.
        
        Args:
            *args: Arguments passed to matplotlib scatter function
            **kwargs: Keyword arguments passed to matplotlib scatter function
        """
        self._ensure_rendered()
        return self.axes.scatter(*args, **kwargs)
        
    def imshow(self, *args, **kwargs):
        """
        Display an image on this mortise's axes.
        
        Args:
            *args: Arguments passed to matplotlib imshow function
            **kwargs: Keyword arguments passed to matplotlib imshow function
        """
        self._ensure_rendered()
        return self.axes.imshow(*args, **kwargs)
        
    def set_xlabel(self, label: str, **kwargs):
        """Set the x-axis label."""
        self._ensure_rendered()
        self.axes.set_xlabel(label, **kwargs)
        
    def set_ylabel(self, label: str, **kwargs):
        """Set the y-axis label."""
        self._ensure_rendered()
        self.axes.set_ylabel(label, **kwargs)
        
    def set_title(self, title: str, **kwargs):
        """Set the title of the mortise."""
        self._ensure_rendered()
        self.axes.set_title(title, **kwargs)
        
    def align_axes(self, direction: str = 'both', mortises: List['mortise'] = None):
        """
        Align coordinate axis ranges with adjacent mortises.
        
        Args:
            direction (str): Direction to align ('x', 'y', or 'both') (default: 'both')
            mortises (list): List of mortises to align with (default: all adjacent tenons)
        """
        self._ensure_rendered()
        
        if mortises is None:
            # Get all adjacent tenons
            mortises = []
            if direction in ['x', 'both']:
                mortises.extend(self.tenons['top'])
                mortises.extend(self.tenons['bottom'])
            if direction in ['y', 'both']:
                mortises.extend(self.tenons['left'])
                mortises.extend(self.tenons['right'])
        
        # Get current limits
        if direction in ['x', 'both']:
            x_lim = self.axes.get_xlim()
        if direction in ['y', 'both']:
            y_lim = self.axes.get_ylim()
        
        # Set the same limits for all mortises
        for mortise in mortises:
            if mortise.axes is not None:
                if direction in ['x', 'both']:
                    mortise.axes.set_xlim(x_lim)
                if direction in ['y', 'both']:
                    mortise.axes.set_ylim(y_lim)
    
    def share_axes(self, direction: str, mortises: List['mortise'] = None):
        """
        Share axes with adjacent mortises (more advanced alignment).
        
        Args:
            direction (str): Direction to share ('x' or 'y')
            mortises (list): List of mortises to share with
        """
        self._ensure_rendered()
        
        if mortises is None:
            mortises = []
            if direction == 'x':
                mortises.extend(self.tenons['left'])
                mortises.extend(self.tenons['right'])
            elif direction == 'y':
                mortises.extend(self.tenons['top'])
                mortises.extend(self.tenons['bottom'])
        
        # Use matplotlib's sharex/sharey functionality
        for mortise in mortises:
            if mortise.axes is not None:
                if direction == 'x':
                    mortise.axes.sharex(self.axes)
                else:
                    mortise.axes.sharey(self.axes)
    
    def get_legend_manager(self) -> 'LegendManager':
        """
        获取或创建 Legend 管理器
        
        Returns:
            LegendManager: Legend 管理器对象
        """
        if self._legend_manager is None:
            root = self.get_root()
            if root._figure is not None:
                self._legend_manager = LegendManager(root._figure)
                # 添加所有 mortise 到管理器
                self._add_all_mortises_to_legend_manager()
        return self._legend_manager
    
    def _add_all_mortises_to_legend_manager(self):
        """将所有 mortise 添加到 legend 管理器"""
        if self._legend_manager is not None:
            self._legend_manager.add_mortise(self)
            # 递归添加所有子 mortise
            for pos in ['top', 'bottom', 'left', 'right']:
                for tenon in self.tenons[pos]:
                    tenon._add_all_mortises_to_legend_manager()
    
    def create_legend(self, mode: str = 'auto', position: str = None, 
                     ncol: int = None, **kwargs):
        """
        创建 legend
        
        Args:
            mode: legend 模式 ('global', 'local', 'mixed', 'auto')
            position: legend 位置
            ncol: legend 列数
            **kwargs: 其他 legend 参数
            
        Returns:
            legend 对象或对象集合
        """
        legend_manager = self.get_legend_manager()
        
        if mode == 'global':
            return legend_manager.create_global_legend(position or 'upper center', ncol, **kwargs)
        elif mode == 'local':
            return legend_manager.create_local_legends(**kwargs)
        elif mode == 'mixed':
            return legend_manager.create_mixed_legends(
                global_position=position or 'upper center',
                global_ncol=ncol, **kwargs)
        elif mode == 'auto':
            return legend_manager.auto_layout_legends(mode='auto', **kwargs)
        else:
            raise ValueError(f"Unknown legend mode: {mode}")
    
    def clear_legends(self):
        """清除所有 legend"""
        if self._legend_manager is not None:
            self._legend_manager.clear_all_legends()
    
    def set_legend_position(self, position: str, **kwargs):
        """
        设置 legend 位置
        
        Args:
            position: legend 位置名称
            **kwargs: 其他 legend 参数
        """
        legend_manager = self.get_legend_manager()
        legend_manager.clear_all_legends()
        return legend_manager.create_global_legend(position, **kwargs)
    
    def add_legend_item(self, handle, label):
        """
        添加 legend 项目
        
        Args:
            handle: matplotlib 图例句柄
            label: legend 标签
        """
        if self.axes is not None:
            # 获取现有 legend
            legend = self.axes.get_legend()
            if legend is None:
                # 创建新 legend
                self.axes.legend([handle], [label])
            else:
                # 添加新项目到现有 legend
                handles, labels = self.axes.get_legend_handles_labels()
                handles.append(handle)
                labels.append(label)
                self.axes.legend(handles, labels)
        
    def __getattr__(self, name):
        """
        Delegate attribute access to the matplotlib axes object.
        This allows direct access to all matplotlib axes methods.
        """
        if self.axes is not None:
            return getattr(self.axes, name)
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")


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
                    position = (positions.get(mortise_name, 'upper right')
                               if positions else 'upper right')

                    legend = mortise.axes.legend(
                        handles, labels,
                        loc=position,
                        **kwargs
                    )
                    local_legends[mortise_name] = legend

        return local_legends
    
    def create_mixed_legends(self, global_position: str = 'upper center',
                             local_positions: Dict[str, str] = None,
                             global_ncol: int = None,
                             **kwargs) -> Tuple[Legend, Dict[str, Legend]]:
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
        global_legend = self.create_global_legend(global_position, global_ncol,
                                                 **kwargs)

        # 创建局部 legend
        local_legends = self.create_local_legends(local_positions, **kwargs)

        return global_legend, local_legends
    
    def auto_layout_legends(self, mode: str = 'auto',
                           **kwargs) -> Union[Legend, Dict[str, Legend], Tuple]:
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
