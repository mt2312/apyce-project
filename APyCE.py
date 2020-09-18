import re
import os

try:
    import vtk
    import vtk.util.numpy_support as ns
except ImportError:
    print("No VTK module loaded.")
    exit()

try:
    import numpy as np
except:
    print("No NumPy module loaded.")
    exit()

class Apyce:
    def __init__(self, filename=''):
        self.fname=filename
        self.vtkUnstructuredGrid=vtk.vtkUnstructuredGrid()

        # Supported Keywords
        self.SPECGRID=[]
        self.NX=None
        self.NY=None
        self.NZ=None
        self.N=None
        self.COORDS=[]
        self.ZCORN=[]
        self.ACTNUM=[]
        self.PORO=[]

        self.FileOpenException(self.fname)
        self.readGRDECL(self.fname)
        self.GRDECL2VTK(self.fname)
        self.WriteVTK(self.vtkUnstructuredGrid, self.fname)

    def readGRDECL(self, filename=''):
        print("[Input] Reading ECLIPSE file \"" + filename + "\"...")

        file=open(filename, 'r')

        for line in file:
            if line.startswith("COORDSYS"):
                continue
            elif line.startswith('SPECGRID'):
                line=file.readline()
                self.SPECGRID=np.array(re.findall('\d+', str(line)), dtype=int)
                self.NX, self.NY, self.NZ=self.SPECGRID[0], self.SPECGRID[1], self.SPECGRID[2]
                self.N = self.NX * self.NY * self.NZ
                print("\tGrid Dimension: {} x {} x {}".format(self.NX, self.NY, self.NZ))
                print("\tNumOfGrids: {}".format(self.N))
            elif line.startswith('COORD'):
                self.COORDS=self.ReadSection(file)
                if (len(self.COORDS) == (6*(self.NX+1)*(self.NY+1))):
                    self.COORDS=np.array(self.COORDS, dtype=float)
                else:
                    print("[Error] COORD data size must be 6*(NX+1)*(NY+1)")
                    exit()
            elif line.startswith('ZCORN'):
                self.ZCORN=self.ReadSection(file)
                if (len(self.ZCORN) == (8*self.N)):
                    self.ZCORN=np.array(self.ZCORN, dtype=float)
                else:
                    print("[Error] ZCORN data size must be 2*NX*2*NY*2*NZ")
                    exit()
            elif line.startswith('ACTNUM'):
                self.ACTNUM=self.ReadSection(file)
                if (len(self.ACTNUM) == self.N):
                    self.ACTNUM=np.array(self.ACTNUM, dtype=int)
                else:
                    print("[Error] ACTNUM data size must be NX*NY*NZ")
                    exit()
            elif line.startswith('PORO'):
                self.PORO=self.ReadSection(file)
                if (len(self.PORO) == self.N):
                    self.PORO=np.array(self.PORO, dtype=float)
                else:
                    print("[Error] PORO data size must be NX*NY*NZ")
                    exit()
            elif line.startswith('INCLUDE'):
                line=file.readline()
                includeFilename='.'+os.path.sep+'Data'+os.path.sep+line.split('\'')[1]
                self.ReadIncludeFile(includeFilename)
        file.close()
        print("....Done!")

    def GRDECL2VTK(self, filename=''):
        print("\n[Output] Converting GRDECL to VTK...")
        
        #print("\tNumOfPoints", self.vtkUnstructuredGrid.GetNumberOfPoints())
        #print("\tNumOfCells", self.vtkUnstructuredGrid.GetNumberOfCells())
        print('....Done!\n')     

    def ReadSection(self, file):
        section=[]
        while True:
            line=file.readline()
            if line.startswith('--') or not line.strip():
                # Ignore blank lines and comments
                continue
            values=self.ExpandsScalars(line)
            section.extend(values)
            if section[-1] == '/':
                section.pop()
                break
        return section

    def ExpandsScalars(self, line):
        values=[]
        for scalar in line.split():
            if not '*' in scalar:
                values.append(scalar)
            else:
                tmp=scalar.split('*')
                tmp=[tmp[1]] * int(tmp[0])
                values.extend(tmp)
        return values

    def FileOpenException(self, filename=''):
        try:
            file=open(filename, 'r')
            file.close()
        except IOError:
            print("Oops! Can't open the file " + filename + ". Try again...")
            exit()

    def ReadIncludeFile(self, filename=''):
        self.FileOpenException(filename)
        file=open(filename, 'r')
        for line in file:
            if line.startswith('COORDSYS'):
                continue
            elif line.startswith('SPECGRID'):
                line=file.readline()
                self.SPECGRID=np.array(re.findall('\d+', str(line)), dtype=int)
                self.NX, self.NY, self.NZ=self.SPECGRID[0], self.SPECGRID[1], self.SPECGRID[2]
                self.N = self.NX * self.NY * self.NZ
                print("\tGrid Dimension: {} x {} x {}".format(self.NX, self.NY, self.NZ))
                print("\tNumOfGrids: {}".format(self.N))
            elif line.startswith('COORD'):
                self.COORDS=self.ReadSection(file)
                if (len(self.COORDS) == (6*(self.NX+1)*(self.NY+1))):
                    self.COORDS=np.array(self.COORDS, dtype=float)
                else:
                    print("[Error] COORD data size must be 6*(NX+1)*(NY+1)")
                    exit()
            elif line.startswith('ZCORN'):
                self.ZCORN=self.ReadSection(file)
                if (len(self.ZCORN) == (8*self.N)):
                    self.ZCORN=np.array(self.ZCORN, dtype=float)
                else:
                    print("[Error] ZCORN data size must be 2*NX*2*NY*2*NZ")
                    exit()
            elif line.startswith('ACTNUM'):
                self.ACTNUM=self.ReadSection(file)
                if (len(self.ACTNUM) == self.N):
                    self.ACTNUM=np.array(self.ACTNUM, dtype=int)
                else:
                    print("[Error] ACTNUM data size must be NX*NY*NZ")
                    exit()
            elif line.startswith('PORO'):
                self.PORO=self.ReadSection(file)
                if (len(self.PORO) == self.N):
                    self.PORO=np.array(self.PORO, dtype=float)
                else:
                    print("[Error] PORO data size must be NX*NY*NZ")
                    exit()
        file.close()
    
    def WriteVTK(self, vtkUnstructuredGrid, filename=''):
        print('[Output] Writing Paraview file...')
        filename = filename.split(os.path.sep)[2]
        filename = filename.split('.')[0]
        legacyWriter = vtk.vtkUnstructuredGridWriter()
        legacyWriter.SetFileName('.'+os.path.sep+'Data'+os.path.sep+filename+'.vtk')
        legacyWriter.SetInputData(vtkUnstructuredGrid)
        legacyWriter.Write()
        print("....Done!")