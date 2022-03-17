import numpy as np

import pyk2
import xpart as xp

k2_engine = pyk2.K2Engine(n_alloc=100000,
        colldb_input_fname="CollDB-RunIII.dat", random_generator_seed=7569)

collimator = pyk2.K2Collimator(k2_engine=k2_engine,
                               length=0.59999999999999998,
                               rotation=0,
                               icoll=31,
                               aperture=0.0025711021962573095,
                               onesided=False,
                               dx=0,
                               dy=0)

x_test = np.loadtxt("./rcx.dump")
xp_test = np.loadtxt("./rcxp.dump")
y_test = np.loadtxt("./rcy.dump")
yp_test = np.loadtxt("./rcyp.dump")
s_test = np.loadtxt("./rcs.dump")
p_test = np.loadtxt("./rcp.dump")

part = xp.Particles(p0c=7e12, x=x_test, y=y_test)
part.psigma = (p_test*1e9 - part.energy0)/part.energy0
rpp_test = part.rpp.copy()
part.px = xp_test/part.rpp
part.py = yp_test/part.rpp
part_test = part.copy()

collimator.track(part)

part_id = part.particle_id.copy()
state_part = part.state.copy(); state_part[part_id]=part.state
x_part = part.x.copy(); x_part[part_id]=part.x
px_part = part.px.copy(); px_part[part_id]=part.px
y_part = part.y.copy(); y_part[part_id]=part.y
py_part = part.py.copy(); py_part[part_id]=part.py
delta_part = part.delta.copy(); delta_part[part_id]=part.delta
psigma_part = part.psigma.copy(); psigma_part[part_id]=part.psigma
zeta_part = part.zeta.copy(); zeta_part[part_id]=part.delta
rpp_part = part.rpp.copy(); rpp_part[part_id]=part.rpp

x_ref = np.loadtxt("./rcx.dump_after_REF")
xp_ref = np.loadtxt("./rcxp.dump_after_REF")
y_ref = np.loadtxt("./rcy.dump_after_REF")
yp_ref = np.loadtxt("./rcyp.dump_after_REF")
s_ref = np.loadtxt("./rcs.dump_after_REF")
p_ref = np.loadtxt("./rcp.dump_after_REF")

# Check that lost particles have their initial coordinates
assert np.all((x_ref == 0.09999) == (state_part<1))
assert np.all(x_part[state_part<1] == x_test[state_part<1])
assert np.all(px_part[state_part<1] == part_test.px[state_part<1])
assert np.all(y_part[state_part<1] == y_test[state_part<1])
assert np.all(py_part[state_part<1] == part_test.py[state_part<1])
assert np.all(delta_part[state_part<1] == part_test.delta[state_part<1])
assert np.all(zeta_part[state_part<1] == part_test.zeta[state_part<1])

xp_part = px_part*rpp_part
yp_part = py_part*rpp_part
p_part = (psigma_part*part.energy0 + part.energy0)/1e9
assert np.allclose(x_part[state_part>0], x_ref[state_part>0], atol=1e-9, rtol=0)
assert np.allclose(xp_part[state_part>0], xp_ref[state_part>0], atol=5e-9, rtol=0)
assert np.allclose(y_part[state_part>0], y_ref[state_part>0], atol=1e-9, rtol=0)
assert np.allclose(yp_part[state_part>0], yp_ref[state_part>0], atol=5e-9, rtol=0)
assert np.allclose(p_part[state_part>0], p_ref[state_part>0], atol=0, rtol=1e-7)
