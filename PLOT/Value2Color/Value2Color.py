#!/usr/bin/env python3

"""

    Map color based on input value.
    @Author: wavefancy@gmail.com

    Usage:
        Value2Color.py -k int [--cmax int] [-r] [-n cname] [--rl float] [--rr float]
        Value2Color.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read results from stdin, and output results to stdout.
        2. See example by -f.

    Options:
        -k int        Color index for input value.
        --cmax int    Color scale max value, set all the input value larger than this as this value.
        --rl float    Set color range left end, default min(inputValues).
        --rr float    Set color range right end, default max(inputValues).
        -r            Replace the value as color, otherwise append the color value at the line end.
        -n cname      Color scale name, default YlOrRd, full list:
                      https://plot.ly/ipython-notebooks/color-scales/
        -h --help     Show this screen.
        -v --version  Show version.
        -f --format   Show input/output file format example.
"""
import sys
from docopt import docopt
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE, SIG_DFL)

def ShowFormat():
    '''Input File format example:'''
    print('''
    #input example
    ------------------------
c1  1   10  1
c2  2   -5  3
c3  5   3   2
    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    #print(args)

    # add regression line to scatter plot
    # https://plot.ly/python/linear-fits/

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    col = int(args['-k']) -1
    indata = []
    zcolor = []
    for line in sys.stdin:
        line = line.strip()
        if line:
            ss = line.split()
            try:
                x = float(ss[col])

                indata.append(ss)
                zcolor.append(x)

            except ValueError:
                sys.stdout.write('Warning: Parse Value Error (Skipped): %s\n'%(line))


    #print(zcolor)
    #color max
    cmax = max(zcolor)
    if args['--cmax']:
        cmax = int(args['--cmax'])
        zcolor = [ cmax if x >= cmax else x for x in zcolor]

    import colorlover as cl
    from numpy import interp
    import webcolors
    #https://plot.ly/ipython-notebooks/color-scales/
    #define color map.
    colorName = 'YlOrRd'
    if args['-n']:
        colorName = args['-n']
    color = cl.scales['9']['seq'][colorName]

    #map color to 500 bins, convert to rgb and then to numberic format of rgb.
    c500 = cl.to_numeric(cl.to_rgb(cl.interp( color, 500 )))
    #rgb to hex format.
    c500 = [webcolors.rgb_to_hex((int(x[0]), int(x[1]), int(x[2]))) for x in c500]

    vrange=[min(zcolor), max(zcolor)]
    if args['--rl']:
        vrange[0] = float(args['--rl'])
    if args['--rr']:
        vrange[1] = float(args['--rr'])
    #value to color.
    cindex = [interp(x, vrange, [0,499]) for x in zcolor]
    oColor = [c500[int(x)] for x in cindex]
    #oColor = [cl.to_numeric(c500[int(x)]) for x in cindex]

    if args['-r']:
        for x, y in zip(indata, oColor):
            x[col] = y
            sys.stdout.write('%s\n'%('\t'.join(x)))
    else:
        for x,y in zip(indata, oColor):
            x.append(y)
            sys.stdout.write('%s\n'%('\t'.join(x)))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
