
configfile: "ComGVCFs_config.yaml"
SAMPLES = config["samples"]
OUTNAME = config["outname"]
#combine gvcf by input sample list.
#SAMPLES=['Sample_C0701-index2','Sample_C0801-index4']
#OUTNAME='combined1.g.vcf.gz'

###### ----- DIR configuration ----- ########
vcfDir="06_vcf/"
inputDir="07_gvcf/"
refGenome="/groups/pollak/mxw_data/hg38/1kgGRCH38Ref/GRCh38_full_analysis_set_plus_decoy_hla.fa"
refGenomeAlt="/groups/pollak/mxw_data/hg38/1kgGRCH38Ref/GRCh38_full_analysis_set_plus_decoy_hla.fa.alt"
gatkJar="~/jars/GenomeAnalysisTK.jar"

localrules: all_output

# All final files need to be outputed.
rule all_output_recalibratedVCF:
    input:
        vcfDir + OUTNAME

#### ----- Combined all gVCF together ----- #####
import glob
rule CombineGVCF:
    params:
        gvcfs = expand("--variant "+inputDir+"{sample}/{sample}.g.vcf.gz", sample=SAMPLES)
    output:
        #vcfDir + "Combined.g.vcf"
        vcfDir + OUTNAME
    shell:
        # CombineGVCFs can't be run in parallel model.
        "java -Xmx18000m -jar {gatkJar} -T CombineGVCFs -R {refGenome}"
        + " {params.gvcfs} "
        + " -o {output}"
