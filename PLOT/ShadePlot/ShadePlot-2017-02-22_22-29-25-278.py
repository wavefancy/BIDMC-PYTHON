#!/usr/bin/env python3

"""

    Plot shade plot, with function to shade area.
    @Author: wavefancy@gmail.com

    Usage:
        ShadePlot.py -x xtitle -y ytitle -o outname --sa sa [--yerr ycol] [--yr yrange] [--vl vline] [--hl hline] [--ms msize] [--mt mtype] [--lloc lloc] [--lfs lfs]
        ShadePlot.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read results from stdin, and output results to stdout.
        2. See example by -f.

    Options:
        -x xtitle
        -y ytitle
        -o outname    Output file name: output.html.
        --sa sa       Position for shade area left and right: float1, float2.
        --yerr yecol  Column index for y error bar.
        --yr yrange   Set the yAxis plot range: float1,float2.
        --hl hline    Add horizontal lines: float1,float2.
        --vl vline    Add vertical lines: float1, float2...
        --ms msize    Set marker size: float, default 5.
        --mt mtype    Set marker type: 1 dot(default), 2 line, 3 dot + line.
        --lloc lloc   Legend location: 2 right_top, 3 left_bottom.
        --lfs lfs     Legend font size.
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

    ''');

# plotly api: multiple axes
# https://plot.ly/python/multiple-axes/
if __name__ == '__main__':
    args = docopt(__doc__, version='3.0')
    #version
    print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    errYCol = '' #value column for error bar for Y.
    xtitle = args['-x']
    ytitle = args['-y']
    outname = args['-o']
    mode = 'lines' #markers or lines
    hlines = [] #location for horizontal lines.
    vlines = []
    msize = 5

    yrange = []
    if args['--yerr']:
        errYCol = int(args['--yerr']) -1
    if args['--yr']:
        yrange = list(map(float, args['--yr'].split(',')))
    if args['--hl']:
        hlines = list(map(float, args['--hl'].split(',')))
    if args['--vl']:
        vlines = list(map(float, args['--vl'].split(',')))
    if args['--ms']:
        msize = float(args['--ms'])
    if args['--mt']:
        if args['--mt'] == '2':
            mode = 'lines'
        elif args['--mt'] == '3':
            mode = 'lines+markers'

    ci = []
    if args['--sa']:
        ci = list(map(float, args['--sa'].split(',')))

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

    dataLeftX = []
    dataLeftY = []
    dataCenterX = []
    dataCenterY = []
    dataRightX = []
    dataRightY = []

    commands = ['vl', 'y2']
    y2Xdata = []
    y2Ydata = []
    for line in sys.stdin:
        line = line.strip()
        if line:
            ss = line.split()
            if ss[0]=='COMMAND' and ss[1] in commands:
                if ss[1] == 'vl':
                    vlines.append(float(ss[2]))
                if ss[1] == 'y2':
                    try:
                        x = float(ss[2])
                        y = float(ss[3])
                        y2Xdata.append(x)
                        y2Ydata.append(y)
                    except ValueError:
                        sys.stderr.write('Warning: parse value error: %s\n'%(line))
            else:
                try:
                    x = float(ss[0])
                    y = float(ss[1])

                    if x < ci[0]:
                        dataLeftX.append(x)
                        dataLeftY.append(y)
                    elif x > ci[1]:
                        dataRightX.append(x)
                        dataRightY.append(y)
                    else:
                        dataCenterX.append(x)
                        dataCenterY.append(y)

                except ValueError:
                    sys.stderr.write('Warning: parse value error: %s\n'%(line))
    #fill gap for data
    dataLeftX.append(dataCenterX[0])
    dataLeftY.append(dataCenterY[0])
    dataRightX.insert(0, dataCenterX[-1])
    dataRightY.insert(0, dataCenterY[-1])

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
     if y2Xdata:
         plotData.append(
            go.Scatter(
            x=dataLeftX,
            y=dataLeftY,
            marker = marker,
            mode = 'markers',
            line=dict(
                color=color,
            )
         ))

    color = '#1F77B4'
    if dataLeftX:
         plotData.append(
                go.Scatter(
                x=dataLeftX,
                y=dataLeftY,
                marker = marker,
                mode = mode,
                line=dict(
                    color=color,
                )
            ))
    if dataRightX:
        plotData.append(
               go.Scatter(
               x=dataRightX,
               y=dataRightY,
               marker = marker,
               mode = mode,
               line=dict(
                   color=color,
               )
           ))

    plotData.append(
           go.Scatter(
           x=dataCenterX,
           y=dataCenterY,
           marker = marker,
           mode = mode,
           line=dict(
               color=color,
           ),
           fill='tozeroy',
       ))

    layout = {
        'margin': {
            'l' : 60,
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

    legend={
        'showlegend': False,
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
    alllines = hl_data + vl_data
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
