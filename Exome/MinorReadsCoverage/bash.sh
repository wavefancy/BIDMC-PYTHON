
 zcat test1.vcf.gz | python3 MinorReadsCoverage.py -o >out1.txt
 zcat test1.vcf.gz | python3 MinorReadsCoverage.py -f 0.2 >out2.vcf
