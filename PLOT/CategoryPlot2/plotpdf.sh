
cat test.txt | python3 CategoryPlot2.py -x myx -y myy -o temp-plot.html --yerr 4 --yr -10,50 --hl 2 --lloc 1\
&& phantomjs ~/scripts/js/rasterize.js temp-plot.html test.pdf 10in*5in \
&& display test.pdf
