#!/usr/bin/env python

"""

    Combine SAM files.
    @Author: wavefancy@gmail.com

    Usage:
        CombineSam.py [--rpg] <file.sam.gz>...
        CombineSam.py -h | --help | -v | --version | -f | --format

    Notes:
        1. CombineSam files, merge and uniq headers from different SAM files.
        2. Output results to stdout.
        3. See example by -f.

    Options:
        --rpg         Remove @PG line in sam headers.
        -h --help     Show this screen.
        -v --version  Show version.
        -f --format   Show input/output file format example.

"""
import sys
from docopt import docopt
from signal import signal, SIGPIPE, SIG_DFL

def ShowFormat():
    '''File format example'''
    print('''
    #SAM 01
    ------------------------
     @SQ     SN:chrUn_GL000218v1     LN:161147
     @SQ     SN:chrEBV       LN:171823
     @RG     ID:Sample_M_CHOP-AP22C_003_003-H3TL3BBXX-1      SM:Sample_M_CHOP-AP22C_003_003  PL:illumina     LB:K00162       PU:H3TL3BBXX.1

    #SAM 02
    ------------------------
     @SQ     SN:chrUn_GL000218v1     LN:161147
     @SQ     SN:chrEBV       LN:171823
     @RG     ID:Sample_M_CHOP-AP22C_003_003-H3TL3BBXX-2      SM:Sample_M_CHOP-AP22C_003_003  PL:illumina     LB:K00162       PU:H3TL3BBXX.1

     #Combined SAM header:
     ------------------------
     @SQ     SN:chrUn_GL000218v1     LN:161147
     @SQ     SN:chrEBV       LN:171823
     @RG     ID:Sample_M_CHOP-AP22C_003_003-H3TL3BBXX-1      SM:Sample_M_CHOP-AP22C_003_003  PL:illumina     LB:K00162       PU:H3TL3BBXX.1
     @RG     ID:Sample_M_CHOP-AP22C_003_003-H3TL3BBXX-2      SM:Sample_M_CHOP-AP22C_003_003  PL:illumina     LB:K00162       PU:H3TL3BBXX.1
          ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    removePG = False
    if args['--rpg']:
        removePG = True

    def readHeaders(file):
        '''Read headers from sam file.
           Return (headers_in_list, first_content_line)
        '''
        #print('readHeaders')
        headers = []
        while True:
            x = file.readline().strip()
            #print(x)
            if x:
                if x.startswith('@'):
                    if removePG and x.startswith('@PG'):
                        continue
                    else:
                        headers.append(x)
                else:
                    return (headers, x)

    import gzip
    files = [gzip.open(f,'rt') for f in args['<file.sam.gz>']]
    head_firstlines = [readHeaders(f) for f in files]
    from collections import OrderedDict
    head_map = OrderedDict()
    #[ (head_map[x] = '1') for x in head_firstlines if x not in head_map]
    for h, _ in head_firstlines:
        for x in h:
            if x not in head_map:
                head_map[x] = '1'

    #print(head_map)
    #write out headers
    sys.stdout.write('%s\n'%('\n'.join(list( head_map.keys() ))))

    #write file contents.
    for n in range(0, len(files)):
        sys.stdout.write('%s\n'%(head_firstlines[n][1]))
        for line in files[n]:
            line = line.strip()
            if line:
                sys.stdout.write('%s\n'%(line))

    #close files.
    [f.close() for f in files]

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
