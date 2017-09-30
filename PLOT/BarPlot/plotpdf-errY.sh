cat erry.text.txt | python3 BarPlot.py -y Frequency -o temp-plot.html --yerr\
&& phantomjs ~/scripts/js/rasterize.js temp-plot.html test-ey.pdf 4in*4in \
&& display test-ey.pdf
