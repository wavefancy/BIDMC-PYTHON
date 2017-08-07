#!/usr/bin/env python3

"""

    Map color based on input value.
    @Author: wavefancy@gmail.com

    Usage:
        Value2ColorV2.py -k int [-r] [-n cname] [--rl float] [--rr float]
        Value2ColorV2.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read results from stdin, and output results to stdout.
        2. See example by -f.

    Options:
        -k int        Color index for input value.
        --rl float    Set color range left end, default min(inputValues).
        --rr float    Set color range right end, default max(inputValues).
        -r            Reverse color map.
        -n cname      Color scale name, default Sequential.YlGnBu_4, full list:
                      https://jiffyclub.github.io/palettable/colorbrewer/
        -h --help     Show this screen.
        -v --version  Show version.
        -f --format   Show input/output file format example.

    API:
        Palette names please ref. https://jiffyclub.github.io/palettable/#matplotlib-colormap
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
    opacity = 1
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

    #API ref: https://stackoverflow.com/questions/28752727/map-values-to-colors-in-matplotlib
    #API ref: https://jiffyclub.github.io/palettable/colorbrewer/sequential/#previews
    #API ref: https://matplotlib.org/api/cm_api.html
    from palettable.colorbrewer.sequential import YlGnBu_4
    import matplotlib
    import matplotlib.cm as cm
    #ax.imshow(data, cmap=Blues_8.mpl_colormap)

    vrange=[min(zcolor), max(zcolor)]
    if args['--rl']:
        vrange[0] = float(args['--rl'])
    if args['--rr']:
        vrange[1] = float(args['--rr'])

    norm = matplotlib.colors.Normalize(vmin=vrange[0], vmax=vrange[1], clip=True)
    mapper = cm.ScalarMappable(norm=norm, cmap=YlGnBu_4.mpl_colormap)

    # if args['-r']:
    #     for x, y in zip(indata, oColor):
    #         x[col] = y
    #         sys.stdout.write('%s\n'%('\t'.join(x)))
    # else:
    for x,y in zip(indata, zcolor):
        x.append(str(mapper.to_rgba(y,alpha=opacity,bytes=True,norm=True)).replace(' ',''))
        sys.stdout.write('%s\n'%('\t'.join(x)))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
