import numpy as np
import re
import os

import gridprocessing
import utils

def readGRDECL(fn=''):
    '''
    Read subset of ECLIPSE GRID file

    SYNOPSIS
        G = readGRDECL(fn)

    PARAMETERS
        fn - String holding name of GRDECL specification

    RETURNS
        Output structure containing the kown fields of the GRDECL
        specification, i.e., the 'GRID' section of an ECLIPSE input deck

    The currently recognized keywords are:

    'ACTNUM', 'COORD', 'INCLUDE', 'PERMX', 'PERMY', 'PERMZ'
    'PORO', 'ZCORN'
    '''

    # Supported Keywords
    supportedKeywords = ['ACTNUM', 'COORD', 'INCLUDE', 'PERMX', 'PERMY', 'PERMZ', 'PORO', 'ZCORN']

    # Try to open the file
    utils.fileOpenException(fn)

    # Create the G structure
    G = gridprocessing.Grid()
    G.fname=fn

    file = open(fn, 'r')

    # Print info in screen
    utils.printReadInfoStart(fn)

    for line in file:
        for key in supportedKeywords:
            if not line.startswith(key):
                G.unrec.append(key)
        if line.startswith("COORDSYS"):
            G.unrec.append('COORDSYS')
            continue
        elif line.startswith('SPECGRID'):
            line = file.readline()
            G.cartDims = np.array(re.findall('\d+', str(line)), dtype=int)
            G.N = G.cartDims[0] * G.cartDims[1] * G.cartDims[2]
            G.keywordsInFile.append('SPECGRID')
        elif line.startswith('COORD'):
            G.COORD = readSection(file)
            if len(G.COORD) == 6*(G.cartDims[0]+1)*(G.cartDims[1]+1):
                G.COORD = np.array(G.COORD, dtype=float)
                G.keywordsInFile.append('COORD')
            else:
                print("[Error] COORD data size must be 6*(NX+1)*(NY+1)")
                exit()
        elif line.startswith('ZCORN'):
            G.ZCORN = readSection(file)
            if len(G.ZCORN) == 8*G.N:
                G.ZCORN = np.array(G.ZCORN, dtype=float)
                G.keywordsInFile.append('ZCORN')
            else:
                print("[Error] ZCORN data size must be 2*NX*2*NY*2*NZ")
                exit()
        elif line.startswith('ACTNUM'):
            G.ACTNUM = readSection(file)
            if len(G.ACTNUM) == G.N:
                G.ACTNUM = np.array(G.ACTNUM, dtype=int)
                G.keywordsInFile.append('ACTNUM')
            else:
                print("[Error] ACTNUM data size must be NX*NY*NZ")
                exit()
        elif line.startswith('PORO'):
            G.PORO = readSection(file)
            if len(G.PORO) == G.N:
                G.PORO = np.array(G.PORO, dtype=float)
                G.keywordsInFile.append('PORO')
            else:
                print("[Error] PORO data size must be NX*NY*NZ")
                exit()
        elif line.startswith('PERMX'):
            G.PERMX = readSection(file)
            if len(G.PERMX) == G.N:
                G.PERMX = np.array(G.PERMX, dtype=float)
                G.keywordsInFile.append('PERMX')
            else:
                print("[Error] PERMX data size must be NX*NY*NZ")
                exit()
        elif line.startswith('PERMY'):
            G.PERMY = readSection(file)
            if len(G.PERMY) == G.N:
                G.PERMY = np.array(G.PERMY, dtype=float)
                G.keywordsInFile.append('PERMY')
            else:
                print("[Error] PERMY data size must be NX*NY*NZ")
                exit()
        elif line.startswith('PERMZ'):
            G.PERMZ = readSection(file)
            if len(G.PERMZ) == G.N:
                G.PERMZ = np.array(G.PERMZ, dtype=float)
                G.keywordsInFile.append('PERMZ')
            else:
                print("[Error] PERMZ data size must be NX*NY*NZ")
                exit()
        elif line.startswith('INCLUDE'):
            if not 'INCLUDE' in G.keywordsInFile:
                G.keywordsInFile.append('INCLUDE')
            line = file.readline()
            includeFilename='.'+os.path.sep+'Data'+os.path.sep+line.split('\'')[1]
            G = readIncludeFile(G,includeFilename)
    file.close()

    # Print Grid Info
    utils.printReadGridInfo(G)

    return G

def readSection(file):
    '''
    Read the section of data in the ECLIPSE
    input file and return the values

    PARAMETERS
        file - Structure with ECLIPSE input file

    RETURNS
        Data of the section
    '''
    section = []
    while True:
        line = file.readline()
        if line.startswith('--') or not line.strip():
            # Ignore black lines and comments
            continue
        values = expandsScalars(line)
        section.extend(values)
        if section[-1] == '/':
            # End of section
            section.pop() # remove '/'
            break
    return section

def expandsScalars(line):
    '''
    Expand the values of the format:
        2*3 => [3,3]

    PARAMETERS
        line - Line of the ECLIPSE input file

    RETURNS
        Values expanded
    '''
    values = []
    for scalar in line.split():
        if not '*' in scalar:
            values.append(scalar)
        else:
            tmp = scalar.split('*')
            tmp = [tmp[1]] * float(tmp[0])
            values.extend(tmp)
    return values

def readIncludeFile(G, fn):
    '''
    Read the include file passed in the keyword INCLUDE

    PARAMETERS
        G - Structure containing the known fields of the GRDECL specification
        fn - String holding the include filename

    RETURNS
        Output structure containing the kown fields of the GRDECL
        specification, i.e., the 'GRID' section of an ECLIPSE input deck
    '''
    # Try to open the file
    utils.fileOpenException(fn)

    file = open(fn, 'r')
    for line in file:
        if line.startswith('COORDSYS'):
            G.unrec.append('COORDSYS')
            continue
        elif line.startswith('SPECGRID'):
            line = file.readline()
            G.cartDims = np.array(re.findall('\d+', str(line)), dtype=int)
            G.N = G.cartDims[0] * G.cartDims[1] * G.cartDims[2]
            G.keywordsInFile.append('SPECGRID')
        elif line.startswith('COORD'):
            G.COORD = readSection(file)
            if len(G.COORD) == 6*(G.cartDims[0]+1)*(G.cartDims[1]+1):
                G.COORD = np.array(G.COORD, dtype=float)
                G.keywordsInFile.append('COORD')
            else:
                print("[Error] COORD data size must be 6*(NX+1)*(NY+1)")
                exit()
        elif line.startswith('ZCORN'):
            G.ZCORN = readSection(file)
            if len(G.ZCORN) == 8*G.N:
                G.ZCORN = np.array(G.ZCORN, dtype=float)
                G.keywordsInFile.append('ZCORN')
            else:
                print("[Error] ZCORN data size must be 2*NX*2*NY*2*NZ")
                exit()
        elif line.startswith('ACTNUM'):
            G.ACTNUM = readSection(file)
            if len(G.ACTNUM) == G.N:
                G.ACTNUM = np.array(G.ACTNUM, dtype=int)
                G.keywordsInFile.append('ACTNUM')
            else:
                print("[Error] ACTNUM data size must be NX*NY*NZ")
                exit()
        elif line.startswith('PORO'):
            G.PORO = readSection(file)
            if len(G.PORO) == G.N:
                G.PORO = np.array(G.PORO, dtype=float)
                G.keywordsInFile.append('PORO')
            else:
                print("[Error] PORO data size must be NX*NY*NZ")
                exit()
        elif line.startswith('PERMX'):
            G.PERMX = readSection(file)
            if len(G.PERMX) == G.N:
                G.PERMX = np.array(G.PERMX, dtype=float)
                G.keywordsInFile.append('PERMX')
            else:
                print("[Error] PERMX data size must be NX*NY*NZ")
                exit()
        elif line.startswith('PERMY'):
            G.PERMY = readSection(file)
            if len(G.PERMY) == G.N:
                G.PERMY = np.array(G.PERMY, dtype=float)
                G.keywordsInFile.append('PERMY')
            else:
                print("[Error] PERMY data size must be NX*NY*NZ")
                exit()
        elif line.startswith('PERMZ'):
            G.PERMZ = readSection(file)
            if len(G.PERMZ) == G.N:
                G.PERMZ = np.array(G.PERMZ, dtype=float)
                G.keywordsInFile.append('PERMZ')
            else:
                print("[Error] PERMZ data size must be NX*NY*NZ")
                exit()
    file.close()

    return G

def writeVTK(G):
    '''
    Create a VTK file with all data of ECLIPSE file.

    PARAMETERS
        G - Structure with all the data

    RETURNS
        None
    '''
    vtkUnstructuredGrid = G.vtkUnstructuredGrid
    filename = G.fname
    filename = filename.split(os.path.sep)[2]
    filename = filename.split('.')[0]
    utils.printInfoWriteVTKStart(filename)
    legacyWriter = vtk.vtkUnstructuredGridWriter()
    legacyWriter.SetFileName('.'+os.path.sep+'Data'+os.path.sep+filename+'.vtk')
    legacyWriter.SetInputData(vtkUnstructuredGrid)
    legacyWriter.Write()
    utils.printInfoWriteVTK()