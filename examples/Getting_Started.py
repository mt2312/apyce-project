import apyce as ap

G = ap.grid.Grid(filename='Data/PSY.grdecl', grid_origin='eclipse', verbose=True)
G.process_grid()
G.load_cell_data("Data/PSY/PORO.INC", "PORO")
G.export_data()
G.plot_grid(filename='Data/Results/PSY.vtu', lighting=False, property='PORO', show_edges=True, specular=0.0,
            specular_power=0.0, show_scalar_bar=True, cmap='viridis')
