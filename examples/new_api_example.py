"""
Basic example showing how to use the new sunmao mortise-tenon API.

This example demonstrates the basic usage of the mortise class
to create flexible subplot layouts using the traditional Chinese
mortise-tenon joinery concept, including automatic axis alignment.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import matplotlib.pyplot as plt
from sunmao import mortise


def main():
    """Create a basic layout example using the new API."""
    
    # Create the root mortise
    fig, root = mortise(width=2, height=2, axoff=True, cbar_pos=(.02, .8, .05, .18))
    #root.ax.set_facecolor('black')
    root.ax.plot([0, 1], [0, 1], 'o', color='white', markersize=10)

    # Add tenons in different directions
    root_top1 = root.tenon(pos='top', size=1, pad=.1, title='title1', title_pos='top')
    root_top2 = root_top1.tenon(pos='top', size=1, pad=.1, title='title2', title_pos='top')
    
    # Try to add a tenon in the same position (should raise an error)
    try:
        root_top2 = root_top1.tenon(pos='bottom', size=1, pad=.1, title='title2', title_pos='top')
    except Exception as e:
        print(f"Error as expected: {e}")
    
    # Add more tenons
    root.tenon(pos='bottom', size=1, pad=.1, title='title2', title_pos='bottom', axoff=False, cbar_pos=(.02, .8, .05, .18))
    root.tenon(pos='left', size=1, pad=.1, title='title3', title_pos='left', axoff=False)
    root.tenon(pos='right', size=1, pad=.1, title='title4', title_pos='right', axoff=False)
    
    # Access tenons using get_tenon
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
    
    # Print structure
    print("Root structure:")
    print(root.structure)
    print("\nTop1 structure:")
    print(root_top1.structure)
    
    # Show the plot
    #plt.show()
    fig.savefig('new_api_example.png')


def advanced_example():
    """Create a more complex layout example."""
    
    # Create the main mortise
    fig, main = mortise(width=3, height=3, figsize=(14, 12))
    
    # Add tenons in all directions
    top_tenon = main.tenon(pos='top', size=1, pad=0.1, title='Top Panel', title_pos='top')
    bottom_tenon = main.tenon(pos='bottom', size=1, pad=0.1, title='Bottom Panel', title_pos='bottom')
    left_tenon = main.tenon(pos='left', size=1, pad=0.1, title='Left Panel', title_pos='left')
    right_tenon = main.tenon(pos='right', size=1, pad=0.1, title='Right Panel', title_pos='right')
    
    # Add nested tenons
    top_left = top_tenon.tenon(pos='left', size=1, pad=0.05, title='Top-Left', title_pos='top')
    top_right = top_tenon.tenon(pos='right', size=1, pad=0.05, title='Top-Right', title_pos='top')
    
    bottom_left = bottom_tenon.tenon(pos='left', size=1, pad=0.05, title='Bottom-Left', title_pos='bottom')
    bottom_right = bottom_tenon.tenon(pos='right', size=1, pad=0.05, title='Bottom-Right', title_pos='bottom')
    
    # Generate sample data
    x = np.linspace(0, 2*np.pi, 100)
    
    # Plot in main mortise
    main.plot(x, np.sin(x), 'b-', linewidth=2, label='sin(x)')
    main.plot(x, np.cos(x), 'r-', linewidth=2, label='cos(x)')
    main.set_title('Main Panel: Trigonometric Functions')
    main.set_xlabel('x')
    main.set_ylabel('y')
    main.grid(True, alpha=0.3)
    
    # Plot in top tenons
    top_tenon.plot(x, np.sin(x) * np.cos(x), 'g-', linewidth=2, label='sin(x) * cos(x)')
    top_tenon.set_ylabel('Amplitude')
    
    top_left.plot(x, np.sin(x)**2, 'm-', linewidth=2, label='sin²(x)')
    top_right.plot(x, np.cos(x)**2, 'c-', linewidth=2, label='cos²(x)')
    
    # Plot in bottom tenons
    bottom_tenon.plot(x, np.tan(x), 'orange', linewidth=2, label='tan(x)')
    bottom_tenon.set_xlabel('x')
    bottom_tenon.set_ylabel('Amplitude')
    
    bottom_left.plot(x, np.exp(-x/10), 'purple', linewidth=2, label='exp(-x/10)')
    bottom_right.plot(x, np.log(x + 1), 'brown', linewidth=2, label='log(x+1)')
    
    # Plot in side tenons
    left_tenon.plot(np.sin(x), x, 'orange', linewidth=2, label='sin(x) vs x')
    left_tenon.set_xlabel('sin(x)')
    left_tenon.set_ylabel('x')
    
    right_tenon.scatter(np.sin(x[::5]), np.cos(x[::5]), 
                       c=x[::5], cmap='viridis', s=20, label='Parametric')
    right_tenon.set_xlabel('sin(x)')
    right_tenon.set_ylabel('cos(x)')
    
    # Print structure
    print("Complex layout structure:")
    print(main.structure)
    
    # Show the plot
    plt.show()


def auto_align_example():
    """Example demonstrating automatic axis alignment."""
    print("=== Auto-Align Example ===")
    
    # Create root mortise
    fig, root = mortise(width=2, height=2, figsize=(12, 8))
    
    # Plot data in main panel
    x = np.linspace(0, 10, 100)
    root.plot(x, np.sin(x), 'b-', linewidth=2, label='sin(x)')
    root.set_title('Main Panel')
    root.set_xlim(0, 10)
    root.set_ylim(-1.5, 1.5)
    root.grid(True, alpha=0.3)
    
    print("Main panel coordinate ranges:")
    print(f"xlim: {root.axes.get_xlim()}")
    print(f"ylim: {root.axes.get_ylim()}")
    
    # Add tenons with automatic alignment (default behavior)
    print("\nAdding tenons with automatic alignment:")
    
    # Top tenon - automatically aligns x-axis
    top_panel = root.tenon(pos='top', size=1, title='Top Panel (Auto-align)')
    top_panel.plot(x, np.cos(x), 'r-', linewidth=2, label='cos(x)')
    top_panel.set_title('Top: cos(x)')
    top_panel.grid(True, alpha=0.3)
    
    # Bottom tenon - automatically aligns x-axis
    bottom_panel = root.tenon(pos='bottom', size=1, title='Bottom Panel (Auto-align)')
    bottom_panel.plot(x, np.sin(x)**2, 'g-', linewidth=2, label='sin²(x)')
    bottom_panel.set_title('Bottom: sin²(x)')
    bottom_panel.grid(True, alpha=0.3)
    
    # Left tenon - automatically aligns y-axis
    left_panel = root.tenon(pos='left', size=1, title='Left Panel (Auto-align)')
    left_panel.plot(np.sin(x), x, 'orange', linewidth=2, label='sin(x) vs x')
    left_panel.set_title('Left: sin(x) vs x')
    left_panel.grid(True, alpha=0.3)
    
    # Right tenon - automatically aligns y-axis
    right_panel = root.tenon(pos='right', size=1, title='Right Panel (Auto-align)')
    right_panel.scatter(np.sin(x[::5]), np.cos(x[::5]), c=x[::5], cmap='viridis', s=20)
    right_panel.set_title('Right: Scatter')
    right_panel.grid(True, alpha=0.3)
    
    print(f"\nCoordinate ranges after automatic alignment:")
    print(f"Top panel xlim: {top_panel.axes.get_xlim()}")
    print(f"Bottom panel xlim: {bottom_panel.axes.get_xlim()}")
    print(f"Left panel ylim: {left_panel.axes.get_ylim()}")
    print(f"Right panel ylim: {right_panel.axes.get_ylim()}")
    
    # Demonstrate manual alignment for comparison
    print("\nDemonstrating manual alignment:")
    root.align_axes('both')  # Manually align all axes
    
    print(f"After manual alignment:")
    print(f"Top panel xlim: {top_panel.axes.get_xlim()}")
    print(f"Bottom panel xlim: {bottom_panel.axes.get_xlim()}")
    print(f"Left panel ylim: {left_panel.axes.get_ylim()}")
    print(f"Right panel ylim: {right_panel.axes.get_ylim()}")
    
    fig.savefig('auto_align_example.png', dpi=150, bbox_inches='tight')
    print("\nSaved: auto_align_example.png")


if __name__ == "__main__":
    print("=== Basic Example ===")
    main()
    
    print("\n=== Advanced Example ===")
    advanced_example()
    
    print("\n=== Auto-Align Example ===")
    auto_align_example()
