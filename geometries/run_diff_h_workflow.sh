#!/bin/bash

base_path="hBN_water_geometries/supercells_one_water"
system="hBN_water_Oup_Hdown"
diff_h_folder="diff_h"
Ns=3

if [ ! -d "${base_path}/${diff_h_folder}" ]; then
	mkdir ${base_path}/${diff_h_folder}
fi

for h in 2.9907 3.1944 3.3889 3.5926 3.7963 4.5000 5.0093 6.0093
	do
		python generate_diff_h.py ${base_path}/${system}_${Ns}x${Ns}x1_supercell.xyz $diff_h_folder $h 
	done
