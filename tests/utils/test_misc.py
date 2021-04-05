from apyce.utils import misc

import os

FILE = '../Data/dome.grdecl'
BASENAME = 'dome.grdecl'
ABSOLUTE_PATH = '/home/metzker/Desktop/Repositories/apyce-project/tests/Data/dome.grdecl'
DIRNAME = '../Data'


class TestMisc():
    def test_file_open_exception(self):
        assert misc.file_open_exception(FILE) is None

    def test_get_path(self):
        assert misc.get_path(FILE) == ABSOLUTE_PATH

    def test_get_basename(self):
        assert misc.get_basename(FILE) == BASENAME

    def test_get_dirname(self):
        assert misc.get_dirname(FILE) == DIRNAME

    def test_include_file(self):
        assert misc.get_include_file('../Data/PSY.grdecl', '\'PSY/PORO.INC\'') == '../Data/PSY/PORO.INC'

    def test_check_dim(self):
        cart_dims = [20, 20, 4]
        num_cell = 1600
        keywords = ''
        file = None
        assert misc.check_dim(cart_dims, num_cell, keywords, file) is None

    def test_check_grid(self):
        cart_dims = [20, 20, 4]
        coord = [0]
        zcorn = [0]
        assert misc.check_grid(cart_dims, coord, zcorn) is None

    def test_create_results_directory(self):
        assert misc.create_results_directory(FILE) == '../Data/Results/'
        os.removedirs('../Data/Results')

    def test_expand_scalars(self):
        assert misc.expand_scalars('3*2 2*4 5*1.2') == ['2', '2', '2', '4', '4', '1.2', '1.2', '1.2', '1.2', '1.2']
        assert misc.expand_scalars('10*0 4*1') == ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '1', '1', '1']

    def test_get_ijk(self):
        assert misc.get_ijk(0, 0, 0, 22, 74, 350) == 0
        assert misc.get_ijk(10, 20, 0, 22, 74, 350) == 450
        assert misc.get_ijk(22, 74, 350, 22, 74, 350) == 571450