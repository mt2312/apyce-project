from APyCE import *

#Apyce('./Data/dome.grdecl')
#Apyce('./Data/Norne.GRDECL')
#Apyce('./Data/Johansen.grdecl')
G=Apyce("./Data/MAC7A-TM02.txt")
G.processGRDECL()
G.WriteVTK()