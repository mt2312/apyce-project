import os

def fileOpenException(fn):
    '''
    Try to open the file

    PARAMETERS
        fn - String holding the filename

    RETURNS
        None
    '''
    try:
        file = open(fn, 'r')
        file.close()
    except IOError:
        print("Oops! Can't open the file " + fn)
        exit()

def printReadInfoStart(fn):
    print("[Input] Reading ECLIPSE file \"" + fn + "\"...")

def printReadGridInfo(G):
    print("\tGrid Dimension(NX, NY, NZ): {} x {} x {}".format(G.cartDims[0], G.cartDims[1], G.cartDims[2]))
    print("\tNumOfGrids: {}".format(G.N))
    print("\tKeywords: " + str(G.keywordsInFile))
    print("\tNumOfKeywords: " + str(len(G.keywordsInFile)))
    print("\tUnrecognized Keywords: " + str(G.unrec))
    print("....Done!\n")

def printProcessInfoStart():
    print("[Process] Converting GRDECL to VTK...")

def printProcessGridInfo(vtkUnstructuredGrid):
    print("\tNumOfPoints " + vtkUnstructuredGrid.GetNumberOfPoints())
    print("\tNumOfCells " + vtkUnstructuredGrid.GetNumberOfCells())
    print("....Done!\n")

def transform3DArrayIntoFlat3DMatrix(i , j, k, NX, NY, NZ):
    '''
    If you have a 3D array:
        Original[HEIGHT, WIDTH, DEPTH] 

    then you could turn it into:
        Flat[HEIGHT * WIDTH * DEPTH] by

    Flat[x + WIDTH * (y + DEPTH * z)] = Original[x, y, z]

    See more:
    https://stackoverflow.com/questions/7367770/how-to-flatten-or-index-3d-array-in-1d-array/7367812
    '''
    return (i + NX * (j + NY * k))

def printInfoSaveData(name):
    print('\tInserting data [' + name + '] into vtk array')

def printInfoWriteVTKStart(fn):
    print("[Output] Writing Paraview file \"." + os.path.sep + "Data" + os.path.sep + fn + ".vtk\"...")

def printInfoWriteVTK():
    print("....Done!")