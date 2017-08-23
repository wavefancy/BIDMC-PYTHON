# Rscript ~/Rscripts/qValueFDR.R col4Pvalue
#
# Estimate qValue FDR by https://github.com/StoreyLab/qvalue
#------------------------------
# Read data from stdin(One column for pvalue)
# Output results to stdout, add one column for qvalue.
#------------------------------

library(qvalue)
library(abind)

args <- commandArgs(TRUE)
if(length(args) != 1){
    print(args)
    print("Please set arguments: 'arg1' for the column of pvalues.")
    quit()
}
col = as.numeric(args[1])

inData = read.table(file("stdin"))
qv = qvalue(p=inData[col,])
out = abind(inData,qv$qvalues)
write.table(out, stdout(), col.names = F, row.names = F, quote = F, sep='\t')
