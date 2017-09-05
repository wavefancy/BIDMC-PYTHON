
#--------------------------
# Remove intermediate files, only keep results for
# 1.QC to ubam.

# *** IMPORTANT ****
# Only work for pair end sequencing files.
#--------------------------

configfile: "config.yaml"
print(config)

#set sample variable by --config sample=NAME when run snakemake, each run one sample.
sample = config["sample"]
#sample = "M_FG-NL113"

#SAMPLES = [sample]
#mthreads = "1", the number of threads for majority of works.
mthreads = config["mthreads"]

removeTemp=config["removeTemp"]
#print(removeTemp)

#quality score format for fastq file, set "" if let program auto detect.
#qphred =  "phred33" | "" | "phred64" : choose one from these three possible values.
#phredCoding = ""
phredCoding = config["phredCoding"]

#convert phred64 quality score to phred33, please make sure the input quality score is encoded as phred64.
#otherwise please set this as false.
#TOPHRED33 = False
TOPHRED33 = config["TOPHRED33"]
#print(SAMPLES)

#fastq file location.
sampleDir = config["sampleDir"]

libraryName = config['libraryName']

# output root dir.
orootDir = config["orootDir"]
fastqcDIR=orootDir + "/01_fastqc/"
trimDir=orootDir + "/02_trim/"
trimQCDir=orootDir + "/03_fastqcTrim/"
qcUBAMDir=orootDir + "/04_qcUBAM/"
logDir="10_logs/"

trimmomaticJar="~/jars/trimmomatic-0.36.jar"
picardJar="/groups/pollak/mxw_data/excallV4/wdl/scripts/broad_pipelines/local/software/gitc/picard.jar"
adapterPE="/groups/pollak/mxw_data/illumina/adapters/PE_all.fa"
adapterSE="/groups/pollak/mxw_data/illumina/adapters/SE_all.fa"

localrules: all_output

# All final files need to be outputed.
rule all_output_gVCF:
    input:
        #Generate QC summaries for raw reads.
        expand(fastqcDIR + "{sample}" + "/done_flag.txt", sample=sample),
        #Generate QC summaries for trimed reads.
        expand(trimQCDir + "{sample}" + "/done_flag.txt", sample=sample),
        #Generate uBAMs.
        expand(qcUBAMDir + sample + "/done_flag.txt")

import glob
def fastq4Sample(wildcards):
    """get fastq file list for sample."""
    return sorted(glob.glob(sampleDir +"/"+ sample + "/*.fastq.gz"))

#### ----- Quality Check by fastqc for raw reads ----- #####
rule fastqc4Raw:
    params: prefix = fastqcDIR + sample
    input:
        #lambda wildcards: glob.glob(sampleDir + wildcards.sample + "/*.fastq.gz")
        fastq4Sample
    output:
        #at least one wildcard match.
        fastqcDIR + sample + "/done_flag.txt"
        #expand(fastqcDIR + "{sample}", sample=SAMPLES)
    shell:
        "fastqc {input} -o {params.prefix} && touch {output}"
        #"fastqc {input}/*.fastq.gz -o {output}"

#### ----- Adapters and low quality base trim ----- #####
def fastqR1files(wildcards):
    """Get all the fastq R1 files"""
    #print(sampleDir + "/" +wildcards.sample)
    #print(sorted(glob.glob(sampleDir + "/" + wildcards.sample + "/*_R1_*.fastq.gz")))
    return sorted(glob.glob(sampleDir + "/" + sample + "/*_R1_*.fastq.gz"))

outputSuffix = ['_TR1_.fastq.gz','_TR1_unpair.fastq.gz','_TR2_.fastq.gz','_TR1_unpair.fastq.gz']
rule trimmomatic_rgTagFile:
    #50min, 1G mem.
    params:
        sample=sample,
        outDir=trimDir + sample
    input:
        fastqR1files
        #sorted(glob.glob(sampleDir + "/" + sample + "/*_R1_*.fastq.gz"))
    output:
        trimDir + sample + "/done_flag.txt"
    run:
        #default parameters setting: http://www.usadellab.org/cms/index.php?page=trimmomatic
        phred = phredCoding.strip()  #set phred format.
        if phred:
            phred = "-" + phred

        #for pair end reads.
        pairENDfiles = set()
        for f in input:
            f2 = f.replace('_R1_', '_R2_')
            pairENDfiles.add(f)
            pairENDfiles.add(f2)
            out = [trimDir + params.sample + "/" + f.split('/')[-1].split('.fastq.gz')[0] + x for x in outputSuffix]
            if TOPHRED33:
                shell(
                "java -jar -Xmx9500m " + trimmomaticJar + " PE "+phred+" -threads " + mthreads
                + " {f} {f2}"
                + " {out}"
                + " TOPHRED33"  #convert to phred33 quality encoding.
                + " ILLUMINACLIP:"+ adapterPE +":2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:15 MINLEN:36")
            else:
                shell(
                "java -jar -Xmx9500m " + trimmomaticJar + " PE "+phred+" -threads " + mthreads
                + " {f} {f2}"
                + " {out}"
                + " ILLUMINACLIP:"+ adapterPE +":2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:15 MINLEN:36")

        print(pairENDfiles)
        shell(
            "touch {output}"
        )

#### ----- Quality Check by fastqc for trimed reads ----- #####
rule fastqc4trimed:
    #1G Mem, 5min.better local run.
    params:
        prefix = trimQCDir + sample,
        inDir  = trimDir + sample
    input:
        trimDir + sample + "/done_flag.txt"

    output:
        trimQCDir + sample + "/done_flag.txt"
    shell:
        "fastqc {params.inDir}/*.fastq.gz -o {params.prefix} && touch {output}"

#### ----- convert trimmomatic QC files to UBAM ----- #####
def trimedR1files():
    """Get all the fastq R1 files for trimed data"""
    return sorted(glob.glob(trimDir + sample + "/*_TR1_.fastq.gz"))

rule convertTrimed2uBAM:
    params:
        inDir = trimDir + sample
    input:
        trimDir + sample + "/done_flag.txt"
    output:
        qcUBAMDir + sample + "/done_flag.txt"
    run:
        files = trimedR1files()
        for f in files:
            f2 = f.replace('_TR1_', '_TR2_')
            shell(
                "python3 ~/python/commands4Fastq2ubam.py -l " + libraryName
                + " -j " + picardJar
                + " -d " + qcUBAMDir + sample
                + " -w -s _TR1_"
                # + " -n " + sample
                + " " + f
                + " >" + qcUBAMDir + sample + "/fastq2ubam.sh"
            )
            shell(
                "bash " + qcUBAMDir + sample + "/fastq2ubam.sh"
            )
        shell(
            "touch {output}"
        )
