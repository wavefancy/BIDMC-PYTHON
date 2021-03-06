#!/usr/bin/env python3

"""

    Plot distribution data by plotly.
    @Author: wavefancy@gmail.com

    Usage:
        DistributionPlotV2.py -o outname -x xtitle [-t] [--bs binsize] [--an anno] [--xr xrange]
        DistributionPlotV2.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read results from stdin, and output results to stdout.
        2. See example by -f.

    Options:
        -x xtitle
        -t            In test mode.
        -o outname    Output file name: output.html.
        --bs binsize  Set binsize, float, default 0.2
        --an anno     Vertical arrow annotation, pattern as: x_y_text_color[_arrowLen],x_y_text_color...
                      [_arrowLen] is optional, default 100.
        --yerr yecol  Column index for y error bar.
        --xr xrange   Set the xAxis plot range: float1,float2.
        --hl hline    Add horizontal lines: float1,float2.
        --ms msize    Set marker size: float, default 5.
        .
        -h --help     Show this screen.
        -v --version  Show version.
        -f --format   Show input/output file format example.

        https://plot.ly/python/distplot/
        https://plot.ly/python/text-and-annotations/
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
    args = docopt(__doc__, version='2.1')
    #verison 2.0
    # 1. add function to change bin_size
    # 2. add function to add arrow annotation.

    #version 2.1
    # 1. add function to change arrow length for annotation.

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
    binsize = 0.2
    if args['--bs']:
        binsize = float(args['--bs'])
    arowAnnotation = ''
    if args['--an']:
        arowAnnotation = args['--an']

    xrange = []
    # if args['--yerr']:
    #     errYCol = int(args['--yerr']) -1
    if args['--xr']:
        xrange = list(map(float, args['--xr'].split(',')))
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

    if args['-t']:
        import numpy as np
        dataMap = {'test': np.random.randn(400)}

    hist_data = []
    group_labels = []
    for k,v in dataMap.items():
        hist_data.append(v)
        group_labels.append(k)

    # Create distplot
    colors = ['#37AA9C', '#2BCDC1','#F66095','#393E46']
    fig = FF.create_distplot(hist_data, group_labels,bin_size=binsize,
    curve_type='normal',
    colors=colors,
    show_rug=False)

    afsize = 10 #annotation font size.
    #arrow annotation
    annoArray = []
    if arowAnnotation:
        for x in arowAnnotation.split(','):
            ss = x.split('_')
            arrowLen = -100
            if len(ss) == 5:
                arrowLen = -1 * int(ss[4])

            annoArray.append(
                dict(
                    x=float(ss[0]),
                    y=float(ss[1]),
                    xref='x',
                    yref='y',
                    #yref='paper',
                    text=ss[2],
                    showarrow=True,
                    arrowhead=2,
                    arrowcolor=ss[3],
                    font=dict(
                        color=ss[3],
                        size = afsize,
                    ),
                    ax=0,
                    ay=arrowLen
                ))

    annoLayout = go.Layout(
        annotations = annoArray
    )

    layout = go.Layout(
        #title='Points Scored by the Top 9 Scoring NBA Players in 2012',
        yaxis=dict(
            title=ytitle,
        #     autorange=True,
        #     showgrid=True,
        #     zeroline=False,
        #     #dtick=5,
        #     gridcolor='rgb(255, 255, 255)',
        #     #gridwidth=1,
        #     zerolinecolor='rgb(255, 255, 255)',
        #     zerolinewidth=2,
        ),
        xaxis=dict(
            title = xtitle,
            range=xrange,
        )
        ,
        margin=dict(
            l=60,
            r=30,
            b=40,
            t=10,
        ),
        paper_bgcolor='rgb(243, 243, 243)',
        plot_bgcolor='rgb(243, 243, 243)',
        showlegend=False
    )

    fig['layout'].update(layout)
    if annoArray:
        fig['layout'].update(annoLayout)
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
