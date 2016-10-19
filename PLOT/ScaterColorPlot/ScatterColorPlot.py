#!/usr/bin/env python3

"""

    Plot one category scatter plot using plotly library.
    @Author: wavefancy@gmail.com

    Usage:
        ScatterColorPlot.py -y ytitle -o outname [-x xtitle ] [--lr] [--colorscale] [--cmax int] [--yerr ycol] [--yr yrange] [--hl hline] [--ms msize]
        ScatterColorPlot.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read results from stdin, and output results to stdout.
        2. See example by -f.

    Options:
        -x xtitle
        -y ytitle
        -o outname    Output file name: output.html.
        --lr          Add a linear-fits regression line.
        --colorscale  Color dot by local density.
        --cmax int    Color scale max value.

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

    # add regression line to scatter plot
    # https://plot.ly/python/linear-fits/

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
    msize = 5
    linear = False # whether add a linear-fit lines.
    if args['--lr']:
        linear = True
    colorByDensity = False
    if args['--colorscale']:
        colorByDensity = True

    yrange = []
    if args['--yerr']:
        errYCol = int(args['--yerr']) -1
    if args['--yr']:
        yrange = list(map(float, args['--yr'].split(',')))
    if args['--hl']:
        hlines = list(map(float, args['--hl'].split(',')))
    if args['--ms']:
        msize = float(args['--ms'])

    commands = {'vl'}

    colors = ['rgba(93, 164, 214, 0.5)', 'rgba(255, 144, 14, 0.5)', 'rgba(44, 160, 101, 0.5)', 'rgba(255, 65, 54, 0.5)', 'rgba(207, 114, 255, 0.5)', 'rgba(127, 96, 0, 0.5)', 'rgba(255, 140, 184, 0.5)', 'rgba(79, 90, 117, 0.5)', 'rgba(222, 223, 0, 0.5)']
    x_data = [] # [xvalues]
    y_data = [] # [yvalues]
    colors = []
    color = 'RGBA(79, 79, 79, 1)'

    for line in sys.stdin:
        line = line.strip()
        if line:
            ss = line.split()
            if ss[0]=='COMMAND' and ss[1] in commands:
                if ss[1] == 'vl':
                    vlines.append(float(ss[2]))
            else:
                try:
                    x = float(ss[0])
                    y = float(ss[1])
                    x_data.append(x)
                    y_data.append(y)
                    if len(ss) >= 3:
                        colors.append(ss[2])
                    else:
                        colors.append(color)

                except ValueError:
                    sys.stdout.write('Warning: Parse Value Error: %s\n'%(line))

    import plotly
    import plotly.plotly as py
    import plotly.graph_objs as go
    plotData = []

    zcolor = ''
    if colorByDensity:
        # import numpy as np
        # from scipy.stats import gaussian_kde
        # xy = np.vstack([np.array(x_data), np.array(y_data)])
        # zcolor = gaussian_kde(xy)(xy)
        zcolor = [x*y for x,y in zip(x_data, y_data)]

    #print(zcolor)
    #color max
    cmax = max(zcolor)
    if args['--cmax']:
        cmax = int(args['--cmax'])
        zcolor = [ cmax if x >= cmax else x for x in zcolor]

    #print(zcolor)

    if colorByDensity:
        trace1 = go.Scatter(
                  x=x_data,
                  y=y_data,
                  mode='markers',
                  marker=go.Marker(
                        color=zcolor,
                        colorscale='Viridis',
                        reversescale=True,
                        #colorscale=[[0.0, 'rgb(165,0,38)'], [0.0011111111111111, 'rgb(215,48,39)'], [0.2222222222222222, 'rgb(244,109,67)'], [0.3333333333333333, 'rgb(253,174,97)'], [0.4444444444444444, 'rgb(254,224,144)'], [0.5555555555555556, 'rgb(224,243,248)'], [0.6666666666666666, 'rgb(171,217,233)'], [0.7777777777777778, 'rgb(116,173,209)'], [0.8888888888888888, 'rgb(69,117,180)'], [1.0, 'rgb(49,54,149)']]
                        size = msize,
                        cmax = cmax,
                        line = dict(
                            width = 0.01,
                            color = 'rgba(0, 0, 0, 0.1)',
                        ),
                        ),
                  name='Data'
                  )
    else:
        trace1 = go.Scatter(
                  x=x_data,
                  y=y_data,
                  mode='markers',
                  marker=go.Marker(
                        color=colors,
                        size = msize,
                        # line = dict(
                        #     width = 1,
                        #     color = 'white'
                        # ),
                        ),
                  name='Data'
                  )

    plotData.append(trace1)

    #add regression line.
    from numpy import array
    x_data = array(x_data)
    y_data = array(y_data)
    trace2 = []
    lineAnno = []
    if linear:
        from scipy import stats
        slope, intercept, r_value, p_value, std_err = stats.linregress(x_data,y_data)
        line = slope*x_data+intercept
        #add fit line.
        trace2 = go.Scatter(
              x=x_data,
              y=line,
              mode='lines',
              marker=go.Marker(
                color='RGBA(255, 147, 46, 1.00)',
                ),
              name='Fit'
              )
        #add fit equation.
        annotation = go.Annotation(
                  x=0.8,
                  y=0.99,
                  ax=0,
                  ay=0,
                  xref='paper',
                  yref='paper',
                  #text='\$X=Y\$',
                  #text='$R^2 = 0.9551,\\Y = 0.716X + 19.18$',
                  text='R^2 = %.4f,Y = %.4fX + %.4f'%(r_value, slope, intercept),
                  showarrow=False,
                  )
        lineAnno = annotation

    if trace2:
        plotData.append(trace2)

    layout = go.Layout(
        #title='Points Scored by the Top 9 Scoring NBA Players in 2012',
        yaxis=dict(
            title=ytitle,
            autorange=True,
            showgrid=True,
            zeroline=False,
            showline = True,
            #dtick=5,
            #gridcolor='rgb(255, 255, 255)',
            ticks='outside',
            #gridwidth=1,
            #zerolinecolor='rgb(255, 255, 255)',
            #zerolinewidth=2,
        ),
        xaxis=dict(
            title = xtitle,
            zeroline = False,
            showline = True,
            ticks='outside',
        ),
        margin=dict(
            l=40,
            r=30,
            b=40,
            t=10,
        ),
        paper_bgcolor='rgb(243, 243, 243)',
        plot_bgcolor='rgb(243, 243, 243)',
        showlegend=False,
        #annotations = [lineAnno]
    )

    if lineAnno:
        layout.update({
            'annotations': [lineAnno]
        })

    fig = go.Figure(data=plotData, layout=layout)
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
