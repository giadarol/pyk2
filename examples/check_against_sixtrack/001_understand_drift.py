import numpy as np

import pyk2

pyk2.pyk2_init(n_alloc = 100000, colldb_input_fname="CollDB-RunIII.dat",
               random_generator_seed=7569)

x_test = np.loadtxt("./rcx.dump")*0
xp_test = np.loadtxt("./rcxp.dump")*0 + 1e-3
y_test = np.loadtxt("./rcy.dump")*0
yp_test = np.loadtxt("./rcyp.dump")*0
s_test = np.loadtxt("./rcs.dump")*0
p_test = np.loadtxt("./rcp.dump")

part_hit_pos = np.zeros(len(x_test), dtype=np.int32)
part_hit_turn = np.zeros(len(x_test), dtype=np.int32)
part_abs_pos = np.zeros(len(x_test), dtype=np.int32)
part_abs_turn = np.zeros(len(x_test), dtype=np.int32)
part_impact = np.zeros(len(x_test), dtype=np.float)
part_indiv = np.zeros(len(x_test), dtype=np.float)
part_linteract = np.zeros(len(x_test), dtype=np.float)
nhit_stage = np.zeros(len(x_test), dtype=np.int32)
nabs_type = np.zeros(len(x_test), dtype=np.int32)
linside = np.zeros(len(x_test), dtype=np.int32)

# `linside` is an array of logicals in fortran. Beware of the fortran converion:
# True <=> -1 (https://stackoverflow.com/questions/39454349/numerical-equivalent-of-true-is-1)

pyk2.pyk2_run(x_particles=x_test,
              xp_particles=xp_test,
              y_particles=y_test,
              yp_particles=yp_test,
              s_particles=s_test,
              p_particles=p_test,
              part_hit_pos=part_hit_pos,
              part_hit_turn=part_hit_turn,
              part_abs_pos=part_abs_pos,
              part_abs_turn=part_abs_turn,
              part_impact=part_impact,
              part_indiv=part_indiv,
              part_linteract=part_linteract,
              nhit_stage=nhit_stage,
              nabs_type=nabs_type,
              linside=linside,
              icoll=31,
              iturn=1,
              ie=1,
              c_length=0.59999999999999998,
              c_rotation=0,
              c_aperture=0.0025711021962573095,
              c_offset=0,
              c_tilt=np.array([0,0], dtype=np.float64),
              c_enom=7000000,
              onesided=False,
              #random_generator_seed=-1, # skips rng re-initlization
              random_generator_seed=7569
              )

# Check that it behaves like a thick drift
assert np.allclose(s_test, 0.6, rtol=0, atol=1e-10)
assert np.allclose(x_test, 0.6e-3, rtol=0, atol=1e-10)
