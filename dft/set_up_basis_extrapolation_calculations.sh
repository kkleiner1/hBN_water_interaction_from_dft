#!/bin/bash

ryd_per_ev=0.0734986176
base_dir=basis_extrapolation_calculations
system=hBN_water_Oup_Hdown
Nk=1
Ns=1

if [ ! -d "${base_dir}" ]; then
	mkdir $base_dir
fi

for ecut_ev in 400 500 600 700 800
	do
		ecut_dir=${base_dir}/ecut_${ecut_ev}_ev
		if [ ! -d "${ecut_dir}" ]; then
			mkdir $ecut_dir
		fi
		cp quantum_espresso_example/pw.x quantum_espresso_example/*.UPF $ecut_dir
		ecut_ryd=$(bc<<<${ecut_ev}*${ryd_per_ev})
		python generate_scf_input_file.py $ecut_dir $system $ecut_ryd $Nk $Ns
	done
