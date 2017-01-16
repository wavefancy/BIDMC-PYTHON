#!/usr/bin/env python3

"""

    Plot category data using plotly library.
    @Author: wavefancy@gmail.com

    Usage:
        CategoryPlot2.py -x xtitle -y ytitle -o outname [--yerr ycol] [--yr yrange] [--vl vline] [--hl hline] [--ab abline] [--ms msize] [--mt mtype] [--lloc lloc] [--lfs lfs] [--lm lmargin]
        CategoryPlot2.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read results from stdin, and output results to stdout.
        2. See example by -f.

    Options:
        -x xtitle
        -y ytitle
        -o outname    Output file name: output.html.
        --yerr yecol  Column index for y error bar.
        --yr yrange   Set the yAxis plot range: float1,float2.
        --hl hline    Add horizontal lines: float1,float2.
        --vl vline    Add vertical lines: float1,float2...
        --ab abline   Add ablines: x1_y1_x2_y2_color,...
        --ms msize    Set marker size: float, default 5.
        --mt mtype    Set marker type: 1 dot(default), 2 line, 3 dot + line.
        --lloc lloc   Legend location:
                        1 left_top, 2 right_top, 3 left_bottom, 4 right_bottom, 0 no legend.
        --lfs lfs     Legend font size.
        --lm lmargin  Left margin, default 60.
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
    #Output from: FamilyHitByGene.py
    ------------------------
c1  1   10  1
c2  2   -5  3
c3  5   3   2
COMMAND vl  3
COMMAND vl  4

    #output:
    ------------------------
    FamilyName      #SeqMember      #hitGeneNum     GeneList
    S55     3       5       CHRNA7-chr15-3  NCAM2-chr21-3
    FGJG1   3       4       JAK3-chr19-2    KRT3-chr12-3    NKD2-chr5-4     MKLN1-chr7-1
    FGEG    3       21      RET-chr10-2-Auto-Dominant-CAKUT COLEC12-chr18-6 NUDT6-chr4-2    C6or
    f222-chr6-5
    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='2.2')
    # version 2.2: add the option for abline.
    print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    errYCol = '' #value column for error bar for Y.
    xtitle = args['-x']
    ytitle = args['-y']
    outname = args['-o']
    mode = 'markers' #markers or lines
    hlines = [] #location for horizontal lines.
    vlines = []
    msize = 5
    lm = 60    #left margin.

    yrange = []
    if args['--yerr']:
        errYCol = int(args['--yerr']) -1
    if args['--yr']:
        yrange = list(map(float, args['--yr'].split(',')))
    if args['--hl']:
        hlines = list(map(float, args['--hl'].split(',')))
    if args['--vl']:
        vlines = list(map(float, args['--hl'].split(',')))
    if args['--ms']:
        msize = float(args['--ms'])
    if args['--mt']:
        if args['--mt'] == '2':
            mode = 'lines'
        elif args['--mt'] == '3':
            mode = 'lines+markers'
    if args['--lm']:
        lm = float(args['--lm'])

    xanchor = 'right'
    yanchor = 'bottom'
    xlloc = 0.99
    ylloc = 0
    if args['--lloc']:
        if args['--lloc'] == '1':
            yanchor = 'top'
            xanchor = 'left'
            xlloc = 0.01
            ylloc = 0.99
        elif args['--lloc'] == '2':
            yanchor = 'top'
            xlloc = 0.99
            ylloc = 0.99
        elif args['--lloc'] == '3':
            yanchor = 'bottom'
            xanchor = 'left'
            xlloc = 0.01
            ylloc = 0.01
        elif args['--lloc'] == '4':
            yanchor = 'bottom'
            xanchor = 'right'
            xlloc = 0.99
            ylloc = 0.01

    ablines = []
    abcolor = '#EA3232' #line color for ablines, if not set from command line.
    if args['--ab']:
        for x in args['--ab'].split(','):
            ablines.append(x.split('_'))

    lfontSize = 10
    if args['--lfs']:
        lfontSize = int(args['--lfs'])

    from collections import OrderedDict
    xdata = OrderedDict() #{categoryName -> []}
    ydata = OrderedDict() #{categoryName -> []}
    errY  = {} #{categoryName -> []} error bar for Y.ss
    commands = {'vl'}

    def addData(dictName,keyName,val):
        '''add data to a dict'''
        if keyName not in dictName:
            dictName[keyName] = []
        dictName[keyName].append(val)

    for line in sys.stdin:
        line = line.strip()
        if line:
            ss = line.split()
            if ss[0]=='COMMAND' and ss[1] in commands:
                if ss[1] == 'vl':
                    vlines.append(float(ss[2]))
            else:
                try:
                    x = float(ss[1])
                    y = float(ss[2])
                    if errYCol and len(ss) >= errYCol +1:
                        z = float(ss[errYCol])
                        addData(errY,ss[0],z)
                    addData(xdata, ss[0], x)
                    addData(ydata, ss[0] ,y)
                except ValueError:
                    sys.stderr.write('Warning: parse value error: %s\n'%(line))

    plotData = []
    import plotly
    import plotly.plotly as py
    import plotly.graph_objs as go

    marker = dict(
        size = msize,
        # line = dict(
        #     width = 1,
        #     color = 'white'
        # )
     )

    for k in xdata.keys():
        if k in errY:
            plotData.append(
                go.Scatter(
                x=xdata[k],
                y=ydata[k],
                name = k,
                mode = mode,
                marker = marker,
                error_y=dict(
                    type='data',
                    array=errY[k],
                    visible=True,
                    color='#E1DFDF',
                    thickness=1,
                    )
            ))
        else:
            plotData.append(
                go.Scatter(
                x=xdata[k],
                y=ydata[k],
                marker = marker,
                name=k,
                mode = mode,
            ))

    layout = {
        'margin': {
            'l' : lm,
            'b' : 40,
            'r' : 10,
            't' : 10
        },
        'xaxis':{
            'autotick': True,
            'mirror'  :True,
            #       range=[0, 500],
            'showgrid':True,
            'showline':True,
            'ticks'   : 'outside',
            'showticklabels' : True,
            'title'   : xtitle,
            'zeroline':False
        },
        'yaxis':{
            'autotick': True,
            'mirror'  :True,
            'range'   :yrange,
            'showgrid':True,
            'showline':True,
            'ticks'   : 'outside',
            'showticklabels' : True,
            'title'   : ytitle,
            'zeroline':False
        },
    }
    # update legend info.
    legend = go.Layout(
        showlegend=False
    )
    if args['--lloc'] != '0':
        legend={
            'legend':{
                'xanchor': xanchor,
                'x': xlloc,
                'y': ylloc,
                'yanchor': yanchor,
                'font': {
                    'size' : lfontSize
                },
            }
        }

    layout.update(legend)

    hl_data = []
    if hlines:
        for y in hlines:
            hl_data.append(
                {
                    'type': 'line',
                    'xref': 'paper',
                    'x0': 0,
                    'y0': y,
                    'x1': 1,
                    'y1': y,
                    'line': {
                        #'color': 'rgb(50, 171, 96)',
                        #'color': '#E2E2E2',
                        'color': 'rgba(0, 0, 0, 0.5)',
                        'width': 1,
                        'dash': 'dashdot',
                }}
            )
        #h = {'shapes':hl_data}
        #layout.update(h)

    #add for ablines
    ab_data = []
    if ablines:
        for y in ablines:
            #print(y)
            cc = abcolor
            if len(y) == 5:
                cc = y[4]

            ab_data.append(
                {
                    'type': 'line',
                    # 'xref': 'paper',
                    'x0': y[0],
                    'y0': y[1],
                    'x1': y[2],
                    'y1': y[3],
                    'line': {
                        'color': cc,
                        #'color': 'rgba(0, 0, 0, 0.5)',
                        'width': 2,
                        # 'dash': 'dashdot',
                    }
                }
            )

    vl_data = []
    if vlines:
        for y in vlines:
            vl_data.append(
                {
                    'type': 'line',
                    'yref': 'paper',
                    'x0': y,
                    'y0': 0,
                    'x1': y,
                    'y1': 1,
                    'line': {
                        'color': '#FFD979',
                        'width': 2,
                        'dash': 'dashdot',
                }}
            )
        #h = {'shapes':vl_data}
        #layout.update(h)
    alllines = hl_data + vl_data + ab_data
    if alllines:
        h = {'shapes':alllines}
        layout.update(h)

    #output the last one
    plotly.offline.plot({'data': plotData,'layout': layout}
         ,show_link=False
         ,auto_open=False
         ,filename=outname
    )
    #fig = go.Figure(data=plotData, layout=layOut)
    #py.image.save_as(fig,outname,width='10in',height='3in')
    #py.image.save_as(fig,outname,width=700,height=500)

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
