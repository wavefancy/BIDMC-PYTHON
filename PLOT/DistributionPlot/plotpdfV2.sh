
cat test.txt | python3 DistributionPlotV2.py -x myx -o temp-plot.html -t --an '0_0_test_red,0.5_0.5_test2_blue_50' --bs 0.1 \
&& phantomjs ~/scripts/js/rasterize.js temp-plot.html test.pdf 10in*5in \
&& display test.pdf
