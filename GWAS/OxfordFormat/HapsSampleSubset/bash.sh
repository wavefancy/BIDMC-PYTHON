
cat haps.txt| python3 HapsSampleSubset.py --sample sample.txt --subset ids.txt --out-sample out.sample.txt -k

#11 rs2280544 204062 C T 1 1 0 1
#11 rs2280544 204062 C T 1 1 0 0

cat haps.txt| python3 HapsSampleSubset.py --sample sample.txt --subset <(cat ids.txt | mycut -f2) --out-sample out.sample.txt -k -n

#11 rs2280544 204062 C T 1 1 0 1
#11 rs2280544 204062 C T 1 1 0 0
