import sys


def extract_z_coords(geometry_fname):
    geometry_lines = open(geometry_fname, "r").read().splitlines()
    sheet_z = float(geometry_lines[-4].split(" ")[-1])
    O_z = float(geometry_lines[-3].split(" ")[-1])
    H_alpha_z = float(geometry_lines[-2].split(" ")[-1])
    H_beta_z = float(geometry_lines[-1].split(" ")[-1])
    return sheet_z, O_z, H_alpha_z, H_beta_z


def compute_new_z_coords(sheet_z, O_z, H_alpha_z, H_beta_z, h):
    O_z_new = sheet_z + h
    O_z_change = O_z_new - O_z
    H_alpha_z_new = H_alpha_z + O_z_change
    H_beta_z_new = H_beta_z + O_z_change
    return O_z_new, H_alpha_z_new, H_beta_z_new


def generate_new_geometry_as_giant_string(default_geometry_fname, h):
    sheet_z, O_z, H_alpha_z, H_beta_z = extract_z_coords(default_geometry_fname)
    O_z_new, H_alpha_z_new, H_beta_z_new = compute_new_z_coords(
        sheet_z, O_z, H_alpha_z, H_beta_z, h
    )
    giant_string = open(default_geometry_fname, "r").read()
    giant_string = giant_string.replace(str(O_z), str(O_z_new))
    giant_string = giant_string.replace(str(H_alpha_z), str(H_alpha_z_new))
    giant_string = giant_string.replace(str(H_beta_z), str(H_beta_z_new))
    return giant_string


default_geometry_path = str(sys.argv[1])
diff_h_folder = str(sys.argv[2])
h = float(sys.argv[3])
h_formatted = "{:0.4f}".format(h)

default_geometry_dir = "/".join(default_geometry_path.split("/")[:-1])
default_geometry_fname = default_geometry_path.split("/")[-1]
default_geometry_fname_minus_xyz = default_geometry_fname.replace(".xyz", "")
new_geometry_path = (
    f"{default_geometry_dir}/{diff_h_folder}/{default_geometry_fname_minus_xyz}_h_{h_formatted}.xyz"
)

with open(new_geometry_path, "w") as new_geometry_file_object:
    sys.stdout = new_geometry_file_object
    giant_string = generate_new_geometry_as_giant_string(default_geometry_path, h)
    print(giant_string)
