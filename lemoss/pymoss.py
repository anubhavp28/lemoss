import subprocess as sp
import re
import os

C = 0
CPP = 1
PYTHON = 2

EXT = [
        ['.c', '.h'],
        ['.cpp', '.cc', '.cxx', '.c++', '.h', '.hh', '.hxx', '.hpp', '.h++'],
        ['.py'],
    ]

def run_moss(paths, language=C, base_file=None, by_dir=False, extensions=None):
    args = ['./moss']
    if type(paths) is str:
        paths = [paths]
    if by_dir:
        args.append('-d')
        if not extensions:
            extensions = EXT[language]
        paths = [os.path.join(x, '*%s' % ext) for ext in extensions for x in paths]
        args.extend(paths)
    else:
        args.extend(paths)
    cp = sp.run(args, stdout=sp.PIPE)
    out = cp.stdout.decode('ascii')
    match = re.search(r'https?:\/\/moss.stanford.edu\/results\/[0-9]+', out)
    if match:
        return match.group(0)
    return None

def run_moss_in_dir(directory, language=C, base_file=None, extensions=None):
    if not type(directory) is str:
        raise TypeError('directory argument to run_mos_in_dir() must be a string')
    if not os.path.isdir(directory):
        raise Exception('directory name passed to run_mos_in_dir() is invalid')
    directory = os.path.join(directory, '*', '')
    return run_moss(directory, language, base_file, True, extensions)

print(run_moss(['dfs.py', 'floyd.py'], language=PYTHON))
