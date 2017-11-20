
'usage: PPIRandomWalkWithRestart.R -n <file> -o <str> [-k <file> -r <s>-<t> -t <n>]

Do random walk on a PPI network, 
prioritize new genes according to RWR steady probability.

options:
 -n <file>  Network file, three columns without header, define a undirected graph.
            Node1 Node2 weight.
 -o <str>   Output file name.
 -k <file>  The list of start gene names, no header.
 -r <s>-<t> Random select <s> genes as start genes, repeat <t> times.
 -t <n>     Set the number of cpus for parallel computing.
            Need packages of biocLite(c("foreach","doParallel"))
 ' -> doc

# load the docopt library
library(docopt)
# retrieve the command-line arguments
opts <- docopt(doc)

### Parse options
inNetWork = opts$'n' # input network file, with weight.
kgenes = NULL #known gens list.
if (!is.null(opts$'k')) {
  kgenes = as.character(read.table(opts$'k', header = F)[,1])
}
numcores = NULL
if (!is.null(opts$'t')){
  numcores = as.numeric(opts$'t')
}

ssize = NULL # resampling size.
stime = NULL # times of resampling.
if (!is.null(opts$'r')){
  xx = strsplit(opts$'r','-')
  ssize = as.numeric(xx[[1]][1])
  stime = as.numeric(xx[[1]][2])
}
### end parse options

# input file
# Code based on: http://www.shizukalab.com/toolkits/sna/weighted-edgelists
library(igraph)
library(dnet)

el = read.table(opts$'n', header = F)
#el=read.csv(file.choose()) # read  the 'el.with.weights.csv' file
el[,1]=as.character(el[,1]) #Because the vertex IDs in this dataset are numbers, we make sure igraph knows these should be treated as characters. Otherwise, it'll create problems (see page on data import)
el[,2]=as.character(el[,2])
el=as.matrix(el) #igraph needs the edgelist to be in matrix format
g=graph.edgelist(el[,1:2], directed=FALSE) #We first greate a network from the first two columns, which has the list of vertices
E(g)$weight=as.numeric(el[,3]) #We then add the edge weights to this network by assigning an edge attribute called 'weight'. 

#plot(g,layout=layout.fruchterman.reingold,edge.width=E(g)$weight)

#node name
nname = V(g)$name
kstarts = NULL
if (!is.null(kgenes)){
  kstarts = seq(0,0,length.out = length(nname))
  kstarts[nname %in% kgenes] = 1
}

#Randomly sample ssize gene as start genes. 
oneRsample = function(arrayIndex){
  m = seq(0,0,length.out = length(nname))
  m[sample(arrayIndex,ssize)] = 1
  return(m)
}

# do random samplesing
randomStars = NULL
if(!is.null(stime)){
  iis = seq(1,length(nname))
  #print(oneRsample(iis))
  randomStars = cbind(oneRsample(iis))
  for(i in 1:(stime-1)){
    randomStars = cbind(randomStars, oneRsample(iis))
  }
}
#print(randomStars)
setSeeds = cbind(kstarts, randomStars)
rownames(setSeeds)=nname
#print(setSeeds)

restart = 0.5
steadyP = dRWR(g, normalise = "column",
     setSeeds = setSeeds, restart = restart, normalise.affinity.matrix ="quantile",
     parallel = TRUE, multicores = opts$'t', verbose = T)
#steadyP

write.table(format(as.matrix(steadyP), digits = 4, scientific = T), 
            opts$'o',quote = FALSE, col.names = FALSE)
