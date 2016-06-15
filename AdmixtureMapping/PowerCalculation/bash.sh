# example in paper. Design and Analysis of admixture mapping studies

python3 PowerCalculationAD.py -r 2 -n 1600 -a 0.8
# 0.8727, expected 0.9 if use equation 4 in paper, but here we used a more precise version. 

python3 PowerCalculationAD.py -r 2 -n 1600 -a 0.8 -s 0.2
# 0.7702
