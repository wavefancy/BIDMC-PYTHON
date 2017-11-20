# PPIRandomWalkWithRestart

An R implementation of Random Walk with Restart (RWR) algorithm

Requires modules `dnet`, `docopt`, `foreach`, and `doParallel`.

```
source("http://bioconductor.org/biocLite.R")
biocLite()
biocLite(c("dnet","docopt","foreach","doParallel"))
```

For a description of the Random Walk with Restart (RWR) algorithm, which
this module implements, see the paper by Kohler et al. at
[http://www.sciencedirect.com/science/article/pii/S0002929708001729](http://www.sciencedirect.com/science/article/pii/S0002929708001729).

## Overview

This module can be used to run:

- A standard random walk with restart from a set of seed nodes, as in the
  Kohler et al. paper referenced above. Undirected network with edge weights.
  As the final results (especially regarding to the rank of the top potential genes)
  is not sensitive to the restarting probability 'c' [ref],
  in this implementation 'c=0.5'. But you can change it as you like.

## Running a random walk

The `PPIRandomWalkWithRestart.R` script can be used to run a random walk. The syntax looks like:

`Rscript PPIRandomWalkWithRestart.R -n ppi.txt -k kgene.txt -o output.txt -t 3`

where the input graph is in edge list format with weights (ppi.txt),
the seed is a list of nodes to start the random walk at (kgene.txt).
Run this scripts in parallel by 3 cores.

The script will write a tab-separated list of nodes and probabilities to output file (output.txt),
where the probability number represents the probability that a random walk
starting at the seed nodes will terminate at the given node.

For more detail about the expected arguments, run `Rscript PPIRandomWalkWithRestart.R -h`.

## Running a random walk with random sampling.

For example, run a random walk with random picking of 2 genes as start from input node pool
without replacement each sampling process, repeat this process 3 times.
The output is quantile normalized between all columns. Each column is the result
for one random sampling.

`Rscript PPIRandomWalkWithRestart.R -n ppi.txt -o output23.txt -t 3 -r 2-3`

Or, run a pre-selected starts with random sampling. The first column is the result for using
the pre-selected genes as start, columns '2-n' is the results for random sampling (without counting row title).
The output is quantile normalized between all columns.

`Rscript PPIRandomWalkWithRestart.R -n ppi.txt -k kgene.txt -o outputk23.txt -t 3 -r 2-3`

## Using the module

If you use the Walker module, please cite:
