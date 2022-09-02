##### LIBRARIES #####
library(Matrix)
library(tictoc)
library(ggplot2)
library(plyr)
library(dplyr)
library(glue)
library(forecast)
library(ggpubr)
library(gridExtra)
library(fANCOVA)

##### DIRECTORIES #####
outputDir <- "C:\\Users\\chawmm\\Desktop\\4D Transcriptome\\output"
dataDir <- "C:\\Users\\chawmm\\Desktop\\4D Transcriptome\\data"
projectDir <- "C:\\Users\\chawmm\\Desktop\\4D Transcriptome"

setwd(projectDir)

`%!in%` <- Negate(`%in%`)

##### GSE KEYS #####
bigDataCell <- read.csv("C:\\Users\\chawmm\\Desktop\\4D Transcriptome\\data\\GSE126954\\GSE126954_cell_annotation.csv")
bigDataGene <- read.csv("C:\\Users\\chawmm\\Desktop\\4D Transcriptome\\data\\GSE126954\\GSE126954_gene_annotation.csv")
founder_key <- read.csv("C:\\Users\\chawmm\\Desktop\\4D Transcriptome\\cell keys\\packer_s6.csv")


##### MATRIX DATA #####
bigmm <- readMM("C:\\Users\\chawmm\\Desktop\\4D Transcriptome\\data\\GSE126954\\GSE126954_gene_by_cell_count_matrix.txt")

##### SPECIFY GENES HERE #####
#genes <- c('unc-5', 'unc-40', 'sax-3', 'vab-1', 'plx-1', 'cfz-2', 'mig-1', 'mom-5', 'lin-17')
# genes <- c('syg-1', 'syg-2', 'pfk-1.1', 'pfk-1.2', 'pfkb-1.1', 'pfkb-1.2')
genes <- c('cha-1', 'cho-1', 'unc-17', 'unc-25', 'unc-30', 'unc-46', 'unc-47', 'unc-49', 'exp-1', 'ace-1', 'ace-2', 'ace-3'  )
##### CELL MODEL KEYS #####
masterkey <- read.csv("C:\\Users\\chawmm\\Desktop\\4D Transcriptome\\cell keys\\masterkey.csv") #Spaces are replaced by dots. data cellname --> data.cellname

##### FUNCTIONS #####
generate_tables <- function(x, table) { # where x = gene
  temp_table <- table
  temp_table$gene <- x
  temp_table$umi_col <- mm[which(genes == x),] 
  return (temp_table)
}

calc_tpm_func <- function(umi, n.umi) {(as.integer(umi) / as.integer(n.umi)) * 1000000}
adj_time_func <- function(x) { return (x+45)}


clade_func <- function(x) { #Where x is a single cell in lineage name column
  if (is.na(x)) { return()}
  if (grepl(substr(x, 1, 2), 'ABMS')) {
    return (substr(x,1,2))
  }else{
    if (grepl(substr(x,1,1), 'ECD')) {
      return(substr(x,1,1))
    if (grepl('Z', x)) {
      return('Z')
    }
    }
  }
}


generation_number_func <- function(x){ #where x is the lineage name
  #In cases where there are numbers in the lineage name (There shouldnt be?)
  if (grepl("[0-9]", x) == TRUE | is.na(x)) {
    return()
  }
  #In cases where there is a '/': 
  if (grepl('/', x) == TRUE) {
    x <- strsplit(x, '/')[[1]][1]
  }
  
  if (grepl('E', substr(x, 1,1))) {
    generation_after_p0 <- nchar(x)-1+4
    return(generation_after_p0)
    
  }else{
    if (grepl('C', substr(x, 1,1))) {
      generation_after_p0 <- nchar(x)-1+4
      return(generation_after_p0)
      
    }else{
      if (grepl('D', substr(x, 1,1))) {
        generation_after_p0 <- nchar(x)-1+5
        return(generation_after_p0)
        
      }else{
        if (grepl('AB', substr(x, 1,2))){
          generation_after_p0 <- nchar(x)-2+2
          return(generation_after_p0)
          
        }else{
          if (grepl('MS', substr(x, 1,2))) {
            generation_after_p0 <- nchar(x)-2+4
            return(generation_after_p0)
            
          }
        }
      }
    }
  }
}

##### INITIATE MAIN TABLE #####

main_table <- bigDataCell %>%
  mutate(index=1:nrow(bigDataCell))

##### UMI COLLECTION #####
genes <- append(genes, 'emb-9')
geneidx <- c()
fin_genes <- c()
for (i in 1:length(genes)) { 
  if (genes[i] %in% bigDataGene$gene_short_name) { 
    fin_genes <- append(fin_genes, genes[i])
    geneidx <- append(geneidx, which(bigDataGene$gene_short_name == genes[i]))
  }else{next}

}

main_table$clade <- lapply(main_table$lineage, clade_func)
main_table$clade <- sapply(main_table$clade, toString)
main_table$generation_num <- lapply(main_table$lineage, generation_number_func)
main_table$generation_num <- sapply(main_table$generation_num, toString)
main_table$generation_num <- sapply(main_table$generation_num, as.integer)

mm <- bigmm[geneidx,]
main_table <- bind_rows(lapply(genes, generate_tables, main_table))

main_table <- main_table %>% 
  filter(passed_initial_QC_or_later_whitelisted == TRUE) %>%
  select( -X, -cell, -time.point, -batch, -raw.embryo.time, -raw.embryo.time.bin, d.name = plot.cell.type, d.lineage = lineage)

main_table$time.mpf <- unlist(lapply(main_table$embryo.time, adj_time_func))
main_table$tpm <- mapply(calc_tpm_func, main_table$umi, main_table$n.umi)


p2_main_table <- main_table %>%
  filter(clade == 'Z')
  
all_cells <- sort(unique(unlist(p2_main_table$d.name)))

plots <- c()
for (i in 1:length(all_cells)) { 
  
  
plot <- main_table %>%
  filter(d.name == all_cells[i]) %>%
  filter(genes %!in% c('syg-1', 'syg-2', 'emb-9')) %>%
  group_by(gene, d.name, time.mpf) %>%
  summarize(mean_tpm = mean(tpm), std_dev = sd(tpm, na.rm = TRUE)) %>%
  ggplot(mapping = aes(x = time.mpf, y = mean_tpm, color = gene)) +
  geom_point() +
  geom_smooth(method = 'loess', se=F) +
  ggtitle(glue("PFK expression in '{all_cells[i]}'"))
  xlab('Time (minutes post fertilization)') +
  ylab('Mean TPM')


}

main_table %>%
  filter(clade %in% c('C', 'D')) %>%
  filter(gene %!in% c('emb-9', 'syg-1', 'syg-2')) %>%
  
  group_by(clade, gene, time.mpf) %>%
  summarize(mean_tpm = mean(tpm), std_dev = sd(tpm)) %>%
  ggplot(mapping = aes(x = time.mpf, y = mean_tpm, color = clade)) + 
  geom_point() + 
  #geom_errorbar(aes(ymin = mean_tpm - std_dev, ymax= mean_tpm + std_dev), width=5, position=position_dodge(0.05)) + 
  geom_smooth(method = 'loess') +
  xlab("Time (minutes post fertilization)") + 
  ylab("Mean TPM") + 
  ggtitle('PFK Expression across P2/3 lineages') + 
  facet_wrap(~gene)





neurons_csv <- read.csv("C:\\Users\\chawmm\\Desktop\\4D Transcriptome\\ALL_WA_NEURONS.csv")
neurons_csv <- neurons_csv %>%
  filter(grepl("\\s", Lineage)) %>%
  filter(!grepl("\\.", Lineage))
neurons_csv$Lineage <- unlist(lapply(neurons_csv$Lineage, function(x){
  splitx <- strsplit(x, " ")
  newx <- paste(splitx[[1]], collapse = "")
  return(newx)
  }))

neurons_s6_joined <- neurons_csv %>% 
  left_join( founder_key, by = c("Lineage" = "cell")) %>%
  select(Neuron, Lineage, annotation_name, annotated_in_this_study)

neurons_main_table <- main_table%>%
  filter(!is.na(d.name)) %>%
  filter(d.name %in% neurons_s6_joined$Neuron | (!is.na(d.lineage) & d.lineage %in% neurons_s6_joined$annotation_name )) %>%
  filter(gene %in% c('syg-1', 'syg-2')) %>%
  group_by(d.name) %>%
  filter(n() > 30)

neurons_filt <- unique(unlist(neurons_main_table$d.name))
neurons_filt <- sort(neurons_filt)
plots <- c()
for (i in 1:length(neurons_filt)) {
  cell <- neurons_filt[i]
  
  plot <- neurons_main_table %>%
    filter(d.name == cell) %>%
    filter(max(tpm) > 0) %>%
    group_by(gene, d.name, time.mpf) %>%
    summarize(mean_tpm = mean(tpm), std_dev = sd(tpm, na.rm = TRUE)) %>%
    ggplot(mapping = aes(x = time.mpf, y = mean_tpm, color = gene)) +
    geom_point() + 
    geom_errorbar(aes(ymin = mean_tpm - std_dev, ymax= mean_tpm + std_dev), width=5, position=position_dodge(0.05)) + 
    geom_smooth(method = 'loess') +
    xlab("Time (minutes post fertilization)") + 
    ylab("Mean TPM") + 
    #scale_x_continuous(breaks = round(seq(0,800, by = 100),1)) +
    lims(x = c(0, 850), y = c(NA, 1000) )
    #coord_trans(y="log2") + 
    ggtitle(glue("syg-1/2 expression in '{cell}'")) #+ 
    #facet_wrap(~d.name)
  
  plots[[i]] <- plot
}
# scale_y_continuous(breaks = round(seq(0, max(output$TPM), by = 2500),1)) + 
#   geom_jitter(alpha=0.1)+ 
#   coord_trans(y="log2") + 
#   xlab("Time (minutes post first-cleavage)") + 
#   ylab("Transcripts per Million")

ggsave(
  filename = 'testplot.pdf',
  #filename = 'syg-1_syg-2_expression_in_packer_neurons_revised.pdf',
  plot = marrangeGrob(plots, nrow=2, ncol = 2),
  #width = 1000, height = 600, units = "px"
  width = 10, height = 7, units = "in"
)
  




##### 8-22-2022 #####
main_table %>%
  filter(d.name == 'ADF') %>%
  group_by(gene, d.name, time.mpf) %>%
  summarize(mean_tpm = mean(tpm), std_dev = sd(tpm, na.rm = TRUE)) %>%
  ggplot(mapping = aes(x = time.mpf, y = mean_tpm, color = gene)) +
  #geom_point() +
  geom_smooth(method = 'loess', se=F) +
  xlab('Time (minutes post fertilization)') +
  ylab('Mean TPM')



cells <- c('BWM_posterior', 'BWM_anterior', 'BWM_head_row_1', 'hyp4_hyp5_hyp6')
plots <- c()
for (i in 1:length(cells)) {
  
name <- cells[i]
gname <- 'emb-9'
filt_tab <- main_table %>%
  filter(d.name == name) %>%
  filter(gene == gname) %>%
  group_by(gene, d.name, time.mpf) %>%
  summarize(mean_tpm = mean(tpm), std_dev = sd(tpm, na.rm = TRUE))


model <- loess.as(filt_tab$time.mpf, filt_tab$mean_tpm, degree = 1, criterion = c("aicc"))
pred <- predict(model)

plot <- ggplot(data = cbind(filt_tab, pred), mapping = aes(time.mpf, mean_tpm)) +
  geom_point() +
  ggtitle(glue('{gname} in {name}: ggplot Loess (B) vs fanCOVA loess (R)')) + 
  xlab('Time') + 
  ylab('TPM') + 
  geom_smooth(method = 'loess') + 
  geom_line(aes(y=pred, color = 'red'))

plots[[i]] <- plot

}
ggsave(
  filename = 'ggplot_vs_fancova_comp.pdf',
  plot = marrangeGrob(plots, nrow=1, ncol = 1),
  #width = 1000, height = 600, units = "px"
  width = 10, height = 7, units = "in"
)



# pred <- predict(model)
# main_table %>%
#   filter(d.name == 'ADF') %>%
#   filter(gene == 'sax-3') %>%
#   group_by(gene, d.name, time.mpf) %>%
#   summarize(mean_tpm = mean(tpm), std_dev = sd(tpm, na.rm = TRUE)) %>%
#   ggplot(mapping = aes(x = time.mpf, y = mean_tpm)) +
#   geom_point() +
#   geom_smooth(method = 'loess', se=F) +
#   xlab('Time (minutes post fertilization)') +
#   ylab('Mean TPM')






# cells <- main_table %>%
#   filter('neuron' %in% cell.type) %>%
#   filter(nchar(d.name) < 5) %>%
#   select(d.name)
# 
# cells <- as.vector(cells$d.name)
# cells <- unique(cells)
# plots <- c()
# for (i in 1:length(cells)) {
#   
#   plot <- main_table %>%
#     filter(d.name == cells[i]) %>%
#     group_by(gene, d.name, time.mpf) %>%
#     summarize(mean_tpm = mean(tpm), std_dev = sd(tpm, na.rm = TRUE)) %>%
#     ggplot(mapping = aes(x = time.mpf, y = mean_tpm, color = gene)) + 
#     #geom_point() + 
#     geom_smooth(method = 'loess', se=F) +
#     xlab('Time (minutes post fertilization)') + 
#     ylab('Mean TPM') + 
#     ggtitle(glue("Guidance Factors in {cells[i]}"))
#   plots[[i]] <- plot
# }
# 
# ggsave(
#   filename = 'NON_FAC_cil-amph-neur_vs_guid-fac.pdf', 
#   plot = marrangeGrob(plots, nrow=1, ncol = 1), 
#   #width = 1000, height = 600, units = "px"
#   width = 10, height = 7, units = "in"
# )






