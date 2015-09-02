#!/usr/bin/env python2

from ConfigParser import ConfigParser
import os
import re
import subprocess
import sys
from termcolor import colored


config = ConfigParser()

ANSI_ESCAPE_RE = re.compile(r'\x1b[^m]*m')
ID_FILE = 'hgnids.txt'
CONFIG_FILE = '.hgnrc'


def fail(msg):
    print colored(msg, 'red')
    sys.exit(1)


def id_file_path():
    return os.path.join(hg_root(), '.hg', ID_FILE)


def config_file_path():
    return os.path.join(os.path.expanduser('~'), CONFIG_FILE)


def hg_status():
    args = ['hg', 'st']
    if config_getboolean('color', False):
        args.extend(['--color', 'always'])

    return subprocess.check_output(args).strip()


def hg_root():
    return subprocess.check_output(['hg', 'root']).strip()


def get_filenames():
    path = id_file_path()
    if not os.path.exists(path):
        fail(path + " doesn't exist. Run hg-number with no arguments first to generate this file.")

    with open(path) as f:
        status_output = f.read()
        lines = status_output.split('\n')
        return map(lambda l: l.split(' ')[1], lines)


def save_status_output(status_output):
    # Strip colors
    status_output = ANSI_ESCAPE_RE.sub('', status_output)

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


def prepend_numbers(lines):
    output = []
    i = 1
    for l in lines.split('\n'):
        output.append(str(i) + ' ' + l)
        i += 1

    return '\n'.join(output)


def load_config():
    global config

    path = config_file_path()
    if os.path.exists(path):
        with open(path) as f:
            config.read(path)


def config_get(name, default, func):
    if config.has_option('main', name):
        return func('main', name)
    else:
        return default


def config_getboolean(name, default):
    return bool(config_get(name, default, config.getboolean))


def main():
    load_config()
    if len(sys.argv) == 1:
        status_output = hg_status()
        save_status_output(status_output)
        if status_output != '':
            print prepend_numbers(status_output)
    else:
        files = get_filenames()
        new_args = substitute_filenames(files)
        print ' '.join(new_args)
        subprocess.check_output(new_args, cwd=hg_root())


if __name__ == '__main__':
    main()
