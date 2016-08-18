#!/usr/bin/env python3

"""

    Count the number of columns for each line

    @Author: wavefancy@gmail.com

    Usage:
        LineColumns.py [-d delimeter]
        LineColumns.py -h | --help | -v | --version

    Notes:
        1. Read content from stdin, and output results to stdout.
        2. Line index start from 1.

    Options:
        -d string     Delimeter for columns. -d 'tab' for tab delimeter.
        -h --help     Show this screen.
        -v --version  Show version.

"""
import sys
from docopt import docopt
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL)

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    #print(args)

    de = None
    if args['-d']:
        de = args['-d']
        if de == 'tab':
            de = '\t'

    ln = 0
    for line in sys.stdin:
        ln += 1
        sys.stdout.write('%d\t%d\n'%(ln, len(line.split(de))))

    sys.stdout.flush()
    sys.stdout.close()
    sys.stderr.flush()
    sys.stderr.close()
