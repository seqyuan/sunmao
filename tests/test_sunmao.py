"""
Basic tests for sunmao package
"""

import pytest
import numpy as np
import matplotlib.pyplot as plt
from sunmao import mortise, LegendManager, LegendPosition


def test_mortise_creation():
    """Test basic mortise creation"""
    fig, root = mortise(width=2, height=2)
    assert root.width == 2
    assert root.height == 2
    assert root.parent is None
    assert fig is not None


def test_tenon_creation():
    """Test tenon creation"""
    fig, root = mortise(width=2, height=2)
    top_panel = root.tenon(pos='top', size=1, title='Top Panel')
    
    assert top_panel.parent == root
    assert top_panel.title == 'Top Panel'
    assert len(root.tenons['top']) == 1


def test_plotting():
    """Test plotting functionality"""
    fig, root = mortise(width=2, height=2)
    x = np.linspace(0, 10, 100)
    line = root.plot(x, np.sin(x), 'b-', linewidth=2, label='sin(x)')
    
    assert line is not None
    assert root.axes is not None


def test_legend_management():
    """Test legend management"""
    fig, root = mortise(width=2, height=2)
    x = np.linspace(0, 10, 100)
    root.plot(x, np.sin(x), 'b-', linewidth=2, label='sin(x)')
    
    # Test legend creation
    legend = root.create_legend(mode='global', position='upper center')
    assert legend is not None
    
    # Test legend clearing
    root.clear_legends()
    assert root.get_legend_manager().global_legend is None


def test_axis_alignment():
    """Test axis alignment"""
    fig, root = mortise(width=2, height=2)
    top_panel = root.tenon(pos='top', size=1)
    
    x = np.linspace(0, 10, 100)
    root.plot(x, np.sin(x), 'b-', linewidth=2)
    top_panel.plot(x, np.cos(x), 'r-', linewidth=2)
    
    # Test manual alignment
    root.align_axes('x')
    assert root.axes.get_xlim() == top_panel.axes.get_xlim()


def test_legend_manager():
    """Test LegendManager class"""
    fig, root = mortise(width=2, height=2)
    legend_manager = LegendManager(fig)
    
    assert legend_manager.figure == fig
    assert len(legend_manager.mortises) == 0
    
    legend_manager.add_mortise(root)
    assert len(legend_manager.mortises) == 1


def test_legend_position():
    """Test LegendPosition class"""
    # Test getting predefined position
    pos = LegendPosition.get_position('top_right')
    assert pos == (0.98, 0.98)
    
    # Test calculating optimal position
    fig, root = mortise(width=2, height=2)
    optimal_pos = LegendPosition.calculate_optimal_position([root], (0.1, 0.1))
    assert optimal_pos in LegendPosition.POSITIONS


if __name__ == "__main__":
    pytest.main([__file__])
