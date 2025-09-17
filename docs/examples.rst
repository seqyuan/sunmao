Examples
========

Basic Layout Example
--------------------

.. code-block:: python

    import numpy as np
    import matplotlib.pyplot as plt
    from sunmao import mortise

    # Create root mortise
    fig, root = mortise(width=2, height=2, figsize=(10, 8))

    # Add tenons
    top_panel = root.tenon(pos='top', size=1, title='Top Panel')
    bottom_panel = root.tenon(pos='bottom', size=1, title='Bottom Panel')

    # Plot data
    x = np.linspace(0, 10, 100)
    root.plot(x, np.sin(x), 'b-', linewidth=2, label='sin(x)')
    top_panel.plot(x, np.cos(x), 'r-', linewidth=2, label='cos(x)')
    bottom_panel.plot(x, np.sin(x)**2, 'g-', linewidth=2, label='sin²(x)')

    # Create legend
    root.create_legend(mode='global', position='upper center')

    plt.show()

Complex Nested Layout
---------------------

.. code-block:: python

    import numpy as np
    import matplotlib.pyplot as plt
    from sunmao import mortise

    # Create complex nested layout
    fig, root = mortise(width=3, height=3, figsize=(12, 10))

    # First level
    top_panel = root.tenon(pos='top', size=1, title='Level 1')
    bottom_panel = root.tenon(pos='bottom', size=1, title='Level 1')
    left_panel = root.tenon(pos='left', size=1, title='Level 1')
    right_panel = root.tenon(pos='right', size=1, title='Level 1')

    # Second level - nested tenons
    top_left = top_panel.tenon(pos='left', size=0.5, title='Level 2')
    top_right = top_panel.tenon(pos='right', size=0.5, title='Level 2')
    bottom_left = bottom_panel.tenon(pos='left', size=0.5, title='Level 2')
    bottom_right = bottom_panel.tenon(pos='right', size=0.5, title='Level 2')

    # Plot different data types
    x = np.linspace(0, 5, 50)
    root.plot(x, np.sin(x), 'b-', linewidth=2, label='sin(x)')
    top_panel.plot(x, np.cos(x), 'r-', linewidth=2, label='cos(x)')
    bottom_panel.scatter(x[::2], np.sin(x[::2]), c=x[::2], cmap='viridis', s=20)
    left_panel.plot(x, np.exp(-x), 'g-', linewidth=2, label='exp(-x)')
    right_panel.plot(x, np.log(x + 1), 'orange', linewidth=2, label='log(x+1)')

    # Nested plots
    top_left.plot(x, np.tan(x), 'purple', linewidth=2, label='tan(x)')
    top_right.plot(x, np.sqrt(x), 'brown', linewidth=2, label='sqrt(x)')
    bottom_left.plot(x, x**2, 'pink', linewidth=2, label='x²')
    bottom_right.plot(x, x**3, 'cyan', linewidth=2, label='x³')

    # Create mixed legend
    root.create_legend(mode='mixed', position='upper center', ncol=3)

    plt.show()

Legend Management Examples
-------------------------

Global Legend
~~~~~~~~~~~~~

.. code-block:: python

    # Global legend for all panels
    root.create_legend(mode='global', position='upper center', ncol=2)

Local Legends
~~~~~~~~~~~~~

.. code-block:: python

    # Individual legend for each panel
    root.create_legend(mode='local')

Mixed Legends
~~~~~~~~~~~~~

.. code-block:: python

    # Combination of global and local legends
    root.create_legend(mode='mixed', position='upper center', ncol=2)

Auto Legend
~~~~~~~~~~~

.. code-block:: python

    # Automatic legend mode selection
    root.create_legend(mode='auto')

Axis Alignment Examples
-----------------------

Automatic Alignment
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Automatic alignment when adding tenons
    top_panel = root.tenon(pos='top', size=1, auto_align=True)
    bottom_panel = root.tenon(pos='bottom', size=1, auto_align=True)

Manual Alignment
~~~~~~~~~~~~~~~~

.. code-block:: python

    # Manual axis alignment
    root.align_axes('x')  # Align x-axis
    root.align_axes('y')  # Align y-axis
    root.align_axes('both')  # Align both axes

Custom Alignment
~~~~~~~~~~~~~~~~

.. code-block:: python

    # Align specific mortises
    root.align_axes('x', mortises=[top_panel, bottom_panel])
