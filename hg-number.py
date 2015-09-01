#!/usr/bin/python2

import os
import subprocess
import sys
from termcolor import colored


ID_FILE = 'hgids.txt'


def fail(msg):
    print colored(msg, 'red')
    sys.exit(1)


def id_file_path():
    return hg_root() + '/.hg/' + ID_FILE


def hg_status():
    return subprocess.check_output(['hg', 'st']).strip()


def hg_root():
    return subprocess.check_output(['hg', 'root']).strip()


def get_filenames():
    path = id_file_path()
    if not os.path.exists(path):
        # TODO: Don't hardcode name
        fail(path + " doesn't exist. Run hg-number first to generate this file.")

    with open(path) as f:
        status_output = f.read()
        lines = status_output.split('\n')
        return map(lambda l: l.split(' ')[1], lines)


def save_status_output(status_output):
    with open(id_file_path(), 'w+') as f:
        f.write(status_output)


def substitute_filenames(files):
    num_files = len(files)
    new_args = []
    for arg in sys.argv:
        try:
            arg_int = int(arg)
            if arg_int <= 0:
                fail(arg + ' is not a positive number')
            elif arg_int > num_files:
                fail(arg + ' is exceeds the number of files')
            else:
                new_args.append(files[arg_int - 1])
        except ValueError:
            new_args.append(arg)

    new_args[0] = 'hg'

    return new_args


def main():
    if len(sys.argv) == 1:
        status_output = hg_status()
        save_status_output(status_output)
        print status_output
    else:
        files = get_filenames()
        new_args = substitute_filenames(files)
        print ' '.join(new_args)
        subprocess.check_output(new_args)


if __name__ == '__main__':
    main()
