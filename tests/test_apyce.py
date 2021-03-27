import pytest
import os
import vtk

from src.APyCE import Model


class TestModel():
    def test_str(self):
        grid_file = 'Data/dome.grdecl'
        test_dir = os.path.dirname(__file__)
        grid_file_path = os.path.abspath(os.path.join(test_dir, grid_file))
        G = Model(fn=grid_file_path, verbose=False)
        assert str(G) == '\nMODEL DATA\ncartDims = [20 20  4]\nnumCell = 1600\nkeywords = [\'SPECGRID\', \'COORD\', \'ZCORN\', \'PORO\', \'PERMX\', \'PERMY\', \'PERMZ\']\nunrec = [\'NOECHO\', \'PINCH\', \'MAPUNITS\', \'MAPAXES\', \'GRIDUNIT\', \'ECHO\']\n'

    def test_read_grdecl(self):
        grid_file = 'Data/dome.grdecl'
        test_dir = os.path.dirname(__file__)
        grid_file_path = os.path.abspath(os.path.join(test_dir, grid_file))
        G = Model(fn=grid_file_path, verbose=False)
        assert isinstance(G, Model)
        assert G._num_cell == 1600

    def test_process_grdecl(self):
        grid_file = 'Data/dome.grdecl'
        test_dir = os.path.dirname(__file__)
        grid_file_path = os.path.abspath(os.path.join(test_dir, grid_file))
        G = Model(fn=grid_file_path, verbose=False)
        G.process_grdecl()
        assert isinstance(G, Model)
        assert G._n_collapsed == 544

    '''
    def test_process_dat(self):
        return NULL
    '''

    def test_load_cell_data(self):
        grid_file = 'Data/dome.grdecl'
        test_dir = os.path.dirname(__file__)
        grid_file_path = os.path.abspath(os.path.join(test_dir, grid_file))
        G = Model(fn=grid_file_path, verbose=False)
        load_file = 'Data/dome_Temperature.txt'
        load_file_path = os.path.abspath(os.path.join(test_dir, load_file))
        G.load_cell_data(load_file_path, 'TEMP')
        assert 'TEMP' in G._keywords

    def test_write_vtk(self):
        grid_file = 'Data/dome.grdecl'
        test_dir = os.path.dirname(__file__)
        vtk_dir = os.path.dirname('Data/Results/')
        grid_file_path = os.path.abspath(os.path.join(test_dir, grid_file))
        G = Model(fn=grid_file_path, verbose=False)
        G.process_grdecl()
        G.write_vtk()
        vtk_file_path = os.path.abspath(os.path.join(vtk_dir))
        assert os.stat(os.path.normpath(vtk_file_path+'/dome.vtu')).st_size == 133670
        os.remove(os.path.normpath(vtk_file_path+'/dome.vtu'))
        os.rmdir(os.path.normpath(vtk_file_path))
        
    def test_update(self):
        grid_file = 'Data/dome.grdecl'
        test_dir = os.path.dirname(__file__)
        grid_file_path = os.path.abspath(os.path.join(test_dir, grid_file))
        G = Model(fn=grid_file_path, verbose=False)
        G._update()
        assert G._vtk_unstructured_grid.GetCellData().GetArray('PORO').GetSize() == 1600
        assert G._vtk_unstructured_grid.GetCellData().GetArray('PERMX').GetMaxId() == 1599
        assert G._vtk_unstructured_grid.GetCellData().GetArray('PERMY').GetSize() == 1600
        assert G._vtk_unstructured_grid.GetCellData().GetArray('PERMZ').GetSize() == 1600

    def test_check_dim(self):
        grid_file = 'Data/dome.grdecl'
        test_dir = os.path.dirname(__file__)
        grid_file_path = os.path.abspath(os.path.join(test_dir, grid_file))
        G = Model(fn=grid_file_path, verbose=False)
        f = open(grid_file_path)
        G._model_helpers.check_dim(G._cart_dims, G._num_cell, 'KEYWORD', f)

    def test_to_1D(self):
        grid_file = 'Data/dome.grdecl'
        test_dir = os.path.dirname(__file__)
        grid_file_path = os.path.abspath(os.path.join(test_dir, grid_file))
        G = Model(fn=grid_file_path, verbose=False)
        assert G._model_helpers.to_1D(0, 0, 0, 22, 74, 350) == 0
        assert G._model_helpers.to_1D(10, 20, 0, 22, 74, 350) == 450
        assert G._model_helpers.to_1D(22, 74, 350, 22, 74, 350) == 571450


    def test_np_to_vtk(self):
        grid_file = 'Data/dome.grdecl'
        test_dir = os.path.dirname(__file__)
        grid_file_path = os.path.abspath(os.path.join(test_dir, grid_file))
        G = Model(fn=grid_file_path, verbose=False)
        G._model_helpers.np_to_vtk('PORO', G._poro, G._vtk_unstructured_grid, verbose=False)
        assert G._vtk_unstructured_grid.GetCellData().GetArray('PORO').GetSize() == 1600

    def test_expand_scalars(self):
        grid_file = 'Data/dome.grdecl'
        test_dir = os.path.dirname(__file__)
        grid_file_path = os.path.abspath(os.path.join(test_dir, grid_file))
        G = Model(fn=grid_file_path, verbose=False)
        assert G._model_helpers.exapand_scalars('2*3 1 2 3 04 9 3 3*2.12312') == ['3', '3', '1', '2', '3', '04', '9', '3', '2.12312', '2.12312', '2.12312']

    def test_file_open_exception(self):
        grid_file = 'Data/dome.grdecl'
        test_dir = os.path.dirname(__file__)
        grid_file_path = os.path.abspath(os.path.join(test_dir, grid_file))
        G = Model(fn=grid_file_path, verbose=False)
        G._model_helpers.file_open_exception()
