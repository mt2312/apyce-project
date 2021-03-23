[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]

APyCE Project: A Python-based Builder/Eclipse wrapper for 3D visualization of reservoir grids
==============================================================================================
Mateus Tosta (mateustosta@outlook.com.br), Petroleum Engineering Modelling Laboratory, Federal University of Paraíba, João Pessoa, BR

<p align="center">
  <img src = "./img/PSY_Model.png" width="100%">
</p>

This project is intended to develop an open-source Python implementation focused on post-processing 3D reservoir grid files for integration between the softwares CMG Builder and Schlumberger Eclipse

## Installation
#### Linux
To setup the development environment do the following:

    git clone https://github.com/mateustosta/apyce-project.git
    cd apyce-project
    virtualenv --python=python3 venv3
    source venv3/bin/activate
    pip install -r requirements.txt

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
from APyCE import Model

# MUST be in src/Data folder
pathToFile = './Data/PSY.grdecl'
G = Model(pathToFile, 'Eclipse')
G.process_grdecl()
G.write_vtk()
```

## Usage Windows
```python
from APyCE import Model

# MUST be in src/Data folder
pathToFile = '.\\Data\\PSY.grdecl'
G = Model(pathToFile, 'Eclipse')
G.process_grdecl()
G.write_vtk()
```

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