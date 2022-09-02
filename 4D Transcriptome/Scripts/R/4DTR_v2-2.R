# Use for loop to run all genes

library(Matrix)
library(tictoc)
library(ggplot2)
library(plyr)
library(dplyr)
library(glue)
outputDir <- "C:\\Users\\chawmm\\Desktop\\4D Transcriptome\\output"
dataDir <- "C:\\Users\\chawmm\\Desktop\\4D Transcriptome\\data"
projectDir <- "C:\\Users\\chawmm\\Desktop\\4D Transcriptome"

setwd(projectDir)

`%!in%` <- Negate(`%in%`)

##### Step 1: Load data #####
tic("Step 1")
bigDataCell <- read.csv("C:\\Users\\chawmm\\Desktop\\4D Transcriptome\\data\\GSE126954_cell_annotation.csv")
bigDataGene <- read.csv("C:\\Users\\chawmm\\Desktop\\4D Transcriptome\\data\\GSE126954_gene_annotation.csv")

bigmm <- readMM("C:\\Users\\chawmm\\Desktop\\RNAseq Project\\scRNAseq Data\\Raw\\GSE126954_gene_by_cell_count_matrix.txt")


#Housekeeping genes
#(rps-23, rps-26, rps-27, rps-16, rps-2, rps-4, rps-17, rpl-24.1, rpl-27, rpl-33, rpl-36, rpl-35, and rpl-15)
#'lin-42', 'vab-19', 'let-502', 'mel-11', 'fem-2', 'mlc-4', 'hmp-1', 'hmp-2', 'hmr-1', 'spc-1', 'ifb-1', 'ifa-1', 'unc-52', 'elt-6', 'elt-3'
#CAN ONLY DO ONE GENE AT A TIME. CAN COMBINE IN PANDAS


#Instead of using cell names to search, use lineage names to search. 


masterkey <- read.csv("C:\\Users\\chawmm\\Desktop\\4D Transcriptome\\cell keys\\masterkey.csv") #Spaces are replaced by dots. data cellname --> data.cellname


##### Specify genes #####
# Functional genes genes <- c('hmp-2','hmp-1','emb-9')

#genes <- c('acr-16', 'lev-11', 'unc-54', 'let-502', 'unc-29', 'elt-1', 'vab-19', 'ceh-17')

#genes <- c('eps-8', 'hmr-1', 'cut-6', 'elt-3', 'let-502', 'mel-11')

genes <- c('unc-5', 'unc-6', 'unc-40', 'egl-21', 'egl-3', 'nmr-1', 'snf-11', 'cha-1', 'cho-1',
            'ace-1', 'ace-2', 'nmr-2', 'eat-4', 'cat-1', 'ceh-17', 'aptf-1')
toc()
##### Step 2: Filtering #####
tic("Step 2")
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



templateTable <- bind_rows(apply(bigDataCell,1,outerfunc)) #21.86s, 22.06
toc()
##### Running For Loop #####
for (gene in genes) {
  if (gene%!in%bigDataGene$gene_short_name) {
    next
  }
  tic(gene)
  aTable <- templateTable
  geneidx <- c()
  geneidx <- append(geneidx, which(bigDataGene$gene_short_name %in% gene))
  mm <- bigmm[geneidx,]
  
  fill_umi <- function(x){ #where x == list of cell indices
    return(mm[as.integer(x)])  
  }
  
  aTable$UMI <- lapply(aTable$cell.index, fill_umi)
  
  calc_tpm_func <- function(x, y) {(as.integer(x) / as.integer(y)) * 1000000}
  
  aTable$TPM <- mapply(calc_tpm_func, aTable$UMI, aTable$total.umi)
  
  
  
  mean_tpm_table <- aTable %>%
    group_by(model.cellname, time) %>% 
    dplyr::summarize(mean_tpm = mean(TPM, na.rm = TRUE),std_err = sd(TPM, na.rm = TRUE) / n(), association_mean = mean(as.integer(association), na.rm = TRUE))
  
  mean_tpm_table <- mean_tpm_table %>%
    group_by(model.cellname) %>%
    filter(n() >= 6)
  
  mean_tpm_table <- transform(mean_tpm_table, time = as.numeric(time))
  
  ##### Better generation #####
  
  setwd(outputDir)
  outputgene <- as.character(gene)
  outputdate <- as.character(Sys.Date())
  dir.create(file.path(getwd(), outputdate))
  setwd(glue("{getwd()}\\{outputdate}"))
  dir.create(file.path(getwd(), outputgene))
  setwd(glue("{getwd()}\\{outputgene}"))
  sessionDir <- getwd()
  
  split_df <- split(mean_tpm_table, mean_tpm_table$model.cellname)
  
  loess_generate <- function(listofdf){
    cellname <- listofdf
    cell_df <- split_df[[listofdf]]
    loess_range <- max(cell_df[2]) - min(cell_df[2]) #MIN / MAX Time
    bplot <- ggplot(data = cell_df, mapping = aes(x=cell_df[,2], y=cell_df[,3])) +
      xlab("time") + 
      ylab("tpm") + 
      geom_errorbar(aes(ymin = cell_df[,3]-cell_df[,4], ymax=cell_df[,3]+cell_df[,4]), width=5, position=position_dodge(0.05)) + 
      stat_smooth(formula = y~x, method = "loess", n = loess_range+1, span = 0.6)
    tpm_loess_iso <- ggplot_build(bplot)$data
    #print(nrow(tpm_loess_iso[[1]]))
    #print(nrow(tpm_loess_iso[[2]]))
    tpm_loess_iso[[1]]["data.type"] <- 'means'
    tpm_loess_iso[[2]]["data.type"] <- 'loess'
    cplot <- ggplot(data = cell_df, mapping = aes(x=cell_df[,2], y=cell_df[,5])) +
      xlab("time") + 
      ylab("assoc") + 
      stat_smooth(formula = y~x, method = "loess", n = loess_range+1, span = 0.6)
    
    assoc_loess_iso <- ggplot_build(cplot)$data
    tpm_loess_iso[[2]]['assoc.factor'] <- assoc_loess_iso[[1]]$y
    
    
    fin_df <- rbind.fill((tpm_loess_iso[[1]]), (tpm_loess_iso[[2]]))
    
    outputloc <- glue("{sessionDir}\\{cellname}.csv")
    setwd(sessionDir)
    write.csv(fin_df, outputloc, row.names = FALSE)
  }
  
  lapply(names(split_df), loess_generate)
  
  ##### Generate plots.pdf #####
  plots <- list()
  for (i in 1:length(split_df)) {
    data <- split_df[[i]]
    title <- glue("Expression of {outputgene} in {names(split_df)[i]}")
    loess_range <- max(data[2]) - min(data[2])
    plot <- ggplot(data, mapping = aes(x = time, y = mean_tpm)) + 
      ggtitle(title) + 
      xlab("Time (minutes post-first-cleavage)") + 
      ylab("Transcripts per Million") + 
      geom_point() +
      geom_errorbar(aes(ymin = mean_tpm-std_err, ymax = mean_tpm+std_err)) + 
      stat_smooth(formula = y~x, method = "loess", n = loess_range+1, span = 0.6)
    
    plots[[i]] <- plot
  }
  setwd(sessionDir)
  filename <- glue("{outputgene}_plots.pdf")
  ggsave(
    filename = filename, 
    plot = marrangeGrob(plots, nrow=4, ncol=4), 
    width = 15, height = 9
  )
  
  
  toc()
}
