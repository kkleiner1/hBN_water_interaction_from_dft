#!/bin/bash

system=$1

for Ns in 1 2 3 4 5
	do
		python generate_supercells_pymatgen.py $system $Ns
		python convert_POSCAR_to_xyz_ase.py $system $Ns
	done
