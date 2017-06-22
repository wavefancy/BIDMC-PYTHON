
cat test.txt | python3 StackedAreaPlot.py -x myx -y yy -o temp-plot.html --aclr '#2CA02C,#F3F3F3,#1F77B4' --xr '1,3' --lclr orange --lw 5\
&& phantomjs ~/scripts/js/rasterize.js temp-plot.html test.pdf 10in*5in \
&& display test.pdf
