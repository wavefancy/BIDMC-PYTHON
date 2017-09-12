cat test.txt | python3 IlluminaGSGT2VCF.py -a <(cat strand.reports.txt | python3 ParseIllumiaStrandReport.py) >vcf.txt
