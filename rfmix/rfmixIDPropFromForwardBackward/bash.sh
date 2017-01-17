
cat test.txt | python3 rfmixIDPropFromForwardBackwardV2.py -n 2 -s >mean.sd.txt
# anc1    anc2
# 0.2333  0.7667
# 0.4000  0.6000

cat test.txt | python3 rfmixIDPropFromForwardBackwardV2.py -n 2 -i --ms <(cat mean.sd.txt)
#-0.7073 0.7073  1.2255  -1.2255
#-0.7073 0.7073  -1.2255 1.2255
#1.4141  -1.4141 0.0000  0.0000


