
configfile: "jointCall.yaml"
gvcfDir = config["gvcfDir"]
region = config["region"]
#print(SAMPLES)
mthreads=config["mthreads"]

vcfDir="07_vcfs/"
refGenome="/groups/pollak/mxw_data/hg38/1kgGRCH38Ref/GRCh38_full_analysis_set_plus_decoy_hla.fa"
refGenomeAlt="/groups/pollak/mxw_data/hg38/1kgGRCH38Ref/GRCh38_full_analysis_set_plus_decoy_hla.fa.alt"
gatkJar="~/jars/GenomeAnalysisTK.jar"

localrules: all_output

# All final files need to be outputed.
rule all_output_recalibratedVCF:
    input:
        #vcfDir + "all.jontly.called.vcf.gz",
        #vcfDir + "recal_snps_recal_indels.vcf.gz"
        vcfDir + region + ".all.jontly.called.vcf.gz"

#### ----- Combined all gVCF together ----- #####
import glob

#### ----- Jointly call on combined gvcfs ----- #####
def gvcfs(wildcards):
    '''Get all gvcf files from input dir[gvcfDir]'''
    files = []
    for x in gvcfDir:
        for f in sorted(glob.glob(x + "/*/*.g.vcf.gz")):
            files.append(f)
    return files

rule JointlyCallVCF_JC:
    input:
        #vcfDir + "Combined.g.vcf"
        gvcfs
    output:
        vcfDir + region + ".all.jontly.called.vcf.gz"
    run:
        vfiles = ""
        #for x in input[0:2]:
        for x in input:
            vfiles = vfiles + " --variant " + x
        #print(vfiles)

        shell(
            "java -Xmx45000m -jar {gatkJar} -T GenotypeGVCFs -R {refGenome}"
            + " -nt " + mthreads
            + " -L " + region
            + " {vfiles}" #variant file list.
            + " -o {output}"
            )
