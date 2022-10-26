#!/bin/bash
#SBATCH --job-name="water_Oleft_Hright_pbe_paw_ecut_700_Nk_3_Ns_1"
#SBATCH --time=1-00:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=128
#SBATCH --ntasks-per-core=1
#SBATCH --constraint=rome 
#SBATCH --partition=ccq
#SBATCH --output=err_out_files/water_Oleft_Hright_pbe_paw_ecut_700_Nk_3_Ns_1.out
#SBATCH --error=err_out_files/water_Oleft_Hright_pbe_paw_ecut_700_Nk_3_Ns_1.err
#SBATCH --mail-type=fail
#SBATCH --mail-user=kevingk2@illinois.edu

export OMP_NUM_THREADS=1
ulimit -s unlimited

module purge
module load slurm
module load quantum_espresso/7.1_nix2_gnu_ompi
source ~/venv-rocky8-iron-project/bin/activate

cd water_reference_calculations/water_Oleft_Hright_pbe_paw_ecut_700_Nk_3_Ns_1
time mpirun -np 128 pw.x -i scf.in > scf.out
