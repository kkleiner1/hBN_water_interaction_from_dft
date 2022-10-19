from ase.io import read
import sys


def determine_file_names(system, Ns):
	if "water" in system:
		if "hBN" in system:
			dir = f"hBN_water_geometries/"
		else:
			dir = f"water_geometries/"
	else:
		dir = f"{system}_geometries/"
	poscar_file = dir + f"POSCAR_{system}_{Ns}x{Ns}x1_supercell"
	xyz_file = dir + f"{system}_{Ns}x{Ns}x1_supercell.xyz"
	return poscar_file, xyz_file


system = str(sys.argv[1])
Ns = int(sys.argv[2])
poscar_file, xyz_file = determine_file_names(system, Ns)

read(poscar_file).write(xyz_file)
