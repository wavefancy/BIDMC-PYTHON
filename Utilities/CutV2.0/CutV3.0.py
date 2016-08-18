#!/usr/bin/env python

'''
    A new enhanced implementation for cut.
    
    @Autor: wavefancy@gmail.com
    @Version1.0
    
    @Version3.0
    1. Add the function to set the delimiter.
    
'''
import sys

def help():
    sys.stderr.write('''
    -------------------------------------------
    Cut columns from stdin input (V3.0)
    -------------------------------------------
    
    @Author: wavefancy@gmail.com
    @Version: 1.0
    
    @Usages:
    -f: specifiy the columns want to cut.(eg. -f4,3; -f4,2-1)
    -t: all parameters following -t were treated as title parameter.
    -d: set the delimiter for fields.
    -h: help info.
    
    @Note:
    1. (-f mode): Important, difference with unix 'cut', the output columns' order is dependent
       on the occurance order in -f option, not the occurance in file.
    2. (-t mode): If -t specified, the fist line were treated as title.
       output based on the occurance oder of input parameters.
    3. Both for the input and output, columns are seperated by whitespace('\\t').
    4. Read input from stdin, and output to stdout.
    5. Column index starts from 1.
    -------------------------------------------
    \n''')
    sys.stderr.close()
    sys.exit(-1)

class P(object):
    outArrayId = [] # output array id.
    title = False
    tArray = [] # title parameters.
    delimiter = ''
    toEnd = False #output all the column from a starting point.
    
def runApp():
    
    if P.title:
        line = sys.stdin.readline()
        if P.delimiter:
            ss = line.strip().split(P.delimiter)
        else:
            ss = line.strip().split()
            
        for x in P.tArray:
            try:
                ii = ss.index(x)
                P.outArrayId.append(ii)
            except ValueError:
                sys.stderr.write('In title,can\'t find: %s\nPlease check!\n'%(x))
                sys.exit(-1)
        #output title line
        s_out = [ss[i] for i in P.outArrayId]
        sys.stdout.write('\t'.join(s_out))
        sys.stdout.write('\n')
    
    
    for line in sys.stdin:
        line = line.strip()
        if line:
            if P.delimiter:
                ss = line.split(P.delimiter)
            else:
                ss = line.split()
                
            if P.toEnd:
                s_n = ss[P.outArrayId[0]:]
            else:
                s_n = [ss[i] for i in P.outArrayId]
            sys.stdout.write('\t'.join(s_n))
            sys.stdout.write('\n')
    
    sys.stdout.close()
    
if __name__ == '__main__':
    #check delimiter
    i = 1
    args = []
    while(i < len(sys.argv)):
        if sys.argv[i].lower().startswith('-d'):
            P.delimiter = sys.argv[i+1]
            i = i +1
        else:
            args.append(sys.argv[i])
            
        i = i+1
    sys.argv = args

    #parse arguments.
    # args = []
    add = False
    for x in sys.argv:
        if add:
            P.tArray.append(x)
            continue
        
        if x.lower().startswith('-f'):
            ss = x[2:].split(',')
            for s in ss:
                t_arr = s.split('-')
                if len(t_arr) ==1 :
                     P.outArrayId.append(int(t_arr[0]) -1)
                elif t_arr[1]:
                    ss_n = list(map(int, t_arr))
                    if(ss_n[0] <= ss_n[1]):
                        for k in range(ss_n[0],ss_n[1]+1):
                            P.outArrayId.append(k -1)
                    else: #reverse order
                        for k in range(ss_n[0],ss_n[1]-1,-1):
                            P.outArrayId.append(k -1)
                else:
                    P.outArrayId.append(int(t_arr[0]) -1)
                    P.toEnd = True
                
            continue
        if x.lower() == '-h':
            help()
            continue
        
        if x.startswith('-t'):
            add = True
            P.title = True
        
        # args.append(x)
        
    if len(P.outArrayId) <= 0 and len(P.tArray) <= 0:
        help()
    
    runApp()
    

