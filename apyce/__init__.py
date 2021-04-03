r"""

            ___    ____        ____________
           /   |  / __ \__  __/ ____/ ____/
          / /| | / /_/ / / / / /   / __/
         / ___ |/ ____/ /_/ / /___/ /___
        /_/  |_/_/    \__, /\____/_____/
                     /____/


**APyCE**

A Python-based Builder/Eclipse wrapper for 3D visualization of reservoir grids.

It consists of the following modules:

+----------------+------------------------------------------------------------+
|     module     | Contents and Description                                   |
+================+============================================================+
|   ``grid``     | Houses the ``Grid`` class, this is the main class of APyCE |
+----------------+------------------------------------------------------------+
|   ``io``       | Export data to ParaView                                    |
+----------------+------------------------------------------------------------+
|   ``utils``    | Helpers utilities                                          |
+----------------+------------------------------------------------------------+

"""

from .__version__ import __version__

from . import grid
from . import io
from . import utils