#!/usr/bin/env python

'''
    ATCGVariants

    @Author: wavefancy@gmail.com
    @Version: 1.0
    
    @Algorithms:
        
'''
import sys
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL) #prevent IOError: [Errno 32] Broken pipe. If pipe closed by 'head'.

def help():
    sys.stderr.write('''
    -------------------------------------
    ATCGVariants
    -------------------------------------
    
    @Author: wavefancy@gmail.com
    @Version: 1.0
    
    @Usages:
    para1: -h, output help message.

    @Notes:
    1. Read plink bim file from stdin, and output A/T, C/G variants to stdout.
    -------------------------------------
    \n''')
    sys.stderr.close()
    sys.exit(-1)
    
if __name__ == '__main__':
    if len(sys.argv) != 1:
        help()
    
    AT=['A', 'T']
    CG=['C', 'G']
    
    for line in sys.stdin:
        line = line.strip()
        if line:
            ss = line.upper().split()
            vs = sorted(ss[4:6])
            if vs == AT or vs == CG:
                sys.stdout.write('%s\n'%(line))
    
sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()