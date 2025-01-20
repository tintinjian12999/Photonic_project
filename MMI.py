import meep as mp
import numpy as np
import matplotlib.pyplot as plt
from common_element import *
cell = mp.Vector3(32,8,0)
curve_length = 4                                 
num_segments = 200             
sources = [mp.Source(mp.ContinuousSource(wavelength=source_wavelength, end_time=50),
                     component=mp.Ez,
                     center=mp.Vector3(-15,-0.5),
                     size=mp.Vector3(0, waveguide_width))]
  
geometry = []

geometry.append(
        mp.Block(mp.Vector3(mp.inf, waveguide_width, mp.inf), 
             center=mp.Vector3(-6, -0.5), 
             material=waveguide_material),
)

geometry.append(
        mp.Block(mp.Vector3(24.65, 10 * waveguide_width, mp.inf), 
             center=mp.Vector3(0, 0), 
             material=waveguide_material),
)


geometry.append(
        mp.Block(mp.Vector3(mp.inf, waveguide_width, mp.inf), 
             center=mp.Vector3(6, 0.5), 
             material=waveguide_material),
)


sim = mp.Simulation(
    cell_size=cell,
    boundary_layers=pml_layers,
    default_material=background_material,
    geometry=geometry,
    sources=sources,
    resolution=resolution,
)

flux1 = mp.FluxRegion(
    center=mp.Vector3(-14, -0.5), size=mp.Vector3(0,  waveguide_width, 0)
)
flux1_sim = sim.add_flux(fcen, 0, 1, flux1)

flux2 = mp.FluxRegion(
    center=mp.Vector3(14, -0.5), size=mp.Vector3(0,  waveguide_width, 0)
)
flux2_sim = sim.add_flux(fcen, 0, 1, flux2)

flux3 = mp.FluxRegion(
    center=mp.Vector3(14, 0.5), size=mp.Vector3(0, waveguide_width, 0)
)
flux3_sim = sim.add_flux(fcen, 0, 1, flux3)

sim.use_output_directory()
#sim.run(until=200)
sim.run(mp.at_beginning(mp.output_epsilon),
        mp.to_appended("ez", mp.at_every(3, mp.output_efield_z)),
        until=1000)
flux_data = []
flux_data.append(mp.get_fluxes(flux1_sim)[0])
flux_data.append(mp.get_fluxes(flux2_sim)[0])
flux_data.append(mp.get_fluxes(flux3_sim)[0])
for data in flux_data:
    data = round(data, 3)
    data = abs(data)
    print(data)

eps_data = sim.get_array(center=mp.Vector3(), size=cell, component=mp.Dielectric)
plt.figure()
plt.imshow(eps_data.transpose(), interpolation="spline36", cmap="binary")
plt.axis("off")
plt.show()

ex_data = sim.get_array(center=mp.Vector3(), size=cell, component=mp.Ez)
plt.figure()
plt.imshow(eps_data.transpose(), interpolation="spline36", cmap="binary")
plt.imshow(ex_data.transpose(), interpolation="spline36", cmap="RdBu", alpha=0.9)
plt.axis("off")
plt.show()
