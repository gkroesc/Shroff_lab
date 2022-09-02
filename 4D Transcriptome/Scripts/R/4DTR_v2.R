library(Matrix)
library(tictoc)
library(ggplot2)
library(plyr)
library(dplyr)
library(glue)
tic('Total Time:')
genes <- c('lev-11', 'mir-67', 'sups-1')

outputDir <- "C:\\Users\\chawmm\\Desktop\\4D Transcriptome\\output"
dataDir <- "C:\\Users\\chawmm\\Desktop\\4D Transcriptome\\data"
projectDir <- "C:\\Users\\chawmm\\Desktop\\4D Transcriptome"

setwd(projectDir)

`%!in%` <- Negate(`%in%`)

##### Step 1: ~ 77s Load data #####
tic("Step 1")
bigDataCell <- read.csv("C:\\Users\\chawmm\\Desktop\\4D Transcriptome\\data\\GSE126954_cell_annotation.csv")
bigDataGene <- read.csv("C:\\Users\\chawmm\\Desktop\\4D Transcriptome\\data\\GSE126954_gene_annotation.csv")

tic("Reading in matrix") #Times: 77.41s, 77.68s
bigmm <- readMM("C:\\Users\\chawmm\\Desktop\\RNAseq Project\\scRNAseq Data\\Raw\\GSE126954_gene_by_cell_count_matrix.txt")

toc()
toc()

#Housekeeping genes
#(rps-23, rps-26, rps-27, rps-16, rps-2, rps-4, rps-17, rpl-24.1, rpl-27, rpl-33, rpl-36, rpl-35, and rpl-15)
#'lin-42', 'vab-19', 'let-502', 'mel-11', 'fem-2', 'mlc-4', 'hmp-1', 'hmp-2', 'hmr-1', 'spc-1', 'ifb-1', 'ifa-1', 'unc-52', 'elt-6', 'elt-3'
#CAN ONLY DO ONE GENE AT A TIME. CAN COMBINE IN PANDAS


#Instead of using cell names to search, use lineage names to search. 


masterkey <- read.csv("C:\\Users\\chawmm\\Desktop\\4D Transcriptome\\cell keys\\masterkey.csv") #Spaces are replaced by dots. data cellname --> data.cellname





##### Step 2: ~ 150s Filling Index Data #####
tic('Step 2')
##### Filtering #####
bdc <- bigDataCell
bdc$index <- 1:nrow(bigDataCell)
bdc <- bdc[which(bdc$embryo.time >= 350 & bdc$passed_initial_QC_or_later_whitelisted == TRUE),]
bdc <- bdc[which(bdc$lineage %in% masterkey$data.lineage | bdc$plot.cell.type %in% masterkey$data.cellname),]
bigDataCell$index <- 1:nrow(bigDataCell)

##### Functions #####
namelin <- function(aname, alin) {
  rows <- masterkey[which(masterkey$data.lineage == alin & masterkey$data.cellname == aname),]
  return(rows)
}

#Name known

name_only <- function(aname, alin){
  rows <- masterkey[which(masterkey$data.cellname == aname),]
  return(rows)
}

#Lineage known 

lin_only <- function(aname, alin) {
  rows <- masterkey[which(masterkey$data.lineage == alin),]
  return(rows)
}

outerfunc <- function(x){ #Where x = row of dataframe
  d_name <- x['plot.cell.type']
  d_lin <- x['lineage']
  d_time <- x['embryo.time']
  d_numi <- x['n.umi']
  d_idx <- x['index']
  #print(d_name)
  #print(d_lin)
  if (!is.na(d_name) & !is.na(d_lin) ) {
    #d_name and d_lin in masterkey || ASSOCIATION == 3
    assoc <- 3
    rows <- namelin(d_name, d_lin)
    #print(rows)
  }else if(!is.na(d_name) & is.na(d_lin)) {
    #d_name in mk but d_lin not in masterkey || ASSOCIATION == 1
    assoc <- 1
    rows <- name_only(d_name, d_lin)
    #print(rows)
  }else if(is.na(d_name) & !is.na(d_lin) ) {
    #d_name not in mk but d_lin in masterkey || ASSOCIATION == 2
    assoc <- 2
    rows <- lin_only(d_name, d_lin)
    #print(rows)
  }else if(is.na(d_name) & is.na(d_lin) ) {
    #d_name not in mk and d_lin not in master key || ASSOCIATION == 0
    assoc <- 0
    rows <- data.frame(matrix(ncol = 3, nrow = 0))
  }
  if (nrow(rows) >= 1) {
    rows$time <- d_time
    rows$total.umi <- d_numi
    rows$association <- assoc
    rows$cell.index <- d_idx
    return(rows)
  }
}



tic()
aTable <- bind_rows(apply(bigDataCell,1,outerfunc)) #21.86s, 22.06
toc()


##### Step 3: Collecting UMI Data #####

tic("Subsetting matrix") #Times: 12.55s, 12.55s, 11.8s

#ABILITY TO RUN MULTIPLE GENES AT A TIME DONE HERE
genes <- c('rps-23')
genes_present <- c()
geneidx <- c()
for (gene in genes) {
  
  geneidx <- append(geneidx, which(bigDataGene$gene_short_name %in% c(gene)))
  genes_present <- append(genes_present, bigDataGene$gene_short_name[which(bigDataGene$gene_short_name %in% c(gene))])

}

mm <- bigmm[geneidx,]
toc()


tic('Scraping UMI table')
UMI_col <- vector(mode="character", length=nrow(aTable))
calc_tpm_func <- function(x, y) {(as.integer(x) / as.integer(y)) * 1000000}

for (i in 1:length(geneidx)) {
  UMI_col <- mm[as.integer(aTable$cell.index)]
  aTable[genes_present[i]] <- UMI_col

}
toc()

for (i in 1:length(genes_present)) {
  name <- glue("{genes_present[i]}_TPM")
  aTable[as.character(name)] <- mapply(calc_tpm_func, aTable[genes_present[i],], aTable$total.umi)
}


mean_tpm_table <- aTable %>%
  group_by(model.cellname, gene.name, time) %>% 
  dplyr::summarize(mean_tpm = mean(TPM, na.rm = TRUE),std_err = sd(TPM, na.rm = TRUE) / n(), association_mean = mean(as.integer(association), na.rm = TRUE))

mean_tpm_table <- mean_tpm_table %>%
  group_by(model.cellname) %>%
  filter(n() >= 6)

mean_tpm_table <- transform(mean_tpm_table, time = as.numeric(time))


tic("Generating output CSVs") #Times: 


#Make path
setwd(outputDir)
outputgene <- as.character(genes[1])
outputdate <- as.character(Sys.Date())
dir.create(file.path(getwd(), outputdate))
setwd(glue("{getwd()}\\{outputdate}"))
dir.create(file.path(getwd(), outputgene))
setwd(glue("{getwd()}\\{outputgene}"))
sessionDir <- getwd()

split_df <- split(mean_tpm_table, mean_tpm_table$model.cellname)
for (i in 1:length(split_df)) {
  #Goes through every cell df
  cell_df <- as.data.frame(split_df[i])
  cellname <- cell_df[1,1]
  #loess range changes the number of loess points. may have detrimental effects if there is little data. Current min: 35 points
  loess_range <- max(cell_df[3]) - min(cell_df[3])
  print(cellname)
  
  bplot <- ggplot(data = cell_df, mapping = aes(x=cell_df[,3], y=cell_df[,4])) +
    xlab("time") + 
    ylab("tpm") + 
    geom_errorbar(aes(ymin = cell_df[,4]-cell_df[,5], ymax=cell_df[,4]+cell_df[,5]), width=5, position=position_dodge(0.05)) + 
    stat_smooth(method = "loess", n = loess_range+1, span = 0.6)
  tpm_loess_iso <- ggplot_build(bplot)$data
  
  tpm_loess_iso[[1]]["data.type"] <- 'means'
  tpm_loess_iso[[2]]["data.type"] <- 'loess'
  
  
  cplot <- ggplot(data = cell_df, mapping = aes(x=cell_df[,3], y=cell_df[,6])) +
    xlab("time") + 
    ylab("assoc") + 
    stat_smooth(method = "loess", n = loess_range+1, span = 0.6)
  
  assoc_loess_iso <- ggplot_build(cplot)$data
  tpm_loess_iso[[2]]['assoc.factor'] <- assoc_loess_iso[[1]]$y
  
  
  fin_df <- rbind.fill((tpm_loess_iso[[1]]), (tpm_loess_iso[[2]]))
  
  outputloc <- glue("{sessionDir}\\{cellname}.csv")
  setwd(sessionDir)
  write.csv(fin_df, outputloc, row.names = FALSE)
  
}
toc()
##### #####
toc()
toc()
