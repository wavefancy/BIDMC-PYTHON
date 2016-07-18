
cat test.txt | python3 ScatterPlot.py -x myx -y myy -o temp-plot.html --lr --ms 5 \
&& phantomjs ~/scripts/js/rasterize.js temp-plot.html test.pdf 7in*6in \
&& display test.pdf
