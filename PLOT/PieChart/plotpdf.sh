
#zcat all.group.idp.gz | grep -v case | python3 BoxPlot.py -x myx -y myy -o temp-plot.html\
cat test.txt | python3 PieChart.py -o temp-plot.html --lx 1.5 \
&& phantomjs ~/scripts/js/rasterize.js temp-plot.html test.pdf 5in*4in \
&& display test.pdf
