Quick Start
===========

Basic Usage
-----------

Sunmao provides a flexible way to create complex subplot layouts using the traditional Chinese mortise-tenon joinery concept. Here's a quick example:

.. code-block:: python

    import numpy as np
    import matplotlib.pyplot as plt
    from sunmao import mortise

    # Create the root mortise
    fig, root = mortise(width=2, height=2, figsize=(10, 8))

    # Add tenons in different directions
    top_panel = root.tenon(pos='top', size=1, title='Top Panel')
    bottom_panel = root.tenon(pos='bottom', size=1, title='Bottom Panel')
    left_panel = root.tenon(pos='left', size=1, title='Left Panel')
    right_panel = root.tenon(pos='right', size=1, title='Right Panel')

    # Plot data
    x = np.linspace(0, 10, 100)
    root.plot(x, np.sin(x), 'b-', linewidth=2, label='sin(x)')
    top_panel.plot(x, np.cos(x), 'r-', linewidth=2, label='cos(x)')
    bottom_panel.plot(x, np.sin(x)**2, 'g-', linewidth=2, label='sin²(x)')
    left_panel.plot(x, np.exp(-x/5), 'orange', linewidth=2, label='exp(-x/5)')
    right_panel.scatter(x[::5], np.cos(x[::5]), c=x[::5], cmap='viridis', s=20)

    # Create legend
    root.create_legend(mode='auto')

    plt.show()

Key Concepts
------------

Mortise-Tenon Architecture
~~~~~~~~~~~~~~~~~~~~~~~~~~

Sunmao uses the traditional Chinese mortise-tenon joinery concept:

- **Mortise**: The main panel that can contain matplotlib axes
- **Tenon**: Child panels that extend from the mortise in four directions (top, bottom, left, right)

Each mortise is an independent matplotlib axes object that can be fully customized.

Legend Management
~~~~~~~~~~~~~~~~~

Sunmao provides unified legend management with four modes:

- **Global**: Single legend for all panels
- **Local**: Individual legend for each panel
- **Mixed**: Combination of global and local legends
- **Auto**: Automatic selection based on data characteristics

Axis Alignment
~~~~~~~~~~~~~~

Sunmao supports automatic axis alignment:

- **Implicit alignment**: Automatically aligns axes when adding tenons
- **Explicit alignment**: Manual control using `align_axes()` method
- **Flexible control**: Choose alignment direction (x, y, or both)

Advanced Features
-----------------

Nested Layouts
~~~~~~~~~~~~~~

Sunmao supports unlimited nesting of mortise-tenon structures:

.. code-block:: python

    # Create nested structure
    fig, root = mortise(width=2, height=2)
    
    # First level
    top_panel = root.tenon(pos='top', size=1)
    
    # Second level
    top_left = top_panel.tenon(pos='left', size=1)
    
    # Third level
    top_left_top = top_left.tenon(pos='top', size=0.5)

Custom Styling
~~~~~~~~~~~~~~

Each mortise can be fully customized:

.. code-block:: python

    # Custom styling
    root.ax.set_facecolor('lightgray')
    root.grid(True, alpha=0.3)
    root.set_title('Custom Styled Panel')
    root.set_xlabel('X Axis')
    root.set_ylabel('Y Axis')

Next Steps
----------

- Check out the :doc:`api_reference` for detailed API documentation
- Explore the :doc:`examples` for more complex use cases
- See the :doc:`changelog` for version history
