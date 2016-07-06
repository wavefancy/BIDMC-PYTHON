
cat test.txt | python3 StackedBarPlot.py -y Frequency -o temp-plot.html\
&& phantomjs ~/scripts/js/rasterize.js temp-plot.html test.pdf 4in*4in \
&& display test.pdf
