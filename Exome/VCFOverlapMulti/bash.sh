
python3 VCFOverlapMulti.py -n 1 test1.vcf.gz test2.vcf.gz test3.vcf.gz >test.out.txt

python3 VCFOverlapMulti.py -n 1 test1.name.vcf.gz test2.vcf.gz test3.vcf.gz 2>name.err.txt

python3 VCFOverlapMulti.py -n 1 test1.alleles.vcf.gz test2.vcf.gz test3.vcf.gz 2>alleles.err.txt

