subroutine pyk2_init(n_alloc)
  use floatPrecision
  use numerical_constants
  ! use crcoall    NODIG ??
  use parpro ,           only : npart
  use mod_alloc ,        only : alloc      ! to allocate partID etc
  use mod_common ,       only : iexact, napx, unit208, aa0
  use mod_common_main ,  only : partID, parentID, pairID, naa
  use mod_ranlux ,       only : rluxgo     ! for ranlux init

  use coll_common ,      only : rnd_seed, rcx, rcxp, rcy, rcyp, rcp, rcs, coll_expandArrays
  use coll_materials ! for collmat_init
  use coll_db        ! for cdb_readCollDB
  use coll_k2        ! for scattering

  use files  ! for testing

  implicit none

  integer, intent(in)       :: n_alloc

  ! Set default values for collimator materials
  call collmat_init
  cdb_fileName="CollDB-RunIII.dat"
  call cdb_readCollDB

  rnd_seed = 7569

  ! Initialize random number generator
  !if(rnd_seed == 0) rnd_seed = time_getSysClock()
  if(rnd_seed <  0) rnd_seed = abs(rnd_seed)
  call rluxgo(3, rnd_seed, 0, 0)

  call coll_expandArrays(n_alloc)

end subroutine
 
subroutine pyk2(num_particles, x_particles, xp_particles, &
                y_particles, yp_particles, s_particles, &
                p_particles, part_hit_pos, part_hit_turn, &
                part_abs_pos, part_abs_turn, part_impact, &
                part_indiv, part_linteract, nhit_stage, nabs_type, linside)

  use floatPrecision
  use numerical_constants
  ! use crcoall    NODIG ??
  use parpro ,           only : npart
  use mod_alloc ,        only : alloc      ! to allocate partID etc
  use mod_common ,       only : iexact, napx, unit208, aa0
  use mod_common_main ,  only : partID, parentID, pairID, naa
  use mod_ranlux ,       only : rluxgo     ! for ranlux init

  use coll_common ,      only : rnd_seed, rcx, rcxp, rcy, rcyp, rcp, rcs, coll_expandArrays
  use coll_materials ! for collmat_init
  use coll_db        ! for cdb_readCollDB
  use coll_k2        ! for scattering

  use files  ! for testing

  implicit none


  ! ####################
  ! ## test variables ##
  ! ####################

  integer, intent(in)       :: num_particles
  real(kind=8), intent(inout)  :: x_particles(num_particles)
  real(kind=8), intent(inout)  :: xp_particles(num_particles)
  real(kind=8), intent(inout)  :: y_particles(num_particles)
  real(kind=8), intent(inout)  :: yp_particles(num_particles)
  real(kind=8), intent(inout)  :: s_particles(num_particles)
  real(kind=8), intent(inout)  :: p_particles(num_particles)

  integer(kind=4)  , intent(inout) :: part_hit_pos(num_particles)
  integer(kind=4)  , intent(inout) :: part_hit_turn(num_particles)
  integer(kind=4)  , intent(inout) :: part_abs_pos(num_particles)
  integer(kind=4)  , intent(inout) :: part_abs_turn(num_particles)
  real(kind=8) , intent(inout) :: part_impact(num_particles)
  real(kind=8) , intent(inout) :: part_indiv(num_particles)
  real(kind=8) , intent(inout) :: part_linteract(num_particles)
  integer(kind=4)  , intent(inout) :: nhit_stage(num_particles)
  integer(kind=4)  , intent(inout) :: nabs_type(num_particles)
  logical(kind=4)  , intent(inout) :: linside(num_particles)

  integer j


  ! ########################
  ! ## function variables ##
  ! ########################
  integer(kind=4)  :: icoll
  integer(kind=4)  :: iturn
  integer(kind=4)  :: ie
  real(kind=fPrec) :: c_length
  real(kind=fPrec) :: c_rotation
  real(kind=fPrec) :: c_aperture
  real(kind=fPrec) :: c_offset
  real(kind=fPrec) :: c_tilt(2)
  real(kind=fPrec) :: c_enom
  logical(kind=4)  :: onesided


  ! ####################
  ! ## initialisation ##
  ! ####################
  !character(len=:),    allocatable   :: numpart
  !numpart="20000"
  !read(numpart,*) napx
  npart=20000
  
  call alloc(naa, npart, aa0, "naa")
  call alloc(partID, npart, 0, "partID")
  call alloc(parentID, npart, 0, "parentID")
  call alloc(pairID, 2, npart, 0, "pairID")
  do j=1,npart
    partID(j)   = j
    parentID(j) = j
    pairID(1,j) = (j+1)/2    ! The pairID of particle j
    pairID(2,j) = 2-mod(j,2) ! Either particle 1 or 2 of the pair
  end do
  
  napx=npart  ! this decreases after absorptions!
  unit208=109

  icoll = 31
  iturn = 1
  ie =1
  c_length = 0.59999999999999998
  c_rotation = 0
  c_aperture = 0.0025711021962573095
  c_offset = 0
  c_tilt = (0, 0)
  c_enom = 7000000
  onesided = .FALSE.
  linside(:) = .FALSE.



  do j=1,npart
    rcx(j) = x_particles(j)
    rcxp(j) = xp_particles(j)
    rcy(j) = y_particles(j)
    rcyp(j) = yp_particles(j)
    rcs(j) = s_particles(j)
    rcp(j) = p_particles(j)
  end do

  call k2coll_collimate(icoll, iturn, ie, c_length, c_rotation, c_aperture, c_offset, &
     c_tilt, rcx, rcxp, rcy, rcyp, rcp, rcs, c_enom*c1m3, part_hit_pos, part_hit_turn, &
     part_abs_pos, part_abs_turn, part_impact, part_indiv, part_linteract,             &
     onesided, nhit_stage, 1, nabs_type, linside)

  do j=1,npart
     x_particles(j) = rcx(j)
     xp_particles(j) = rcxp(j)
     y_particles(j) = rcy(j)
     yp_particles(j) = rcyp(j)
     s_particles(j) = rcs(j)
     p_particles(j) = rcp(j)
  end do
end subroutine 

