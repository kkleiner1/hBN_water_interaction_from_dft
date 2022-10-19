from pymatgen.core import Structure
import sys


def determine_file_names(system, Ns):
	if "water" in system:
        	if "hBN" in system:
                	dir = f"hBN_water_geometries/"
        	else:
                	dir = f"water_geometries/"
	else:
        	dir = f"{system}_geometries/"
	primitive_cell_file = dir + f"POSCAR_{system}_primitive_cell"
	supercell_file = dir + f"POSCAR_{system}_{Ns}x{Ns}x1_supercell"
	return primitive_cell_file, supercell_file


system = str(sys.argv[1])
Ns = int(sys.argv[2])
primitive_cell_file, supercell_file = determine_file_names(system, Ns)

structure = Structure.from_file(primitive_cell_file)
structure.make_supercell([Ns, Ns, 1])
structure.to("poscar", supercell_file)
