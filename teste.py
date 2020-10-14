from APyCE import *

G = Apyce('./Data/dome.grdecl')
#G = Apyce('./Data/Norne.GRDECL')
#G = Apyce('./Data/Johansen.grdecl')
#G = Apyce("./Data/MAC7A-TM02.txt")
G.processGRDECL()
G.WriteVTK()