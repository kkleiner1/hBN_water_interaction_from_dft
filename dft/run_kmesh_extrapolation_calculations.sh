#!/bin/bash

base_dir=kmesh_extrapolation_calculations
system=hBN_water_Oup_Hdown
functional=pbe
ecp=paw
ecut_ev=700
Ns=1

for Nk in 1 2 3 4 5
	do
		echo "Now starting KS-DFT for ${system} with ${functional}, ${ecp}, ecut = ${ecut_ev} eV, Nk = ${Nk}, and Ns = ${Ns}"
		calc_dir=${base_dir}/${system}_${functional}_${ecp}_ecut_${ecut_ev}_Nk_${Nk}_Ns_${Ns}
		cd $calc_dir
		start_time=`date +%s`
		pw.x < scf.in > scf.out
		echo "Runtime = $(expr `date +%s` - $start_time) sec"
		cd ../..
	done
