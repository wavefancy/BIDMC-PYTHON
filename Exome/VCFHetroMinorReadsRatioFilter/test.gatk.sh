
zcat test1.vcf.gz | python3 VCFHetroMinorReadsRatioFilter.py -a 0.2 >out.gatk.gz

