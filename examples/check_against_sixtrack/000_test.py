import numpy as np

import pyk2

pyk2.pyk2_init(n_alloc = 100000, colldb_input_fname="CollDB-RunIII.dat",
               random_generator_seed=7569)

for _ in range(3):
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

    part_hit_pos_ref = np.loadtxt("./part_hit_pos.dump_after_REF")
    part_hit_turn_ref = np.loadtxt("./part_hit_turn.dump_after_REF")
    part_abs_pos_ref = np.loadtxt("./part_abs_pos.dump_after_REF")
    part_abs_turn_ref = np.loadtxt("./part_abs_turn.dump_after_REF")
    part_impact_ref = np.loadtxt("./part_impact.dump_after_REF")
    part_indiv_ref = np.loadtxt("./part_indiv.dump_after_REF")
    part_linteract_ref = np.loadtxt("./part_linteract.dump_after_REF")
    nhit_stage_ref = np.loadtxt("./nhit_stage.dump_after_REF")
    nabs_type_ref = np.loadtxt("./nabs_type.dump_after_REF")

    assert np.allclose(part_hit_pos, part_hit_pos_ref, atol=1e-9, rtol=0)
    assert np.allclose(part_hit_turn, part_hit_turn_ref, atol=1e-9, rtol=0)
    assert np.allclose(part_abs_pos, part_abs_pos_ref, atol=1e-9, rtol=0)
    assert np.allclose(part_abs_turn, part_abs_turn_ref, atol=1e-9, rtol=0)
    assert np.allclose(part_impact, part_impact_ref, atol=1e-9, rtol=0)
    assert np.allclose(part_indiv, part_indiv_ref, atol=1e-9, rtol=0)
    assert np.allclose(part_linteract, part_linteract_ref, atol=2e-4, rtol=0)
    assert np.allclose(nhit_stage, nhit_stage_ref, atol=1e-9, rtol=0)
    assert np.allclose(nabs_type, nabs_type, atol=1e-9, rtol=0)
