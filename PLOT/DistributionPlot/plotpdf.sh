
cat test.txt | python3 DistributionPlotUBD.py -x myx -o temp-plot.html\
&& phantomjs ~/scripts/js/rasterize.js temp-plot.html test.pdf 10in*5in \
&& display test.pdf
