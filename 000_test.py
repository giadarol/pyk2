import numpy as np

import pyk2

x_test = np.loadtxt("./rcx.dump")
xp_test = np.loadtxt("./rcxp.dump")
y_test = np.loadtxt("./rcy.dump")
yp_test = np.loadtxt("./rcyp.dump")
s_test = np.loadtxt("./rcs.dump")
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

pyk2.pyk2_init(n_alloc = 100000)
pyk2.pyk2(x_particles=x_test,
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
          nabs_type=nabs_type)

x_ref = np.loadtxt("./rcx.dump_after_REF")
xp_ref = np.loadtxt("./rcxp.dump_after_REF")
y_ref = np.loadtxt("./rcy.dump_after_REF")
yp_ref = np.loadtxt("./rcyp.dump_after_REF")
s_ref = np.loadtxt("./rcs.dump_after_REF")
p_ref = np.loadtxt("./rcp.dump_after_REF")

assert np.allclose(x_test, x_ref, atol=1e-9, rtol=0)
assert np.allclose(xp_test, xp_ref, atol=5e-9, rtol=0)
assert np.allclose(y_test, y_ref, atol=1e-9, rtol=0)
assert np.allclose(yp_test, yp_ref, atol=5e-9, rtol=0)
assert np.allclose(s_test, s_ref, atol=2e-4, rtol=0)
assert np.allclose(p_test, p_ref, atol=0, rtol=1e-7)


