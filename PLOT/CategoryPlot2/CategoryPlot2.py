#!/usr/bin/env python3

"""

    Plot category data using plotly library.
    @Author: wavefancy@gmail.com

    Usage:
        CategoryPlot2.py -x xtitle -y ytitle -o outname [--yerr ycol] [--yr yrange] [--hl hline] [--ms msize]
        CategoryPlot2.py -h | --help | -v | --version | -f | --format

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
        --ms msize    Set marker size: float, default 10.
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
    S55     3       5       CHRNA7  chr15   3
    S55     3       5       NCAM2   chr21   3
    FGJG1   3       4       JAK3    chr19   2
    FGJG1   3       4       KRT3    chr12   3
    FGJG1   3       4       NKD2    chr5    4
    FGJG1   3       4       MKLN1   chr7    1
    FGEG    3       21      RET     chr10   2       Auto-Dominant-CAKUT
    FGEG    3       21      COLEC12 chr18   6
    FGEG    3       21      NUDT6   chr4    2
    FGEG    3       21      C6orf222        chr6    5

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
    msize = 10

    yrange = []
    if args['--yerr']:
        errYCol = int(args['--yerr']) -1
    if args['--yr']:
        yrange = list(map(float, args['--yr'].split(',')))
    if args['--hl']:
        hlines = list(map(float, args['--hl'].split(',')))
    if args['--ms']:
        msize = float(args['--ms'])

    xdata = {} #{categoryName -> []}
    ydata = {} #{categoryName -> []}
    errY  = {} #{categoryName -> []} error bar for Y.ss
    commands = {'vl'}

    def addData(dictName,keyName,val):
        '''add data to a dict'''
        if keyName not in dictName:
            dictName[keyName] = []
        dictName[keyName].append(val)

    for line in sys.stdin:
        line = line.strip()
        if line:
            ss = line.split()
            if ss[0]=='COMMAND' and ss[1] in commands:
                if ss[1] == 'vl':
                    vlines.append(float(ss[2]))
            else:
                try:
                    x = float(ss[1])
                    y = float(ss[2])
                    if errYCol:
                        z = float(ss[errYCol])
                        addData(errY,ss[0],z)
                    addData(xdata, ss[0], x)
                    addData(ydata, ss[0] ,y)
                except ValueError:
                    sys.stderr.write('Warning: parse value error: %s\n'%(line))

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

    for k in xdata.keys():
        if errY:
            plotData.append(
                go.Scatter(
                x=xdata[k],
                y=ydata[k],
                mode = mode,
                marker = marker,
                error_y=dict(
                    type='data',
                    array=errY[k],
                    visible=True,
                    color='#E1DFDF',
                    thickness=1,
                    )
            ))
        else:
            plotData.append(
                go.Scatter(
                x=xdata[k],
                y=ydata[k],
                mode = mode,
            ))

    layout = {
        'margin': {
            'l' : 40,
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
                        'color': 'rgb(50, 171, 96)',
                        'width': 2,
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

    # hlines = {
    #     'shapes': [{
    #         'type': 'line',
    #         'xref': 'paper',
    #         'x0': 0,
    #         'y0': 0.5,
    #         'x1': 1,
    #         'y1': 0.5,
    #         'line': {
    #             'color': 'rgb(50, 171, 96)',
    #             'width': 2,
    #             'dash': 'dashdot',
    #         },
    #     }]
    # }

    # layOut = go.Layout(
    #     #title="hello world"
    #       margin = go.Margin( # update the left, bottom, right, top margin
    #       l= 40,
    #       b= 40,
    #       r= 10,
    #       t= 10
    #      ),
    #      xaxis=go.XAxis(
    #         autotick=True,
    #         mirror=True,
    #         #range=[0, 500],
    #         showgrid=True,
    #         showline=True,
    #         ticks='outside',
    #         showticklabels=True,
    #         title = xtitle
    #      ),
    #      yaxis=go.YAxis(
    #         autotick=True,
    #         mirror=True,
    #         range=yrange,
    #         showgrid=True,
    #         showline=True,
    #         ticks='outside',
    #         title= ytitle,
    #         zeroline=False
    #     )
    # )
    #add horizontal line
    # hline = go.Line(
    #     xref = 'paper',
    #     yref = 'paper',
    #     x0 = 0,
    #     'y0' = 0,
    #     'x1' = 1,
    #     'y1' = 1
    # )
    # hline = {
    #     'shapes':{
    #         'type': 'line',
    #         'xref': 'paper',
    #         'yref': 'paper',
    #         'x0' : 0,
    #         'y0' : 1,
    #         'x1' : 1,
    #         'y1' : 1
    #     }
    # }
    #layOut.update(hline)

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
