import sys
import numpy as np


def extract_supercell_lattice_vectors(file_line_with_lattice_vectors):
    # Line looks like the following:
    # Lattice="5.00909 0.0 0.0 0.0 4.338 0.0 0.0 0.0 30.0" Properties=species:S:1:pos:R:3 pbc="T T T"
    first_quote_index = file_line_with_lattice_vectors.find('"')
    second_quote_index = file_line_with_lattice_vectors.find('"', first_quote_index + 1)
    supercell_lattice_vectors_components = file_line_with_lattice_vectors[
        first_quote_index + 1 : second_quote_index
    ].split(" ")
    i = 3
    while i < len(supercell_lattice_vectors_components):
        supercell_lattice_vectors_components.insert(i, "\n")
        i += 4
    supercell_lattice_vectors = ""
    for component in supercell_lattice_vectors_components:
        if component == "\n":
            supercell_lattice_vectors += f"{component}"
        else:
            supercell_lattice_vectors += f"{component} "
    return supercell_lattice_vectors


def extract_atomic_positions(file_lines_with_atomic_positions):
    atomic_positions = ""
    for line in file_lines_with_atomic_positions:
        if (
            file_lines_with_atomic_positions.index(line)
            == len(file_lines_with_atomic_positions) - 1
        ):
            atomic_positions += f"{line}"
        else:
            atomic_positions += f"{line}\n"
    return atomic_positions


def extract_geometry_info(system, Ns):
    if "water" in system:
        if "hBN" in system:
            dir = f"../geometries/hBN_water_geometries/"
        else:
            dir = f"../geometries/water_geometries/"
    else:
        dir = f"../geometries/{system}_geometries/"
    geometry_file = dir + f"{system}_{Ns}x{Ns}x1_supercell.xyz"
    file_lines = open(geometry_file, "r").read().splitlines()
    num_atoms = int(file_lines[0])
    supercell_lattice_vectors = extract_supercell_lattice_vectors(file_lines[1])
    atomic_positions = extract_atomic_positions(file_lines[2:])
    return num_atoms, supercell_lattice_vectors, atomic_positions


def generate_scf_input_as_giant_string(
    system, ecut_ryd, Nk, Ns, spin_deg=2, max_val_elec_per_atom=6
):
    num_atoms, supercell_lattice_vectors, atomic_positions = extract_geometry_info(
        system, Ns
    )
    num_types = len(np.unique(np.array([pos[0] for pos in atomic_positions.splitlines()])))
    num_bands = int(max_val_elec_per_atom * num_atoms / spin_deg)
    giant_string = f"""&control
 calculation='scf',
 restart_mode='from_scratch',
 prefix='{system}',
 outdir='.',
 pseudo_dir = '.',
/
&system
 ibrav=0,
 nat={num_atoms},
 ntyp={num_types},
 ecutwfc={ecut_ryd},
 occupations='fixed',
 nbnd={num_bands},
/
&electrons
/
CELL_PARAMETERS angstrom
{supercell_lattice_vectors}
ATOMIC_SPECIES
B 10.811 B.pbe-n-kjpaw_psl.1.0.0.UPF
N 14.0067 N.pbe-n-kjpaw_psl.1.0.0.UPF
O 15.999 O.pbe-n-kjpaw_psl.1.0.0.UPF
H 1.00784 H.pbe-kjpaw_psl.1.0.0.UPF
ATOMIC_POSITIONS angstrom
{atomic_positions}
K_POINTS automatic
{Nk} {Nk} 1 0 0 0"""
    return giant_string

dir = str(sys.argv[1])
system = str(sys.argv[2])
ecut_ryd = float(sys.argv[3])
Nk = int(sys.argv[4])
Ns = int(sys.argv[5])

with open(f"{dir}/scf.in", "w") as scf_input_script:
    sys.stdout = scf_input_script
    giant_string = generate_scf_input_as_giant_string(system, ecut_ryd, Nk, Ns)
    print(giant_string)