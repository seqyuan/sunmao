"""
Basic example showing how to use sunmao for creating flexible subplot layouts.

This example demonstrates the basic usage of Panel and Layout classes
to create a simple layout with panels in different directions.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import matplotlib.pyplot as plt
from sunmao import mortise


def main():
    """Create a basic layout example."""
    
    # Create the root panel
    fig, root = mortise(width=2, height=2, axoff=True, cbar_pos=(.02, .8, .05, .18))
    root.ax.set_facecolor('white')
    root.ax.plot([0, 1], [0, 1], 's', color='white', markersize=10)

    root_top1 = root.tenon(pos='top', size=1, pad=.1, title='title1', title_pos='top')
    root_top2 = root_top1.tenon(pos='top', size=1, pad=.1, title='title2', title_pos='top')
    try:
        root_top2 = root_top1.tenon(pos='bottom', size=1, pad=.1, title='title2', title_pos='top')
    except Exception as e:
        ## 这种方式不允许，因为已经有一个 mortise 了
        print(e)
    # add_top 的size是 height, add_bottom 的size是 height, add_left 的size是 width, add_right 的size是 width
    root.tenon(pos='bottom', size=1, pad=.1, title='title2', title_pos='bottom', axoff=True, cbar_pos=(.02, .8, .05, .18))
    root.tenon(pos='left', size=1, pad=.1, title='title3', title_pos='left')
    root.tenon(pos='right', size=1, pad=.1, title='title4', title_pos='right')
    
    root_top1 = root.get_tenon(pos='top', index=0)
    root_top2 = root.get_tenon(pos='top', index=1)

    root_bottom1 = root.get_tenon(pos='bottom', index=0)
    
    # Access nested tenons (these will be None if they don't exist)
    root_top2_from_bottom = root_bottom1.get_tenon(pos='top', index=2) if root_bottom1 else None
    root_bottom1_from_top2 = root_top2_from_bottom.get_tenon(pos='bottom', index=-3) if root_top2_from_bottom else None
    
    # Only set properties if the tenon exists
    if root_bottom1_from_top2:
        root_bottom1_from_top2.ax.set_facecolor('red')
        root_bottom1_from_top2.ax.plot([0, 1], [0, 1], 'o', color='white', markersize=10)
    
    print(root.structure)
    print(root_top1.structure)
    
    fig.savefig('demo.png')
    
    


if __name__ == "__main__":
    main()

