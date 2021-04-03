r"""

**apyce.grid**

----

This module contains the main class of APyCE.

----

+----------------+------------------------------------------------------------+
|     Method     | Description                                                |
+================+============================================================+
|  process_grid  | Compute grid topology and geometry from pillar grid        |
|                | description                                                |
+----------------+------------------------------------------------------------+
| load_cell_data | Read a file with data and append this data to model        |
+----------------+------------------------------------------------------------+
|   plot_grid    | Plot the grid with PyVista                                 |
+----------------+------------------------------------------------------------+
|   export_data  | Save grid data to a single vtu file for visualizing in     |
|                | ParaView                                                   |
+----------------+------------------------------------------------------------+

"""

from .Grid import Grid
