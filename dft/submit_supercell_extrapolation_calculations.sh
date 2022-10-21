#!/bin/bash
#SBATCH --job-name="Ns-extrapolation"
#SBATCH --time=08:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=128
#SBATCH --ntasks-per-core=1
#SBATCH --constraint=rome 
#SBATCH --partition=ccq
#SBATCH --output=err_out_files/Ns-extrapolation.out
#SBATCH --error=err_out_files/Ns-extrapolation.err

export OMP_NUM_THREADS=128
ulimit -s unlimited

module purge
module load slurm
module load quantum_espresso/7.1_nix2_gnu_ompi
source ~/venv-rocky8-iron-project/bin/activate

base_dir=supercell_extrapolation_calculations
system=hBN_water_Oup_Hdown
functional=pbe
ecp=paw
ecut_ev=700
Nk=3

for Ns in 1 2 3 4 5
	do
		echo "Now starting KS-DFT for ${system} with ${functional}, ${ecp}, ecut = ${ecut_ev} eV, Nk = ${Nk}, and Ns = ${Ns}"
		calc_dir=${base_dir}/${system}_${functional}_${ecp}_ecut_${ecut_ev}_Nk_${Nk}_Ns_${Ns}
		cd $calc_dir
		start_time=`date +%s`
		srun --threads-per-core=$OMP_NUM_THREADS pw.x < scf.in > scf.out
		echo "Runtime = $(expr `date +%s` - $start_time) sec"
		cd ../..
	done
