#!/usr/bin/env python3

"""

    Reformat genmod model description output.

    @Author: wavefancy@gmail.com

    Usage:
        FormatGenmodModel.py -c col
        FormatGenmodModel.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read results from stdin, and output results to stdout.
        2. Directly copy comment line, comment line started by '#'.
        3. See example by -f.

    Options:
        -c cols        Column indexes for reformat, 1|1,3. 1 based.
        -h --help      Show this screen.
        -v --version   Show version.
        -f --format    Show input/output file format example.
"""
import sys
from docopt import docopt
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL) #prevent IOError: [Errno 32] Broken pipe. If pipe closed by 'head'.

def ShowFormat():
    '''Input File format example:'''
    print('''
#Input data (output from genmod).
------------------------
Exonic;Annotation=MFF;Compounds=FGCP1:chr2_227332588_A_AATCC,AATCCGAGCAGTTG,AATCCGAGCAGTT;GeneticModels=FGCP1:AD_dn|AR_comp_dn;M
odelScore=FGCP1:79
Exonic;Annotation=PCDH12;GeneticModels=FGCP1:AD_dn;ModelScore=FGCP1:5

#output data:
------------------------
GM:AD_dn|AR_comp_dn;Compounds:chr2_227332588_A_AATCC,AATCCGAGCAGTTG,AATCCGAGCAGTT;
GM:AD_dn;
    ''');

class P(object):
    col = []

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    P.col = [int(x)-1 for x in args['-c'].split(',')] #shift one column.
    import re
    for line in sys.stdin:
        line = line.strip()
        if line:
            if line.startswith('#'):
                sys.stdout.write('%s\n'%(line))
            else:
                ss = line.split()
                for c in P.col:
                    out = ss[c]
                    gm = re.findall('GeneticModels=.*?;', ss[c])
                    if gm:
                        out = ''
                        out += 'GM:' + gm[0].split(':')[1]

                    co = re.findall('Compounds=.*?;', ss[c])
                    if co:
                        out += 'Compounds:' + co[0].split(':')[1]

                    ss[c] = out

                sys.stdout.write('%s\n'%('\t'.join(ss)))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
