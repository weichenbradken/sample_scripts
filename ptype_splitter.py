import os
import argparse
from functools import partial
from multiprocessing import Pool, cpu_count


def load_file(file, path, file_pattern, split):
    tally = [0]*2
    with open(file, 'r') as f:
        file_list = []
        sub_file_lines = []
        s = file_pattern.split('*')
        s[0] = os.path.join(path, s[0])
        file_timestep = int(file[len(s[0]):-len(s[1])])
        lines = f.readlines()

        for i in split:
            file_list.append(open(s[0] + '_'.join([str(j) for j in i]) + '_' + str(file_timestep) + '.liggghts', 'w'))
            sub_file_lines.append(lines[:9])

        for line in lines[9:]:
            split_line = line.split(' ')
            atom_type = 0 if int(split_line[1]) in split[0] else 1
            tally[atom_type] += 1
            sub_file_lines[atom_type].append(line)

        for sub_file in range(len(sub_file_lines)):
            sub_file_lines[sub_file][3] = str(tally[sub_file]) + '\n'
            file_list[sub_file].writelines(sub_file_lines[sub_file])
        for file in file_list:
            file.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Input file path for splitting.')
    parser.add_argument('--path', metavar='path', type=str, nargs=1, required=True,
                        help='The path to the file containing LIGGGHTS output files.')
    parser.add_argument('--pattern', metavar='ptn', type=str, nargs=1, required=True,
                        help='The pattern of the sequence (e.g. mill_*.liggghts)')

    args = parser.parse_args()

    # split1=(1, 2)
    # split2=(3, 4)

    split1=[1]
    split2=[2]
    # wei added below
    split3=[3]

    files = os.listdir(args.path[0])
    start, end = args.pattern[0].split('*')
    files = [os.path.join(args.path[0], f) for f in files if f.startswith(start) and f.endswith(end)]

    with Pool(processes=cpu_count()) as pool:
        pool.map(partial(load_file, path=args.path[0], file_pattern=args.pattern[0], split=(split1, split2)), files)
