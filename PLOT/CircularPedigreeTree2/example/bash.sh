
cat fglv.ped | python3 ../data/PED2HTML.py --html ../data/base.html | sed 's|FGLV||g' >fglv.html
