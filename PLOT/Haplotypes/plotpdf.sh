
cat test.txt | python3 Haplotypes.py -x myx -y myy -o temp-plot.html --yerr 4 --yr -10,50 --hl 2\
&& phantomjs ~/scripts/js/rasterize.js temp-plot.html test.pdf 4in*3in \
&& display test.pdf
