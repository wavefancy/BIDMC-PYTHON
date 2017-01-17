
cat test.txt | python3 rfmixIDPropFromForwardBackwardA2V1.py -s

#AVEanc1 AVEanc2 SDanc1  SDanc2
#0.4667  1.5333  0.2357  0.2357
#0.8000  1.2000  0.0816  0.0816

cat test.txt | python3 rfmixIDPropFromForwardBackwardA2V1.py -i --ms mean.sd.txt 

#-0.7073 1.2255
#-0.7073 -1.2255
#1.4141  0.0000

