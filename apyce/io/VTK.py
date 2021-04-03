import vtk
import vtk.util.numpy_support as np_support

from apyce.utils import misc


class VTK:
    r"""
    The Visualization Toolkit (VTK) format defined by Kitware and used by ParaView

    """
    def __new__(cls, *args, **kwargs):
        return vtk.vtkUnstructuredGrid()

    @classmethod
    def export_data(cls, filename, vtk_unstructured_grid, verbose):
        r"""
        Save grid data to a single vtu file for visualizing in ParaView.

        Parameters
        ----------
        filename : string
            A string that holds the name (path) of the grid file.
        vtk_unstructured_grid : vtkUnstructuredGrid Object
            Object holding VTK Unstructured Grid.
        verbose : boolean, default is True.
            A boolean that will be used to emit (or not) messages to screen while processing.

        Notes
        -----
        The vtu file will be created on the directory 'Results' that will be created
            on the same directory than grid file

        """

        # Create the 'Results' directory
        results_dir = misc.create_results_directory(misc.get_basename(filename))

        if verbose:
            print("\n[OUTPUT] Writting ParaView file \"" + misc.get_basename(misc.get_basename(filename)).split('.')[0] + ".vtu\"")

        xml_writer = vtk.vtkXMLUnstructuredGridWriter()
        xml_writer.SetFileName(results_dir + misc.get_basename(misc.get_basename(filename)).split('.')[0] + '.vtu')
        xml_writer.SetInputData(vtk_unstructured_grid)
        xml_writer.Write()

    @classmethod
    def create_points(cls):
        r"""
        Return a vtk.vtkPoints() object.

        """

        return vtk.vtkPoints()

    @classmethod
    def create_hexahedron(cls):
        r"""
        Return a vtk.vtkHexahedron() object.

        """

        return vtk.vtkHexahedron()

    @classmethod
    def get_duplicatecell(cls):
        r"""
        Return the vtk.vtkDataSetAttributes.DUPLICATECELL attribute.

        """

        return vtk.vtkDataSetAttributes.DUPLICATECELL

    @classmethod
    def numpy_to_vtk(cls, name, numpy_data, vtk_unstructured_grid, verbose=True):
        r"""
        Convert the numpy array to vtk array and add this array to structure grid.

        Parameters
        ----------
        name : string
            Name of the property e.g. ACTNUM.
        numpy_data : ndarray
            Array with values of the property.
        vtk_unstructured_grid : vtkUnstructuredGrid Object
            Object holding VTK Unstructured Grid.
        verbose : boolean, default is True.
            A boolean that will be used to emit (or not) messages to screen while processing.

        Notes
        -----
        https://pyscience.wordpress.com/2014/09/06/numpy-to-vtk-converting-your-numpy-arrays-to-vtk-arrays-and-files/

        """

        if verbose:
            print('\tInserting data [' + name + '] into vtk array')

        vtk_data = np_support.numpy_to_vtk(num_array=numpy_data.ravel(), deep=True, array_type=vtk.VTK_FLOAT)
        vtk_data.SetName(name)
        vtk_data.SetNumberOfComponents(1)
        vtk_unstructured_grid.GetCellData().AddArray(vtk_data)