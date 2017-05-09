#!/usr/bin/env python3

"""

    Plot StackedBarPlot by plotly library.
    @Author: wavefancy@gmail.com

    Usage:
        BarPlot.py -y ytitle -o outname [-x xtitle] [--yerr ycol] [--yr yrange] [--vl vline] [--hl hline] [--ms msize] [--mt mtype] [--lloc lloc] [--lfs lfs] [--lm lmargin] [--bm bm] [--or or] [--cl color]
        BarPlot.py -h | --help | -v | --version | -f | --format

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
        --lloc lloc   Legend location:
                        1 left_top, 2 right_top, 3 left_bottom, 4 right_bottom, 0 no legend.
                        5 right_top out of box.
        --lfs lfs     Legend font size.
        --lm lmargin  Left margin, default 60.
        --bm bm       Barmode, default 2. 1: stack, 2: group.
        --or or       Orientation, default 1. 1: vertical, 2: horizontal.
        --cl color    Set the color for different group, eg: #FA1A1A,#0784FF,#8AC300
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
    line1: population label for each population.
    ------------------------
xname AFR   CEU AA
hap1    0.1 0.2 0.4
hap2    0.6 0.8 0.5
hap3    0.3 0   0.1
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

    colors = ['#419F8D','#C9E14F','#FCE532','#FC8E32','#F4B9C0','#9970AB','gray']

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
    lm = 60    #left margin.
    if args['--lm']:
        lm = float(args['--lm'])
    barmode = 'group'
    if args['--bm']:
        if args['--bm'] == '1':
            barmode = 'stack'
    orientation = ''
    if args['--or'] == '2':
        orientation = 'h'
    if args['--cl']:
        colors = args['--cl'].split(',')

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
    tc = []
    for i in range(len(y_data)):
        tc.append(colors[i%len(colors)])
    colors = tc
    #colors = colors[:len(y_data)]
    # print(xtickName)
    for g, d, cl in zip(groupName, y_data, colors):
        if orientation == 'h':
            traces.append(go.Bar(
                y = xtickName,
                x = d,
                name = g,
                orientation = orientation,
                marker=dict(
                    color=cl,
                ),
            ))
        else:
            traces.append(go.Bar(
                x = xtickName,
                y = d,
                name = g,
                orientation = orientation,
                marker=dict(
                    color=cl,
                ),
            ))

    layout = go.Layout(
        barmode= barmode,
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
            # dtick = 0.25
            # showgrid=False,
            # showline=False,
            # showticklabels=False,
            zeroline=True,
        ),
        margin= dict(
            l = lm,
            b = 20,
            r = 0,
            t = 0
        ),

        showlegend = True,
    )

    # api: https://plot.ly/python/legend/
    if args['--lloc'] != '0':
        if args['--lloc'] == '5':
            legend = go.Layout(
                showlegend=True
            )
        else:
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

    #print(legend)
    layout.update(legend)

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
