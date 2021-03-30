from apyce import Model

G = Model(fn='./Data/dome.grdecl', grid_origin='Eclipse', verbose=True)
G.process_grdecl()
G.write_vtu()