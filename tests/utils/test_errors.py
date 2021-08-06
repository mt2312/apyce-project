from apyce.utils import Errors


class TestErrors():
    def test_errors(self):
        assert Errors.CART_DIMS_ERROR.value == "Attempting to change already defined grid size"
        assert Errors.COORD_ERROR.value == "COORD data size must be 6*(NX+1)*(NY+1)"
        assert Errors.ZCORN_ERROR.value == "ZCORN data size must be 2*NX*2*NY*2*NZ"
        assert Errors.PORO_ERROR.value == "PORO data size must be NX*NY*NZ"
        assert Errors.PERMX_ERROR.value == "PERMX data size must be NX*NY*NZ"
        assert Errors.PERMY_ERROR.value == "PERMY data size must be NX*NY*NZ"
        assert Errors.PERMZ_ERROR.value == "PERMZ data size must be NX*NY*NZ"
        assert Errors.ACTNUM_ERROR.value == "ACTNUM data size must be NX*NY*NZ"
        assert Errors.SO_ERROR.value == "SO data size must be NX*NY*NZ"
        assert Errors.GRID_NOT_DEFINED_ERROR.value == "The grid is not defined!"
        assert Errors.CHECK_DIM_ERRROR.value == "GRDECL keyword {} found before dimension specification"
        assert Errors.LOAD_CELL_DATA_ERROR.value == "{} data size must be NX*NY*NZ"
        assert Errors.TOPS_ERROR.value == "TOPS data size must be NX*NY"
        assert Errors.DX_ERROR.value == "DX data size must be NX*NY*NZ"
        assert Errors.DY_ERROR.value == "DY data size must be NX*NY*NZ"
        assert Errors.DZ_ERROR.value == "DZ data size must be NX*NY*NZ"
        assert Errors.FILE_NOT_FOUND_ERROR.value == "Can't open the file {}"
        assert Errors.EOF_ERROR.value == "EOF when reading a line"