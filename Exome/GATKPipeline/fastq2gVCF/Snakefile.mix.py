
#--------------------------
# Remove intermediate files, only keep results for
# 1.QC
# 2.bwa men mapping
# 2.BQSR cram
# 3.gVCF
#
# mix(Version)
# 1. handle mixture of single end and pair end reads.
# @Data 08/12/2016.
# 2. add option to select smart pairing of pair end input.
# 3. limit picard garbage gc resource use. -XX:ParallelGCThreads=2
#--------------------------

configfile: "config.yaml"
print(config)
#SAMPLES=['Sample_M_CHOP-AI111_003_003','Sample_M_CHOP-AO111_003_003']
#SAMPLES = config["samples"]

#set sample variable by --config sample=NAME when run snakemake, each run one sample.
sample = config["sample"]
#sample = "M_FG-NL113"

#SAMPLES = [sample]
#mthreads = "1", the number of threads for majority of works.
mthreads = config["mthreads"]
#number of threads for HaplotypeCaller
hcthreads = config["hcthreads"]
#number of threads for bwa_mem
memthreads = config["memthreads"]

removeTemp=config["removeTemp"]
#print(removeTemp)

#check all reads name for rg tag. set this as true if input has single end reads.
#allReads4Tag = False
allReads4Tag = config["allReads4Tag"]

#quality score format for fastq file, set "" if let program auto detect.
#qphred =  "phred33" | "" | "phred64" : choose one from these three possible values.
#phredCoding = ""
phredCoding = config["phredCoding"]

#convert phred64 quality score to phred33, please make sure the input quality score is encoded as phred64.
#otherwise please set this as false.
#TOPHRED33 = False
TOPHRED33 = config["TOPHRED33"]
#print(SAMPLES)

#whether remove final step cram file [after bqsr].
removeFinalCram = False
#fire smart pairing function for bwa.
smartPairBwa = config["smartPairBwa"]

###### ----- DIR configuration ----- ########
#fastq file location.
sampleDir = config["sampleDir"]

# output root dir.
orootDir = config["orootDir"]
fastqcDIR=orootDir + "/01_fastqc/"
trimDir=orootDir + "/02_trim/"
trimQCDir=orootDir + "/03_fastqcTrim/"
bwaDir=orootDir + "/04_bwa/"
gatkDir=orootDir + "/05_gatk/"
vcfDir= "06_vcf/"   #put gvcf at current location
logDir="10_logs/"

trimmomaticJar="~/jars/trimmomatic-0.36.jar"
picardJar="~/jars/picard.jar"
adapterPE="/groups/pollak/mxw_data/illumina/adapters/PE_all.fa"
adapterSE="/groups/pollak/mxw_data/illumina/adapters/SE_all.fa"
refGenome="/groups/pollak/mxw_data/hg38/1kgGRCH38Ref/GRCh38_full_analysis_set_plus_decoy_hla.fa"
refGenomeAlt="/groups/pollak/mxw_data/hg38/1kgGRCH38Ref/GRCh38_full_analysis_set_plus_decoy_hla.fa.alt"
bwaPostaltJS="/home/mrp1/mxw_bin/bwa/bwa/bwakit/bwa-postalt.js"
gatkJar="~/jars/GenomeAnalysisTK.jar"
knownIndel="/groups/pollak/mxw_data/gatk/b38/hg38bundle/Mills_and_1000G_gold_standard.indels.hg38.vcf.gz"
knownSites="/groups/pollak/mxw_data/gatk/b38/hg38bundle/chr.dbsnp_144.hg38.vcf.gz"
getTagsPy="~/python/getRGTags.py"
comSamPy="~/python/CombineSam.py"
addTagPy="~/python/AddRGTag4Sam.py"
cramJar="~/jars/cramtools-3.0.jar"
exregion="/groups/pollak/mxw_data/gatk/b38/exomeIntervalP100/exon.p100.refSeq.interval_list"

localrules: all_output

# All final files need to be outputed.
rule all_output_gVCF:
    input:
        #Generate QC summaries for raw reads.
        expand(fastqcDIR + "{sample}" + "/done_flag.txt", sample=sample),
        #Generate QC summaries for trimed reads.
        expand(trimQCDir + "{sample}" + "/done_flag.txt", sample=sample),
        expand(bwaDir + "{sample}" + "/done_bwaTag.txt", sample=sample),
        expand(gatkDir + "{sample}" + "/done_sort.txt", sample=sample),
        expand(gatkDir + "{sample}" + "/done_mark.txt", sample=sample),
        expand(gatkDir + "{sample}" + "/done_localRealign.txt",sample=sample),
        expand(gatkDir + "{sample}" + "/done_BQSR.txt", sample=sample),
        expand(vcfDir + "{sample}" + "/done_HaplotypeCaller.txt", sample=sample)

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

outputSuffix = ['_r1.fastq.gz','_r1_unpair.fastq.gz','_r2.fastq.gz','_r2_unpair.fastq.gz']
rule trimmomatic_rgTagFile:
    #50min, 1G mem.
    params:
        sample=sample,
        outDir=trimDir + sample
    input:
        fastqR1files
        #sorted(glob.glob(sampleDir + "/" + sample + "/*_R1_*.fastq.gz"))
    output:
        trimDir + sample + "/rgTags.txt"
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

        #for single end reads. [*.fastq.gz file except *_R1_* and *_R2_* files]
        allFiles = glob.glob(sampleDir + "/" + params.sample + "/*.fastq.gz")
        singleEndFiles = [x for x in allFiles if x not in pairENDfiles]
        #print(singleEndFiles)
        if singleEndFiles:
            for fin in singleEndFiles:
                fout = trimDir + params.sample + "/" + fin.split('/')[-1].split('.fastq.gz')[0] + "_single_r1_unpair.fastq.gz"
                if TOPHRED33:
                    shell(
                    "java -jar -Xmx9500m " + trimmomaticJar + " SE "+phred+" -threads " + mthreads
                    + " {fin} {fout}"
                    + " TOPHRED33"  #convert to phred33 quality encoding.
                    + " ILLUMINACLIP:"+ adapterSE +":2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:15 MINLEN:36")
                else:
                    shell(
                    "java -jar -Xmx9500m " + trimmomaticJar + " SE "+phred+" -threads " + mthreads
                    + " {fin} {fout}"
                    + " ILLUMINACLIP:"+ adapterSE +":2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:15 MINLEN:36")

        print(singleEndFiles)
        print(pairENDfiles)
        #if len(singleEndFiles) <= 0 and len(pairENDfiles) <= 0:
        #     sys.stdout.buffer.write("No fastq file in dir: %s\n"%(sampleDir + wildcards.sample))
        #     sys.exit(-1)

        if allReads4Tag: #only forward reads is enough for generate tags.
            shell("python3 " + getTagsPy +" -s {params.sample} -q {params.outDir}/*_r1*fastq.gz -a >{output}")
        else:
            shell("python3 " + getTagsPy +" -s {params.sample} -q {params.outDir}/*_r1*fastq.gz >{output}")
        #"java -jar -Xmx2G " + trimmomaticJar + " PE -threads 1 {input} {output} ILLUMINACLIP:"+ adapter +":2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:15 MINLEN:36"

#### ----- Quality Check by fastqc for trimed reads ----- #####
rule fastqc4trimed:
    #1G Mem, 5min.better local run.
    params:
        prefix = trimQCDir + sample,
        inDir  = trimDir + sample
    input:
        trimDir + sample + "/rgTags.txt"
        #[trimDir + "{sample}" + f.split('/')[-1].split('.fastq.gz')[0] + x for f in sorted(glob.glob(sampleDir + "{sample}" + "/*_R1_*.fastq.gz")) for x in outputSuffix]
        #sorted(glob.glob(trimDir + "{sample}" + "/*.fastq.gz"))
        #trimDir + "{sample}" + "/trim_{sample}_r1.fastq.gz",
        #trimDir + "{sample}" + "/trim_{sample}_r2.fastq.gz"
    output:
        trimQCDir + sample + "/done_flag.txt"
    shell:
        "fastqc {params.inDir}/*.fastq.gz -o {params.prefix} && touch {output}"

# def trimedR1files(wildcards):
#     """Get all the fastq R1 files"""
#     #print(sorted(glob.glob(sampleDir + wildcards.sample + "/*_R1_*.fastq.gz")))
#     return sorted(glob.glob(trimDir + wildcards.sample + "/*_r1.fastq.gz"))
#### ----- Align reads by bwamen, and sort and markdup by sambamba ----- #####
#rule bwamen_align_sort_markduplicate:
#do alignment and add tags.
rule bwamenTag:
    params: sample = sample,
            hla = bwaDir + sample + "/hla_"+sample+"",
            stemp = bwaDir + sample + "/allTaged.sam.gz",
            dir=bwaDir + sample,
            inDir=trimDir + sample

    input:
        # Control BWA_MEM start after trim and QC for trimed file.
        # if removeTemp=True, after BWA_MEM, trimed files will be removed.
        trimDir + sample + "/rgTags.txt",
        trimQCDir + sample + "/done_flag.txt"
    output:
        bwaDir + sample + "/done_bwaTag.txt"
        #bwaDir + "{sample}" + "/hla_{sample}"
    run:
        #print(trimDir + params.sample + "/*_r1.fastq.gz")
        #direct reference for scripts.
        #infiles = sorted(glob.glob(trimDir + params.sample + "/*_r1.fastq.gz"))
        infiles = sorted(glob.glob(trimDir + sample + "/*_r1.fastq.gz"))
        #print(infiles)

        #mapping single end reads.
        sfiles = glob.glob(params.inDir + "/*_unpair.fastq.gz")
        if sfiles:
            shell("zcat {params.inDir}/*_unpair.fastq.gz | bwa mem "
            +" -t " + memthreads
            +" -M " + refGenome
            +" -"
            +" | gzip >{params.dir}/unparied.sam.gz"
            )

        #mapping paired end
        for f in infiles:
            f2=f.replace('_r1.fastq.gz', '_r2.fastq.gz')
            nbase = f.split('/')[-1].split('_r1.fastq.gz')[0]
            if smartPairBwa:
                shell("seqtk mergepe " + f +" " + f2
                +" | bwa mem -t " + memthreads
                +" -M -p " + refGenome
                +" -"
                +" | gzip >{params.dir}/" + "paried_" + nbase + ".sam.gz"
                )
            else:
                shell("bwa mem -t " + memthreads
                + " -M " + refGenome
                + " " + f + " " + f2
                + " | gzip >{params.dir}/" + "paried_" + nbase + ".sam.gz"
                )

        #post bwa process, combine sam, add tags, sort and convert to bam.
        shell("python3 "+ comSamPy +" --rpg {params.dir}/*paried*.sam.gz"
        +" | k8 " + bwaPostaltJS + " -p {params.hla} " + refGenomeAlt
        +" | python3 " + addTagPy + " -r {params.inDir}/rgTags.txt"
        +" | pigz -p {memthreads} "
        +" > {params.stemp} && touch {output}"
        )
        #compress hla seqs.
        shell("gzip -f {params.hla}*")

        #MarkDuplicates
        #shell("sambamba markdup -t "+memthreads+" -l 5 {params.stemp} {output}")
        #***IMPORTANT*** Strange problem to process converted cram in next step for GATK.
        # shell("sambamba markdup -t "+mthreads+" -l 0 {params.stemp} /dev/stdout"
        # +" | java -Xmx5G -jar " + cramJar + " cram -R " + refGenome
        # +" >{output}"
        # +" && java -Xmx5G -jar " + cramJar + " index -I {output}"
        # )
        #remove files:
        if removeTemp:
            shell(
            #"rm {params.stemp}"
            "rm {params.dir}/*paried*.sam.gz"
            #remove trimmomatic files, but keep done flag files.
            + " && rm -r " + trimDir + "{params.sample}" + "/*.gz"
            )

rule picard_sortbam:
    params:
        #remove = expand(" && rm " + bwaDir + sample + "/allTaged.sam.gz" if removeTemp == True else "")
        remove = " && rm " + bwaDir + sample + "/allTaged.sam.gz" if removeTemp == True else ""
    input:
        bwaDir + sample + "/done_bwaTag.txt"
    output:
        gatkDir + sample + "/done_sort.txt"
    shell:
        "  java -jar -XX:ParallelGCThreads=2 -Xmx20G {picardJar} SortSam "
        +" INPUT=" + bwaDir + "{sample}" + "/allTaged.sam.gz"
        +" OUTPUT=" + gatkDir + "{sample}" + "/sorted.bam"
        +" SORT_ORDER=coordinate"
        +" && touch {output}"
        +" {params.remove}"

rule picard_duplicatemark:
    params:
        #remove = expand(" && rm " + bwaDir + sample + "/allTaged.sam.gz" if removeTemp == True else "")
        remove = " && rm " + gatkDir + sample + "/sorted.bam" if removeTemp == True else "",
        metrics = gatkDir + sample  + "/metrics.txt",
        out = gatkDir + sample + "/dup_marked.bam"
    input:
        gatkDir + sample + "/done_sort.txt"
    output:
        gatkDir + sample + "/done_mark.txt"
    shell:
        "  java -jar -XX:ParallelGCThreads=2 -Xmx20G {picardJar} MarkDuplicates "
        +" INPUT=" + gatkDir + sample + "/sorted.bam"
        +" OUTPUT=" + "{params.out}"
        +" METRICS_FILE=" + "{params.metrics}"
        +" && java -jar -Xmx20G {picardJar} BuildBamIndex INPUT={params.out}"
        +" && touch {output} && gzip -f {params.metrics}"
        +" {params.remove}"

rule localRealignment:
    params:
        tlist = gatkDir + sample + "/realign_target.list",
        inf= gatkDir + sample + "/dup_marked.bam",
        out= gatkDir + sample + "/realigned_"+sample+".cram",
        remove = " && rm " + gatkDir + sample + "/dup_marked.ba?" if removeTemp == True else ""
    input:
        gatkDir + sample + "/done_mark.txt"
        #bwaDir + "{sample}" + "/mdup_sorted_{sample}.bam",
    output:
        gatkDir + sample + "/done_localRealign.txt"
        #gatkDir + "{sample}" + "/realigned_{sample}.cram"
    shell:
        "java -Xmx20G -jar {gatkJar} -T RealignerTargetCreator"
        +" -L {exregion}"
        +" -R {refGenome} -I {params.inf} -known {knownIndel} -o {params.tlist}"
        +" && java -Xmx20G -jar {gatkJar} -T IndelRealigner -R {refGenome}"
        +" -I {params.inf} -known {knownIndel} -targetIntervals {params.tlist}"
        +" -o {params.out}"
        +" && gzip -f {params.tlist}"
        +" && touch {output}"
        +" {params.remove}"

rule BQSR:
    #105min,
    params:
        dir= gatkDir + sample,
        inf = gatkDir + sample + "/realigned_"+sample+".cram",
        out = gatkDir + sample + "/bqsr_"+sample+".cram",
        remove = " && rm " + gatkDir + sample + "/realigned_"+sample+".cram*" if removeTemp == True else ""
    input:
        gatkDir + sample + "/done_localRealign.txt"
        #gatkDir + "{sample}" + "/realigned_{sample}.cram"
    output:
        gatkDir + sample + "/done_BQSR.txt"
        #gatkDir + "{sample}" + "/bqsr_{sample}.cram"

    shell:
        "java -Xmx20G -jar {gatkJar} -T BaseRecalibrator -R {refGenome}"
        + " -L {exregion}"
        + " -I {params.inf} -knownSites {knownSites} -knownSites {knownIndel}"
        + " -o {params.dir}/bqsr_table"
        # Generate post reports
        #+ " && java -Xmx20G -jar {gatkJar} -T BaseRecalibrator -nct 5 -R {refGenome}"
        #+ " -I {input} -knownSites {knownSites} -knownSites {knownIndel}"
        #+ " -BQSR {params.dir}/bqsr_table"
        #+ " -o {params.dir}/post_bqsr_table"
        #+ " && java -Xmx20G -jar {gatkJar} -T AnalyzeCovariates -R {refGenome}"
        #+ " -before {params.dir}/bqsr_table"
        #+ " -after {params.dir}/post_bqsr_table"
        #+ " -plots {params.pdf}"
        # BQSR on bam data
        + " && java -Xmx20G -jar {gatkJar} -T PrintReads -R {refGenome}"
        + " -I {params.inf}"
        + " --disable_indel_quals "
        #+ " --bam_compression 5"
        + " -BQSR {params.dir}/bqsr_table"
        + " -o {params.out}"
        + " && gzip -f {params.dir}/bqsr_table"
        + " && touch {output}"
        + " {params.remove}"

rule HaplotypeCaller:
    #10G,
    params:
        dir= gatkDir + sample,
        inf = gatkDir + sample + "/bqsr_"+sample+".cram",
        out = vcfDir + sample + "/"+sample+".g.vcf.gz",
        remove = " && rm " + gatkDir + sample + "/bqsr_"+sample+".cram*" if removeFinalCram == True else ""
    input:
        gatkDir + sample + "/done_BQSR.txt"
        #gatkDir + "{sample}" + "/bqsr_{sample}.cram"
    output:
        vcfDir + sample + "/done_HaplotypeCaller.txt"
        #vcfDir + "{sample}" + "/{sample}.g.vcf.gz"
    shell:
        " java -Xmx35G -jar {gatkJar} -T HaplotypeCaller -R {refGenome}"
        + " -nct " +hcthreads
        + " -L {exregion}"
        #+" --emitRefConfidence GVCF --variant_index_type LINEAR --variant_index_parameter 128000"
        + " --emitRefConfidence GVCF"
        #+" -I {input} -o {output}"
        + " -I {params.inf} -o {params.out}"
        + " && touch {output}"
        + " {params.remove}"
