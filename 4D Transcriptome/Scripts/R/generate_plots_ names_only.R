#Purpose: Generate plots of target gene across all cells

library(Matrix)
library(tictoc)
library(ggplot2)
library(plyr)
library(dplyr)
library(glue)
tic("Total Runtime:") # 156.3s
outputDir <- "C:\\Users\\chawmm\\Desktop\\4D Transcriptome\\output"
dataDir <- "C:\\Users\\chawmm\\Desktop\\4D Transcriptome\\data"
projectDir <- "C:\\Users\\chawmm\\Desktop\\4D Transcriptome"

setwd(projectDir)

`%!in%` <- Negate(`%in%`)

bigDataCell <- read.csv("C:\\Users\\chawmm\\Desktop\\4D Transcriptome\\data\\GSE126954_cell_annotation.csv")
bigDataGene <- read.csv("C:\\Users\\chawmm\\Desktop\\4D Transcriptome\\data\\GSE126954_gene_annotation.csv")

bigmm <- readMM("C:\\Users\\chawmm\\Desktop\\RNAseq Project\\scRNAseq Data\\Raw\\GSE126954_gene_by_cell_count_matrix.txt")



##### Step 1: filter out all cells where the name is unknown #####

bdc <- bigDataCell[, c("n.umi", "plot.cell.type", "lineage", "embryo.time")]
bdc$index <- 1:nrow(bigDataCell)

bdc_copy <- bdc[!is.na(bdc$plot.cell.type),]


calc_tpm_func <- function(x, y) {(as.integer(x) / as.integer(y)) * 1000000}


#genes <- c('hmr-1', 'cdh-1', 'cdh-2', 'cdh-3', 'cdh-4', 'cdh-5', 'cdh-6', 'cdh-7', 'cdh-8', 'cdh-9', 'cdh-10', 'cdh-11', 'cdh-12', 'T01D3.1', 'T01D3',
#'efn-1', 'efn-2', 'efn-3', 'vab-1', 'unc-5', 'unc-6', 'unc-40', 'sax-3',
#'par-1', 'par-2', 'par-3', 'par-4', 'par-5', 'par-6')

#genes <- c('cha-1','cho-1','ace-1','ace-2')
genes <- c('unc-17')
for (gene in genes) {
  
  if (gene%!in%bigDataGene$gene_short_name) {
    next
  }
  geneidx <- c()
  geneidx <- append(geneidx, which(bigDataGene$gene_short_name %in% c(gene)))
  bdc <- bdc_copy
  
  
  mm <- bigmm[geneidx,bdc$index]
  fill_umi <- function(x){ #where x == list of cell indices
    return(mm[as.integer(x)])  
  }
  
  bdc$UMI <- lapply(bdc$index, fill_umi)
  
  bdc$TPM <- mapply(calc_tpm_func, bdc$UMI, bdc$n.umi)
  
  mean_tpm_table <- bdc %>%
    group_by(plot.cell.type, embryo.time) %>% 
    dplyr::summarize(mean_tpm = mean(TPM, na.rm = TRUE),std_err = sd(TPM, na.rm = TRUE) / n())
  
  mean_tpm_table <- mean_tpm_table %>%
    group_by(plot.cell.type) %>%
    filter(n() >= 6)
  
  mean_tpm_table <- transform(mean_tpm_table, time = as.numeric(embryo.time))
  
  
  setwd(outputDir)
  outputgene <- as.character(gene)
  outputfolder <- "ACh_plots"
  dir.create(file.path(getwd(), outputfolder))
  setwd(glue("{getwd()}\\{outputfolder}"))
  sessionDir <- getwd()
  
  split_df <- split(mean_tpm_table, mean_tpm_table$plot.cell.type)
  
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
  filename <- glue("{outputgene}_name_plots.pdf")
  ggsave(
    filename = filename, 
    plot = marrangeGrob(plots, nrow=5, ncol=2), 
    width = 15, height = 9
  )
}
