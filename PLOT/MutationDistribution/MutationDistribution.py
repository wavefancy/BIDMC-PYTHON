#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Plot mutation distribution based on genometools.
    *** not support stream for gff3 input.
    @Author: wavefancy@gmail.com

    Usage:
        MutationDistribution.py -s style -g gff3 -o filename [--start int] [--end int] [-w int] [--intron] [--snp file] [-r]
        MutationDistribution.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read results from stdin.
        2. See example by -f.

    Options:
        -s style      Style file.
        -g gff3       Input gff3 file
        -o filename   Output file name: output.pdf.
        --start int   Range start, int.
        --end int     Range end, int.
        --intron      add intron feature.
        --snp file    Add snp annotation.
        -r            Plot data in reverse oder, default ordered by color.
        -w int        Figure width, default 600.
        -h --help     Show this screen.
        -v --version  Show version.
        -f --format   Show input/output file format example.
"""

#download from: https://raw.githubusercontent.com/genometools/genometools/master/gtpython/sketch_parsed.py

from gt.annotationsketch import *
from gt.core.gtrange import Range
from gt.core import *
from gt.extended import *
import webcolors
import sys
from docopt import docopt
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE, SIG_DFL)

# for add CustomTrack, triangle.
class CustomTrackInsertions(CustomTrack):
    def __init__(self, sidelength, data):
        super(CustomTrackInsertions, self).__init__()
        self.sidelength = sidelength #triangle side length.
        self.data = data
        self.mheight = 5
        self.color = Color(1, 0, 0, 0.7)
        self.title = "Variants"

    def set_color(self, hexColor):
        '''set ploting colors'''
        rgb = webcolors.hex_to_rgb(hexColor)
        self.color = Color(rgb[0]/255.0, rgb[1]/255.0, rgb[2]/255.0, 0.7)

    def get_height(self):
        return (self.sidelength + self.mheight)* len(self.data)

    def get_title(self):
        return self.title

    def set_title(self, title):
        self.title = title

    def free(self):
        return 0

    def render(self, graphics, ypos, rng, style, error):
        #ypos = ypos - 10 #shift annotation a little bit up.
        height = (self.sidelength*math.sqrt(3))/2
        margins = graphics.get_xmargins()
        #red = Color(1, 0, 0, 0.7)
        red = self.color
        #for pos, desc in self.data.iteritems():
        for pos, desc in self.data.items():
            drawpos = margins + (float(pos)-rng.start)/(rng.end-rng.start+1) * (graphics.get_image_width()-2*margins)

            graphics.draw_line(drawpos-self.sidelength/2, ypos + height,
                drawpos, ypos,red, 1)

            graphics.draw_line(drawpos, ypos,
                drawpos+self.sidelength/2, ypos + height,red, 1)

            graphics.draw_line(drawpos-self.sidelength/2, ypos + height,
                drawpos+self.sidelength/2, ypos + height,red, 1)

            #graphics.draw_text_centered(drawpos, ypos + height + 13, str(desc))
            #graphics.draw_text_centered(drawpos, ypos + height + 8, str(desc))
            #right of triangle.
            graphics.draw_text(drawpos + 0.8*height, ypos + height*3.0/4 , str(desc))

            #shift 20
            ypos += (self.sidelength+self.mheight)
        return 0

def ShowFormat():
    '''Input File format example:'''
    print('''
    #Input format:
    #position mutationLabel Color groupLabel.
    ------------------------
105169501       p.Cys151Arg     #F00D0A AFFECTED
105169520       p.Gly157Asp     #F00D0A AFFECTED
105169653       p.Arg177Cys     #F00D0A AFFECTED
105169666       p.Val181Gly     #F00D0A AFFECTED
105169776       p.Arg218Trp     #F00D0A AFFECTED
105169777       p.Arg218Gln     #F00D0A AFFECTED
105175020       p.Asp634Asn     #0A56F0 CONTROL
105176023       p.Leu707Phe     #0A56F0 CONTROL
105181113       p.Gly1205Asp    #F00D0A AFFECTED
    ''');

if __name__ == "__main__":
    args = docopt(__doc__, version='1.0')
    print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    # if len(sys.argv) != 4:
    #     sys.stderr.write("Usage: " + (sys.argv)[0] +
    #                      " Style_file PNG_file GFF3_file\n")
    #     sys.stderr.write("Create PNG representation of GFF3 annotation file.")
    #     sys.exit(1)

    #pngfile = (sys.argv)[2]
    pngfile = args['-o']

  # load style file
    style = Style()
    #style.load_file((sys.argv)[1])
    style.load_file(args['-s'])

  # create feature index
    feature_index = FeatureIndexMemory()

  # add GFF3 file to index
    #feature_index.add_gff3file((sys.argv)[3])
    #feature_index.add_gff3file(args['-g'])
    #ref: https://github.com/genometools/genometools/blob/ba61a9536c5e1b1f2f2141f3a0816fe8d5c3fb74/testdata/gtpython/sketch_stream.py
    in_stream = GFF3InStream(args['-g'])
    if args['--intron']:
        add_introns_stream = AddIntronsStream(in_stream)
        feature_stream = FeatureStream(add_introns_stream, feature_index)
    else:
        feature_stream = FeatureStream(in_stream, feature_index)

    gn = feature_stream.next_tree()

  # fill feature index
    while gn:
        gn = feature_stream.next_tree()

  # create diagram for first sequence ID in feature index
    seqid = feature_index.get_first_seqid()
    range = feature_index.get_range_for_seqid(seqid)
    if args['--start']:
        range.start = int(args['--start'])
    if args['--end']:
        range.end = int(args['--end'])

    diagram = Diagram.from_index(feature_index, seqid, range, style)

    snpdata = {} #color -> {loc:name}
    color = '#E40A00' #default red
    inclr = color
    if args['--snp']:
        with open(args['--snp']) as ifile:
            for line in ifile:
                line = line.strip()
                if line:
                    ss = line.split()
                    # group data by color.
                    if len(ss) >= 3:
                        inclr = ss[2]
                    else:
                        inclr = color

                    if inclr not in snpdata:
                        if len(ss) >= 4:
                            snpdata[inclr] = ({}, ss[3])
                        else:
                            snpdata[inclr] = ({}, 'Variants')

                    snpdata[inclr][0][ss[0]] = ss[1]
                    #snpdata[ss[0]] = ss[1]

        keys = sorted(snpdata.keys())
        if args['-r']:
            keys = sorted(snpdata.keys(), reverse=True)

        for color in keys:
            ctt = CustomTrackInsertions(13, snpdata[color][0])
            ctt.set_color(color)
            ctt.set_title(snpdata[color][1])
            diagram.add_custom_track(ctt)

        #ctt = CustomTrackInsertions(15, snpdata)
        #diagram.add_custom_track(ctt)
    #ctt = CustomTrackInsertions(15, {105177703:"foo", 105180703:"bar", 105182703:"baz"})
    #diagram.add_custom_track(ctt)

    canvas_width = 600
    if args['-w']:
        canvas_width = int(args['-w'])
  # create layout
    layout = Layout(diagram, canvas_width, style)
    height = layout.get_height()

  # create canvas
    #canvas = CanvasCairoFile(style, canvas_width, height)
    canvas = CanvasCairoFilePDF(style, canvas_width, height)

  # sketch layout on canvas
    layout.sketch(canvas)

  # write canvas to file
    canvas.to_file(pngfile)
