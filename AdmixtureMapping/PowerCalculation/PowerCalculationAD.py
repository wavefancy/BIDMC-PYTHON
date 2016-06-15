#!/usr/bin/env python

"""

    Power calculation based for admixture mapping.
    @ref: Design and Analysis of admixture mapping studies, (2004).

    @Author: wavefancy@gmail.com

    Usage:
        PowerCalculationAD.py -r aratio -n nhap -a aprop [-s sd]
        PowerCalculationAD.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read parameters from stdin, and output to stdout.

    Options:
        -r aratio        Ancestry risk ratio. aratio = f2/f0 for multiplicative model. (f1/f0)^2.
        -n nhap          Number of haplotypes, n = 2*N, N for sample size.
        -a aprop         Average admixture proportion for hish-risk group.
        -s sd            Standard deviaton for ancestral proportion of hish-risk group.
        -h --help        Show this screen.
        -v --version     Show version.
        -f --format      Show input/output file format example.
"""
import sys
from docopt import docopt
from signal import signal, SIGPIPE, SIG_DFL

def ShowFormat():
    '''File format example'''
    print('''
          ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    # print(args)
    # sys.exit(0)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    aratio = float(args['-r'])  # r in paper,  Ancestry risk ratio. aratio = f2/f0 for multiplicative model.
    n = int(args['-n'])         # n, Number of haplotypes, n = 2*N, N for sample size.
    aprop = float(args['-a'])   # theta in paper.
    if args['-s']:
        sd = float(args['-s'])

    import math
    from scipy.stats import norm
    # http://docs.scipy.org/doc/scipy-0.16.0/reference/generated/scipy.stats.norm.html
    import scipy.integrate as integrate
    #http://docs.scipy.org/doc/scipy/reference/tutorial/integrate.html

    lam = math.log(aratio)      # lambda in paper.
    Za = 4.27 # pvalue 1e-5 for type I error.

    def V(riskRatio, prop):
        ''''Compute value V for the first equation of Statistical Power calculation in ref paper.
            riskRatio: ancestral risk ratio for f2/f0,
            prop: ancestral proportion for hish-risk group.
        '''
        t_r = math.pow(riskRatio, 0.5)
        return (prop * (1 - prop) * t_r) / (4 * math.pow(prop * t_r + 1 - prop, 2))

    def ZbOfProp(p):
        return (lam * math.pow(n, 0.5) - Za * math.pow( V(1, p), - 0.5)) / math.pow(V(aratio, p), - 0.5)
    def inteFun(p):
        '''Function for integration'''
        #print('inteFun: %.4f'%(p))
        #print(ZbOfProp(p))
        #print('density: %.4f'%(norm.pdf(p, loc=aprop, scale=sd)))
        power = 1 - norm.sf(ZbOfProp(p))
        #print('power: %.4f'%(power))
        return  power * norm.pdf(p, loc=aprop, scale=sd)

    if args['-s']:
        #calculate based on sd value.

        reweight = norm.sf(0, loc=aprop, scale=sd) - norm.sf(1, loc=aprop, scale=sd)
        #print('reweight: %.4f'%(reweight))
        #print(inteFun(0.001))
        total = integrate.quad(lambda x: inteFun(x), 0.001 , 0.999)
        #print(total)
        sys.stdout.write('%.4f\n'%(total[0] / reweight))

    else:
        Zb = (lam * math.pow(n, 0.5) - Za * math.pow( V(1, aprop), - 0.5)) / math.pow(V(aratio, aprop), - 0.5)
        #print(Zb)
        power = 1 - norm.sf(Zb)
        sys.stdout.write('%.4f\n'%(power))

    #paper
    #print(V(1))
    #print(V(aratio))
    #Zb = math.pow( n * V(1), 0.5) * lam - Za

    #print(Zb)
    #power = 1 - norm.sf(Zb)
    #sys.stdout.write('%.4f\n'%(power))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
