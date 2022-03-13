#!/bin/bash
rm *.mod *.o

gfortran -fpic -c \
 core_tools.f90 \
 constants.f90 \
 strings.f90 \
 mod_alloc.f90 \
 common_modules.f90  \
 string_tools.f90  \
 mod_units.f90  \
 bouncy_castle.f90  \
 libcrlibm.a  \
 libroundctl.a  \
 coll_jawfit.f90  \
 coll_common.f90  \
 coll_db.f90  \
 mod_ranlux.f90  \
 mod_funlux.f90  \
 coll_crystal.f90  \
 coll_k2.f90 \
 files.f90  \
 

#gfortran -shared -o libk2.so\
# core_tools.o \
# constants.o \
# strings.o \
# mod_alloc.o \
# common_modules.o  \
# string_tools.o  \
# mod_units.o  \
# bouncy_castle.o  \
# libcrlibm.a  \
# libroundctl.a  \
# coll_jawfit.o  \
# coll_common.o  \
# coll_db.o  \
# mod_ranlux.o  \
# mod_funlux.o  \
# coll_crystal.o  \
# coll_k2.o \
# files.o  \

f2py -m pyk2f -c pyk2.f90 \
 core_tools.o \
 constants.o \
 strings.o \
 mod_alloc.o \
 common_modules.o  \
 string_tools.o  \
 mod_units.o  \
 bouncy_castle.o  \
 libcrlibm.a  \
 libroundctl.a  \
 coll_jawfit.o  \
 coll_common.o  \
 coll_db.o  \
 mod_ranlux.o  \
 mod_funlux.o  \
 coll_crystal.o  \
 coll_k2.o \
 files.o  \

 mv pyk2f.*.so ../
