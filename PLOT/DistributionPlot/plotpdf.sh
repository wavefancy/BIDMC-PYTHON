
cat test.txt | python3 DisPlotESRDChr1-2.py -x myx -o temp-plot.html\
&& phantomjs ~/scripts/js/rasterize.js temp-plot.html test.pdf 10in*5in \
&& display test.pdf
