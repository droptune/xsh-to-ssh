#!/bin/python
import sys
import re
import os


def get_files_from_dir(path, extension):
    filelist = []
    extension_check = re.compile('\.'+extension, re.I)
    path = os.path.abspath(path)
    dir_contents = os.listdir(path)

    for filename in dir_contents:
        fullname = os.path.join(path, filename)
        if os.path.isdir(fullname):
            filelist.extend(get_files_from_dir(fullname, extension))
            continue
        if extension_check.search(filename):
            filelist.append(fullname)

    return filelist

def xsh_to_ssh(xsh_file):
    values = {}
    param_and_value = re.compile('(.*)=(.*)')
    with open(xsh_file, encoding='ascii', errors='replace') as xsh:
        for line in xsh:
            if line.startswith('['):
                continue
            match = param_and_value.search(line)
            values[match.group(1)] = match.group(2)

    if values['Protocol'] != 'SSH':
        return 1
    print('Host ' + os.path.basename(xsh_file)[:-4])
    print('\tHostName ' + values['Host'])
    print('\tPort ' + values['Port'])
    print('\tUser ' + values['UserName'])

def main(argv):
    extension = 'xsh'
    filelist = []
    working_dir = argv[1]

    filelist = get_files_from_dir(working_dir, extension)

    for xsh in filelist:
        xsh_to_ssh(xsh)
        print('\n')

if __name__ == '__main__':
    main(sys.argv)

