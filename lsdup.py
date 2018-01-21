from collections import defaultdict
import hashlib
import os
import stat
import sys

def is_regular_file(f):
    return not os.path.islink(f) and stat.S_ISREG(os.stat(f).st_mode)

def get_size(f):
    return os.stat(f).st_size

def get_hash(f):
    with open(f, 'rb') as inp:
        return hashlib.md5(inp.read()).hexdigest()

def _check_content(files, show_md5=False):
    hash2files = defaultdict(list)
    for f in files:
        hash2files[get_hash(f)].append(f)
    for h, fs in hash2files.items():
        if len(fs) >= 2:
            if show_md5:
                for f in fs:
                    print('%s %s' % (h, f))
            else:
                print('----\n%s' % '\n'.join(fs))

def find_duplicated_files(files, show_md5=False):
    size2files = defaultdict(list)
    for f in files:
        if is_regular_file(f):
            size2files[get_size(f)].append(f)
    for fs in size2files.values():
        _check_content(fs, show_md5)

def main():
    option_show_md5 = False
    files = sys.argv[1:]
    if files and files[0] == '-m':
        option_show_md5 = True
        del files[0]

    find_duplicated_files(files, option_show_md5)

if __name__ == '__main__':
    main()
