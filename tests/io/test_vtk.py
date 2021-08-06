from apyce.io import VTK

import vtk
import os
import numpy as np

FILE = '../Data/dome.grdecl'
BASENAME = 'dome.grdecl'
ABSOLUTE_PATH = '/home/metzker/Documents/Repositories/apyce-project/tests/Data/dome.grdecl'
DIRNAME = '../Data'


class TestVTK():
    def test_new(self):
        vtk_instance = VTK()
        vtk_instance_2 = vtk.vtkUnstructuredGrid()
        assert isinstance(vtk_instance, type(vtk_instance_2))

    def test_export_data(self):
        assert VTK.export_data(FILE, VTK(), False) is None
        os.remove(DIRNAME + '/Results/dome.vtu')
        os.removedirs(DIRNAME + '/Results')

    def test_create_points(self):
        vtk_points_instance = VTK()
        vtk_points_instance_2 = vtk.vtkUnstructuredGrid()
        assert isinstance(vtk_points_instance, type(vtk_points_instance_2))

    def test_create_hexahedron(self):
        vtk_hexahedron_instance = VTK()
        vtk_hexahedron_instance_2 = vtk.vtkUnstructuredGrid()
        assert isinstance(vtk_hexahedron_instance, type(vtk_hexahedron_instance_2))

    def test_get_duplicatecell(self):
        assert VTK.get_duplicatecell() == 1

    def test_numpy_to_vtk(self):
        data_array = np.arange(1600)
        keyword = 'PORO'
        vtk_unstructured_grid = VTK()
        VTK.numpy_to_vtk(keyword, data_array, vtk_unstructured_grid, False)
        assert vtk_unstructured_grid.GetCellData().GetArray('PORO').GetSize() == 1600
