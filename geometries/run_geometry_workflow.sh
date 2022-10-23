#!/bin/bash

system=hBN

for Ns in 6 7 8 9 10
	do
		python generate_supercells_pymatgen.py $system $Ns
		python convert_POSCAR_to_xyz_ase.py $system $Ns
	done
