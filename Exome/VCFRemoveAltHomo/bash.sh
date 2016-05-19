
zcat test1.vcf.gz | python3 VCFRemoveAltHomo.py -p ped.txt -m | gzip > out.vcf.gz

