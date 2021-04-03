from enum import Enum

class Errors(Enum):
    CART_DIMS_ERROR = "[ERROR] Attempting to change already defined grid size"
    DIMENS_ERROR = "[ERROR] Only corner-point grid are supported"
    COORD_ERROR = "[ERROR] COORD data size must be 6*(NX+1)*(NY+1)"
    ZCORN_ERROR = "[ERROR] ZCORN data size must be 2*NX*2*NY*2*NZ"
    PORO_ERROR = "[ERROR] PORO data size must be NX*NY*NZ"
    PERMX_ERROR = "[ERROR] PERMX data size must be NX*NY*NZ"
    PERMY_ERROR = "[ERROR] PERMY data size must be NX*NY*NZ"
    PERMZ_ERROR = "[ERROR] PERMZ data size must be NX*NY*NZ"
    ACTNUM_ERROR = "[ERROR] ACTNUM data size must be NX*NY*NZ"
    SO_ERROR = "[ERROR] SO data size must be NX*NY*NZ"
    GRID_NOT_DEFINED_ERROR = "[ERROR] Invoking process_grdecl before read_grdecl"
    CHECK_DIM_ERRROR = "[ERROR] GRDECL keyword {} found before dimension specification"
    LOAD_CELL_DATA_ERROR = "[ERROR] {} data size must be NX*NY*NZ"