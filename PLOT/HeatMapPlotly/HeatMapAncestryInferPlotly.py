#!/usr/bin/env python3

"""

    Plot heatmap using plotly library.
    @Author: wavefancy@gmail.com

    Usage:
        HeatMapPlotly.py -x xtitle -o outname [--yt ytick] [--ye ytext] [--yerr ycol] [--yr yrange] [--vl vline] [--hl hline] [--ms msize] [--mt mtype] [--lloc lloc] [--lfs lfs]
        HeatMapPlotly.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read results from stdin, and output results to stdout.
        2. See example by -f.

    Options:
        -x xtitle
        -o outname    Output file name: output.html.
        --yt ytick    Y tick locatin, float1, float2...
        --ye ytext    Y text text and location. float1-text1,float2-text2...
        --yerr yecol  Column index for y error bar.
        --yr yrange   Set the yAxis plot range: float1,float2.
        --hl hline    Add horizontal lines: float1,float2.
        --vl vline    Add vertical lines: float1, float2...
        --ms msize    Set marker size: float, default 5.
        --mt mtype    Set marker type: 1 dot(default), 2 line.
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

    #API: https://plot.ly/python/heatmaps/
    #https://plot.ly/python/heatmap-and-contour-colorscales/
    #reversescale
    #https://plot.ly/python/reference/#mesh3d-reversescale
    #ticks
    #https://plot.ly/python/axes/
    #color bar size
    #http://codepen.io/plotly/pen/MaLQwE
    #multiple axes
    #https://plot.ly/python/multiple-axes/

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    errYCol = '' #value column for error bar for Y.
    xtitle = args['-x']
    # ytitle = args['-y']
    outname = args['-o']
    # mode = 'markers' #markers or lines
    # hlines = [] #location for horizontal lines.
    vlines = []
    # msize = 5

    tickloc = []
    tickTextLoc = []
    tickTextText = []
    if args['--yt']:
        tickloc = list(map(float, args['--yt'].split(',')))

    if args['--ye']:
        ss = args['--ye'].split(',')
        for x in ss:
            xx = x.split('-')
            tickTextLoc.append(float(xx[0]))
            tickTextText.append(xx[1])
    # yrange = []
    # if args['--yerr']:
    #     errYCol = int(args['--yerr']) -1
    # if args['--yr']:
    #     yrange = list(map(float, args['--yr'].split(',')))
    # if args['--hl']:
    #     hlines = list(map(float, args['--hl'].split(',')))
    # if args['--vl']:
    #     vlines = list(map(float, args['--hl'].split(',')))
    # if args['--ms']:
    #     msize = float(args['--ms'])
    # if args['--mt']:
    #     if args['--mt'] == '2':
    #         mode = 'lines'
    #
    # xanchor = 'right'
    # yanchor = 'bottom'
    # xlloc = 0.99
    # ylloc = 0
    # if args['--lloc']:
    #     if args['--lloc'] == '2':
    #         yanchor = 'top'
    #         xlloc = 0.99
    #         ylloc = 0.99
    #     elif args['--lloc'] == '3':
    #         yanchor = 'bottom'
    #         xanchor = 'left'
    #         xlloc = 0.01
    #         ylloc = 0.01
    #
    # lfontSize = 10
    # if args['--lfs']:
    #     lfontSize = int(args['--lfs'])

    # read data
    data = []
    xdata = []
    ydata = []
    for line in sys.stdin:
        line = line.strip()
        if line:
            ss = line.split()
            if ss[0]=='COMMAND' and ss[1] in commands:
                if ss[1] == 'vl':
                    vlines.append(float(ss[2]))
            else:
                try:
                    d = [float(x) for x in ss]
                    if not xdata:
                        xdata = d
                    else:
                        ydata.append(d[0])
                        data.append(d[1:])
                except ValueError:
                    sys.stderr.write('Warning(skipped): parse value error: %s\n'%(line))

    import plotly
    import plotly.plotly as py
    import plotly.graph_objs as go

    plotData = [
        go.Heatmap(
            z=data,
            x=xdata,
            y=ydata,
            colorscale='Viridis',
            reversescale=True,
            # colorscale=[
            #     # Let first 50% (0.5) of the values have color rgb(0, 0, 0)
            #     [0, '#FDE624'],
            #     [0.5, '#FDE624'],
            #     # Let values between 50-80% of the min and max of z
            #     [0.5, '#B5DE2C'],
            #     [0.8, '#B5DE2C'],
            #     # Let values between 80-100% of the min and max of z
            #     [0.8, '#440053'],
            #     [1, '#440053'],
            # ]
            colorbar = dict(
                borderwidth=0,
                thickness=0.03,
                thicknessmode = 'fraction',
            )
        )
    ]

    layout = go.Layout(
        # title='GitHub commits per day',
        # xaxis = dict(ticks='', nticks=36),
        # yaxis = dict(ticks='' )
        margin= dict(
            l = 20,
            b = 40,
            r = 10,
            t = 10
        ),
        xaxis = dict(
            title = xtitle
        ),
        yaxis = dict(
            showticklabels = False,
            tickvals = tickloc
        ),
        yaxis2=dict(
            tickfont=dict(
                color='#ff7f0e'
            ),
            anchor='middle',
            overlaying='y',
            side='left',
            tickangle = -90,
            position=0,
            ticktext = tickTextText,
            tickvals = tickTextLoc
        ),
    )

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
