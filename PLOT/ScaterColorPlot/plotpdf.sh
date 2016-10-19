
cat test.txt | python3 ScatterColorPlot.py -x myx -y myy -o temp-plot.html --lr --colorscale --ms 5 --cmax 40\
&& phantomjs ~/scripts/js/rasterize.js temp-plot.html test.pdf 7in*6in \
&& display test.pdf
