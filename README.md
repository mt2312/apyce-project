APyCE Project: A Python-based Builder/Eclipse wrapper for 3D visualization of reservoir grids
==============================================================================================
Mateus Tosta (mateustosta@outlook.com.br), Petroleum Engineering Modelling Laboratory, Federal University of Paraíba, João Pessoa, BR

<p align="center">
  <img src = "https://github.com/mateustosta/apyce-repo/blob/master/img/resultado.png" height="400">
</p>

This project is intended to develop an open-source Python implementation focused on post-processing 3D reservoir grid files for integration between the softwares CMG Builder and Schlumberger Eclipse

## Features available in APyCE

#### Plotting

- [ ] plotGrid - Currently, the file is exported to Paraview, but the goal is to plot the grid using Python.

#### Grid Pocessing

- [ ] Grid Structure - Structure a class to contain all the data on the grid.
- [ ] Fault Process - Process and display reservoir faults

#### Paraview Export

- [ ] CreateVTKPoints - Method for creating VTK points, which will be used to assemble the structure to be exported.
- [ ] CreateVTKCells - Method to create the VTK cells, which will be used to assemble the structure to be exported.

## Installation
#### Linux
To setup the development environment do the following:

    git clone https://github.com/mateustosta/apyce-repo.git
    cd apyce-repo
    virtualenv --python=python3 venv3
    source venv3/bin/activate
    pip install -r requirements.txt
   
#### Windows
Use Anaconda (https://www.anaconda.com/download/)  

    conda create -n apyce
    activate apyce
    conda install numpy vtk
    
## Usage
```python
from inout import readGRDECL
from inout import writeVTK
from gridprocessing import Grid

# Read the data from ECLIPSE INPUT file
G = readGRDECL('./Data/dome.grdecl')

# Process the file
G.processGRDECL(G)

# Save the data in VTK format
G = writeVTK(G)
```

## License

This code is released under the terms of the BSD license, and thus free for commercial and research use. Feel free to use the code into your own project with a PROPER REFERENCE.  

Mateus Tosta, APyCE Project: A Python-based Builder/Eclipse wrapper for 3D visualization of reservoir grids, (2020), GitHub repository, https://github.com/mateustosta/apyce-repo
    
