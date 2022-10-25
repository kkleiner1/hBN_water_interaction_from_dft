import sys
import numpy as np


def generate_submission_script_as_giant_string(base_dir, calc_dir):
    giant_string = f"""#!/bin/bash
#SBATCH --job-name="{calc_dir}"
#SBATCH --time=1-00:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=128
#SBATCH --ntasks-per-core=1
#SBATCH --constraint=rome 
#SBATCH --partition=ccq
#SBATCH --output=err_out_files/{calc_dir}.out
#SBATCH --error=err_out_files/{calc_dir}.err
#SBATCH --mail-type=fail
#SBATCH --mail-user=kevingk2@illinois.edu

export OMP_NUM_THREADS=1
ulimit -s unlimited

module purge
module load slurm
module load quantum_espresso/7.1_nix2_gnu_ompi
source ~/venv-rocky8-iron-project/bin/activate

cd {base_dir}/{calc_dir}
time mpirun -np 128 pw.x -i scf.in > scf.out"""
    return giant_string


base_dir = str(sys.argv[1])
calc_dir = str(sys.argv[2])


with open(f"{calc_dir}.sh", "w") as quantum_espresso_submission_script:
    sys.stdout = quantum_espresso_submission_script
    giant_string = generate_submission_script_as_giant_string(base_dir, calc_dir)
    print(giant_string)
