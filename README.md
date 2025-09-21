# Sunmao

[![PyPI version](https://badge.fury.io/py/sunmao.svg)](https://badge.fury.io/py/sunmao)
[![Documentation Status](https://readthedocs.org/projects/sunmao/badge/?version=latest)](https://sunmao.readthedocs.io/en/latest/?badge=latest)
[![Python Support](https://img.shields.io/pypi/pyversions/sunmao.svg)](https://pypi.org/project/sunmao/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A flexible subplot layout library for matplotlib with support for adding panels in all directions using the traditional Chinese mortise-tenon joinery concept.

## Features

- **🎯 Mortise-Tenon Architecture**: Traditional Chinese joinery concept for flexible layouts
- **📐 Four-Directional Expansion**: Add panels in all directions (top, bottom, left, right)
- **🎨 Independent Axes**: Each panel is a fully customizable matplotlib axes object
- **🌳 Nested Structures**: Support for complex nested panel hierarchies
- **📊 Unified Legend Management**: Automatic legend positioning and management
- **⚡ Auto Alignment**: Automatic axis alignment between adjacent panels
- **🔧 Full Matplotlib Integration**: Direct access to all matplotlib plotting functions

## Installation

```bash
pip install sunmao
```

Or using Poetry:

```bash
poetry add sunmao
```

## Quick Start

```python
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

# Create unified legend
root.create_legend(mode='auto')

plt.show()
```



## Advanced Features

### Legend Management

Sunmao provides unified legend management with four modes:

```python
# Global legend for all panels
root.create_legend(mode='global', position='upper center', ncol=2)

# Individual legend for each panel
root.create_legend(mode='local')

# Mixed mode (global + local)
root.create_legend(mode='mixed', position='upper center')

# Automatic mode selection
root.create_legend(mode='auto')
```

### Axis Alignment

Automatic axis alignment between adjacent panels:

```python
# Automatic alignment when adding tenons
top_panel = root.tenon(pos='top', size=1, auto_align=True)

# Manual alignment
root.align_axes('x')  # Align x-axis
root.align_axes('y')  # Align y-axis
root.align_axes('both')  # Align both axes
```

### Nested Structures

Support for unlimited nesting:

```python
# Create nested structure
fig, root = mortise(width=2, height=2)

# First level
top_panel = root.tenon(pos='top', size=1)

# Second level
top_left = top_panel.tenon(pos='left', size=1)

# Third level
top_left_top = top_left.tenon(pos='top', size=0.5)
```

## Documentation

- 📚 [Full Documentation](https://sunmao.readthedocs.io/)
- 🚀 [Quick Start Guide](https://sunmao.readthedocs.io/en/latest/quickstart.html)
- 📖 [API Reference](https://sunmao.readthedocs.io/en/latest/api_reference.html)
- 💡 [Examples](https://sunmao.readthedocs.io/en/latest/examples.html)

## Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/seqyuan/sunmao.git
cd sunmao

# Install in development mode
poetry install

# Run tests
make test

# Run linting
make lint
```

### Release Process

See [RELEASE_GUIDE.md](RELEASE_GUIDE.md) for detailed instructions on:

- 🚀 Pushing to GitHub
- 📦 Publishing to PyPI
- 📚 Setting up ReadTheDocs documentation
- 🔄 Automated CI/CD with GitHub Actions

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- 🏗️ Inspired by [trackc's tenon class](https://github.com/seqyuan/trackc) for vertical stacking
- 📊 Layout concepts influenced by [PyComplexHeatmap](https://github.com/DingWB/PyComplexHeatmap)
- 🎨 General approach inspired by [marsilea](https://github.com/Marsilea-viz/marsilea)
- 🔧 Release process inspired by [evapro](https://github.com/seqyuan/evapro)
