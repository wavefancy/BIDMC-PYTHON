
cat in.txt | python3 CategoryPlot2.py -x x -y y -o out.html --yerr 4  --hl 4,5 --ms 0.1 --lloc 5 --mt 2 --vl "" --ab 2_0_10_10 --ifs 50 \
&&
phantomjs ~/js/rasterize.js out.html out.pdf 8in*3in \
&&
display out.pdf
