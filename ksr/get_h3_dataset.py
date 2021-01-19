import os
import sys
sys.path.append('../')
sys.path.append('../DFT_1d')

import numpy as np
from DFT_1d import ks_dft
from DFT_1d import functionals

import matplotlib.pyplot as plt
import time

h = 0.08
grids = np.arange(-256, 257) * h

external_potentials = np.load('h3_external_potentials.npy')
num_samples = len(external_potentials)
num_electrons = 3

lda_xc = functionals.ExponentialLDAFunctional

total_energies = []
densities = []
time_per_molecule = []
for i, v_ext in enumerate(external_potentials):
  start_time = time.time()

  solver = ks_dft.Spinless_KS_Solver(grids, v_ext=v_ext, xc=lda_xc,
                                     num_electrons=num_electrons)
  solver.solve_self_consistent_density(max_iterations=30,
                                       energy_converge_tolerance=-1)

  time_elapsed = time.time() - start_time
  time_per_molecule.append(time_elapsed)
  if i == 0:
    est_time_remain = time_elapsed * num_samples
    hours, rem = divmod(est_time_remain, 3600)
    minutes, seconds = divmod(rem, 60)
    print("Estimated time to complete: ")
    print("{:0>2}:{:0>2}:{:05.2f}".format(int(hours), int(minutes), seconds))

  total_energies.append(solver.total_energy)
  densities.append(solver.density)

out_dir = 'molecule_dissociation/h3/unpol_lda/'
if not os.path.exists(out_dir):
  os.makedirs(out_dir)

np.save(os.path.join(out_dir, 'time_per_molecule.npy'), time_per_molecule)
np.save(os.path.join(out_dir, 'total_energies.npy'), total_energies)
np.save(os.path.join(out_dir, 'densities.npy'), densities)