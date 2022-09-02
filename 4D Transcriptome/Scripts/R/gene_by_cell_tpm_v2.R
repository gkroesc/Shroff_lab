##### Step 0: Load libraries, set directories #####
library(Matrix)
library(tictoc)
library(ggplot2)
library(plyr)
library(dplyr)
library(glue)
library(forecast)
library(ggpubr)

outputDir <- "C:\\Users\\chawmm\\Desktop\\4D Transcriptome\\output"
dataDir <- "C:\\Users\\chawmm\\Desktop\\4D Transcriptome\\data"
projectDir <- "C:\\Users\\chawmm\\Desktop\\4D Transcriptome"

setwd(projectDir)

`%!in%` <- Negate(`%in%`)

##### Step 1: Load data #####
tic("Step 1")
bigDataCell <- read.csv("C:\\Users\\chawmm\\Desktop\\4D Transcriptome\\data\\GSE126954\\GSE126954_cell_annotation.csv")
bigDataGene <- read.csv("C:\\Users\\chawmm\\Desktop\\4D Transcriptome\\data\\GSE126954\\GSE126954_gene_annotation.csv")
bigmm <- readMM("C:\\Users\\chawmm\\Desktop\\4D Transcriptome\\data\\GSE126954\\GSE126954_gene_by_cell_count_matrix.txt")

masterkey <- read.csv("C:\\Users\\chawmm\\Desktop\\4D Transcriptome\\cell keys\\masterkey.csv") #Spaces are replaced by dots. data cellname --> data.cellname

main_table <- bigDataCell %>%
  mutate(index=1:nrow(bigDataCell))

##### Step 1.a: Specify Genes #####


#genes <- c("fmi-1",  "par-1", 'rps-23', 'eps-8')

# Cadherin superfamily proteins
#genes <- c('hmr-1','cdh-1','cdh-3','cdh-4','cdg-5','fmi-1','cdh-7','cdh-8','cdh-9','cdh-10','cdh-11','cdh-12')

# Cell signaling regulators of adhesion in the ephrin/Eph receptor pathway
#genes <- c('efn-2','efn-4','vab-1')

# Guidance cue promoters
#genes <- c('unc-5','unc-6','unc-40','sax-3')

# The PAR Proteins
#genes <- c('par-1','par-2','par-3','par-4','par-5','par-6')

genes <- c('eps-8', 'emb-9', 'efn-2')
genels <- c()
for (gene in genes) {
  if (gene %in% bigDataGene$gene_short_name) { 
    genels <- append(genels, gene)
    }
}
genes <- genels
##### Step 2: Collect UMI, TPM Data #####
toc()
tic("Step 2")

mm <- bigmm[which(bigDataGene$gene_short_name %in% genes),]

generate_tables <- function(x, table) {
  temp_table <- table
  temp_table$gene <- x
  temp_table$umi_col <- mm[which(genes %in% x),] 
  return (temp_table)
}

main_table <- bind_rows(lapply(genes, generate_tables, main_table))
main_table <- main_table %>% 
  filter(passed_initial_QC_or_later_whitelisted == TRUE)# %>%
  # select(n.umi, d.name = plot.cell.type, time.mpfc = embryo.time, d.lineage = lineage,
  #        m.name = index, gene, umi= umi_col) %>%
  # filter(!is.na(d.name) | !is.na(d.lineage))

calc_tpm_func <- function(umi, n.umi) {(as.integer(umi) / as.integer(n.umi)) * 1000000}
adj_time_func <- function(x) { return (x+45)}

main_table$time.mpf <- unlist(lapply(main_table$time.mpfc, adj_time_func))
main_table$time.mpf <- unlist(lapply(main_table$embryo.time, adj_time_func))

main_table$tpm <- mapply(calc_tpm_func, main_table$umi, main_table$n.umi)
fndr_cell_func <- function(x){
  if (substr(x, 1, 2) == "AB" | substr(x, 1, 2) == "MS"){
    return (substr(x, 1, 2))
  }else{
    return (substr(x,1,1))
  }
}
##### Step 3: #####
toc()
tic("Step 3")
##### Step 3.a: Descriptive statistics#####
main_table %>%
  group_by(gene) %>%
  summarize(mean(tpm), median(tpm), sd(tpm))
##### Step 3.b: Time distribution graphs #####

time_distribution <- ggplot(data = main_table, mapping = aes(x = time.mpf)) + 
  geom_histogram(bins=30, color = 'white') + 
  #ggtitle("Distribution of data across time") + 
  xlab("Time (minutes post-fertilization)") + 
  ylab("Count") 
time_dist_ymax <- max(ggplot_build(time_distribution)$data[[1]]$count)*1.1

time_distribution + scale_y_continuous(expand = c(0,0),
                          limits=c(0, time_dist_ymax))

#time_dist_ymax <- max(ggplot_build(time_distribution)$data[[1]]$count)*1.1

time_distribution_lin <- main_table %>% 
  filter(!is.na(d.lineage) & is.na(d.name)) %>%
  ggplot(mapping = aes(x = time.mpf)) + 
  geom_histogram(bins=30, color = 'white') + 
  #ggtitle("Distribution of data with known lineage") + 
  xlab("Time (minutes post-fertilization)") + 
  ylab("Count") + 
  scale_y_continuous(expand = c(0,0),
                     limits=c(0,time_dist_ymax))

time_distribution_name <- main_table %>% 
  filter(!is.na(d.name) & is.na(d.lineage)) %>%
  ggplot(mapping = aes(x = time.mpf)) + 
  geom_histogram(bins=30, color = 'white') + 
  #ggtitle("Distribution of data with known name") + 
  xlab("Time (minutes post-fertilization)") + 
  ylab("Count") + 
  scale_y_continuous(expand = c(0,0),
                     limits=c(0,time_dist_ymax))

time_distribution_name_lin <- main_table %>% 
  filter(!is.na(d.name) & !is.na(d.lineage)) %>%
  ggplot(mapping = aes(x = time.mpf)) + 
  geom_histogram(bins=30, color = 'white') + 
  #ggtitle("Distribution of data with known name and lineage") + 
  xlab("Time (minutes post-fertilization)") + 
  ylab("Count") + 
  scale_y_continuous(expand = c(0,0),
                     limits=c(0,time_dist_ymax))

time_dist_fig <- ggarrange(time_distribution, 
                           time_distribution_lin, 
                           time_distribution_name,
                           time_distribution_name_lin, 
                           nrow = 2, ncol = 2,
                           labels = c("A", "B", "C", "D"))
time_dist_fig











#####Workspace#####

lins_only <- main_table[!is.na(main_table$d.lineage),]
lins_only$founder.cell <- unlist(lapply(lins_only$d.lineage, fndr_cell_func)) #Some cases where: ABplxppap/MSappap will be labelled as AB

data <- lins_only
neworder <- c("AB", "MS", "C", "D", "E")
data <- arrange(transform(data,
                          founder.cell=factor(founder.cell,levels=neworder)),founder.cell)

time_distribution_name_lin <- data %>%
  filter(tpm > 0) %>%
  filter(time.mpf < 200) %>%
  filter(founder.cell == 'AB') %>%
  # filter(founder.cell %in% neworder) %>%
  ggplot(mapping = aes(x = tpm)) +
  geom_histogram(bins=50, color = 'black') +
  ggtitle("Number of cells expressing cadherin superfamily genes (0 - 200 m.p.f)") +
  xlab("Transcripts per Million (TPM)") +
  ylab("Count") + 
  facet_wrap(~gene)
  # facet_wrap(~founder.cell) + 
  # labs(fill = "Gene")
time_distribution_name_lin


bigDataCell %>%
  filter(is.na(cell.type) | 
           cell.type %in% c("Body_wall_muscle","Hypodermis", "Coelomocyte", 
                            "Ciliated_amphid_neuron", "Ciliated_non_amphid_neuron", 
                            "Glia", "GLR", "Intestinal_and_rectal_muscle", "Intestine", 
                            "Seam_cell", "Pharyngeal_muscle", "Pharyngeal_intestinal_valve", "Pharyngeal_neuron")) %>%
  ggplot(mapping = aes(x = embryo.time)) + 
    geom_histogram(color = "white") + 
    #scale_y_continuous(trans = 'log10') + 
    facet_wrap(~cell.type)

bigDataCell %>%
  filter(!is.na(lineage) & !is.na(plot.cell.type)) %>% 

  ggplot(mapping = aes(x = embryo.time)) + 
  geom_histogram(color = "white") + 
  ggtitle("Distribution of all cells with cell name and lineage") + 
  scale_y_continuous(expand = c(0,0),
                     limits=c(0,13500))

bdc <- bdc %>% 
  mutate(linname = case_when(
    !is.na(plot.cell.type) & !is.na(lineage) ~ "lineage and cell name",
    !is.na(plot.cell.type) & is.na(lineage) ~ "cell name only",
    is.na(plot.cell.type) & !is.na(lineage) ~ "lineage only")) %>%
  mutate(adj.time = embryo.time+45)




main_table %>%  
  filter(cell.subtype %in% c('BWM_head_row_1', 'BWM_posterior', 'hyp1_hyp2', 'hyp4_hyp5_hyp6')) %>%
  filter(gene != 'efn-2') %>%
  group_by(gene, cell.type, time.mpf) %>%
  summarize(mean_tpm = mean(tpm), std_dev = sd(tpm)) %>%

  ggplot(mapping = aes(x = time.mpf, y = mean_tpm, color = cell.type)) + 
  ggtitle("emb-9, eps-8 expression in body wall muscles, hypodermis") + 
  geom_line() + 
  xlab('Time (minutes post fertilization') + 
  ylab('Mean Transcripts per Million') + 
  geom_errorbar(aes(ymin = mean_tpm - std_dev, ymax= mean_tpm + std_dev), width=5, position=position_dodge(0.05)) + 
  
  geom_smooth(method = 'loess') + 
  facet_wrap(~gene)
  

unique(bigDataCell[which(bigDataCell$cell.type == 'Hypodermis'),]['plot.cell.type'])






# ##### Functions #####
# namelin <- function(aname, alin) {
#   rows <- masterkey[which(masterkey$data.lineage == alin & masterkey$data.cellname == aname),]
#   return(rows)
# }
# 
# #Name known
# 
# name_only <- function(aname, alin){
#   rows <- masterkey[which(masterkey$data.cellname == aname),]
#   return(rows)
# }
# 
# #Lineage known 
# 
# lin_only <- function(aname, alin) {
#   rows <- masterkey[which(masterkey$data.lineage == alin),]
#   return(rows)
# }
# 
# outerfunc <- function(x){ #Where x = row of dataframe
#   d_name <- x['plot.cell.type']
#   d_lin <- x['lineage']
#   d_time <- x['embryo.time']
#   d_numi <- x['n.umi']
#   d_idx <- x['index']
#   #print(d_name)
#   #print(d_lin)
#   if (!is.na(d_name) & !is.na(d_lin) ) {
#     #d_name and d_lin in masterkey || ASSOCIATION == 3
#     assoc <- 3
#     rows <- namelin(d_name, d_lin)
#     #print(rows)
#   }else if(!is.na(d_name) & is.na(d_lin)) {
#     #d_name in mk but d_lin not in masterkey || ASSOCIATION == 1
#     assoc <- 1
#     rows <- name_only(d_name, d_lin)
#     #print(rows)
#   }else if(is.na(d_name) & !is.na(d_lin) ) {
#     #d_name not in mk but d_lin in masterkey || ASSOCIATION == 2
#     assoc <- 2
#     rows <- lin_only(d_name, d_lin)
#     #print(rows)
#   }else if(is.na(d_name) & is.na(d_lin) ) {
#     #d_name not in mk and d_lin not in master key || ASSOCIATION == 0
#     assoc <- 0
#     rows <- data.frame(matrix(ncol = 3, nrow = 0))
#   }
#   if (nrow(rows) >= 1) {
#     rows$time <- d_time
#     rows$total.umi <- d_numi
#     rows$association <- assoc
#     rows$cell.index <- d_idx
#     return(rows)
#   }
# }
# 
# 
# 
# 
# ##### Gene Selection #####
# gene <- "eps-8"
# geneidx <- which(bigDataGene$gene_short_name == gene)
# ##### Execution#####
# templateTable <- bind_rows(apply(bigDataCell,1,outerfunc)) #21.86s, 22.06
# 
# aTable <- templateTable
# 
# mm <- bigmm[geneidx,]
# 
# fill_umi <- function(x){ #where x == list of cell indices
#   return(mm[as.integer(x)])  
# }
# 
# aTable$UMI <- lapply(aTable$cell.index, fill_umi)
# 
# calc_tpm_func <- function(x, y) {(as.integer(x) / as.integer(y)) * 1000000}
# 
# aTable$TPM <- mapply(calc_tpm_func, aTable$UMI, aTable$total.umi)
# 
# 
# 
# mean_tpm_table <- aTable %>%
#   group_by(model.cellname, time) %>% 
#   dplyr::summarize(mean_tpm = mean(TPM, na.rm = TRUE),std_err = sd(TPM, na.rm = TRUE) / n(), association_mean = mean(as.integer(association), na.rm = TRUE))
# 
# mean_tpm_table <- mean_tpm_table %>%
#   group_by(model.cellname) %>%
#   filter(n() >= 6)
# 
# mean_tpm_table <- transform(mean_tpm_table, time = as.numeric(time))
# ##### Generate Loess #####
# subset_table <- mean_tpm_table[which(mean_tpm_table$model.cellname == 'xxxr'),]
# loess_range <- max(subset_table$time) - min(subset_table$time) + 1
# sample_plot <- ggplot(data = subset_table, mapping = aes(x=time, y=mean_tpm)) + 
#   ggtitle("Average TPM vs Time")+
#   xlab("Time (minutes pfc)") + 
#   geom_line() + 
#   geom_errorbar(aes(ymin = mean_tpm-std_err, ymax= mean_tpm+std_err), width=5, position=position_dodge(0.05)) + 
#   geom_smooth(method = "loess", span=0.2, color="red") +
#   geom_smooth(method = "loess", span=0.4, color="green") +in
#   geom_smooth(method = "loess", span=0.6, color="blue") +
#   geom_smooth(method = "loess", span=0.75, color="yellow") +
#   geom_smooth(method = "loess", span=0.9, color="orange") +
#   ylab("TPM")
# sample_plot
# 
# loess_plot <- ggplot(data = subset_table, mapping = aes(x=time, y=mean_tpm)) + 
#   ggtitle("Average TPM vs Time")+
#   xlab("Time (minutes pfc)") + 
#   geom_smooth(method = "loess", span=0.6, color="green") +
#   ylab("TPM")
# 
# loess_plot
# loess_data <- ggplot_build(loess_plot)$data[[1]]
# 
# 
# 
# 
# 
# model1 <- lm(mean_tpm ~ time, subset_table)
# model2 <- lm(mean_tpm ~ time+std_err, subset_table)
# 
# library(AICcmodavg)
# 
# #define list of models
# models <- list(model1, model2)
# 
# #specify model names
# mod.names <- c('model1', 'model2')
# 
# #calculate AIC of each model
# aictab(cand.set = models, modnames = mod.names)
# 
# cars.lo <- loess(dist ~ speed, cars)
# predict(cars.lo, data.frame(speed = seq(5, 30, 1)), se = TRUE)
# 
# subs.lo <- loess(mean_tpm ~ time, subset_table)
# 
# loess.as(subset_table$time, subset_table$mean_tpm, degree = 1, criterion = c("aicc", "gcv"), 
#          family = c("gaussian", "symmetric"), user.span = NULL, 
#          plot = TRUE)

