from convert import convert_serum_to_waveedit
import glob
import os


def main():
    cwd = os.getcwd()
    input_dir = cwd + '/serum'
    output_dir = cwd + '/converted'
    input_files = glob.glob(input_dir + '/**/*.wav', recursive=True)
    for file in input_files:
        rel_file = file.replace(input_dir + '/', '')
        output_file = output_dir + '/' + rel_file
        print("Converting " + rel_file)
        convert_serum_to_waveedit(file, output_file)


if __name__ == '__main__':
    main()
