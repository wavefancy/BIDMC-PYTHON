
cat test.txt | python3 HeatMapAncestryInferPlotly.py  -x myx --yt 2,3 --ye 0-fsgs,3-esrd -o temp-plot.html\
&& phantomjs ~/scripts/js/rasterize.js temp-plot.html test.pdf 10in*5in \
&& display test.pdf
