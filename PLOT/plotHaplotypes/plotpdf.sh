
cat test.txt | python3 plotHaplotypes.py --bm 60 -o temp-plot.html\
&& phantomjs ~/scripts/js/rasterize.js temp-plot.html test.pdf 4in*3in \
&& display test.pdf
