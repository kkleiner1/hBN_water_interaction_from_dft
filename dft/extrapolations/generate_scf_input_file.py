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
            geom_dir = f"../../geometries/hBN_water_geometries/supercells_one_water/"
        else:
            geom_dir = f"../../geometries/water_geometries/"
    else:
        geom_dir = f"../../geometries/{system}_geometries/"
    geometry_file = geom_dir + f"{system}_{Ns}x{Ns}x1_supercell.xyz"
    file_lines = open(geometry_file, "r").read().splitlines()
    num_atoms = int(file_lines[0])
    supercell_lattice_vectors = extract_supercell_lattice_vectors(file_lines[1])
    atomic_positions = extract_atomic_positions(file_lines[2:])
    return num_atoms, supercell_lattice_vectors, atomic_positions


def generate_atomic_species_info(
    functional, masses={"B": 10.811, "N": 14.0067, "O": 15.999, "H": 1.00784}
):
    atomic_species_info = ""
    for atom in masses:
        if "lda" in functional:
            pseudopotential_file = f"{atom}.pz-hgh.UPF"
        elif "pbe" in functional:
            pseudopotential_file = f"{atom}.pbe-hgh.UPF"
        elif "lyp" in functional:
            pseudopotential_file = f"{atom}.blyp-hgh.UPF"
        atomic_species_info += f"{atom} {masses[atom]} {pseudopotential_file}"
        if atom != list(masses.keys())[-1]:
            atomic_species_info += "\n"
    return atomic_species_info


def generate_scf_input_as_giant_string(
    system, functional, vdw_corr, ecut_ryd, Nk, Ns, spin_deg=2, max_val_elec_per_atom=6
):
    num_atoms, supercell_lattice_vectors, atomic_positions = extract_geometry_info(
        system, Ns
    )
    num_types = len(
        np.unique(np.array([pos[0] for pos in atomic_positions.splitlines()]))
    )
    num_bands = int(max_val_elec_per_atom * num_atoms / spin_deg)
    atomic_species_info = generate_atomic_species_info(functional)
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
 ecutwfc={ecut_ryd},
 input_dft='{functional}',
 vdw_corr='{vdw_corr}',
 occupations='fixed',
 nbnd={num_bands},
/
&electrons
/
CELL_PARAMETERS angstrom
{supercell_lattice_vectors}
ATOMIC_SPECIES
{atomic_species_info}
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

with open(f"{base_dir}/{calc_dir}/scf.in", "w") as scf_input_script:
    sys.stdout = scf_input_script
    giant_string = generate_scf_input_as_giant_string(system, functional, vdw_corr, ecut_ryd, Nk, Ns)
    print(giant_string)
