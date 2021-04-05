[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]

APyCE Project: A Python-based Builder/Eclipse wrapper for 3D visualization of reservoir grids
==============================================================================================
Mateus Tosta (mateustosta@outlook.com.br), Petroleum Engineering Modelling Laboratory, Federal University of Paraíba, João Pessoa, BR

<p align="center">
  <img src="https://raw.githubusercontent.com/mateustosta/apyce-project/master/img/PSY_Model.png" width="100%"></img>
</p>

This project is intended to develop an open-source Python implementation focused on post-processing 3D reservoir grid files for integration between the softwares CMG Builder and Schlumberger Eclipse

## Installation
APyCE is developed under Python>=3.8

To get the most current version, install from github:  
    
    git clone https://github.com/mateustosta/apyce-project.git
    cd apyce-project

#### Linux
To setup the development environment do the following:

    virtualenv --python=python3.8 venv3
    source venv3/bin/activate
    pip install -r requirements.txt
    pip install .

or, use Anaconda (https://www.anaconda.com/download/):  

    conda create -n apyce
    conda activate apyce
    conda install numpy vtk
   
#### Windows
Use Anaconda (https://www.anaconda.com/download/)  

    conda create -n apyce
    conda activate apyce
    conda install numpy vtk
    
## Usage Linux
```python
import apyce as ap

G = ap.grid.Grid(filename='Data/dome.grdecl', grid_origin='eclipse', verbose=True)
G.process_grid()
G.export_data()
G.plot_grid(filename='Data\\Results/dome.vtu', lighting=False, property='PORO', show_edges=True, specular=0.0,
            specular_power=0.0, show_scalar_bar=True, cmap='viridis')

```

## Usage Windows
```python
import apyce as ap

G = ap.grid.Grid(filename='Data\\dome.grdecl', grid_origin='eclipse', verbose=True)
G.process_grid()
G.export_data()
G.plot_grid(filename='Data\\Results\\dome.vtu', lighting=False, property='PORO', show_edges=False, specular=0.0,
            specular_power=0.0, show_scalar_bar=True, cmap='viridis')
```

Output of Getting_Started.py example
<p align="center">
  <img src="https://raw.githubusercontent.com/mateustosta/apyce-project/master/img/DOME_PORO.png" width="70%"></img>
</p>

## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are greatly appreciated.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature`)
3. Commit your Changes (`git commit -m 'Add some feature'`)
4. Push to the Branch (`git push origin feature`)
5. Open a Pull Request

You can help too by requesting some feature or reporting bugs on [issues](https://github.com/mateustosta/apyce-project/issues).

## License

This code is released under the terms of the BSD license, and thus free for commercial and research use. Feel free to use the code into your own project with a PROPER REFERENCE.  

Mateus Tosta, APyCE Project: A Python-based Builder/Eclipse wrapper for 3D visualization of reservoir grids, (2020), GitHub repository, https://github.com/mateustosta/apyce-project
    
[contributors-shield]: https://img.shields.io/github/contributors/mateustosta/apyce-project.svg?style=for-the-badge
[contributors-url]: https://github.com/mateustosta/apyce-project/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/mateustosta/apyce-project.svg?style=for-the-badge
[forks-url]: https://github.com/mateustosta/apyce-project/network/members
[stars-shield]: https://img.shields.io/github/stars/mateustosta/apyce-project.svg?style=for-the-badge
[stars-url]: https://github.com/mateustosta/apyce-project/stargazers
[issues-shield]: https://img.shields.io/github/issues/mateustosta/apyce-project.svg?style=for-the-badge
[issues-url]: https://github.com/mateustosta/apyce-project/issues
[license-shield]: https://img.shields.io/github/license/mateustosta/apyce-project.svg?style=for-the-badge
[license-url]: https://github.com/mateustosta/apyce-project/blob/master/LICENSE