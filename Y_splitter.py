# From the Meep tutorial: plotting permittivity and fields of a straight waveguide
import meep as mp
import matplotlib.pyplot as plt
import numpy as np
from common_element import *

geometry = [
    mp.Block(mp.Vector3(9, waveguide_width, mp.inf), 
             center=mp.Vector3(-6, 0), 
             material=waveguide_material),
    mp.Block(mp.Vector3(6.5, waveguide_width, mp.inf),
             center=mp.Vector3(1, 1), 
             e1=mp.Vector3(1, np.tan(np.pi / 10), 0),
             material=waveguide_material, 
             ),
    mp.Block(mp.Vector3(6.5, waveguide_width, mp.inf),
             center=mp.Vector3(1, -1), 
             e1=mp.Vector3(1, -np.tan(np.pi / 10), 0),
             material=waveguide_material, 
             ),
    mp.Block(mp.Vector3(4, waveguide_width, mp.inf), 
             center=mp.Vector3(6, -2), 
             material=waveguide_material
             ),
    mp.Block(mp.Vector3(4, waveguide_width, mp.inf), 
             center=mp.Vector3(6, 2), 
             material=waveguide_material
             )
]
sim = mp.Simulation(
    cell_size=cell,
    boundary_layers=pml_layers,
    default_material=background_material,
    geometry=geometry,
    sources=sources,
    resolution=resolution,
)

flux1 = mp.FluxRegion(
    center=mp.Vector3(-2.75, 0), size=mp.Vector3(0,  waveguide_width, 0)
)
flux1_sim = sim.add_flux(fcen, 0, 1, flux1)

flux2 = mp.FluxRegion(
    center=mp.Vector3(7, -2), size=mp.Vector3(0,  waveguide_width, 0)
)
flux2_sim = sim.add_flux(fcen, 0, 1, flux2)

flux3 = mp.FluxRegion(
    center=mp.Vector3(7, 2), size=mp.Vector3(0,  waveguide_width, 0)
)
flux3_sim = sim.add_flux(fcen, 0, 1, flux3)
sim.use_output_directory()
#sim.run(until=1000)
sim.run(mp.at_beginning(mp.output_epsilon),
        mp.to_appended("ez", mp.at_every(1.0, mp.output_efield_z)),
        until=200)
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
#plt.show()

ez_data = sim.get_array(center=mp.Vector3(), size=cell, component=mp.Ez)
plt.figure()
plt.imshow(eps_data.transpose(), interpolation="spline36", cmap="binary")
plt.imshow(ez_data.transpose(), interpolation="spline36", cmap="RdBu", alpha=0.9)
plt.axis("off")
#plt.show()