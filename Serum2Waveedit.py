from convert import convert_serum_to_waveedit
import glob
import os

cwd = os.getcwd()
input_dir = os.path.join(cwd, 'serum')
output_dir = os.path.join(cwd, 'converted')

input_files = glob.glob(os.path.join(input_dir, '**', '*.wav'), recursive=True)
for file in input_files:
    rel_file = file.replace(os.path.join(input_dir, ''), '')
    output_file = os.path.join(output_dir, rel_file)
    print("Converting " + rel_file)
    convert_serum_to_waveedit(file, output_file)

input("Press Enter to close...")
