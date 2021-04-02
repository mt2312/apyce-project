from apyce import Model

G = Model(fn='./Data/dome.grdecl', grid_origin='Eclipse', verbose=True)
G.process_grdecl()
G.write_vtu()
G.plot_grid(filename='./Data/Results/dome.vtu', lighting=True, property='PORO', show_edges=True,
            specular=0.5, specular_power=128, show_scalar_bar=True)