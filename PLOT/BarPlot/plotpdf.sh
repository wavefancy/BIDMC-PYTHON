cat temp.txt | python3 BarPlot.py -y Frequency -o temp-plot.html --or 2 --cl '#FA1A1A,#0784FF,#8AC300'\
&& phantomjs ~/scripts/js/rasterize.js temp-plot.html test.pdf 4in*4in \
&& display test.pdf
