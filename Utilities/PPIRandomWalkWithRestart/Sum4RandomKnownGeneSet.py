#!/usr/bin/env python3

"""

    Compute the sum of the gene ranking score of known gene set or random gene set.
    @Author: wavefancy@gmail.com

    Usage:
        Sum4RandomKnownGeneSet.py ([-k file] | [-s int -r int])
        Sum4RandomKnownGeneSet.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read data from stdin, and output results to stdout.
        2. Input data format: two columns, gene_name and ranking score.


    Options:
        -k file       Known gene set. One gene name one line.
        -s int        The number of genes for random selection.
        -r int        The number of times for repeating the random selection process.
        -h --help     Show this screen.
        -v --version  Show version.
        -f --format   Show input/output file format example.

"""
import sys
from docopt import docopt
import signal
signal.signal(signal.SIGPIPE, signal.SIG_DFL)

def ShowFormat():
    '''File format example'''
    print('''
    #Input example
    ------------------------
    "
    123 # comments #
    456 # multiple
    line
    comments#
    // line comments
    789
    !new line
    "
    "123 # comments# 456 789"

    #Output example
    ------------------------
    123  456 789
          ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='2.0')
    #version 2.0
    #1. add function for line comments.

    commentDelimeter = '#'
    linecomment = '//'
    linebreaker = '!'

    if args['-d']:
        commentDelimeter = args['-d']
    if args['-l']:
        linecomment = args['-l']
    if args['-b']:
        linebreaker = args['-b']
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    #split by lines.
    import re
    lines = args['<string>'].strip()
    lines = lines.split(commentDelimeter)
    if len(lines) %2 == 0:
        sys.stderr.write('Error: Comment delimter should be appeared in pair!.\n')
        sys.exit(-1)

    #skip comments
    arr2 = []
    for i in range(0,len(lines),2):
        arr2.append(lines[i])

    #remove line breakers.
    arr1 = []
    for x in arr2:
        if x:
            for y in x.splitlines():
                y = y.strip()
                #compatible with bash line breaker.
                y = y.strip('\\')
                if not y.startswith(linecomment): #skip line commented line.
                    arr1.append(y)

    out = ' '.join(arr1)
    out = re.sub(r'\s+',' ',out)
    out = out.split(linebreaker)
    for x in out:
        x = x.strip()
        sys.stdout.write('%s\n'%(x))

    # if len(lines) == 1:
    #     lines = re.split('\\\\n',lines[0])

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
