from apyce.utils import Errors

import os
import sys

def file_open_exception(filename=''):
    r"""
    Try to open the file.

    Parameters
    ----------
    filename : string
        A string that holds the name (path) of the grid file.

    """

    try:
        file = open(get_path(filename), 'r')
        file.close()
    except IOError:
        print("[ERROR] Can't open the file {}".format(get_path(filename)))
        sys.exit()


def get_path(filename=''):
    r"""
    Get the absolute path of the file.

    Parameters
    ----------
    filename : string
        A string that holds the name (path) of the grid file.

    """

    return os.path.normpath(os.path.abspath(filename))


def get_basename(filename=''):
    r"""
    Get the basename of the file.

    Parameters
    ----------
    filename : string
        A string that holds the name (path) of the grid file.

    """

    return os.path.normpath(os.path.basename(filename))


def get_dirname(filename=''):
    r"""
    Get the directory name of the file.

    Parameters
    ----------
    filename : string
        A string that holds the name (path) of the grid file.

    """

    return os.path.normpath(os.path.dirname(filename))


def get_include_file(filename='', line=''):
    r"""
    Get the include file path.

    Parameters
    ----------
    filename : string
        A string that holds the name (path) of the grid file.
    line : string
        A string that holds the name of the include file.

    """

    return os.path.normpath(get_dirname(filename) + os.path.sep + line.split('\'')[1])


def check_dim(cart_dims, num_cell, keyword, file):
    r"""
    Check dimension of the grid.

    Parameters
    ----------
    cart_dims : ndarray
        Dimensions of the grid.
    num_cell : int
        Number of cells in the grid.
    keyword : string
        Keyword currently being reading.
    file : file
        Opened file with grid specification.

    """

    if len(cart_dims) == 0 or num_cell is None or len([x for x in cart_dims if x < 1]) > 0:
        print(Errors.CHECK_DIM_ERRROR.replace('{}', keyword))
        file.close()
        sys.exit()


def check_corner_point_grid(cart_dims, coord, zcorn):
    r"""
    Check if corner-point grid is already defined.

    Parameters
    ----------
    cart_dims : ndarray
        Dimensions of the grid.
    coord : ndarray
        A list of floating point numbers that represents the COORD keyword from Schlumberger Eclipse.
    zcorn : ndarray
        A list of floating point numbers that represents the ZCORN keyword from Schlumberger Eclipse.

    """

    assert len(cart_dims) != 0,Errors.GRID_NOT_DEFINED_ERROR
    assert len(coord) != 0,Errors.GRID_NOT_DEFINED_ERROR
    assert len(zcorn) != 0,Errors.GRID_NOT_DEFINED_ERROR

def check_cartesian_grid(cart_dims, dx, dy, dz, tops):
    r"""
    Check if cartesian grid is already defined.

    Parameters
    ----------
    cart_dims : ndarray
        Dimensions of the grid.
    dx : ndarray
        A list of integer point numbers that represents the DX keyword from Schlumberger Eclipse.
    dy : ndarray
        A list of integer point numbers that represents the DY keyword from Schlumberger Eclipse.
    dz : ndarray
        A list of integer point numbers that represents the DZ keyword from Schlumberger Eclipse.
    tops : ndarray
        A list of integer point numbers that represents the TOPS keyword from Schlumberger Eclipse.

    """

    assert len(cart_dims) != 0,Errors.GRID_NOT_DEFINED_ERROR
    assert len(dx) != 0,Errors.GRID_NOT_DEFINED_ERROR
    assert len(dy) != 0,Errors.GRID_NOT_DEFINED_ERROR
    assert len(dz) != 0, Errors.GRID_NOT_DEFINED_ERROR
    assert len(tops) != 0, Errors.GRID_NOT_DEFINED_ERROR


def create_results_directory(filename=''):
    r"""
    Create the 'Results" directory to save ParaView file.

    filename : string
         A string that holds the name (path) of the grid file.

    """

    if not os.path.exists(get_dirname(filename) + '/Results'):
        os.makedirs(get_dirname(filename) + '/Results')

    return get_dirname(filename) + '/Results/'


def expand_scalars(line=''):
    r"""
    Expand the values of the format:
        2*3 => [3,3]

    Parameters
    ----------
    line : string
        A string that holds the numbers to be expanded

    """

    values = []
    for scalar in line.split():
        if '*' not in scalar:
            values.append(scalar)
        else:
            tmp = scalar.split('*')
            tmp = [tmp[1]] * int(tmp[0])
            values.extend(tmp)
    return values


def get_ijk(i, j, k, nx, ny, nz):
    r"""
    Convert index [HEIGHT, WIDTH, DEPTH] to a flat 3D matrix index [HEIGHT * WIDTH * DEPTH].

    If you have:
        Original[HEIGHT, WIDTH, DEPTH]

    then you could turn it into:
        Flat[HEIGHT * WIDTH * DEPTH] by

    Flat[x + WIDTH * (y + DEPTH * z)] = Original[x, y, z] or
    Flat[(z * xMax * yMax) + (y * xMax) + x] = Original[x, y, z]

    Notes
    -----
    https://stackoverflow.com/questions/7367770/how-to-flatten-or-index-3d-array-in-1d-array/7367812

    """

    return (k * nx * ny) + (j * nx) + i