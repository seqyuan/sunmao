Changelog
=========

Version 0.3.0 (2025-01-XX)
---------------------------

New Features
~~~~~~~~~~~~

- Added unified legend management system with `LegendManager` class
- Implemented four legend modes: global, local, mixed, and auto
- Added automatic axis alignment functionality
- Integrated legend management into mortise class
- Added `LegendPosition` class for position management

API Changes
~~~~~~~~~~~

- Added `create_legend()` method to mortise class
- Added `clear_legends()` method to mortise class
- Added `set_legend_position()` method to mortise class
- Added `add_legend_item()` method to mortise class
- Added `get_legend_manager()` method to mortise class
- Added `align_axes()` method to mortise class
- Added `share_axes()` method to mortise class

Improvements
~~~~~~~~~~~~

- Enhanced mortise class with legend management capabilities
- Improved automatic rendering system
- Better error handling and validation
- Enhanced documentation and examples

Version 0.2.0 (2025-01-XX)
---------------------------

New Features
~~~~~~~~~~~~

- Implemented mortise-tenon architecture
- Added support for four-directional tenon placement
- Added automatic rendering system
- Added structure visualization
- Added matplotlib axes integration

API Changes
~~~~~~~~~~~

- Introduced `mortise` class as main building block
- Added `tenon()` method for adding child panels
- Added `get_tenon()` method for accessing child panels
- Added `structure` property for layout visualization
- Added `ax` property for direct axes access

Version 0.1.0 (2025-01-XX)
---------------------------

Initial Release
~~~~~~~~~~~~~~~

- Basic subplot layout functionality
- Simple panel management
- matplotlib integration
- Basic documentation
