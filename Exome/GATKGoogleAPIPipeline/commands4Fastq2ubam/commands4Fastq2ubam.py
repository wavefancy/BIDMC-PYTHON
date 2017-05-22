#!/usr/bin/env python3

"""

    Generate the commands for convert fastq(Pair end sequencing) to ubam format.
    @Author: wavefancy@gmail.com

    Usage:
        commands4Fastq2ubam.py -l library -j picard [-d odir] [-n sampleName] [-p platform] <r1fNames>...
        commands4Fastq2ubam.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Concatenate multiple VCF files together, order as the appearence in parameters.
        2. Only keep the header from the first vcf.
        3. input vcf files either in ziped(.gz) or flat txt model.

    Options:
        <r1fNames>... File names for R1 reads fastq file.
        -n sampleName Sample name, default extract from r1fName.
                      Format like sampleName_barcode_*.gz
        -j picard     Path for picard jar file.
        -l library    Library name.
        -p platform   Platform name, default illumina.
        -d odir       Output dir, default ./data.
        -h --help     Show this screen.
        -v --version  Show version.
        -f --format   Show input/output file format example.

"""
import sys
import os
from docopt import docopt
from signal import signal, SIGPIPE, SIG_DFL

def ShowFormat():
    '''File format example'''
    print('''
          ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    #r1fName = args['-f']
    LIBRARY_NAME = args['-l']
    PLATFORM = 'illumina'
    picardJar = args['-j']
    if args['-p']:
        PLATFORM = args['-p']
    sampleName = ""
    if args['-n']:
        sampleName = args['-n']
    odir = 'data'
    if args['-d']:
        odir = args['-d']

    import gzip
    files = []
    fnames = [] #file name with absolute path.
    for f in args['<r1fNames>']:
        fnames.append(os.path.abspath(f))
        if f.endswith('.gz'):
            files.append(gzip.open(f, 'rt'))
        else:
            files.append(open(f,'r'))

    '''
        java -jar -Xmx8G
        $p
        FastqToSam
        FASTQ=${in}_R1_001.fastq.gz
        #first read file of pair#
        FASTQ2=${in}_R2_001.fastq.gz
        #second read file of pair#
        OUTPUT=data/$n.bam
        READ_GROUP_NAME=HJCK2BBXX.3
        #required; changed from default of A#
        SAMPLE_NAME=$n
        LIBRARY_NAME=YaleXgen
        PLATFORM_UNIT=47_HJCK2BBXX.3
        #run_barcode.lane#
        PLATFORM=illumina
        #recommended#
        SEQUENCING_CENTER=YaleXgen
    '''
    errorCode = False
    for f,n in zip(files, fnames):
        if not sampleName:
            sampleName = n.split('/')[-1].split('_')[0]
        ss = f.readline().split(':')
        READ_GROUP_NAME = ss[2]+'.'+ss[3]
        PLATFORM_UNIT = ss[1] + '_' + READ_GROUP_NAME

        n2 = ""
        if len(n.split('_R1_')) == 2:
            ss = n.split('_R1_')
            n2 = ss[0] + '_R2_' + ss[1]
        elif len(n.split('_r1_')) == 2:
            ss = n.split('_r1_')
            n2 = ss[0] + '_r2_' + ss[1]
        else:
            sys.stderr.write('ERROR: Input fastq file name should have keyword "_R1_" or "_r1_", please check!')
            errorCode = True
            break

        out = []
        out.append("java -jar -Xmx8G")
        out.append(picardJar)
        out.append("FastqToSam FASTQ=" + n)
        out.append("FASTQ2=" + n2)
        out.append('OUTPUT=%s/%s.bam'%(odir,sampleName))
        out.append('READ_GROUP_NAME=%s'%(READ_GROUP_NAME))
        out.append('SAMPLE_NAME=%s'%(sampleName))
        out.append("LIBRARY_NAME=" + LIBRARY_NAME)
        out.append("PLATFORM_UNIT="+PLATFORM_UNIT)
        out.append("PLATFORM="+PLATFORM)
        out.append("SEQUENCING_CENTER="+LIBRARY_NAME)

        #output commands.
        sys.stdout.write('%s\n'%(' '.join(out)))

    #close files.
    [f.close() for f in files]
    if errorCode:
        sys.exit(-1)
sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
