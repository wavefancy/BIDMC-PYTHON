
zcat all.group.idp.gz | grep -v case | python3 BoxPlot.py -x myx -y myy -o temp-plot.html\
&& phantomjs ~/scripts/js/rasterize.js temp-plot.html test.pdf 10in*5in \
&& display test.pdf
