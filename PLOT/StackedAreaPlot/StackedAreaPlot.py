#!/usr/bin/env python3

"""

    Plot Stacked Area Plot using plotly library.
    @Author: wavefancy@gmail.com

    Usage:
        StackedAreaPlot.py -y ytitle -o outname [-x xtitle ] [--yr yrange] [--xr yrange] [--hl hline] [--ms msize] [--bm bmargin] [--aclr colors] [--lclr colors] [--lw int] [--ydt float]
        StackedAreaPlot.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read results from stdin, and output results to stdout.
        2. See example by -f.

    Options:
        -x xtitle
        -y ytitle
        -o outname    Output file name: output.html.
        --yr yrange   Set the yAxis plot range: float1,float2.
        --xr yrange   Set the xAxis plot range: float1,float2.
        --hl hline    Add horizontal lines: float1,float2.
        --ms msize    Set marker size: float, default 2.
        --bm bmargin  Bottom margin, default 40.
        --aclr colors Set colors for each area. Order as input data. Lenth as input data.
                      '#2CA02C,#F3F3F3,#1F77B4'
        --lclr colors Set colors for line.format as '--aclr'.
        --lw int      Line width, default 2.
        --ydt float   Distance between y ticks.
        -h --help     Show this screen.
        -v --version  Show version.
        -f --format   Show input/output file format example.

        https:https://plot.ly/python/filled-area-plots/
        https://plot.ly/python/reference/#scatter-marker-symbol
"""
import sys
from docopt import docopt
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE, SIG_DFL)

def ShowFormat():
    '''Input File format example:'''
    print('''
c1  1   2   area
c1  2   4   area
c1  3   5   area
c2  1   10  area
c2  2   3   area
c2  3   7   area
c3  1   11  area
c3  2   15  area
c3  3   15  area
c4  1   3   line
c4  2   5   line
c4  3   10  line
c5  2   2   marker
COMMAND xticktext       chr1    chr2
COMMAND xtickvals       1     2
    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    xtitle = args['-x']
    ytitle = args['-y']
    outname = args['-o']
    mode = 'markers'
    hlines = [] #location for horizontal lines.
    vlines = []
    msize = 2
    bmargin = 40 #  bottom margin.
    lineWidth = 2

    yrange = []
    xxrange = []
    if args['--yr']:
        yrange = list(map(float, args['--yr'].split(',')))
    if args['--xr']:
        xxrange = list(map(float, args['--xr'].split(',')))
    if args['--hl']:
        hlines = list(map(float, args['--hl'].split(',')))
    if args['--ms']:
        msize = float(args['--ms'])
    if args['--bm']:
        bmargin = int(args['--bm'])
    if args['--lw']:
        lineWidth = int(args['--lw'])
    ydt = ''
    if args['--ydt']:
        ydt = float(args['--ydt'])

    commands = {'vl','xticktext','xtickvals'}
    xticktext = ''
    xtickvals = ''
    from collections import OrderedDict
    dataMap = OrderedDict()
    lineDataMap = OrderedDict()
    markerDataMap = OrderedDict()
    for line in sys.stdin:
        line = line.strip()
        if line:
            ss = line.split()
            if ss[0]=='COMMAND' and ss[1] in commands:
                if ss[1] == 'vl':
                    vlines.append(float(ss[2]))
                if ss[1] == 'xticktext':
                    xticktext = ss[2:]
                if ss[1] == 'xtickvals':
                    xtickvals = [float(x) for x in ss[2:]]
            else:
                try:
                    x = float(ss[1])
                    y = float(ss[2])
                    if ss[3] == 'area':
                        if ss[0] not in dataMap:
                            dataMap[ss[0]] = []
                        dataMap[ss[0]].append((x,y))
                    elif ss[3] == 'line':
                        if ss[0] not in lineDataMap:
                            lineDataMap[ss[0]] = []
                        lineDataMap[ss[0]].append((x,y))
                    elif ss[3] == 'marker':
                        if ss[0] not in markerDataMap:
                            markerDataMap[ss[0]] = []
                        markerDataMap[ss[0]].append((x,y))

                except ValueError:
                    sys.stderr.write('WARN: Parse value error at(SKIPPED): %s\n'%(line))

    #colors = ['rgba(93, 164, 214, 0.5)', 'rgba(255, 65, 54, 0.5)', 'rgba(44, 160, 101, 0.5)','rgba(255, 144, 14, 0.5)', 'rgba(207, 114, 255, 0.5)', 'rgba(127, 96, 0, 0.5)', 'rgba(255, 140, 184, 0.5)', 'rgba(79, 90, 117, 0.5)', 'rgba(222, 223, 0, 0.5)']
    #colors = ['#2CA02C','#FF7F0E','#1F77B4']
    colors = ['']
    if args['--aclr']:
        colors = args['--aclr'].split(',')

    lineColors = ['']
    if args['--lclr']:
        lineColors = args['--lclr'].split(',')

    markerColors = ['#404040']

    import plotly
    import plotly.plotly as py
    import plotly.graph_objs as go

    traces = []
    plotData = OrderedDict()
    keyArray = []
    for k,v in dataMap.items():
        xx = [x[0] for x in v]
        yy = [x[1] for x in v]
        plotData[k] = (xx,yy)
        keyArray.append(k)

    #for shaded area.
    for i in range(len(keyArray)):
        if i == 0:
            traces.append(
                go.Scatter(
                x = plotData[keyArray[i]][0],
                y = plotData[keyArray[i]][1],
                fill='tozeroy',
                line=dict(
                    width=0,
                    color=colors[i%(len(colors))],
                ),
                mode= 'lines'
                )
            )
        else:
            traces.append(
                go.Scatter(
                x = plotData[keyArray[i]][0],
                y = plotData[keyArray[i]][1],
                fill='tonexty',
                line=dict(
                    width=0.5,
                    color=colors[i%(len(colors))],
                ),
                mode= 'lines'
                )
            )

    #for lines.
    tindex = 0
    for k,v in lineDataMap.items():
        xx = [x[0] for x in v]
        yy = [x[1] for x in v]
        traces.append(
            go.Scatter(
            x = xx,
            y = yy,
            line=dict(
                color=lineColors[tindex%len(lineColors)],
                width=lineWidth
            ),
            mode = 'lines'
            )
        )
        tindex += 1

    #for markers.tindex = 0
    tindex = 0
    symbol = 'triangle-up'
    #symbol = 'star'
    #print(markerDataMap)
    for k,v in markerDataMap.items():
        xx = [x[0] for x in v]
        yy = [x[1] for x in v]
        traces.append(
            go.Scatter(
            x = xx,
            y = yy,
            marker=dict(
                color=markerColors[tindex%len(markerColors)],
                symbol=symbol,
                size=10
            ),
            mode = 'markers'
            )
        )
        tindex += 1

    # print(xxrange)
    layout = go.Layout(
        #title='Points Scored by the Top 9 Scoring NBA Players in 2012',
        yaxis=dict(
            title=ytitle,
            # autorange=True,
            showgrid=True,
            zeroline=False,
            dtick = ydt,
            # gridcolor='rgb(255, 255, 255)',
            #gridwidth=1,
            zerolinecolor='rgb(255, 255, 255)',
            zerolinewidth=2,
            ticks='outside',
            showline=True,
            range=yrange
        ),
        xaxis=dict(
            ticks='outside',
            showline=True,
            title = xtitle,
            range=xxrange,
            ticktext=xticktext,
            tickvals=xtickvals,
        ),
        margin=dict(
            l=50,
            r=10,
            b=bmargin,
            t=10,
        ),
        #paper_bgcolor='rgb(243, 243, 243)',
        #plot_bgcolor='rgb(243, 243, 243)',
        showlegend=False
    )


    #fig['layout'].update(layout)
    fig = go.Figure(data=traces, layout=layout)
    # if annoArray:
    #     fig['layout'].update(annoLayout)

    #output the last one
    # plotly.offline.plot({'data': traces,'layout': layout}
    plotly.offline.plot(fig
         ,show_link=False
         ,auto_open=False
         ,filename=outname
    )

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
