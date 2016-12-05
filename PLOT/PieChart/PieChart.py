#!/usr/bin/env python3

"""

    Plot category data as box plot using plotly library.
    @Author: wavefancy@gmail.com

    Usage:
        PieChart.py -o outname [--bm bmargin] [--lm lmargin]  [--rm rmargin] [--lx legendx]
        PieChart.py -h | --help | -v | --version | -f | --format

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
        --bm bmargin  Bottom margin, default 10.
        --lm lmargin  Left margin, default 10.
        --rm rmargin  Right margin, default 0.
        --lx legendx  X loction for legend, default 1, percent relative to x-axis.
        --over        Overlap dot with box.
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

    outname = args['-o']
    bmargin = 10
    lmargin = 10
    rmargin = 0
    lengdx = 1
    if args['--bm']:
        bmargin = float(args['--bm'])
    if args['--lm']:
        lmargin = float(args['--lm'])
    if args['--rm']:
        rmargin = float(args['--rm'])
    if args['--lx']:
        lengdx = float(args['--lx'])

    commands = {'vl'}
    data = [] #[[name, val1,val2 ..], [name, val1, val2...]]
    x_data = [] # [name1, name2]
    y_data = [] # [ [val1,val2 ..], [val1,val2 ..] ]
    for line in sys.stdin:
        line = line.strip()
        if line:
            ss = line.split()
            x_data.append(ss[0])
            y_data.append(float(ss[1]))

    colors = ['rgba(93, 164, 214, 0.5)', 'rgba(255, 144, 14, 0.5)', 'rgba(44, 160, 101, 0.5)', 'rgba(255, 65, 54, 0.5)', 'rgba(207, 114, 255, 0.5)', 'rgba(127, 96, 0, 0.5)', 'rgba(255, 140, 184, 0.5)', 'rgba(79, 90, 117, 0.5)', 'rgba(222, 223, 0, 0.5)']
    import plotly
    import plotly.plotly as py
    import plotly.graph_objs as go

    print(x_data)
    print(y_data)
    traces = []
    traces.append(go.Pie(labels=x_data,values=y_data))

    layout = go.Layout(
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
        # xaxis=dict(
        #     ticks='outside',
        #     showline=True
        # ),
        margin=dict(
            l=lmargin,
            r=rmargin,
            b=bmargin,
            t=10,
        ),
        paper_bgcolor='rgb(243, 243, 243)',
        plot_bgcolor='rgb(243, 243, 243)',
        showlegend=True,
        legend=dict(
         x=lengdx,
         y=1
        )
    )

    fig = go.Figure(data=traces, layout=layout)
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
