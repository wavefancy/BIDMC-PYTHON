#!/usr/bin/env python3

"""

    Plot StackedBarPlot by plotly library.
    @Author: wavefancy@gmail.com

    Usage:
        StackedBarPlot.py -y ytitle -o outname [-x xtitle] [--yerr ycol] [--yr yrange] [--vl vline] [--hl hline] [--ms msize] [--mt mtype] [--lloc lloc] [--lfs lfs] [--lm lmargin]
        StackedBarPlot.py -h | --help | -v | --version | -f | --format

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
    #INPUT:
    line1: rsID for each position
    line2: haplotype for color ref, allele different with this hap will be coded as gray.
    line3-n: other haplotypes.
    ------------------------
xname id1 id2 id3 id4
ANC    L   X   M   X
HAP1    L   X   M   S
HAP2    L   X   M   S
HAP3    L   Y   M   S
HAP4    L   X   M   S
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
    colors = ['#419F8D','#C9E14F','#FCE532','#FC8E32','#31627B']

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
    groupName = [x[0] for x in data[1:]]
    y_data = [list(map(float, x[1:])) for x in data[1:]]

    traces = []
    colors = colors[:len(y_data)]
    for g, d, cl in zip(groupName, y_data, colors):
        traces.append(go.Bar(
            x = xtickName,
            y = d,
            name = g,
            marker=dict(
                color=cl,
            ),
        ))


    # traces = []
    # colors = colors[0:len(x_data)]
    # for xd, yd, cl, al in zip(x_data, y_data, colors, alleles):
    #     cls = []
    #     for x,y in zip(al, alleles[-1]):  # compare with anc hap
    #         if x == y:
    #             cls.append(cl)
    #         else:
    #             cls.append("gray")
    #
    #     traces.append(go.Bar(
    #         x = xd,
    #         y = [yd] * len(xd),
    #         orientation = 'h',
    #         marker = dict(
    #             color = cls,
    #             #color = colors[0:len(xd)],
    #             line = dict(
    #                 color = 'white',
    #                 width = 1)
    #         )
    #     ))
    # print(traces)
    #
    # xtickvals = [x + 0.5 for x in range(len(x_data[0]))]

    layout = go.Layout(
        barmode='stack',
        # xaxis=dict(
        #     tickfont=dict(
        #         color='#ff7f0e'
        #     ),
        #     tickangle = -90,
        #     position=0,
        #     ticktext = xtickName,
        #     tickvals = xtickvals,
        #     zeroline=False,
        # ),
        yaxis = dict(
            title =  ytitle,
            dtick = 0.25
            # showgrid=False,
            # showline=False,
            # showticklabels=False,
            # zeroline=False,
        ),
        showlegend = False,
        margin= dict(
            l = 50,
            b = 20,
            r = 0,
            t = 0
        ),
    )

    # annotations = []
    # for text, yd in zip(alleles, y_data):
    #     for t, x in zip(text, xtickvals):
    #         annotations.append(dict(
    #             xref = 'x',
    #             x = x,
    #             yref = 'y',
    #             y = yd,
    #             text = t,
    #             showarrow=False,
    #             font=dict(
    #                 #family='Courier New, monospace',
    #                 #size=16,
    #                 color='white'
    #             ),
    #         ))
    #
    # layout['annotations'] = annotations

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
