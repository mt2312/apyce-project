APyCE Project: A Python-based Builder/Eclipse wrapper for 3D visualization of reservoir grids
==============================================================================================
Mateus Tosta (mateustosta@outlook.com.br), Petroleum Engineering Modeling Laboratory, Federal University of Paraíba, João Pessoa, BR

<p align="center">
  <img src="https://raw.githubusercontent.com/mateustosta/apyce-project/master/img/showcase.png" width="100%"></img>
</p>

This project is intended to develop an open-source Python implementation focused on post-processing 3D reservoir grid files for integration between the softwares CMG Builder and Schlumberger Eclipse and visualization with [ParaView](https://www.paraview.org).

## Components  
All the components of APyCE are briefly described below.

### apyce.grid  
The ``grid`` class houses the main functions of APyCE.

#### Functions  
- process_grid()
- load_cell_data()
- plot_grid()
- export_data()

##### process_grid()
Compute grid topology and geometry from pillar grid description.

##### load_cell_data()
Read a file with data and append this data to model

##### plot_grid()
Plot the grid with [PyVista](https://www.pyvista.org/)

##### export_data()
Save grid data to a single VTU file for visualizing in ParaView

## Installation
APyCE is developed under Python>=3.8

To get the most current version, install from github:  
    
    git clone https://github.com/mateustosta/apyce-project.git
    cd apyce-project

To setup the development environment do the following:

    virtualenv --python=python3.8 venv3
    source venv3/bin/activate
    pip install -r requirements.txt
    pip install .

or, use Anaconda (https://www.anaconda.com/download/):  

    conda create -n apyce
    conda activate apyce
    conda install numpy vtk pyvista matplotlib
    
## Usage  
```python
import apyce as ap

G = ap.grid.Grid(filename='Data/dome.grdecl', grid_origin='eclipse', verbose=True)
G.process_grid()
G.export_data()
G.plot_grid(filename='Data/Results/dome.vtu', lighting=False, property='PORO', show_edges=True, specular=0.0,
            specular_power=0.0, show_scalar_bar=True, cmap='viridis')

```

## Examples
Output of Getting_Started.py example with ``dome`` model
<p align="center">
  <img src="https://raw.githubusercontent.com/mateustosta/apyce-project/master/img/DOME_PORO.png" width="70%"></img>
</p>

Output of Getting_Started.py example with ``PSY`` model
<p align="center">
  <img src="https://raw.githubusercontent.com/mateustosta/apyce-project/master/img/PSY_PORO_Getting_Started.png" width="70%"></img>
</p>

## License

This code is released under the terms of the BSD license, and thus free for commercial and research use. Feel free to use the code into your own project with a PROPER REFERENCE.  

Mateus Tosta, APyCE Project: A Python-based Builder/Eclipse wrapper for 3D visualization of reservoir grids, (2020), GitHub repository, https://github.com/mateustosta/apyce-project