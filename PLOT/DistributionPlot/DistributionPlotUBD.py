#!/usr/bin/env python3

"""

    Plot distribution data by plotly.
    @Author: wavefancy@gmail.com

    Usage:
        BoxPlot.py -o outname -x xtitle
        BoxPlot.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read results from stdin, and output results to stdout.
        2. See example by -f.

    Options:
        -x xtitle
        -o outname    Output file name: output.html.
        --yerr yecol  Column index for y error bar.
        --yr yrange   Set the yAxis plot range: float1,float2.
        --hl hline    Add horizontal lines: float1,float2.
        --ms msize    Set marker size: float, default 5.
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
    print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    errYCol = '' #value column for error bar for Y.
    xtitle = args['-x']
    #ytitle = args['-y']
    ytitle = 'Density'
    outname = args['-o']
    mode = 'markers'
    hlines = [] #location for horizontal lines.
    vlines = []
    msize = 5

    yrange = []
    # if args['--yerr']:
    #     errYCol = int(args['--yerr']) -1
    # if args['--yr']:
    #     yrange = list(map(float, args['--yr'].split(',')))
    # if args['--hl']:
    #     hlines = list(map(float, args['--hl'].split(',')))
    # if args['--ms']:
    #     msize = float(args['--ms'])

    commands = {'vl'}
    data = [] #[[name, val1,val2 ..], [name, val1, val2...]]

    from collections import OrderedDict
    dataMap = OrderedDict() # name -> values.
    for line in sys.stdin:
        line = line.strip()
        if line:
            ss = line.split()
            if ss[0]=='COMMAND' and ss[1] in commands:
                if ss[1] == 'vl':
                    vlines.append(float(ss[2]))
            else:
                if ss[0] not in dataMap:
                    dataMap[ss[0]] = []
                else:
                    dataMap[ss[0]].append(float(ss[1]))

    import plotly
    import plotly.plotly as py
    import plotly.graph_objs as go
    from plotly.tools import FigureFactory as FF

    import numpy as np
    dataMap = {'test': np.random.randn(200)}
    hist_data = []
    group_labels = []
    for k,v in dataMap.items():
        hist_data.append(v)
        group_labels.append(k)

    # Create distplot
    fig = FF.create_distplot(hist_data, group_labels,bin_size=0.02,curve_type='normal')

    layout = go.Layout(
        annotations=[
            dict(
                x=3,
                y=0,
                xref='x',
                yref='y',
                text='FSGS_UBD',
                showarrow=True,
                arrowhead=2,
                ax=0,
                ay=-100
            ),
        ],
        #title='Points Scored by the Top 9 Scoring NBA Players in 2012',
        # yaxis=dict(
        #     title=ytitle,
        #     autorange=True,
        #     showgrid=True,
        #     zeroline=False,
        #     #dtick=5,
        #     gridcolor='rgb(255, 255, 255)',
        #     #gridwidth=1,
        #     zerolinecolor='rgb(255, 255, 255)',
        #     zerolinewidth=2,
        # ),
        xaxis=dict(
            title = xtitle,
        )
        ,
        margin=dict(
            l=60,
            r=30,
            b=30,
            t=10,
        ),
        paper_bgcolor='rgb(243, 243, 243)',
        plot_bgcolor='rgb(243, 243, 243)',
        showlegend=False
    )

    fig['layout'].update(layout)
    #fig = go.Figure(data=traces, layout=layout)
    #py.iplot(fig)
    #output the last one
    plotly.offline.plot(fig
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
