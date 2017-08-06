#!/usr/bin/env python3

"""

    Plot category data as box plot using plotly library.
    @Author: wavefancy@gmail.com

    Usage:
        BoxPlot.py -y ytitle -o outname [-x xtitle ] [--yerr ycol] [--yr yrange] [--hl hline] [--ms msize] [--over] [--bm bmargin] [--ha hanno] [--ady ady] [--haw float]
        BoxPlot.py -h | --help | -v | --version | -f | --format

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
        --ms msize    Set marker size: float, default 2.
        --bm bmargin  Bottom margin, default 40.
        --over        Overlap dot with box.
        --ha hanno    Add horizontal line annotation with text.
                        foramt: x1_x2_y_text,x1_x2_y_text.
                        Example: 1_2_0.5_**
                        Each category for the box plot with x-coordinate as 0,1,2...n-1.
        --ady ady     Set the distance between horizontal annotation line and text (default 0.025).
        --haw float     Set the horizontal annotation line with, default 2.
        -h --help     Show this screen.
        -v --version  Show version.
        -f --format   Show input/output file format example.

        https://plot.ly/python/text-and-annotations/
        (API)https://plot.ly/python/reference/#layout-annotations
"""
import sys
from docopt import docopt
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE, SIG_DFL)

def ShowFormat():
    '''Input File format example:'''
    print('''
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
    mode = 'markers'
    hlines = [] #location for horizontal lines.
    vlines = []
    msize = 2
    overBoxDot = False #overlap box with dots.
    bmargin = 40 #  bottom margin.
    arowAnnotation = ''
    ady = 0.025
    haw = 2


    yrange = []
    if args['--yerr']:
        errYCol = int(args['--yerr']) -1
    if args['--yr']:
        yrange = list(map(float, args['--yr'].split(',')))
    if args['--hl']:
        hlines = list(map(float, args['--hl'].split(',')))
    if args['--ms']:
        msize = float(args['--ms'])
    if args['--over']:
        overBoxDot = True
    if args['--bm']:
        bmargin = int(args['--bm'])
    if args['--ha']:
        arowAnnotation = args['--ha']
    if args['--ady']:
        ady = float(args['--ady'])
    if args['--haw']:
        haw = float(args['--haw'])

    commands = {'vl'}
    data = [] #[[name, val1,val2 ..], [name, val1, val2...]]
    x_data = [] # [name1, name2]
    y_data = [] # [ [val1,val2 ..], [val1,val2 ..] ]
    for line in sys.stdin:
        line = line.strip()
        if line:
            ss = line.split()
            if ss[0]=='COMMAND' and ss[1] in commands:
                if ss[1] == 'vl':
                    vlines.append(float(ss[2]))
            else:
                x_data.append(ss[0])
                y_data.append([float(x) for x in ss[1:]])


    #colors = ['rgba(93, 164, 214, 1)', 'rgba(255, 65, 54, 1)', 'rgba(44, 160, 101, 1)','rgba(255, 144, 14, 1)', 'rgba(207, 114, 255, 1)', 'rgba(127, 96, 0, 1)', 'rgba(255, 140, 184, 1)', 'rgba(79, 90, 117, 1)', 'rgba(222, 223, 0, 1)']
    colors = ['rgba(93, 164, 214,1)', 'rgba(255, 65, 54,1)', 'rgba(44, 160, 101,1)','rgba(255, 144, 14, 1)', 'rgba(207, 114, 255, 1)', 'rgba(127, 96, 0, 1)', 'rgba(255, 140, 184, 1)', 'rgba(79, 90, 117, 1)', 'rgba(222, 223, 0, 1)']
    #colors = ['rgba(93, 164, 214, 0.5)', 'rgba(255, 65, 54, 0.5)', 'rgba(44, 160, 101, 0.5)','rgba(255, 144, 14, 0.5)', 'rgba(207, 114, 255, 0.5)', 'rgba(127, 96, 0, 0.5)', 'rgba(255, 140, 184, 0.5)', 'rgba(79, 90, 117, 0.5)', 'rgba(222, 223, 0, 0.5)']

    colors += colors
    colors += colors
    import plotly
    import plotly.plotly as py
    import plotly.graph_objs as go

    traces = []

    colors = colors[:len(x_data)]
    for xd, yd, cls in zip(x_data, y_data, colors):
            if overBoxDot:
                traces.append(go.Box(
                    y=yd,
                    name=xd,
                    whiskerwidth=0.2,
                    #fillcolor=cls,
                    marker=dict(
                        size=msize,
                        color = cls
                    ),
                    line=dict(width=1),
                ))
            else:
                traces.append(go.Box(
                    y=yd,
                    name=xd,
                    boxpoints='all',
                    jitter=0.5,
                    whiskerwidth=0.2,
                    #fillcolor=cls,
                    marker=dict(
                        size=msize,
                        color = cls
                    ),
                    line=dict(width=1),
                ))

    layout = go.Layout(
        #title='Points Scored by the Top 9 Scoring NBA Players in 2012',
        yaxis=dict(
            title=ytitle,
            autorange=True,
            showgrid=True,
            zeroline=False,
            #dtick=5,
            # gridcolor='rgb(255, 255, 255)',
            #gridwidth=1,
            zerolinecolor='rgb(255, 255, 255)',
            zerolinewidth=2,
        ),
        xaxis=dict(
            ticks='outside',
            showline=True
        ),
        margin=dict(
            l=50,
            r=30,
            b=bmargin,
            t=10,
        ),
        # paper_bgcolor='rgb(243, 243, 243)',
        # plot_bgcolor='rgb(243, 243, 243)',
        showlegend=False
    )


    #https://plot.ly/python/text-and-annotations/
    #(API)https://plot.ly/python/reference/#layout-annotations
    # Each category for the box plot with x-coordinate as 0,1,2...n-1.
    annoArray = []
    # arowAnnotation="1_2_0.8_*"
    annoColor='black'
    # ady = 0.025
    if arowAnnotation:
        for x in arowAnnotation.split(','):
            ss = x.split('_')
            x1 = float(ss[0])
            x2 = float(ss[1])
            y  = float(ss[2])
            t  = ss[3]
            #draw a horizontal line
            annoArray.append(
                dict(
                    x=x1,
                    y=y,
                    xref='x',
                    yref='y',
                    #yref='paper',
                    text='',
                    showarrow=True,
                    arrowhead=0,
                    arrowwidth=haw,
                    arrowcolor=annoColor,
                    font=dict(
                        color=annoColor,
                        size = 12,
                    ),
                    #arrowwidth=1,
                    # If `axref` is an axis, this is an absolute value on that axis, like `x`, NOT a relative value.
                    axref='x',
                    ax=x2,
                    ay=0
                ))
            #draw Font text.
            annoArray.append(dict(
                    x=(x1+x2)/2.0,
                    y=y + ady,
                    xref='x',
                    yref='y',
                    #yref='paper',
                    text=t,
                    showarrow=False,
                    arrowhead=0,
                    arrowcolor=annoColor,
                    font=dict(
                        color= annoColor,
                        size = 14,
                    ),
                    # # If `axref` is an axis, this is an absolute value on that axis, like `x`, NOT a relative value.
                    # axref='x',
                    # ax=float(ss[0])+1,
                    # ay=0
                ))

    annoLayout = go.Layout(
        annotations = annoArray
    )

    #fig['layout'].update(layout)
    fig = go.Figure(data=traces, layout=layout)
    if annoArray:
        fig['layout'].update(annoLayout)

    #fig = go.Figure(data=traces, layout=layout)
    #py.iplot(fig)
    #output the last one
    # plotly.offline.plot({'data': traces,'layout': layout}
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
