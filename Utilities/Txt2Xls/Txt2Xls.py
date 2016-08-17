#!/usr/bin/env python3

"""

    Convert text file to excel file.

    @Author: wavefancy@gmail.com

    Usage:
        Txt2Xls.py -o oname
        Txt2Xls.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read content from stdin, and output selected lines to stdout.
        2. Line index start from 1.

    Options:
        -o string     output file name.
        -n index      Set start line index, or Only copy this line to stdout if only this parameter in set.
        -e index      Set end line index, (inclusive).
        -a number     Set the end line as '-n index' + 'number', (inclusive).
        -r number     From start line, repeatly copy one line then skip 'number' lines, until reach file end.
        -f file       Read line index from 'file', one line one index, load all in memory.
        -h --help     Show this screen.
        -v --version  Show version.

"""
import sys
from docopt import docopt
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL)

class P(object):
    start = -1 # start line index
    end = -1 # end line index
    nskip = -1
    lineSet = set()
    maxLine = -1 #maximum line index need to be output.

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    print(args)
#
#     if(args['--format']):
#         ShowFormat()
#         sys.exit(-1)
# #
    outname = args['-o'] + '.xlsx'
    # if args['-n']:
    #     P.start = int(args['-n'])
    # if args['-e']:
    #     P.end = int(args['-e'])
    # if args['-a']:
    #     P.end = P.start + int(args['-a'])
    # if args['-r']:
    #     P.nskip = int(args['-r'])
    # if args['-f']:
    #     ll = [int(x) for x in open(args['-f'], 'r')]
    #     P.maxLine = max(ll)
    #     P.lineSet = set(ll)

    import xlsxwriter
    from xlsxwriter.utility import xl_rowcol_to_cell
    cell = xl_rowcol_to_cell(1, 2)  # C2

    # Create a workbook and add a worksheet.
    workbook = xlsxwriter.Workbook(outname)
    worksheet = workbook.add_worksheet()

    row = 0
    col = 0
    maxCol = 0
    for line in sys.stdin:
        line = line.strip()
        if line:
            ss = line.split()
            col = 0
            for x in ss:
                worksheet.write(row, col, x) #row col,
                col += 1
                if col > maxCol:
                    maxCol = col
            row += 1


    # Add a format. Light red fill with dark red text.
    # A2 : col row
    format1 = workbook.add_format({'bg_color': '#EEEEEE',
                               #'font_color': '#9C0006'
                               })



    for x in range(row-1):
        lcell = xl_rowcol_to_cell(x, 0)
        rcell = xl_rowcol_to_cell(x, maxCol)
        mcell = xl_rowcol_to_cell(x, 1)
        worksheet.conditional_format(lcell + ':' + rcell, {'type': 'cell',
                                            'criteria': '>=',
                                            'value':    mcell,
                                            'format':   format1})

    workbook.close()

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
