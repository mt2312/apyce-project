import re
import os
import itertools

try:
    import vtk
    import vtk.util.numpy_support as numpy_support
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
        self.PERMX=[]
        self.PERMY=[]
        self.PERMZ=[]

        self.FileOpenException(self.fname)
        self.readGRDECL(self.fname)

    def readGRDECL(self, filename=''):
        '''
        Read subset of ECLIPSE GRID file
        G=Apyce(filename)

        PARAMETERS:
            filename - String holding name of GRDECL specification.

        RETURNS:
            None

        The currently recognized keywords are:

            'ACTNUM', 'COORD', 'INCLUDE', 'PERMX', 'PERMY', 'PERMZ',
            'PORO', 'ZCORN'
        '''
        print("[Input] Reading ECLIPSE file \"" + filename + "\"...")
        keywords_in_file=[]
        file=open(filename, 'r')

        for line in file:
            if line.startswith("COORDSYS"):
                continue
            elif line.startswith('SPECGRID'):
                line=file.readline()
                self.SPECGRID=np.array(re.findall('\d+', str(line)), dtype=int)
                self.NX, self.NY, self.NZ=self.SPECGRID[0:3]
                self.N = self.NX * self.NY * self.NZ
                print("\tGrid Dimension(NX,NY,NZ): {} x {} x {}".format(self.NX, self.NY, self.NZ))
                print("\tNumOfGrids: {}".format(self.N))
                keywords_in_file.append('SPECGRID')
            elif line.startswith('COORD'):
                self.COORDS=self.ReadSection(file)
                if (len(self.COORDS) == (6*(self.NX+1)*(self.NY+1))):
                    self.COORDS=np.array(self.COORDS, dtype=float)
                    keywords_in_file.append('COORD')
                else:
                    print("[Error] COORD data size must be 6*(NX+1)*(NY+1)")
                    exit()
            elif line.startswith('ZCORN'):
                self.ZCORN=self.ReadSection(file)
                if (len(self.ZCORN) == (8*self.N)):
                    self.ZCORN=np.array(self.ZCORN, dtype=float)
                    keywords_in_file.append('ZCORN')
                else:
                    print("[Error] ZCORN data size must be 2*NX*2*NY*2*NZ")
                    exit()
            elif line.startswith('ACTNUM'):
                self.ACTNUM=self.ReadSection(file)
                if (len(self.ACTNUM) == self.N):
                    self.ACTNUM=np.array(self.ACTNUM, dtype=int)
                    keywords_in_file.append('ACTNUM')
                else:
                    print("[Error] ACTNUM data size must be NX*NY*NZ")
                    exit()
            elif line.startswith('PORO'):
                self.PORO=self.ReadSection(file)
                if (len(self.PORO) == self.N):
                    self.PORO=np.array(self.PORO, dtype=float)
                    keywords_in_file.append('PORO')
                else:
                    print("[Error] PORO data size must be NX*NY*NZ")
                    exit()
            elif line.startswith('PERMX'):
                self.PERMX=self.ReadSection(file)
                if (len(self.PERMX) == self.N):
                    self.PERMX=np.array(self.PERMX, dtype=float)
                    keywords_in_file.append('PERMX')
                else:
                    print("[Error] PERMX data size must be NX*NY*NZ")
                    exit()
            elif line.startswith('PERMY'):
                self.PERMY=self.ReadSection(file)
                if (len(self.PERMY) == self.N):
                    self.PERMY=np.array(self.PERMY, dtype=float)
                    keywords_in_file.append('PERMY')
                else:
                    print("[Error] PERMY data size must be NX*NY*NZ")
                    exit()
            elif line.startswith('PERMZ'):
                self.PERMZ=self.ReadSection(file)
                if (len(self.PERMZ) == self.N):
                    self.PERMZ=np.array(self.PERMZ, dtype=float)
                    keywords_in_file.append('PERMZ')
                else:
                    print("[Error] PERMZ data size must be NX*NY*NZ")
                    exit()
            elif line.startswith('INCLUDE'):
                if not 'INCLUDE' in keywords_in_file:
                    keywords_in_file.append('INCLUDE')
                line=file.readline()
                includeFilename='.'+os.path.sep+'Data'+os.path.sep+line.split('\'')[1]
                self.ReadIncludeFile(keywords_in_file,includeFilename)
        file.close()
        print("\tKeywords:",keywords_in_file)
        print("\tNumOfKeywords:",len(keywords_in_file))
        print("....Done!")

    def processGRDECL(self):
        '''
        Compute grid topology and geometry from pillar grid description.

        G=Apyce(filename)
        G.processGRDECL()

        PARAMETERS:
            None

        RETURNS:
            None
        '''
        print("\n[Process] Converting GRDECL to VTK...")
        
        self.CreateVTKPoints()
        self.CreateVTKCells()
    
        # arrumar um jeito de deixar essa inserção/atualização de dados
        # no vtk automática, caso contrário, para muitas propriedades, teremos
        # muitos "if"s sendo utilizados
        if len(self.ACTNUM):
            self.NP2VTK('ACTNUM', self.ACTNUM)
        if len(self.PORO):
            self.NP2VTK('PORO', self.PORO)
        if len(self.PERMX):
            self.NP2VTK('PERMX', self.PERMX)
        if len(self.PERMY):
            self.NP2VTK('PERMY', self.PERMY)
        if len(self.PERMZ):
            self.NP2VTK('PERMZ', self.PERMZ)

        print("\tNumOfPoints", self.vtkUnstructuredGrid.GetNumberOfPoints())
        print("\tNumOfCells", self.vtkUnstructuredGrid.GetNumberOfCells())
        print('....Done!\n')     

    def ReadSection(self, file):
        '''
        Read the section/block of data in the ECLIPSE input file and return the values

        PARAMETERS:
            file - ECLIPSE input file

        RETURNS:
            Values of the section
        '''
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
        '''
        Expand the values of the format:
            2*3 => [3,3]

        PARAMETERS:
            line - line with the values

        RETURNS:
            Values expanded
        '''
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
        '''
        Try to open the file

        PARAMETERS:
            filename - Path to the file

        RETURNS:
            None
        '''
        try:
            file=open(filename, 'r')
            file.close()
        except IOError:
            print("Oops! Can't open the file " + filename + ". Try again...")
            exit()

    def ReadIncludeFile(self, keywords_in_file, filename=''):
        '''
        Read the include file passed in the keyword INCLUDE

        PARAMETERS:
            keywords_in_file - Just an array to save the keywords in the file
            filename - Path to the file

        RETURNS:
            None
        '''
        self.FileOpenException(filename)
        file=open(filename, 'r')
        for line in file:
            if line.startswith('COORDSYS'):
                continue
            elif line.startswith('SPECGRID'):
                line=file.readline()
                self.SPECGRID=np.array(re.findall('\d+', str(line)), dtype=int)
                self.NX, self.NY, self.NZ=self.SPECGRID[0:3]
                self.N = self.NX * self.NY * self.NZ
                print("\tGrid Dimension(NX,NY,NZ): {} x {} x {}".format(self.NX, self.NY, self.NZ))
                print("\tNumOfGrids: {}".format(self.N))
                keywords_in_file.append('SPECGRID')
            elif line.startswith('COORD'):
                self.COORDS=self.ReadSection(file)
                if (len(self.COORDS) == (6*(self.NX+1)*(self.NY+1))):
                    self.COORDS=np.array(self.COORDS, dtype=float)
                    keywords_in_file.append('COORD')
                else:
                    print("[Error] COORD data size must be 6*(NX+1)*(NY+1)")
                    exit()
            elif line.startswith('ZCORN'):
                self.ZCORN=self.ReadSection(file)
                if (len(self.ZCORN) == (8*self.N)):
                    self.ZCORN=np.array(self.ZCORN, dtype=float)
                    keywords_in_file.append('ZCORN')
                else:
                    print("[Error] ZCORN data size must be 2*NX*2*NY*2*NZ")
                    exit()
            elif line.startswith('ACTNUM'):
                self.ACTNUM=self.ReadSection(file)
                if (len(self.ACTNUM) == self.N):
                    self.ACTNUM=np.array(self.ACTNUM, dtype=int)
                    keywords_in_file.append('ACTNUM')
                else:
                    print("[Error] ACTNUM data size must be NX*NY*NZ")
                    exit()
            elif line.startswith('PORO'):
                self.PORO=self.ReadSection(file)
                if (len(self.PORO) == self.N):
                    self.PORO=np.array(self.PORO, dtype=float)
                    keywords_in_file.append('PORO')
                else:
                    print("[Error] PORO data size must be NX*NY*NZ")
                    exit()
            elif line.startswith('PERMX'):
                self.PERMX=self.ReadSection(file)
                if (len(self.PERMX) == self.N):
                    self.PERMX=np.array(self.PERMX, dtype=float)
                    keywords_in_file.append('PERMX')
                else:
                    print("[Error] PERMX data size must be NX*NY*NZ")
                    exit()
            elif line.startswith('PERMY'):
                self.PERMY=self.ReadSection(file)
                if (len(self.PERMY) == self.N):
                    self.PERMY=np.array(self.PERMY, dtype=float)
                    keywords_in_file.append('PERMY')
                else:
                    print("[Error] PERMY data size must be NX*NY*NZ")
                    exit()
            elif line.startswith('PERMZ'):
                self.PERMZ=self.ReadSection(file)
                if (len(self.PERMZ) == self.N):
                    self.PERMZ=np.array(self.PERMZ, dtype=float)
                    keywords_in_file.append('PERMZ')
                else:
                    print("[Error] PERMZ data size must be NX*NY*NZ")
                    exit()
        file.close()

    def CreateVTKCells(self):
        cell = vtk.vtkHexahedron()
        cellArray = vtk.vtkCellArray()

        ## Como criar as células?
        #1. Basta percorrer 8 vezes cada célula (alterando o "node index" da convenção GRDECL para a convenção VTK) - https://vtk.org/wp-content/uploads/2015/04/file-formats.pdf
        # GRDECL = 2 ou 6, VTK = 3 ou 7
        # GRDECL = 3 ou 7, VTK = 2 ou 6
        # para os outros casos GRDECL = VTK
        # Após isso, cell.GetPointIds().SetId(o que vem aqui??)
        # cellArray.InsertNextCell(cell)
        # OS PONTOS DEVEM SER CRIADOS ANTES DAS CÉLULAS
        
        self.vtkUnstructuredGrid.SetCells(cell.GetCellType(), cellArray)

    def CreateVTKPoints(self):
        '''
        Create the VTK points to set in vtkUnstructuredGrid

        PARAMETERS:
            None

        RETURNS:
            None

        How to create the points?
        1. Get the pillar index
            1.1 Get the pillar line from COORD
        2. Get Zs coords for the cell
            2.1 Get corner-point cell index
        3. Loop eight times for each cell
            3.1 Interpolate X,Y from Z
        '''
        points=vtk.vtkPoints()
        points.SetNumberOfPoints(8*self.NX*self.NY*self.NZ) #2*NX*2*NY*2*NZ = len(ZCORN)

        # Recover logical dimension of grid
        NX,NY,NZ=self.SPECGRID[0:3]

        # We need to interact eight times for each cell to get the eight points of each cell
        for k in range(NZ):
            for j in range(NY):
                for i in range(NX):
                    cellCoords=self.getCellCoords(i,j,k)
                    for x in range(8):
                        points.SetPoint(x,cellCoords[x])

        self.vtkUnstructuredGrid.SetPoints(points)

    def getCellCoords(self,i,j,k):
        '''
        Get de coords for eight nodes of the cell

        PARAMETERS:
            i,j,k - Values from NX,NY,NZ

        RETURNS:
            X,Y,Z - Coords of the cell
        '''
        coords=[]

        # Get the pillars
        pillars=self.getCellPillars(i,j)
        print(pillars)
        exit()
        
        return coords

    def getCellPillars(self,i,j):
        '''
        Obtain p0, p1, p2 and p3 - Pillars from one cell then
        use p0, p1, p2 and p3 to get the pillar line from COORD

        PARAMETERS:
            i,j - Values from NX, NY

        RETURNS:
            pillar line from coord - see buildCornerPtNodes.m in MRST

        In Corner-Point grid, the pillars are ordained like the follow example:

        p2    p3
        x------x
        |      |
        |      |
        x------x
        p0    p1

        In a 2D system (2x2x1), we have:

        6 --- 7 --- 8
        |  2  |  3  |
        3 --- 4 --- 5  
        |  0  |  1  |  
        0 --- 1 --- 2 

        As you can see:

        (0,1,3,4) - cell 0
        (1,2,4,5) - cell 1
        (3,4,6,7) - cell 2
        (4,5,7,8) - cell 3

        Some pillars are shared between cells
        '''
        
        # Recover logical dimension of grid
        nx,ny=self.NX+1,self.NY+1
        
        # Get pillar index in COORD
        # p0 - First pillar, so, the values are i,j
        # p1 - The second pillar, so, the values are i+1,j, like the example above
        # p2 - The third pillar, so, the values are i,j+1
        # p3 - The fourth pillar, so, the values are i+1,j+1
        p0=self.transform3DArrayIntoFlat3DMatrix(i,j,0,nx,ny,0)
        p1=self.transform3DArrayIntoFlat3DMatrix(i+1,j,0,nx,ny,0)
        p2=self.transform3DArrayIntoFlat3DMatrix(i,j+1,0,nx,ny,0)
        p3=self.transform3DArrayIntoFlat3DMatrix(i+1,j+1,0,nx,ny,0)

        # Get pillar line from coord
        '''
        In ECLIPSE, the COORD keyword follow the pattern below:
        1. Values are separated into a range of 6 values
        2. The row values follows the order X>Y>Z

        So, for the first COORD line, we have:
            xtop ytop ztop xbtm ybtm zbtm
        '''
        pillars=[p0,p1,p2,p3]
        pillarsCoord=[]

        for pillar in pillars:
            top=[6*pillar,6*pillar+1,6*pillar+2]
            btm=[6*pillar+3,6*pillar+4,6*pillar+5]

            topPoint=np.array([self.COORDS[x] for x in top])
            btmPoint=np.array([self.COORDS[x] for x in btm])

            pillarsCoord.append([topPoint,btmPoint])

        return pillarsCoord

    def transform3DArrayIntoFlat3DMatrix(self,i,j,k,NX,NY,NZ):
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

    def NP2VTK(self, name, numpy_data):
        '''
        Convert the numpy array to vtk array and add this array to structure grid

        PARAMETERS:
            name - Name of the property e.g. ACTNUM
            numpy_data - Array with values of the property

        RETURNS:
            None

        See more:
            https://pyscience.wordpress.com/2014/09/06/numpy-to-vtk-converting-your-numpy-arrays-to-vtk-arrays-and-files/
        '''
        print('\tInserting data [' + name + '] into vtk array')
        VTK_data=numpy_support.numpy_to_vtk(num_array=numpy_data.ravel(), deep=True, array_type=vtk.VTK_FLOAT)
        VTK_data.SetName(name)
        VTK_data.SetNumberOfComponents(1)
        self.vtkUnstructuredGrid.GetCellData().AddArray(VTK_data)
    
    def WriteVTK(self):
        '''
        Create a VTK file with all data of ECLIPSE file.

        G=Apyce(filename)
        G.processGRDECL()
        G.WriteVTK()

        PARAMETERS:
            None

        RETURNS:
            None
        '''
        filename=self.fname
        filename = filename.split(os.path.sep)[2]
        filename = filename.split('.')[0]
        print("[Output] Writing Paraview file \"." + os.path.sep + "Data" + os.path.sep + filename + ".vtk\"...")
        legacyWriter = vtk.vtkUnstructuredGridWriter()
        legacyWriter.SetFileName('.'+os.path.sep+'Data'+os.path.sep+filename+'.vtk')
        legacyWriter.SetInputData(self.vtkUnstructuredGrid)
        legacyWriter.Write()
        print("....Done!")