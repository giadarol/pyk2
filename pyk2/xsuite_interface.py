import numpy as np

class K2Engine:

    def __init__(self, n_alloc, colldb_input_fname, random_generator_seed=None):

        self.n_alloc = n_alloc
        self.colldb_input_fname = colldb_input_fname

        if random_generator_seed is None:
            self.random_generator_seed = np.random.randint(1, 100000)
        else:
            self.random_generator_seed = random_generator_seed

        import pyk2
        pyk2.pyk2_init(n_alloc=n_alloc, colldb_input_fname=colldb_input_fname,
               random_generator_seed=random_generator_seed)
        pyk2._active_engine = self


class K2Collimator:

    iscollective = True
    isthick = True

    def __init__(self, k2_engine, length, rotation, icoll,
                 aperture, onesided, dx, dy):

        self.k2_engine = k2_engine
        self.length = length
        self.rotation = rotation
        self.icoll = icoll
        self.aperture = aperture
        self.onesided = onesided
        self.dx = dx
        self.dy = dy

    def track(self, particles):

        import pyk2
        assert pyk2._active_engine is self.k2_engine

        npart = particles._num_active_particles
        assert npart <= self.k2_engine.n_alloc
        x_part = particles.x[:npart] - self.dx
        xp_part = particles.px[:npart] * particles.rpp[:npart]
        y_part = particles.y[:npart] - self.dy
        yp_part = particles.py[:npart] * particles.rpp[:npart]
        s_part = 0 * x_part
        p_part = particles.energy[:npart] / 1e9 # In GeV? Does it want energy or momentum

        part_hit_pos = np.zeros(len(x_part), dtype=np.int32)
        part_hit_turn = np.zeros(len(x_part), dtype=np.int32)
        part_abs_pos = np.zeros(len(x_part), dtype=np.int32)
        part_abs_turn = np.zeros(len(x_part), dtype=np.int32)
        part_impact = np.zeros(len(x_part), dtype=np.float)
        part_indiv = np.zeros(len(x_part), dtype=np.float)
        part_linteract = np.zeros(len(x_part), dtype=np.float)
        nhit_stage = np.zeros(len(x_part), dtype=np.int32)
        nabs_type = np.zeros(len(x_part), dtype=np.int32)
        linside = np.zeros(len(x_part), dtype=np.int32)

        # `linside` is an array of logicals in fortran. Beware of the fortran converion:
        # True <=> -1 (https://stackoverflow.com/questions/39454349/numerical-equivalent-of-true-is-1)

        pyk2.pyk2_run(x_particles=x_part,
                      xp_particles=xp_part,
                      y_particles=y_part,
                      yp_particles=yp_part,
                      s_particles=s_part,
                      p_particles=p_part,
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
                      icoll=self.icoll,
                      iturn=1,
                      ie=1,
                      c_length=self.length,
                      c_rotation=self.rotation,
                      c_aperture=self.aperture,
                      c_offset=0,
                      c_tilt=np.array([0,0], dtype=np.float64),
                      c_enom=particles.energy0[0]/1e6,
                      onesided=self.onesided,
                      random_generator_seed=-1, # skips rng re-initlization
                      )

        mask_lost = part_abs_turn > 0
        mask_hit = part_hit_turn > 0
        mask_not_hit = ~mask_hit
        mask_survived_hit = mask_hit & (~mask_lost)

        state_out = particles.state[:npart].copy()
        state_out[mask_lost] = -333
        particles.state[:npart] = state_out

        psigma_out = particles.psigma[:npart].copy()
        e0 = particles.energy0[:npart]
        psigma_out[mask_survived_hit] = (
            p_part[mask_survived_hit] * 1e9
               - e0[mask_survived_hit])/e0[mask_survived_hit]
        particles.psigma[:npart] = psigma_out

        x_part_out = particles.x[:npart].copy()
        x_part_out[~mask_lost] = x_part[~mask_lost] + self.dx
        particles.x[:npart] = x_part_out

        y_part_out = particles.y[:npart].copy()
        y_part_out[~mask_lost] = y_part[~mask_lost] + self.dy
        particles.y[:npart] = y_part_out

        rpp_out = particles.rpp[:npart]
        px_out = particles.px[:npart]
        px_out[mask_survived_hit] = xp_part[mask_survived_hit]/rpp_out[mask_survived_hit]
        particles.px[:npart] = px_out

        py_out = particles.py[:npart]
        py_out[mask_survived_hit] = yp_part[mask_survived_hit]/rpp_out[mask_survived_hit]
        particles.py[:npart] = py_out
        
        rvv_out = particles.rvv[:npart]
        zeta_out = particles.zeta[:npart]
        zeta_out[mask_not_hit] += self.length*(
                            rvv_out[mask_not_hit] - (1 + ( xp_part[mask_not_hit]**2 + yp_part[mask_not_hit]**2)/2 ) 
                        )
        particles.zeta[:npart] = zeta_out
        
        s_out = particles.s[:npart]
        s_out[mask_not_hit] += self.length
        particles.s[:npart] = s_out
        
        particles.reorganize()
