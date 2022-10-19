#!/bin/bash

create_new_h_file () {
	old_xyz_path="${base_path}/hBN_water_Oup_Hdown_${Ns}x${Ns}x1_supercell.xyz"
	new_xyz_file="hBN_water_Oup_Hdown_${Ns}x${Ns}x1_supercell_h_${h}.xyz"
	new_xyz_path=${base_path}/${diff_h_folder}/${new_xyz_file}
	cp ${old_xyz_path} ${new_xyz_path}
}

determine_new_O_H_z_coord () {
	new_O_z_coord=$(bc<<<${old_sheet_z_coord}+${h})
	change_in_O_z_coord=$(bc<<<${new_O_z_coord}-${old_O_z_coord})
	new_H_z_coord=$(bc<<<${old_H_z_coord}+${change_in_O_z_coord})
}

base_path="hBN_water_geometries/supercells_one_water"
diff_h_folder="diff_h"
Ns=3
old_sheet_z_coord=6.00000000
old_O_z_coord=9.39999000
old_H_z_coord=8.81412000

if [ ! -d "${base_path}/${diff_h_folder}" ]; then
	mkdir ${base_path}/${diff_h_folder}
fi

for h in 2.9907 3.1944 3.3889 3.5926 3.7963 4.5000
	do
		create_new_h_file $base_path $diff_h_folder $Ns
		determine_new_O_H_z_coord $h $old_sheet_z_coord $old_O_z_coord $old_H_z_coord
		new_xyz_path="${base_path}/${diff_h_folder}/${new_xyz_file}"
		sed -i "" "s/${old_O_z_coord}/${new_O_z_coord}/g" ${new_xyz_path}
		sed -i "" "s/${old_H_z_coord}/${new_H_z_coord}/g" ${new_xyz_path}
	done
