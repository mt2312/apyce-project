import vtk
import vtk.util.numpy_support as numpy_support
import numpy as np

import utils

class Grid(object):
    def __init__(self, filename=''):
        self.fname = filename
        self.vtkUnstructuredGrid = vtk.vtkUnstructuredGrid()

        # Supported Keywords
        self.cartDims = []
        self.N = None
        self.COORD = []
        self.ZCORN = []
        self.ACTNUM = []
        self.PORO = []
        self.PERMX = []
        self.PERMY = []
        self.PERMZ = []

        # Unrecognized Keywords
        self.unrec = []

        # Keyword count
        self.keywordsInFile = []

    class Cell(object):
        def __init__(self, coord, cartDims):
            self.COORD = coord
            self.cartDims = cartDims

        def getCellPillars(self, i, j):
            '''
            Obtain the four pillars of the corner point cell

            PARAMETERS
                i,j - Values from grid dimension

            RETURNS
                Array with all pillars's lines from coord

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

            This method is based on buildCornerPtNodes.m (MRST)
            '''

            # Recover logical dimension of grid
            # The number of pillars are (NX+1)*(NY+1)
            nx,ny = self.cartDims[0]+1, self.cartDims[1]+1

            # Get pillar index in COORD
            # p0 - First pillar, so, the values are i,j
            # p1 - The second pillar, so, the values are i+1,j, like the example above
            # p2 - The third pillar, so, the values are i,j+1
            # p3 - The fourth pillar, so, the values are i+1,j+1
            p0_idx = utils.transform3DArrayIntoFlat3DMatrix(i,j,0,nx,ny,0)
            p1_idx = utils.transform3DArrayIntoFlat3DMatrix(i+1,j,0,nx,ny,0)
            p2_idx = utils.transform3DArrayIntoFlat3DMatrix(i,j+1,0,nx,ny,0)
            p3_idx = utils.transform3DArrayIntoFlat3DMatrix(i+1,j+1,0,nx,ny,0)

            # Get pillar line from coord
            '''
            In ECLIPSE, the COORD keyword follow the pattern below:
            1. Values are separated into a range of 6 values
            2. The row values follows the order X>Y>Z
            So, for the first COORD line, we have:
                xtop ytop ztop xbtm ybtm zbtm
            '''
            pillars=[p0_idx,p1_idx,p2_idx,p3_idx]
            pillarsCoord=[]

            for pillar in pillars:
                top=[6*pillar,6*pillar+1,6*pillar+2]
                btm=[6*pillar+3,6*pillar+4,6*pillar+5]

                topPoint=np.array([self.COORD[x] for x in top])
                btmPoint=np.array([self.COORD[x] for x in btm])

                pillarsCoord.append([topPoint,btmPoint])

            return pillarsCoord
        
        #TODO: Pegar os valores de Z
        def getCellZ(self, i, j, k):
            '''
            Get the Z coords

            PARAMETERS
                i,j,k - Values from grid dimension

            RETURNS
                Array - Zs coords for the cell
            '''
            return None
    
    #TODO: Retornar objeto?
    def processGRDECL(self, G):
        '''
        Compute grid topology and geometry from pillar grid description

        SYNOPSIS
            G = G.processGRDECL(G)

        PARAMETERS
            G - Raw pillar grid structure, as defined by function
                readGRDECL, with fields COORDS, ZCORN and, possibly,
                ACTNUM

        RETURNS
            None
        '''

        # Print process info
        utils.printProcessInfoStart()

        # Create the points for VTK structure
        self.createVTKPoints()

        # Create the cells for VTK structure
        self.createVTKCells()

        #TODO: arrumar um jeito de deixar essa inserção/atualização de dados
               # no vtk automática, caso contrário, para muitas propriedades, teremos
               # muitos "if"s sendo utilizados
        if len(self.ACTNUM == self.N):
            self.numpyToVtk('ACTNUM', self.ACTNUM)
        if len(self.PORO == self.N):
            self.numpyToVtk('PORO', self.PORO)
        if len(self.PERMX == self.N):
            self.numpyToVtk('PERMX', self.PERMX)
        if len(self.PERMY == self.N):
            self.numpyToVtk('PERMY', self.PERMY)
        if len(self.PERMZ == self.N):
            self.numpyToVtk('PERMZ', self.PERMZ)

        utils.printProcessGridInfo(self.vtkUnstructuredGrid)

    def createVTKPoints(self):
        '''
        Create the VTK points to set in vtkUnstructuredGrid

        PARAMETERS
            None
        
        RETURNS
            None

        How to create the points?
        1. Get the pillar index
            1.1 Get the pillar line from COORD
        2. Get Zs coords for the cell
            2.1 Get corner-point cell index
        3. Loop eight times for each cell
            3.1 Interpolate X,Y from Z (Here we get the coords)

        It is easier to do this cell by cell than to take all pillars, coordinates, zs at once
        '''

        # Recover logical dimension of grid
        nx,ny,nz = self.cartDims[0:3]

        points = vtk.vtkPoints()
        points.SetNumberOfPoints(8*nx*ny*nz) #2*NX*2*NY*2*NZ = len(self.ZCORN)

        # Coords of cells
        cellCoords = []

        pointIdx = 0
        for k in range(nz):
            for j in range(ny):
                for i in range(nx):
                    cellCoords = self.getCellCoords(i,j,k)
                    for x in range(8): # Set the eight points for each cell
                        points.SetPoint(pointIdx, cellCoords[x])
                        pointIdx+=1

        self.vtkUnstructuredGrid.SetPoints(points)
    
    #TODO: Criar as células VTK
    def createVTKCells(self):
        return None

    #TODO: Pegar os valores de Z para cada célula e interpolar os valores de Z com os Pilares
    def getCellCoords(self, i, j, k):
        '''
        Get XYZ coords for the eight nodes of a cell

        PARAMETERS
            i,j,k - Values from grid dimension

        RETURNS
            Array - XYZ coords for the eight nodes of a cell

        Node order convention
             6 --------- 7
            /|  btm     /|   
           / |  face   / |   
          4 --------- 5  |   
          |  |        |  |   
          |  2 -------|- 3   
          | /   top   | /    
          |/    face  |/     
          0 --------- 1
        '''

        coords = []

        # Create a cell
        cell = Grid().Cell(self.COORD, self.cartDims)
        
        # Get the four pillars for this cell
        pillars = cell.getCellPillars(i,j)

        # Get the eight values of Z
        zs = cell.getCellZ(i,j,k)

        # Get the cell coords
        for x in range(8):
            # Loop eight times - eight points for each cell
            #TODO: aqui precisa interpolar os valores de Z com os Pilares - buildCornerPtNodes.m (final)
            coords.append()

        return coords

    def numpyToVtk(self, name, numpy_data):
        '''
        Convert the numpy array to vtk array and add this array to structure grid

        PARAMETERS
            name - Name of the property e.g. ACTNUM
            numpy_data - Array with values of the property

        RETURNS
            None

        See more:
            https://pyscience.wordpress.com/2014/09/06/numpy-to-vtk-converting-your-numpy-arrays-to-vtk-arrays-and-files/
        '''
        utils.printInfoSaveData(name)
        VTK_data=numpy_support.numpy_to_vtk(num_array=numpy_data.ravel(), deep=True, array_type=vtk.VTK_FLOAT)
        VTK_data.SetName(name)
        VTK_data.SetNumberOfComponents(1)
        self.vtkUnstructuredGrid.GetCellData().AddArray(VTK_data)