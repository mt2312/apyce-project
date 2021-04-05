from apyce.utils import Errors


class TestErrors():
    def test_errors(self):
        assert Errors.CART_DIMS_ERROR.value == "[ERROR] Attempting to change already defined grid size"
        assert Errors.DIMENS_ERROR.value == "[ERROR] Only corner-point grid are supported"
        assert Errors.COORD_ERROR.value == "[ERROR] COORD data size must be 6*(NX+1)*(NY+1)"
        assert Errors.ZCORN_ERROR.value == "[ERROR] ZCORN data size must be 2*NX*2*NY*2*NZ"
        assert Errors.PORO_ERROR.value == "[ERROR] PORO data size must be NX*NY*NZ"
        assert Errors.PERMX_ERROR.value == "[ERROR] PERMX data size must be NX*NY*NZ"
        assert Errors.PERMY_ERROR.value == "[ERROR] PERMY data size must be NX*NY*NZ"
        assert Errors.PERMZ_ERROR.value == "[ERROR] PERMZ data size must be NX*NY*NZ"
        assert Errors.ACTNUM_ERROR.value == "[ERROR] ACTNUM data size must be NX*NY*NZ"
        assert Errors.SO_ERROR.value == "[ERROR] SO data size must be NX*NY*NZ"
        assert Errors.GRID_NOT_DEFINED_ERROR.value == "[ERROR] Invoking process_grdecl before read_grdecl"
        assert Errors.CHECK_DIM_ERRROR.value == "[ERROR] GRDECL keyword {} found before dimension specification"
        assert Errors.LOAD_CELL_DATA_ERROR.value == "[ERROR] {} data size must be NX*NY*NZ"