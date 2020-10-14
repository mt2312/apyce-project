from inout import readGRDECL
from gridprocessing import Grid

G = readGRDECL('./Data/dome.grdecl')
#G = readGRDECL('./Data/Norne.grdecl')
#G = readGRDECL('./Data/Johansen.grdecl')
#G = readGRDECL('./Data/MAC7A-TM02.txt')
G = G.processGRDECL(G)