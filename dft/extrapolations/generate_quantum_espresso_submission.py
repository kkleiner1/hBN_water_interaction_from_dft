import sys
import numpy as np


def generate_submission_script_as_giant_string(base_dir, calc_dir):
    giant_string = f"""#!/bin/bash
#SBATCH --job-name="{calc_dir}"
#SBATCH --time=08:00:00
#SBATCH --nodes=1
#SBATCH --cpus-per-task=128
#SBATCH --constraint=rome 
#SBATCH --partition=ccq
#SBATCH --output=err_out_files/{calc_dir}.out
#SBATCH --error=err_out_files/{calc_dir}.err

export OMP_NUM_THREADS=128
ulimit -s unlimited

module purge
module load slurm
module load quantum_espresso/7.1_nix2_gnu_ompi
source ~/venv-rocky8-iron-project/bin/activate

cd {base_dir}/{calc_dir}
start_time=`date +%s`
srun --threads-per-core=$OMP_NUM_THREADS pw.x < scf.in > scf.out
echo `Runtime = $(expr `date +%s` - $start_time) sec'"""
    return giant_string


base_dir = str(sys.argv[1])
calc_dir = str(sys.argv[2])


with open(f"{calc_dir}.sh", "w") as quantum_espresso_submission_script:
    sys.stdout = quantum_espresso_submission_script
    giant_string = generate_submission_script_as_giant_string(base_dir, calc_dir)
    print(giant_string)
