#!/usr/bin/env python2

from ConfigParser import ConfigParser
import os
import re
import subprocess
import sys
from termcolor import colored


config = ConfigParser()

ANSI_ESCAPE_RE = re.compile(r'\x1b[^m]*m')
RANGE_RE = re.compile(r'(\d+)-(\d+)')
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

    try:
        return subprocess.check_output(args).strip()
    except:
        exit(1)


def hg_root():
    try:
        return subprocess.check_output(['hg', 'root']).strip()
    except:
        exit(1)


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


def to_int(val, max_num):
    num = int(val)
    if num <= 0:
        fail(val + ' is not a positive number')
    elif num > max_num:
        fail(val + ' is exceeds the number of files')

    return num


def substitute_filenames(files, args, shell_command):
    num_files = len(files)
    new_args = []
    double_dash_pos = None
    for i, arg in enumerate(args):
        # After a '--' don't replace any numbers
        if arg == '--':
            double_dash_pos = i
            break

        try:
            m = RANGE_RE.match(arg)
            if m:
                start, end = m.group(1, 2)
                start, end = to_int(start, num_files), to_int(end, num_files)
                for i in range(start, end + 1):
                    new_args.append(files[i - 1])
            else:
                num = to_int(arg, num_files)
                new_args.append(files[num - 1])
        except ValueError:
            new_args.append(arg)

    if double_dash_pos != None:
        # This is safe because out of bounds slicing isn't an error
        new_args.extend(args[double_dash_pos + 1:])

    if not shell_command:
        new_args.insert(0, 'hg')

        if config_getboolean('color', False):
            new_args.extend(['--color', 'always'])

    return new_args


def prepend_numbers(lines):
    output = []
    for i, l in enumerate(lines.split('\n')):
        output.append(str(i + 1) + ' ' + l)

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


def print_usage():
    print 'usage: %s [-h] [-c] command [-- other_args]' % os.path.basename(sys.argv[0])


def main():
    load_config()

    shell_command = False
    if len(sys.argv) > 1:
        if sys.argv[1] == '-c':
            shell_command = True
        elif sys.argv[1] in ['-h', '--help']:
            print_usage()
            exit(0)

    if len(sys.argv) == 1 or sys.argv[1] in ['st', 'status']:
        status_output = hg_status()
        save_status_output(status_output)
        if status_output != '':
            print prepend_numbers(status_output)
    else:
        files = get_filenames()
        args = sys.argv[2:] if shell_command else sys.argv[1:]
        new_args = substitute_filenames(files, args, shell_command)
        print ' '.join(new_args)
        try:
            cmd_output = subprocess.check_output(new_args, cwd=hg_root()).strip()
            if cmd_output != '':
                print cmd_output
        except:
            exit(1)


if __name__ == '__main__':
    main()
