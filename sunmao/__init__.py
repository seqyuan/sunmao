"""
Sunmao: A flexible subplot layout library for matplotlib.

Sunmao provides a flexible way to create complex subplot layouts using the
traditional Chinese mortise-tenon joinery concept. Each mortise can have
child tenons in all directions (up, down, left, right) around a central
mortise. Each mortise is an independent matplotlib axes object that can be
fully customized.

Main classes:
- mortise: The main building block for creating layouts
- LegendManager: Unified legend management system
- LegendPosition: Legend position management utilities
"""

from .mortise_tenson import mortise, LegendManager, LegendPosition

__version__ = "0.3.2"
__all__ = ["mortise", "LegendManager", "LegendPosition"]
