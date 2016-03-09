
cat test.txt | python3 CategoryPlot2.py -x x -y y -o out.html --yerr 4  --hl 4,5 --ms 20\
&&
phantomjs ~/js/rasterize.js out.html out.pdf 10in*4in \
&&
display out.pdf
