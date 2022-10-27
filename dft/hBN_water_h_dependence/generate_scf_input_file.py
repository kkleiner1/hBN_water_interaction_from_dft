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


def extract_geometry_info(system, Ns, h):
    h_formatted = "{:0.4f}".format(h)
    geom_dir = f"../../geometries/hBN_water_geometries/supercells_one_water/diff_h/"
    geometry_file = geom_dir + f"{system}_{Ns}x{Ns}x1_supercell_h_{h_formatted}.xyz"
    file_lines = open(geometry_file, "r").read().splitlines()
    num_atoms = int(file_lines[0])
    supercell_lattice_vectors = extract_supercell_lattice_vectors(file_lines[1])
    atomic_positions = extract_atomic_positions(file_lines[2:])
    return num_atoms, supercell_lattice_vectors, atomic_positions


def calc_min_num_bands(
    atomic_positions, H_val_el=1, B_val_el=3, N_val_el=5, O_val_el=6, spin_deg=2
):
    num_H = atomic_positions.count("H")
    num_B = atomic_positions.count("B")
    num_N = atomic_positions.count("N")
    num_O = atomic_positions.count("O")
    num_val_el = (
        num_H * H_val_el + num_B * B_val_el + num_N * N_val_el + num_O * O_val_el
    )
    min_num_bands = int(num_val_el / spin_deg) + 1
    return min_num_bands


def generate_scf_input_as_giant_string(system, functional, vdw_corr, ecut_ryd, Nk, Ns, h):
    num_atoms, supercell_lattice_vectors, atomic_positions = extract_geometry_info(
        system, Ns, h
    )
    num_types = len(
        np.unique(np.array([pos[0] for pos in atomic_positions.splitlines()]))
    )
    num_bands = calc_min_num_bands(atomic_positions) + 20
    giant_string = f"""&control
 calculation='scf',
 restart_mode='from_scratch',
 prefix='{system}',
 outdir='.',
 pseudo_dir='.',
/
&system
 ibrav=0,
 nat={num_atoms},
 ntyp={num_types},
 input_dft={functional},
 vdw_corr={vdw_corr},
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


base_dir = str(sys.argv[1])
calc_dir = str(sys.argv[2])
system = str(sys.argv[3])
functional = str(sys.argv[4])
vdw_corr = str(sys.argv[5])
ecut_ryd = float(sys.argv[6])
Nk = int(sys.argv[7])
Ns = int(sys.argv[8])
h = float(sys.argv[9])

with open(f"{base_dir}/{calc_dir}/scf.in", "w") as scf_input_script:
    sys.stdout = scf_input_script
    giant_string = generate_scf_input_as_giant_string(system, ecut_ryd, Nk, Ns, h)
    print(giant_string)
