
cat in.color.txt | python3 CategoryPlot2.py -x x -y y -o out.html --hl 4,5 --ms 4 --lloc 1 --mt 3 --vl 5 --ab 2_0_10_10 --clr 4 \
&&
phantomjs ~/js/rasterize.js out.html out.pdf 8in*3in \
&&
display out.pdf
