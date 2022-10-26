#!/bin/bash
#SBATCH --job-name="hBN_water_Oup_Hdown_pbe_paw_ecut_700_Nk_3_Ns_8_h_6.0093"
#SBATCH --time=1-00:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=128
#SBATCH --ntasks-per-core=1
#SBATCH --constraint=rome 
#SBATCH --partition=ccq
#SBATCH --output=err_out_files/hBN_water_Oup_Hdown_pbe_paw_ecut_700_Nk_3_Ns_8_h_6.0093.out
#SBATCH --error=err_out_files/hBN_water_Oup_Hdown_pbe_paw_ecut_700_Nk_3_Ns_8_h_6.0093.err
#SBATCH --mail-type=fail
#SBATCH --mail-user=kevingk2@illinois.edu

export OMP_NUM_THREADS=1
ulimit -s unlimited

module purge
module load slurm
module load quantum_espresso/7.1_nix2_gnu_ompi
source ~/venv-rocky8-iron-project/bin/activate

cd h_dependence_calculations/hBN_water_Oup_Hdown_pbe_paw_ecut_700_Nk_3_Ns_8_h_6.0093
time mpirun -np 128 pw.x -i scf.in > scf.out
