import re
import os

try:
    import vtk
    import vtk.util.numpy_support as numpy_support
except ImportError:
    print("No VTK module loaded.")
    exit()

try:
    import numpy as np
except ImportError:
    print("No NumPy module loaded.")
    exit()

class Apyce():
    def __init__(self, filename=''):
        self.fname = filename
        self.vtkUnstructuredGrid = vtk.vtkUnstructuredGrid()

        # Supported Keywords
        self.cartDims = []
        self.N = None
        self.COORD = None
        self.ZCORN = None
        self.ACTNUM = None
        self.PORO = None
        self.PERMX = None
        self.PERMY = None
        self.PERMZ = None

        self.fileOpenException(self.fname)
        self.readGRDECL(self.fname)

    def readGRDECL(self, filename=''):
        '''
        Read subset of ECLIPSE GRID file, should not directly called by user

        SYNOPSIS
            G = Apyce(filename)

        PARAMETERS
            filename - String holding name of GRDECL specification

        RETURNS
            This method doesn't have any return, but it save all the data in the fields presents in __init__ method

        '''
        return None
    
    def processGRDECL(self):
        return None

    def readSection(self, file):
        return None

    def expandsScalars(self, line):
        return None

    def fileOpenException(self, filename=''):
        return None

    def readIncludeFile(self, keywordsInFile, filename=''):
        return None

    def createVTKCells(self):
        return None

    def createVTKPoints(self):
        return None
    
    def getCellPillars(self, i, j):
        '''



        The pillar description 'COORD' is stored in a 6*nPillar
        array (number of pillars, nPillar == (NX+1)*(NY+1)) of
        bottom/top coordinate pairs. Specifically,

            grdecl.COORD((i-1)*6+(1:3)) -- (x,y,z)-coordinates of
                                           pillar 'i' top point.
            grdecl.COORD((i-1)*6+(4:6)) -- (x,y,z)-coordinates of
                                           pillar 'i' bottom point.
        '''
        return None

    def getCellZ(self, i, j, k):
        return None

    def getCellCoords(self, i, j, k):
        return None

    def interpolatePointsOnPillar(self, pillar, z):
        return None
    
    def transform3DArrayIntoFlat3DMatrix(self, i, j, k, nx, ny, nz):
        return None

    def numpyToVTK(self, name, numpy_data):
        return None

    def writeVTK(self):
        return None