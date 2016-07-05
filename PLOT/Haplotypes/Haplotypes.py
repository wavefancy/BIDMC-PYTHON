#!/usr/bin/env python3

"""

    Plot haployptes by plotly library.
    @Author: wavefancy@gmail.com

    Usage:
        CategoryPlot2.py -x xtitle -y ytitle -o outname [--yerr ycol] [--yr yrange] [--vl vline] [--hl hline] [--ms msize] [--mt mtype] [--lloc lloc] [--lfs lfs] [--lm lmargin]
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
        --vl vline    Add vertical lines: float1, float2...
        --ms msize    Set marker size: float, default 5.
        --mt mtype    Set marker type: 1 dot(default), 2 line, 3 dot + line.
        --lloc lloc   Legend location: 2 right_top, 3 left_bottom.
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
    args = docopt(__doc__, version='1.0')
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
    colors = ['#31627B','#419F8D','#C9E14F','#FCE532','#FC8E32','']

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
        if args['--lloc'] == '2':
            yanchor = 'top'
            xlloc = 0.99
            ylloc = 0.99
        elif args['--lloc'] == '3':
            yanchor = 'bottom'
            xanchor = 'left'
            xlloc = 0.01
            ylloc = 0.01

    lfontSize = 10
    if args['--lfs']:
        lfontSize = int(args['--lfs'])

    from collections import OrderedDict
    xdata = OrderedDict() #{categoryName -> []}
    ydata = OrderedDict() #{categoryName -> []}
    errY  = {} #{categoryName -> []} error bar for Y.ss
    commands = {'vl'}

    data = []
    for line in sys.stdin:
        line = line.strip()
        if line:
            ss = line.split()
            if ss[0]=='COMMAND' and ss[1] in commands:
                if ss[1] == 'vl':
                    vlines.append(float(ss[2]))
            else:
                data.append(ss)

    plotData = []
    import plotly
    import plotly.plotly as py
    import plotly.graph_objs as go

    xtickName = data[0][1:]
    x_data = [[1]*(len(x)-1) for x in data[1:]]
    y_data = [x[0] for x in data[1:]]
    alleles = [x[1:] for x in data[1:]]

    # x_data = [
    #     [1,1,1,1],
    #     [1,1,1,1]
    # ]
    # y_data = [
    #     'hap1', 'hap2'
    # ]

    traces = []
    colors = colors[0:len(x_data)]
    for xd, yd, cl in zip(x_data, y_data, colors):
        traces.append(go.Bar(
            x = xd,
            y = [yd] * len(xd),
            orientation = 'h',
            marker = dict(
                color = cl,
                line = dict(
                    color = 'white',
                    width = 1)
            )
        ))
    print(traces)

    xtickvals = [x + 0.5 for x in range(len(x_data[0]))]

    layout = go.Layout(
        barmode='stack',
        xaxis=dict(
            tickfont=dict(
                color='#ff7f0e'
            ),
            tickangle = -90,
            position=0,
            ticktext = xtickName,
            tickvals = xtickvals,
            zeroline=False,
        ),
        yaxis = dict(
            showgrid=False,
            showline=False,
            # showticklabels=False,
            zeroline=False,
        ),
        showlegend = False,
        margin= dict(
            l = 40,
            b = 40,
            r = 0,
            t = 10
        ),
    )

    annotations = []
    for text, yd in zip(alleles, y_data):
        for t, x in zip(text, xtickvals):
            annotations.append(dict(
                xref = 'x',
                x = x,
                yref = 'y',
                y = yd,
                text = t,
                showarrow=False
            ))

    # annotations.append(dict(
    #     xref = 'x',
    #     yref = 'paper',
    #     x = xtickvals,
    #     y = ['rs1','rs2','rs3','rs4'],
    #     text = ['rs1','rs2','rs3','rs4'],
    # ))

    layout['annotations'] = annotations

    #output the last one
    plotly.offline.plot({'data': traces,'layout': layout}
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
