import os

from setuptools import setup

about = {}
ver_path = ('src/apyce/__version__.py')
with open(ver_path) as f:
    for line in f:
        if line.startswith('__version__'):
            exec(line, about)

# Read the contents of README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Read the contents of REQUIREMENTS file
with open("requirements.txt") as f:
    required = f.read().splitlines()

setup(
    name='apyce',
    version=about['__version__'],
    classifiers=['Development Status :: 2 - Pre-Alpha',
                 'License :: OSI Approved :: BSD License',
                 'Programming Language :: Python',
                 'Topic :: Scientific/Engineering',
                 'Topic :: Scientific/Engineering :: Visualization'],
    install_requires=required,
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages = ['apyce'],
    package_dir={'apyce': 'src/apyce'},
    url = 'https://github.com/mateustosta/apyce-project',
    license = 'BSD 3-Clause',
    author = 'Mateus Metzker Tosta',
    author_email = 'mateustosta@outlook.com.br',
    description = 'A Python-based Builder/Eclipse wrapper for 3D visualization of reservoir grids',
    python_requires='>=3.8'
)
