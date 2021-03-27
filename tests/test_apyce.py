import pytest
import os

from src.APyCE import Model


class TestModel():
    def test_str(self):
        grid_file = 'Data/dome.grdecl'
        test_dir = os.path.dirname(__file__)
        grid_file_path = os.path.abspath(os.path.join(test_dir, grid_file))
        G = Model(fn=grid_file_path, verbose=0)
        assert str(
            G) == '\nMODEL DATA\ncartDims = [20 20  4]\nnumCell = 1600\nkeywords = [\'SPECGRID\', \'COORD\', \'ZCORN\', \'PORO\', \'PERMX\', \'PERMY\', \'PERMZ\']\nunrec = [\'NOECHO\', \'PINCH\', \'MAPUNITS\', \'MAPAXES\', \'GRIDUNIT\', \'ECHO\']\n'

    def test_read_grdecl(self):
        grid_file = 'Data/dome.grdecl'
        test_dir = os.path.dirname(__file__)
        grid_file_path = os.path.abspath(os.path.join(test_dir, grid_file))
        G = Model(fn=grid_file_path, verbose=0)
        assert isinstance(G, Model)
        assert G._num_cell == 1600

    def test_process_grdecl(self):
        grid_file = 'Data/dome.grdecl'
        test_dir = os.path.dirname(__file__)
        grid_file_path = os.path.abspath(os.path.join(test_dir, grid_file))
        G = Model(fn=grid_file_path, verbose=0)
        G.process_grdecl()
        assert isinstance(G, Model)
        assert G._n_collapsed == 544

    def test_load_cell_data(self):
        grid_file = 'Data/dome.grdecl'
        test_dir = os.path.dirname(__file__)
        grid_file_path = os.path.abspath(os.path.join(test_dir, grid_file))
        G = Model(fn=grid_file_path, verbose=0)
        load_file = 'Data/dome_Temperature.txt'
        load_file_path = os.path.abspath(os.path.join(test_dir, load_file))
        G.load_cell_data(load_file_path, 'TEMP')
        assert 'TEMP' in G._keywords

    # @TODO: Continue from here
    def test_write_vtk(self):
        grid_file = 'Data/dome.grdecl'
        test_dir = os.path.dirname(__file__)
        vtk_dir = os.path.dirname('Data/Results/')
        grid_file_path = os.path.abspath(os.path.join(test_dir, grid_file))
        G = Model(fn=grid_file_path, verbose=0)
        G.process_grdecl()
        G.write_vtk()
        vtk_file_path = os.path.abspath(os.path.join(vtk_dir))
        assert os.stat(vtk_file_path).st_size() == 448125


'''
    def test_update(self):
        return NULL

    def test_read_section(self):
        return NULL

    def test_check_dim(self):
        return NULL

    def test_to_1D(self):
        return NULL

    def test_np_to_vtk(self):
        return NULL

    def test_expand_scalars(self):
        return NULL

    def test_file_open_exception(self):
        return NULL

    def test_parse_file(self):
        return NULL
'''
