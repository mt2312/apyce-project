import numpy as np
import vtk
import re
import os
import vtk.util.numpy_support as np_support


class Model():
    def __init__(self, fn='data.txt', grid_origin='Eclipse'):
        self._fname = fn
        self._vtk_unstructured_grid = vtk.vtkUnstructuredGrid()

        self._cart_dims = []
        self._num_cell = None
        self._coord = []
        self._zcorn = []
        self._actnum = []
        self._poro = []
        self._permx = []
        self._permy = []
        self._permz = []
        self._so = []
        self._keywords = []
        self._unrec = []
        self._n_collapsed = 0

        self._grid_origin = grid_origin
        self._model_helpers = _ModelHelpers()

        self._read_grdecl(self._fname, self._grid_origin, verbose=1)

    def __str__(self):
        structure = "\nMODEL DATA\n"
        structure += "cartDims = {}\n".format(self._cart_dims)
        structure += "numCell = {}\n".format(self._num_cell)
        structure += "keywords = {}\n".format(self._keywords)
        structure += "unrec = {}\n".format(self._unrec)
        return structure

    def _read_grdecl(self, fn, grid_origin, verbose):
        '''
        Read subset of ECLIPSE/BUILDER GRID file

        The currently recognized keywords of ECLIPSE are:
            'COORD', 'DIMENS/SPECGRID', 'INCLUDE', 'PERMX', 'PERMY',
            'PERMZ', 'PORO', 'ZCORN', 'SO'
        and, we have a partial support for:
            'ACTNUM'

        The currently recognized keywords of BUILDER are:
            'Porosity'

        Parameters
        ----------
        fn : str
            String holding name of GRDECL specification

        Returns
        -------
        This method does not return anything, just modify attributes of the class
        '''
        self._model_helpers.file_open_exception(fn)

        if grid_origin == 'Builder':
            self._model_helpers.parse_file(fn)

        if verbose == 1:
            print("[INPUT] Reading input ECLIPSE/BUILDER file...\n")

        with open(fn) as f:
            for line in f:
                # Keyword pattern
                kw = re.match('^[A-Z][A-Z0-9]{0,7}(|/)', str(line))

                if kw != None:
                    if kw.group() == 'SPECGRID':
                        print("[+] Reading keyword {}".format(kw.group()))
                        if kw.group() not in self._keywords:
                            self._keywords.append(kw.group())
                        line = f.readline().strip()
                        self._cart_dims = np.array(
                            re.findall('\d+', str(line))[0:3], dtype=int)
                        self._num_cell = np.prod(self._cart_dims)
                    elif kw.group() == 'DIMENS':
                        print("[ERROR] Only corner-point grid are supported")
                        exit()
                    elif kw.group() == 'INCLUDE':
                        print("[+] Reading keyword {}".format(kw.group()))
                        if kw.group() not in self._keywords:
                            self._keywords.append(kw.group())
                        line = f.readline()
                        inc_fn = '.' + os.path.sep + "Data" + \
                            os.path.sep + line.split('\'')[1]
                        print("\t--> {}".format(line.split('\'')[1]))
                        self._read_grdecl(inc_fn, grid_origin, 0)
                        print("\t<-- {}".format(line.split('\'')[1]))
                    elif kw.group() == 'COORD':
                        self._model_helpers.check_dim(
                            self._cart_dims, self._num_cell, kw.group(), f)
                        print("[+] Reading keyword {}".format(kw.group()))
                        self._coord = self._model_helpers.read_section(f)
                        if len(self._coord) == 6*(self._cart_dims[0]+1)*(self._cart_dims[1]+1):
                            if kw.group() not in self._keywords:
                                self._keywords.append(kw.group())
                            self._coord = np.array(self._coord, dtype=float)
                        else:
                            print(
                                "[ERROR] COORD data size must be 6*(NX+1)*(NY+1)")
                            exit()
                    elif kw.group() == 'ZCORN':
                        self._model_helpers.check_dim(
                            self._cart_dims, self._num_cell, kw.group(), f)
                        print("[+] Reading keyword {}".format(kw.group()))
                        self._zcorn = self._model_helpers.read_section(f)
                        if len(self._zcorn) == 8*self._num_cell:
                            if kw.group() not in self._keywords:
                                self._keywords.append(kw.group())
                            self._zcorn = np.array(self._zcorn, dtype=float)
                        else:
                            print(
                                "[ERROR] ZCORN data size must be 2*NX*2*NY*2*NZ")
                            exit()
                    elif kw.group() == 'PORO':
                        self._model_helpers.check_dim(
                            self._cart_dims, self._num_cell, kw.group(), f)
                        print("[+] Reading keyword {}".format(kw.group()))
                        self._poro = self._model_helpers.read_section(f)
                        if len(self._poro) == self._num_cell:
                            if kw.group() not in self._keywords:
                                self._keywords.append(kw.group())
                            self._poro = np.array(self._poro, dtype=float)
                        else:
                            print("[ERROR] PORO data size must be NX*NY*NZ")
                            exit()
                    elif kw.group() == 'PERMX':
                        self._model_helpers.check_dim(
                            self._cart_dims, self._num_cell, kw.group(), f)
                        print("[+] Reading keyword {}".format(kw.group()))
                        self._permx = self._model_helpers.read_section(f)
                        if len(self._permx) == self._num_cell:
                            if kw.group() not in self._keywords:
                                self._keywords.append(kw.group())
                            self._permx = np.array(self._permx, dtype=float)
                        else:
                            print("[ERROR] PERMX data size must be NX*NY*NZ")
                            exit()
                    elif kw.group() == 'PERMY':
                        self._model_helpers.check_dim(
                            self._cart_dims, self._num_cell, kw.group(), f)
                        print("[+] Reading keyword {}".format(kw.group()))
                        self._permy = self._model_helpers.read_section(f)
                        if len(self._permy) == self._num_cell:
                            if kw.group() not in self._keywords:
                                self._keywords.append(kw.group())
                            self._permy = np.array(self._permy, dtype=float)
                        else:
                            print("[ERROR] PERMY data size must be NX*NY*NZ")
                            exit()
                    elif kw.group() == 'PERMZ':
                        self._model_helpers.check_dim(
                            self._cart_dims, self._num_cell, kw.group(), f)
                        print("[+] Reading keyword {}".format(kw.group()))
                        self._permz = self._model_helpers.read_section(f)
                        if len(self._permz) == self._num_cell:
                            if kw.group() not in self._keywords:
                                self._keywords.append(kw.group())
                            self._permz = np.array(self._permz, dtype=float)
                        else:
                            print("[ERROR] PERMZ data size must be NX*NY*NZ")
                            exit()
                    elif kw.group() == 'ACTNUM':
                        self._model_helpers.check_dim(
                            self._cart_dims, self._num_cell, kw.group(), f)
                        print("[+] Reading keyword {}".format(kw.group()))
                        self._actnum = self._model_helpers.read_section(f)
                        if len(self._actnum) == self._num_cell:
                            if kw.group() not in self._keywords:
                                self._keywords.append(kw.group())
                            self._actnum = np.array(self._actnum, dtype=int)
                        else:
                            print("[ERROR] ACTNUM data size must be NX*NY*NZ")
                            exit()
                    elif kw.group() == 'SO':
                        self._model_helpers.check_dim(
                            self._cart_dims, self._num_cell, kw.group(), f)
                        print("[+] Reading keyword {}".format(kw.group()))
                        self._so = self._model_helpers.read_section(f)
                        if len(self._so) == self._num_cell:
                            if kw.group() not in self._keywords:
                                self._keywords.append(kw.group())
                            self._so = np.array(self._so, dtype=float)
                        else:
                            print("[ERROR] SO data size must be NX*NY*NZ")
                            exit()

                    elif kw.group() not in self._unrec:
                        print(
                            "[+] Unrecognized keyword found {}".format(kw.group()))
                        self._unrec.append(kw.group())

    def process_grdecl(self):
        '''
        Compute grid topology and geometry from pillar grid description

        Parameters
        ----------
        This method does not have parameters

        Returns
        -------
        This method does not return anything
        '''
        print("\n[PROCESS] Converting GRDECL grid to Paraview VTK format...")

        points = vtk.vtkPoints()
        points.SetNumberOfPoints(8*np.prod(self._cart_dims))  # 2*NX*2*NY*2*NZ

        # Recover logical dimension of grid
        nx, ny, nz = self._cart_dims[0:3]

        print("\n[+] Creating VTK Points...")

        point_id = 0
        for k in range(nz):
            for j in range(ny):
                for i in range(nx):
                    # Get the cell coords
                    coords = self._get_cell_coords(i, j, k)
                    # Set the points for the cell
                    for x in range(8):
                        points.SetPoint(point_id, coords[x])
                        point_id += 1
        self._vtk_unstructured_grid.SetPoints(points)

        print(
            "\t[+] Detected {} collapsed pillars.".format(self._n_collapsed))

        if "ACTNUM" in self._keywords:
            _active_cells = [x for x in self._actnum if x == 1]
            _inactive_cells = len(self._actnum) - len(_active_cells)
            print("\t[+] Detected {} active cells and {} inactive cells.".format(
                len(_active_cells), _inactive_cells))

        print("\n[+] Creating VTK Cells...")

        '''
        The VTK indexes elements differently than ECLIPSE.
            Therefore, we must convert indexes from ECLIPSE to VTK before creating the cells.

        ECLIPSE:
           6 --------- 7
          /|          /|
         / |         / |
        4 --------- 5  |
        |  |        |  |
        |  2 -------|- 3
        | /         | /
        |/          |/
        0 --------- 1

        VTK:
           7 --------- 6
          /|          /|
         / |         / |
        4 --------- 5  |
        |  |        |  |
        |  3 -------|- 2
        | /         | /
        |/          |/
        0 --------- 1

        As we can see, the VTK indexes 2, 3, 6, and 7 are different from Eclipse.

        See more:
            https://vtk.org/wp-content/uploads/2015/04/file-formats.pdf (page 9 - VTK_HEXAHEDRON)
        '''
        cell_id = 0
        for k in range(nz):
            for j in range(ny):
                for i in range(nx):
                    cell = vtk.vtkHexahedron()

                    cell.GetPointIds().SetId(0, cell_id*8+0)
                    cell.GetPointIds().SetId(1, cell_id*8+1)
                    cell.GetPointIds().SetId(2, cell_id*8+3)
                    cell.GetPointIds().SetId(3, cell_id*8+2)
                    cell.GetPointIds().SetId(4, cell_id*8+4)
                    cell.GetPointIds().SetId(5, cell_id*8+5)
                    cell.GetPointIds().SetId(6, cell_id*8+7)
                    cell.GetPointIds().SetId(7, cell_id*8+6)

                    self._vtk_unstructured_grid.InsertNextCell(
                        cell.GetCellType(), cell.GetPointIds())

                    cell_id += 1

        # Set the properties to the vtk array
        self._update()

    def _get_cell_coords(self, i, j, k):
        '''
        Get XYZ coords for each node of a cell

        Parameters
        ----------
        i, j, k : int
            Values from grid dimension

        Returns
        -------
        coords : float array
            XYZ coords for each node of a cell (eight nodes for cell)

        In corner-point grid, the nodes are ordained like the follow example:

        n6    n7
        x------x
        |      |
        |      | This is the bottom face
        x------x
        n4    n5

        n2    n3
        x------x
        |      |
        |      | This is the top face
        x------x
        n0    n1

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
        coord = []

        # Get pillars for this cell
        pillars = self._get_pillars(i, j)

        # Get the Zs for this cell (The depth of the nodes)
        zs = self._get_zs(i, j, k)

        # Loop eight times for each cell (eight corners)
        for x in range(8):
            '''
            Recover physical nodal coordinates along pillars

            We assume that all pillars are straight lines so linear interpolation is sufficient.
            As a special case we need to handle "collapsed" pillars of the form

            x0 y0 z0   x0 y0 z0

            where the top pillar point coincides with the bottom pillar point. (degenerated cell)
            Following ECLIPSE, we assume that such pillars are really vertical...

            In MRST:
            ix    = abs(lines(:,6) - lines(:,3)) < abs(opt.CoincidenceTolerance);
            t     = (grdecl.ZCORN(:) - lines(:,3)) ./ (lines(:,6) - lines(:,3));
            t(ix) = 0;

            xCoords = lines(:,1) + t.*(lines(:,4) - lines(:,1));
            yCoords = lines(:,2) + t.*(lines(:,5) - lines(:,2));

            In APyCE:
            MRST performs this process only once, this is because the array [lines]
            already contain all the necessary coordinates, here in APyCE, 
            we will do the process cell by cell.

            Top_points
            pillar[0][0] = 608.14319 = lines(1,1);
            pillar[0][1] = -1219.582 = lines(1,2);
            pillar[0][2] = 2249.7217 = lines(1,3);

            Btm_points
            pillar[1][0] = 598.95313 = lines(1,4);
            pillar[1][1] = -1241.7069 = lines(1,5);
            pillar[1][2] = 2499.0918 = lines(1,6);
            '''
            # p_idx -> [0,3]
            p_idx = x % 4

            # Absolute tolerance used to detect collapsed pillars where the top
            # pillar point coincides with the bottom pillar point
            COINCIDENCE_TOLERANCE = 2.2204e-14

            pillar = pillars[p_idx]
            z_coord = zs[x]

            # degenerated cell condition
            if abs(pillar[1][2] - pillar[0][2]) < COINCIDENCE_TOLERANCE:
                self._n_collapsed += 1
                t = 0.0
            else:
                t = (z_coord - pillar[0][2]) / (pillar[1][2] - pillar[0][2])

            x_coord = pillar[0][0] + t * (pillar[1][0] - pillar[0][0])
            y_coord = pillar[0][1] + t * (pillar[1][1] - pillar[0][1])

            coord.append(np.array([x_coord, y_coord, z_coord]))

        return coord

    def _get_pillars(self, i, j):
        '''
        Obtain the pillars index in [COORD] and the pillars coord for each cell

        Parameters
        ----------
        i, j : int
            Values from grid dimension

        Returns
        -------
        pillars : float array
            Array with the pillars coord

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
        pillars = []

        # Recover logical dimension of grid
        # There are (nx+1)*(ny+1) pillars lines
        nx, ny = self._cart_dims[0]+1, self._cart_dims[1]+1

        # Get the pillar index in [COORD]
        p0 = self._model_helpers.to_1D(i, j, 0, nx, ny, 0)
        p1 = self._model_helpers.to_1D(i+1, j, 0, nx, ny, 0)
        p2 = self._model_helpers.to_1D(i, j+1, 0, nx, ny, 0)
        p3 = self._model_helpers.to_1D(i+1, j+1, 0, nx, ny, 0)

        # Get the pillar from [COORD]
        '''
        In ECLIPSE, the [COORD] keyword follow the pattern below:
        1. A coordinate line (pillar) is specified by two triplets of
            X, Y, and Z coordinates, representing two distinct points on it

        So, we have:
            COORD
            xtop ytop ztop xbtm ybtm zbtm
            xtop ytop ztop xbtm ybtm zbtm
            xtop ytop ztop xbtm ybtm zbtm
            .
            .
            .
            xtop ytop ztop xbtm ybtm zbtm
        '''
        # Create an array with the four pillars' index
        pillars_idx = [p0, p1, p2, p3]

        for pillar_idx in pillars_idx:
            top_idx = [6*pillar_idx, 6*pillar_idx+1, 6*pillar_idx+2]
            btm_idx = [6*pillar_idx+3, 6*pillar_idx+4, 6*pillar_idx+5]

            top_points = np.array([self._coord[x] for x in top_idx])
            btm_points = np.array([self._coord[x] for x in btm_idx])

            pillars.append([top_points, btm_points])

        return pillars

    def _get_zs(self, i, j, k):
        '''
        Get the Z index in ZCORN and Z coords for a cell, each cell have eight Zs (depth of nodes)

        Parameters
        ----------
        i, j, k : int
            Values from grid dimension

        Returns
        -------
        Zs : float array
            Array with the eight Zs coords for this cell

        The depths of the corner points of each cell are specified with 2*NX * 2*NY * 2*NZ values.
            First the two corners in the i-direction of the first grid cell is given,
            then the two corner of the next grid block in the i-direction etc.
            The unit of the values is metres, and the depth values are positive with increasing values downwards.
        '''
        # Recover logical dimension of grid (*2 because we have 8*nx*ny*nz values from [ZCORN])
        nx, ny, nz = 2*self._cart_dims[0], 2 * \
            self._cart_dims[1], 2*self._cart_dims[2]

        # Zs from top layer
        z0 = self._model_helpers.to_1D(2*i, 2*j, 2*k, nx, ny, nz)
        z1 = self._model_helpers.to_1D(2*i+1, 2*j, 2*k, nx, ny, nz)
        z2 = self._model_helpers.to_1D(2*i, 2*j+1, 2*k, nx, ny, nz)
        z3 = self._model_helpers.to_1D(2*i+1, 2*j+1, 2*k, nx, ny, nz)

        # Zs from bottom layer
        z4 = self._model_helpers.to_1D(2*i, 2*j, 2*k+1, nx, ny, nz)
        z5 = self._model_helpers.to_1D(2*i+1, 2*j, 2*k+1, nx, ny, nz)
        z6 = self._model_helpers.to_1D(2*i, 2*j+1, 2*k+1, nx, ny, nz)
        z7 = self._model_helpers.to_1D(2*i+1, 2*j+1, 2*k+1, nx, ny, nz)

        # Create an array with the eight zs' index
        zs_idx = [z0, z1, z2, z3, z4, z5, z6, z7]

        return [self._zcorn[x] for x in zs_idx]

    def load_cell_data(self, fn, name):
        '''
        Read a file with data and append this data to model

        Parameters
        ----------
        fn : str
            String holding the name of the data file
        name : str
            String holding the name of the property

        Returns
        -------
        This method does not return anything, just modify attributes of the class

        Assuming that the data to be loaded is a reservoir
            property that has a value for each cell, we must have NX * NY * NZ values
        '''
        self._model_helpers.file_open_exception(fn)
        data_array = []
        with open(fn) as f:
            f.readline()  # skip keyword
            self._model_helpers.check_dim(
                self._cart_dims, self._num_cell, name, f)
            data_array = self._model_helpers.read_section(f)
            if len(data_array) == self._num_cell:
                data_array = np.array(data_array, dtype=float)
                if name not in self._keywords:
                    self._keywords.append(name)
            else:
                print("[ERROR] " + name + " data size must be NX*NY*NZ")
                exit()
        self._update(data_array, name)

    def write_vtk(self):
        '''
        Create a VTK file with all data of ECLIPSE/BUILDER file.

        Parameters
        ----------
        This method does not have parameters

        Returns
        -------
        This method does not return anything, just create the VTK file
        '''
        fn = self._fname
        fn = fn.split(os.path.sep)[2]
        fn = fn.split('.')[0]
        print("\n[OUTPUT] Writing Paraview file \"." + os.path.sep +
              "Data" + os.path.sep + "Results" + os.path.sep + fn + ".vtk\"...")
        if not os.path.exists('./Data/Results'):
            os.makedirs('.'+os.path.sep+'Data'+os.path.sep+'Results')
        legacyWriter = vtk.vtkUnstructuredGridWriter()
        legacyWriter.SetFileName(
            '.'+os.path.sep+'Data'+os.path.sep+"Results"+os.path.sep+fn+'.vtk')
        legacyWriter.SetInputData(self._vtk_unstructured_grid)
        legacyWriter.Write()

    def _update(self, data_array=[], name='property'):
        '''
        This method update the data in the vtkUnsctructuredGrid.

        Parameters (Optional)
        ----------
        data_array : NumPy array (dtype=int or dtype=float)
            NumPy array holding the data of load_cell_data()
        name : str
            String holding the name of the property

        Returns
        -------
        This method does not return anything
        '''
        if len(self._actnum) != 0:
            self._model_helpers.np_to_vtk(
                'ACTNUM', self._actnum, self._vtk_unstructured_grid)
        if len(self._permx) != 0:
            self._model_helpers.np_to_vtk(
                'PERMX', self._permx, self._vtk_unstructured_grid)
        if len(self._permy) != 0:
            self._model_helpers.np_to_vtk(
                'PERMY', self._permy, self._vtk_unstructured_grid)
        if len(self._permz) != 0:
            self._model_helpers.np_to_vtk(
                'PERMZ', self._permz, self._vtk_unstructured_grid)
        if len(self._poro) != 0:
            self._model_helpers.np_to_vtk(
                'PORO', self._poro, self._vtk_unstructured_grid)
        if len(self._so) != 0:
            self._model_helpers.np_to_vtk(
                'SO', self._so, self._vtk_unstructured_grid)
        if len(data_array) != 0:
            self._model_helpers.np_to_vtk(
                name.upper(), data_array, self._vtk_unstructured_grid)


class _ModelHelpers():
    def read_section(self, file):
        '''
        Read the section of data in the ECLIPSE/BUILDER input file
        and return the array of values

        Parameters
        ----------
        file : file
            ECLIPSE/BUILDER input file

        Returns
        -------
        section
            Array with values of the section
        '''
        section = []
        while True:
            line = file.readline()
            if line.startswith('--') or not line.strip():
                # Ignore blank lines and comments
                continue
            values = self.exapand_scalars(line)
            section.extend(values)
            if section[-1] == '/':
                section.pop()
                break
        return section

    def check_dim(self, cart_dims, num_cell, kw, file):
        '''
        Check dimension of the grid

        Parameters
        ----------
        cart_dims : NumPy array (dtype=int)
            Dimensions of the grid
        num_cell : int
            Number of cells in the grid
        kw : str
            Keyword currently being read
        file : file
            Opened file with GRDECL specification

        Returns
        -------
        This method does not return anything
        '''
        if len(cart_dims) == 0 or num_cell == None or any(cart_dims < 1):
            print(
                "[ERROR] GRDECL keyword {} found before dimension specification".format(kw))
            file.close()
            exit()

    def to_1D(self, i, j, k, nx, ny, nz):
        '''
        Convert index [HEIGHT, WIDTH, DEPTH] to a flat 3D matrix index [HEIGHT * WIDTH * DEPTH]

        If you have:
            Original[HEIGHT, WIDTH, DEPTH]

        then you could turn it into:
            Flat[HEIGHT * WIDTH * DEPTH] by

        Flat[x + WIDTH * (y + DEPTH * z)] = Original[x, y, z]

        See more:
        https://stackoverflow.com/questions/7367770/how-to-flatten-or-index-3d-array-in-1d-array/7367812
        '''
        return ((k * nx * ny) + (j * nx) + i)

    def np_to_vtk(self, name, numpy_data, vtk_unstructured_grid):
        '''
        Convert the numpy array to vtk array and add this array to structure grid

        Parameters
        ----------
        name : str
            Name of the property e.g. ACTNUM
        numpy_data : NumPy array (dtype=int or dtype=float)
            Array with values of the property

        Returns
        -------
        This method does not return anything

        See more:
            https://pyscience.wordpress.com/2014/09/06/numpy-to-vtk-converting-your-numpy-arrays-to-vtk-arrays-and-files/
        '''
        print('\tInserting data [' + name + '] into vtk array')
        vtk_data = np_support.numpy_to_vtk(
            num_array=numpy_data.ravel(), deep=True, array_type=vtk.VTK_FLOAT)
        vtk_data.SetName(name)
        vtk_data.SetNumberOfComponents(1)
        vtk_unstructured_grid.GetCellData().AddArray(vtk_data)

    def exapand_scalars(self, line):
        '''
        Expand the values of the format:
            2*3 => [3,3]

        Parameters
        ----------
        line : str
            line with the values

        Returns
        -------
        values : int[] or float[]
            Values expanded
        '''
        values = []
        for scalar in line.split():
            if not '*' in scalar:
                values.append(scalar)
            else:
                tmp = scalar.split('*')
                tmp = [tmp[1]] * int(tmp[0])
                values.extend(tmp)
        return values

    def file_open_exception(self, fn=''):
        '''
        Try to open the file

        Parameters
        ----------
        fn : str
            String holding name of GRDECL specification.

        Returns
        -------
        This method does not return anything
        '''
        try:
            file = open(fn, 'r')
            file.close()
        except IOError:
            print("[ERROR] Can't open the file.")
            exit()

    def parse_file(self, fn):
        '''
        Parse BUILDER files and put him in ECLIPSE format.

        Parameters
        ----------
        fn : str
            String holding name of GRDECL specification.

        Returns
        -------
        This method does not return anything, 
            but creates a new file named "fn_parsed.txt", 
            and rename the file "fn" to "fn_BuilderFile.bak"
        '''
        self.file_open_exception(fn)

        with open(fn) as f:
            for line in f:
                if line.startswith('\'Porosity'):
                    print("[+] Reading keyword Porosity")
                    new_file = open(fn+'_parsed.txt', 'w')
                    new_file.write('PORO\n')
                    while True:
                        line = f.readline()
                        new_file.write(line)
                        if not line.strip():
                            new_file.write('/')
                            break
                    new_file.close()
                    os.rename(fn, fn+'_BuilderFile.bak')
                    os.rename(fn+'_parsed.txt', fn)
                    break
