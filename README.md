APyCE Project: A Python-based Builder/Eclipse wrapper for 3D visualization of reservoir grids
==============================================================================================

## Graphical abstract

This artwork comprises examples of a few Cartesian and non-Cartesian petroleum 3D reservoirs grid models post-processed by APyCe.

<p align="center">
  <img src="https://raw.githubusercontent.com/mateustosta/apyce-project/master/img/showcase.png" width="100%"></img>
</p>

## Authorship

Mateus Tosta (@mt2312) <sup>1,*</sup> (mateustosta@outlook.com.br), Bin Wang (@BinWang0213) <sup>2</sup> (bin.wang@cup.edu.cn), and Gustavo P. Oliveira (@gcpeixoto) <sup>1</sup> (gustavo.oliveira@ci.ufpb.br)

<sup>1</sup> TRIL Lab, Federal University of Paraíba, João Pessoa, Brazil

<sup>2</sup> Department of Petroleum Engineering, China University of Petroleum, Beijing, China

<sup>*</sup> Currently at Gaudium Corp., Brazil

## Statement of need
APyCE is an open-source Python utility module for 3D visualization of  _corner-point grid_ reservoir models. It improves and expands the pioneer [PyGRDECL](https://github.com/BinWang0213/PyGRDECL) library and provides a seamless conversion from proprietary format (deck-like) files handled by leading softwares of the oil and gas sector, such as CMG Builder™ and Schlumberger Eclipse™, and VTK/VTU format, thus enabling interactive visualization through [ParaView](https://www.paraview.org). Additionally, it outputs static visuals on top of [PyVista](https://www.pyvista.org/).

## Components  
All the components of APyCE are briefly described below.

### apyce.grid  
The ``grid`` class houses the main functions of APyCE.

#### Functions  
- `process_grid()`: computes grid topology and geometry from pillar grid description.
- `load_cell_data()`: reads a file with data and append this data to model.
- `plot_grid()`: renders a static plot of the grid through PyVista.
- `export_data()`: saves grid data to a single VTU file for interactive visualization in ParaView.


## Installation
APyCE is developed under Python>=3.8

To get the most current version, install it from Github:  
    
    git clone https://github.com/mateustosta/apyce-project.git
    cd apyce-project

To setup the development environment, do the following

    virtualenv --python=python3.8 venv3
    source venv3/bin/activate
    pip install -r requirements.txt
    pip install .

or use Anaconda: 

    conda create -n apyce
    conda activate apyce
    conda install numpy vtk pyvista matplotlib
    
## Usage  

A simple APyCe workflow is like this:

```python
import apyce as ap

G = ap.grid.Grid(filename='Data/dome.grdecl', grid_origin='eclipse', verbose=True)
G.process_grid()
G.export_data()
G.plot_grid(filename='Data/Results/dome.vtu', lighting=False, property='PORO', show_edges=True, specular=0.0,
            specular_power=0.0, show_scalar_bar=True, cmap='viridis')

```

## Examples

APyCE produces ready-made visuals for high-quality publications.

- Output of `Getting_Started.py` example with ``dome`` model
<p align="center">
  <img src="https://raw.githubusercontent.com/mateustosta/apyce-project/master/img/DOME_PORO.png" width="70%"></img>
</p>

- Output of `Getting_Started.py` example with ``PSY`` model
<p align="center">
  <img src="https://raw.githubusercontent.com/mateustosta/apyce-project/master/img/PSY_PORO_Getting_Started.png" width="70%"></img>
</p>

## License

This code is released under the terms of the BSD license, and thus free for commercial and research use. Feel free to use the code into your own project with a PROPER REFERENCE.  

Tosta. M, Wang B., Oliveira G.P., APyCE Project: A Python-based Builder/Eclipse wrapper for 3D visualization of reservoir grids, (2020), GitHub repository, https://github.com/mateustosta/apyce-project