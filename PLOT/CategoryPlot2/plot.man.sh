
cat manha.data.txt | python3 manhattonDataHelper.py \
| python3 CategoryPlot2.py -x x -y y -o out.html --clr 4 --xta 45 --xr tight --tfs 10 --ifs 10\
&&
phantomjs ~/js/rasterize.js out.html man.pdf 8in*3in \
&&
display man.pdf
