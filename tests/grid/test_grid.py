from apyce.grid import Grid

import os

FILE = '../Data/dome.grdecl'
BASENAME = 'dome.grdecl'
ABSOLUTE_PATH = '/home/metzker/Desktop/Repositories/apyce-project/tests/Data/dome.grdecl'
DIRNAME = '../Data'

class TestGrid():
    def test_constructor(self):
        G = Grid(filename=FILE, grid_origin='eclipse', verbose=False)
        assert isinstance(G, Grid)

    def test_process_grid(self):
        G = Grid(filename=FILE, grid_origin='eclipse', verbose=False)
        G.process_grid()
        assert isinstance(G, Grid)
        assert G._n_collapsed == 544

    def test_load_cell_data(self):
        G = Grid(filename=FILE, grid_origin='eclipse', verbose=False)
        G.process_grid()
        G.load_cell_data(filename='../Data/dome_Temperature.txt', name='TEMP')
        assert 'TEMP' in G._keywords
        assert G._vtk_unstructured_grid.GetCellData().GetArray('TEMP').GetSize() == 1600

    def test_export_data(self):
        G = Grid(filename=FILE, grid_origin='eclipse', verbose=False)
        G.process_grid()
        assert G.export_data() is None
        os.remove(DIRNAME + '/Results/dome.vtu')
        os.removedirs(DIRNAME + '/Results')