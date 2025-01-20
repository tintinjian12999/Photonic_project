import meep as mp
import numpy as np
cell = mp.Vector3(16,16,0)
n_background = 1
n_waveguide = 3.4792 #Si under wavelength = 1.55um 25。C
background_material = mp.Medium(index=n_background)
waveguide_material = mp.Medium(index=n_waveguide)
source_wavelength = 1.55
fcen = 1 / source_wavelength
NA = np.sqrt(n_waveguide ** 2 - n_background ** 2)
waveguide_width = source_wavelength / (2 * NA) #From M = 2d * NA / lambda. Where represents mode number
pml_layers = [mp.PML(1.0)]
resolution = 20

sources = [mp.Source(mp.ContinuousSource(wavelength=source_wavelength, end_time=50),
                     component=mp.Ez,
                     center=mp.Vector3(-7,0),
                     size=mp.Vector3(0, waveguide_width))]