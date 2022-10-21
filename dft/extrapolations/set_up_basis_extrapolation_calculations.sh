#!/bin/bash

ryd_per_ev=0.0734986176
base_dir=extrapolations/basis_extrapolation_calculations
functional=pbe
ecp=paw
system=hBN_water_Oup_Hdown
Nk=1
Ns=1

cd ..
if [ ! -d "${base_dir}" ]; then
	mkdir $base_dir
fi

for ecut_ev in 400 500 600 700 800
	do
		calc_dir=${base_dir}/${system}_${functional}_${ecp}_ecut_${ecut_ev}_Nk_${Nk}_Ns_${Ns}
		if [ ! -d "${calc_dir}" ]; then
			mkdir $calc_dir
		fi
		cp quantum_espresso_example/pw.x quantum_espresso_example/*.UPF $calc_dir
		ecut_ryd=$(bc<<<${ecut_ev}*${ryd_per_ev})
		python generate_scf_input_file.py $calc_dir $system $ecut_ryd $Nk $Ns
	done
