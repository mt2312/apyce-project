from inout import readGRDECL
from inout import writeVTK
from gridprocessing import Grid

#G = readGRDECL('./Data/Norne.grdecl')
#G = readGRDECL('./Data/Johansen.grdecl')
#G = readGRDECL('./Data/MAC7A-TM02.txt')

# Read the data from ECLIPSE INPUT file
G = readGRDECL('./Data/dome.grdecl')

# Process the file
G.processGRDECL(G)

# Save the data in VTK format
writeVTK(G)