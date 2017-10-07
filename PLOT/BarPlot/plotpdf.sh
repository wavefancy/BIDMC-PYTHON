cat temp.txt | python3 BarPlot.py -y Frequency -o temp-plot.html --or 2 --xdt 1 --gcl '#FA1A1A,#0784FF,#8AC300' --lloc 0 --ta '2_3_*' --ts 20 --bma 50 --rma 30\
&& phantomjs ~/scripts/js/rasterize.js temp-plot.html test.pdf 4in*4in \
&& display test.pdf
