#!/bin/bash

base_dir=basis_extrapolation_calculations
system=hBN_water_Oup_Hdown
Nk=1
Ns=1

for ecut_ev in 400 500 600 700 800
	do
		echo "Now starting KS-DFT for ${system} with ecut = ${ecut_ev} eV, Nk = ${Nk}, and Ns = ${Ns}"
		calc_dir=${base_dir}/${system}_ecut_${ecut_ev}_Nk_${Nk}_Ns_${Ns}
		start_time=`date +%s`
		${calc_dir}/pw.x < ${calc_dir}/scf.in > ${calc_dir}/scf.out
		echo "Runtime = $(expr `date +%s` - $start_time) sec"
	done
