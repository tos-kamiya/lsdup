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

def _check_content(files):
    hash2files = defaultdict(list)
    for f in files:
        hash2files[get_hash(f)].append(f)
    for h, fs in hash2files.items():
        if len(fs) >= 2:
            yield h, fs

def find_duplicated_files(files):
    size2files = defaultdict(list)
    for f in files:
        if is_regular_file(f):
            size2files[get_size(f)].append(f)
    for fs in size2files.values():
        yield from _check_content(fs)

def main():
    option_show_md5 = False
    files = sys.argv[1:]
    if files and files[0] == '-m':
        option_show_md5 = True
        del files[0]

    for h, fs in find_duplicated_files(files):
        if option_show_md5:
            for f in fs:
                print('%s %s' % (h, f))
        else:
            print('----\n%s' % '\n'.join(fs))


if __name__ == '__main__':
    main()
