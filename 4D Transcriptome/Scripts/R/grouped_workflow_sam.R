### Scripts for sam's figures

#After running step 1, run from 1.a
##### Step 0: Load libraries, set directories #####
library(Matrix)
library(tictoc)
library(ggplot2)
library(plyr)
library(dplyr)
library(tidyr)
library(glue)
library(forecast)
library(ggpubr)
library(gridExtra)

outputDir <- "C:\\Users\\chawmm\\Desktop\\4D Transcriptome\\output"
dataDir <- "C:\\Users\\chawmm\\Desktop\\4D Transcriptome\\data"
projectDir <- "C:\\Users\\chawmm\\Desktop\\4D Transcriptome"

setwd(projectDir)

`%!in%` <- Negate(`%in%`)

##### Step 1: Load data #####
tic("Step 1")
bigDataCell <- read.csv("C:/Users/chawmm/Desktop/4D Transcriptome/data/GSE126954/GSE126954_cell_annotation.csv")
bigDataGene <- read.csv("C:/Users/chawmm/Desktop/4D Transcriptome/data/GSE126954/GSE126954_gene_annotation.csv")
bigmm <- readMM("C:/Users/chawmm/Desktop/4D Transcriptome/data/GSE126954/GSE126954_gene_by_cell_count_matrix.txt")

masterkey <- read.csv("C:/Users/chawmm/Desktop/4D Transcriptome/cell keys/masterkey.csv") #Spaces are replaced by dots. data cellname --> data.cellname
founder_key <- read.csv("C:/Users/chawmm/Desktop/4D Transcriptome/for sam early embryogenesis/data/packer_s6.csv")

gast_cells <- read.csv("C:/Users/chawmm/Desktop/4D Transcriptome/for sam early embryogenesis/data/66_gastrulating_cells.csv")


##### Step 1.a: Specify Genes #####

desc <- "test"
t1 <- c("fmi-1",  "par-1", 'rps-23', 'eps-8')

d1 <- "cadherin superfamily proteins"
g1 <- c('hmr-1','cdh-1','cdh-3','cdh-4','cdh-5','fmi-1','cdh-7','cdh-8','cdh-9','cdh-10','cdh-11','cdh-12')

d2 <- "cell signaling reg of adh. efn receptor pathway"
g2 <- c('efn-2','efn-4','vab-1')

d3 <- "guidance cue promoters"
g3 <- c('unc-5','unc-6','unc-40','sax-3')

d4 <- "PAR proteins"
g4 <- c('par-1','par-2','par-3','par-4','par-5','par-6')
group_list <- c(d1, d2, d3, d4)
genes <- c(g1, g2, g3, g4)
gene_groups <- list(g1, g2, g3, g4)
descriptions <- rep(c(d1, d2, d3, d4), times= c(length(g1),
                                             length(g2), 
                                             length(g3), 
                                             length(g4) ))

gene_frame <- data.frame(gene.name = genes, group = descriptions)
gene_frame <- gene_frame %>% filter(gene.name %in% bigDataGene$gene_short_name)
founder_key <- founder_key %>%
  filter(annotated_in_this_study == 'TRUE') %>%
  filter(!is.na(annotation_name))






death_key <- founder_key%>%
  filter(dies == 'TRUE') 
##### Step 1.b: Specify Genes in CSV #####
gast_genes <- read.csv("C:/Users/chawmm/Desktop/4D Transcriptome/for sam early embryogenesis/data/Gastrulation_Genes_Grouped.csv")
gast_genes <- unlist(gast_genes$Gene)
gast_genes <- unlist(lapply(gast_genes, function(x){
  if (grepl('/', x)) {
    x <- strsplit(x, '/')
    x <- x[[1]][1]
    return(tolower(x))
  }else{
    return(tolower(x))
  }
}))

gast_genes <- gast_genes[gast_genes != '']

gene_frame <- data.frame(gene.name = gast_genes, group = 'Gastrulation genes')
gene_frame2 <- data.frame(gene.name = c('rps-23', 'rps-2', 'rps-4'), 
                          group = 'Housekeeping genes')

gene_frame <- rbind(gene_frame, gene_frame2)
gene_frame %>%
  filter(gene.name %!in% bigDataGene$gene_short_name)
gene_frame <- gene_frame %>% filter(gene.name %in% bigDataGene$gene_short_name)

##### Step 1.c: Specify Genes in GROUPED CSV #####
gast_genes <- read.csv("C:/Users/chawmm/Desktop/4D Transcriptome/for sam early embryogenesis/data/Gastrulation_Genes_Grouped.csv")
gene_frame2 <- data.frame(Gene = c('rps-23', 'rps-2', 'rps-4'), 
                          Category = 'Housekeeping genes', Function = "")

gene_frame <- rbind(gast_genes, gene_frame2)
gene_frame <- gene_frame%>% 
  filter(Gene != "") %>%
  rename('gene.name' = Gene, 'group' = Category, 'function' = Function) %>%
  mutate(gene.name = (trimws(gene.name, which = c("both", "left", "right"), whitespace = "[ \t\r\n]"))) %>%
  filter(gene.name %in% bigDataGene$gene_short_name)

##### Functions #####


gene_frame$gene.index = unlist(sapply(gene_frame$gene.name, function(x){return(which(bigDataGene$gene_short_name == x))}))


generate_tables <- function(x, table) {
  temp_table <- table
  temp_table$gene <- x
  temp_table$umi_col <- mm[which(gene_frame$gene.name == x),] 
  temp_table$group <- gene_frame$group[which(gene_frame$gene.name == x)]
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
    }else{
      if (grepl('Z', substr(1,1))) {
        return('P4')
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




##### Step 2: Collect UMI, TPM Data #####
toc()
tic("Step 2")

mm <- bigmm[gene_frame$gene.index,]






main_table <- bigDataCell %>%
  mutate(index=1:nrow(bigDataCell))

#main_table$clade <- lapply(main_table$lineage, clade_func)
#main_table$clade <- sapply(main_table$clade, toString)
main_table$generation_num <- lapply(main_table$lineage, generation_number_func)
main_table$generation_num <- sapply(main_table$generation_num, toString)
main_table$generation_num <- sapply(main_table$generation_num, as.integer)


main_table <- bind_rows(lapply(gene_frame$gene.name, generate_tables, main_table))

main_table <- main_table %>% 
  filter(passed_initial_QC_or_later_whitelisted == TRUE) %>%
  select( -X, -cell, -time.point, -batch, -raw.embryo.time, -raw.embryo.time.bin, d.name = plot.cell.type, d.lineage = lineage)

main_table$time.mpf <- unlist(lapply(main_table$time.mpfc, adj_time_func))
main_table$tpm <- mapply(calc_tpm_func, main_table$umi, main_table$n.umi)

##### Step 3: #####
toc()
tic("Step 3")

##### Generate figures #####

lins_only <- main_table %>%
  filter(!is.na(d.lineage))


gast_cells_joined <- gast_cells %>% 
  left_join( founder_key, by = c("cell" = "cell"))
gast_cells_joined <- gast_cells_joined %>% filter(!is.na(annotation_name))
gast_cells_joined$gastrulation = 'Internalizes during gastrulation'
# 
lins <- gast_cells_joined %>%
  left_join(lins_only, by = c('annotation_name' = 'd.lineage'))

lins <- gast_cells_joined %>%
  full_join(lins_only, by = c('annotation_name' = 'd.lineage'))
lins <- lins %>% select(cell, clade, d.name, annotation_name, gastrulation, group, embryo.time, index, generation_num, gene, tpm, cell.type)
lins$gastrulation <- lins$gastrulation %>% replace_na('Does not internalize')
gg_color_hue <- function(n) {
  hues = seq(15, 375, length=n+1)
  hcl(h=hues, l=65, c=100)[1:n]
}



##### Figures #####

##### 9/1/22 #####


rps_plot <- lins %>%
  filter(gene == 'rps-23') %>%
  filter(embryo.time < 400) %>%
  filter((embryo.time > 100)) %>%
  group_by(gastrulation, gene, embryo.time) %>%
  summarize(mean_tpm = mean(tpm), std_dev = sd(tpm)) %>%
  mutate(mean_tpm, mean_tpm_adj = sapply(mean_tpm, function(x) { if (x <= 1) {return(1)} else{return(x)}})) %>%
  
  
  ggplot(mapping = aes(x = embryo.time, y = mean_tpm_adj, color = gene)) +
  ggtitle('All cells with internalizing cells in black') +
  xlab('Time (minutes post first cleavage)') + 
  ylab('Mean TPM (log10)') +
  geom_point(mapping = aes(x = embryo.time, y = mean_tpm_adj)) +
  scale_y_continuous(trans='log10') + 
  geom_smooth(method = 'loess', se=F)  
  #scale_colour_manual(values=values)

  
  rps_black_pts <- lins %>%  
  filter(gastrulation == 'Internalizes during gastrulation') %>%
  filter(embryo.time < 400) %>%
  filter((embryo.time > 100)) %>%
  filter(gene == 'rps-23') %>%
  group_by(gastrulation, gene, embryo.time) %>%
  summarize(mean_tpm = mean(tpm), std_dev = sd(tpm)) %>%
  mutate(mean_tpm, mean_tpm_adj = sapply(mean_tpm, function(x) { if (x <= 1) {return(1)} else{return(x)}})) %>%
  geom_point(color = 'black', mapping = aes(x = embryo.time, y = mean_tpm_adj))
plot <- rps_plot + rps_black_pts



plots <- c()
cat_groups <- unique(gast_genes$Category)
cat_groups <- cat_groups[cat_groups != '']

# Clarification- Is the "does not internalize group" all cells minus the 66
# identified as internalizing? If that's the case, I think we should also look
# at all cells including the 66. There, plotting all cells with the gastrulating
# cells overlaid as black points (no connecting line) could help us better
# understand global vs. local trends.   
for (i in 1:length(cat_groups)) {
  
  unfilt_genes <- unique(lins[which(lins$group == cat_groups[i]), 'gene'])
  
  adj_names = sort(setdiff(unfilt_genes[unfilt_genes %!in% excl_genes], "rps-23"))
  values = gg_color_hue(length(adj_names))
  names(values) = adj_names
  values = c(values, c('rps-23'="black"))
  
  
  #All cells 100-400
  all_pts <- lins %>%  
    filter(group == cat_groups[i] | gene == 'rps-23') %>%
    filter(gene %in% names(values)) %>%
    # filter(gastrulation == 'Does not internalize') %>%
    filter(embryo.time < 400) %>%
    filter((embryo.time > 100)) %>%
    filter(gene %!in% c('rps-2', 'rps-4', 'act-1', 'act-2', 'act-3', 'act-4')) %>%
    #filter(gene %!in% excl_genes) %>%
    # group_by(gene, clade, embryo.time ) %>%
    group_by(gastrulation, gene, embryo.time) %>%
    summarize(mean_tpm = mean(tpm), std_dev = sd(tpm)) %>%
    mutate(mean_tpm, mean_tpm_adj = sapply(mean_tpm, function(x) { if (x <= 1) {return(1)} else{return(x)}})) %>%
    ggplot(mapping = aes(x = embryo.time, y = mean_tpm_adj, color = gene)) +
    ggtitle(glue("{cat_groups[i]} genes in gastrulating cells")) +
    #xlab('Time (minutes post first cleavage)') + 
    xlab('Generation number (G1 == P0)') + 
    ylab('Mean TPM (log10)') +
    geom_point(mapping = aes(x = embryo.time, y = mean_tpm_adj)) +
    scale_y_continuous(trans='log10') + 
    scale_colour_manual(values=values)+
    # geom_line(mapping = aes(x = generation_num, y = mean_tpm_adj))
    geom_smooth(method = 'loess', se=F)
  #Internalizing cells 100-400
  pts <- lins %>%  
    filter(gastrulation == 'Internalizes during gastrulation') %>%
    filter(group == cat_groups[i] | gene == 'rps-23') %>%
    filter(gene %in% names(values)) %>%
    # filter(gastrulation == 'Does not internalize') %>%
    filter(embryo.time < 400) %>%
    filter((embryo.time > 100)) %>%
    #filter(gene %!in% excl_genes) %>%
    # group_by(gene, clade, embryo.time ) %>%
    group_by(gastrulation, gene, embryo.time) %>%
    summarize(mean_tpm = mean(tpm), std_dev = sd(tpm)) %>%
    mutate(mean_tpm, mean_tpm_adj = sapply(mean_tpm, function(x) { if (x <= 1) {return(1)} else{return(x)}})) %>%
    geom_point(color = 'black', mapping = aes(x = embryo.time, y = mean_tpm_adj))
  
  
  ew <- all_pts+pts
  ew
  plots[[i]] <- ew
}
ggsave(
  filename = "005 _ filtered genes _ Internalizing cells vs not _ 100-400 _ intern on not _ all genes _ no err.pdf", 
  plot = marrangeGrob(plots, nrow=1, ncol = 1), 
  width = 10, height = 7, units = "in"
  #width = 1000, height = 600, units = "px"
)
##### 8/31/22 #####
excl_genes <- c( "rps-2", "rps-4",'rps-23', "act-1", "act-2", "act-3", "act-4", "end-1", "end-3",
                 "med-1", "med-2", "pes-10", "taf-11", "pie-1", "toca-2", "nuo-3a", "vab-9",
                 "slt-1", "rac-2", "bar-1", "sdz-23", "lin-44", "act-4", "mes-1", "tbx-35", 
                 "cka-2", "php-3", "elt-3","itr-1")

excl_genes_rps_23 <- c( "rps-2", "rps-4", "act-1", "act-2", "act-3", "act-4", "end-1", "end-3",
                        "med-1", "med-2", "pes-10", "taf-11", "pie-1", "toca-2", "nuo-3a", "vab-9",
                        "slt-1", "rac-2", "bar-1", "sdz-23", "lin-44", "act-4", "mes-1", "tbx-35", 
                        "cka-2", "php-3", "elt-3","itr-1")


incl_genes <- unique(lins$gene)[unique(lins$gene) %!in% excl_genes_rps_23]



adj_names = sort(setdiff(unique(lins$gene)[unique(lins$gene) %!in% excl_genes], "rps-23"))
values = gg_color_hue(length(adj_names))
names(values) = adj_names
values = c(values, c('rps-23'="black"))



cat_groups <- unique(gast_genes$Category)
cat_groups <- cat_groups[cat_groups != '']


plot <- lins %>%
  filter(gene %in% names(values)) %>%
  filter(embryo.time < 400) %>%
  filter((embryo.time > 100)) %>%
  group_by(gastrulation, gene, generation_num) %>%
  summarize(mean_tpm = mean(tpm), std_dev = sd(tpm)) %>%
  mutate(mean_tpm, mean_tpm_adj = sapply(mean_tpm, function(x) { if (x <= 1) {return(1)} else{return(x)}})) %>%
  
  
  ggplot(mapping = aes(x = generation_num, y = mean_tpm_adj, color = gene)) +
  ggtitle('All cells with internalizing cells in black') +
  xlab('Generation number (G1 == P0)') + 
  ylab('Mean TPM (log10)') +
  geom_point(mapping = aes(x = generation_num, y = mean_tpm_adj)) +
  scale_y_continuous(trans='log10') + 
  geom_smooth(method = 'loess', se=F) + 
  scale_colour_manual(values=values)

black_pts <- lins %>%  
  filter(gastrulation == 'Internalizes during gastrulation') %>%
  filter(embryo.time < 400) %>%
  filter((embryo.time > 100)) %>%
  filter(gene %in% adj_names) %>%
  group_by(gastrulation, gene, generation_num) %>%
  summarize(mean_tpm = mean(tpm), std_dev = sd(tpm)) %>%
  mutate(mean_tpm, mean_tpm_adj = sapply(mean_tpm, function(x) { if (x <= 1) {return(1)} else{return(x)}})) %>%
  geom_point(color = 'black', mapping = aes(x = generation_num, y = mean_tpm_adj))

plot <- plot + black_pts
  
  plots[[1]] <- plot
##### 8/30/22 #####
plots <- c()
cat_groups <- unique(gast_genes$Category)
cat_groups <- cat_groups[cat_groups != '']

# Clarification- Is the "does not internalize group" all cells minus the 66
# identified as internalizing? If that's the case, I think we should also look
# at all cells including the 66. There, plotting all cells with the gastrulating
# cells overlaid as black points (no connecting line) could help us better
# understand global vs. local trends.   
for (i in 1:length(cat_groups)) {
  

  #All cells 100-400
  all_pts <- lins %>%  
    filter(group == cat_groups[i] | gene == 'rps-23') %>%
    # filter(gastrulation == 'Does not internalize') %>%
    filter(embryo.time < 400) %>%
    filter((embryo.time > 100)) %>%
    filter(gene %!in% c('rps-2', 'rps-4', 'act-1', 'act-2', 'act-3', 'act-4')) %>%
    #filter(gene %!in% excl_genes) %>%
    # group_by(gene, clade, embryo.time ) %>%
    group_by(gastrulation, gene, embryo.time) %>%
    summarize(mean_tpm = mean(tpm), std_dev = sd(tpm)) %>%
    mutate(mean_tpm, mean_tpm_adj = sapply(mean_tpm, function(x) { if (x <= 1) {return(1)} else{return(x)}})) %>%
    ggplot(mapping = aes(x = embryo.time, y = mean_tpm_adj, color = gene)) +
    ggtitle('All cells with internalizing cells in black') +
    xlab('Time (minutes post first cleavage)') + 
    ylab('Mean TPM (log10)') +
    geom_point(mapping = aes(x = embryo.time, y = mean_tpm_adj)) +
    scale_y_continuous(trans='log10') + 
    geom_smooth(method = 'loess', se=F)
      #Internalizing cells 100-400
  pts <- lins %>%  
    filter(group == cat_groups[i] | gene == 'rps-23') %>%
    filter(gastrulation == 'Internalizes during gastrulation') %>%
    filter(embryo.time < 400) %>%
    filter((embryo.time > 100)) %>%
    filter(gene %!in% excl_genes_rps_23) %>%
    #filter(gene %!in% excl_genes) %>%
    # group_by(gene, clade, embryo.time ) %>%
    group_by(gastrulation, gene, embryo.time) %>%
    summarize(mean_tpm = mean(tpm), std_dev = sd(tpm)) %>%
    mutate(mean_tpm, mean_tpm_adj = sapply(mean_tpm, function(x) { if (x <= 1) {return(1)} else{return(x)}})) %>%
    geom_point(color = 'black', mapping = aes(x = embryo.time, y = mean_tpm_adj))

  
  ew <- all_pts+pts
  
  plots[[i]] <- ew
}
ggsave(
  filename = "001 _ filtered genes _ Internalizing cells vs not _ 100-400 _ intern on not _ no err.pdf", 
  plot = marrangeGrob(plots, nrow=1, ncol = 1), 
  width = 10, height = 7, units = "in"
  #width = 1000, height = 600, units = "px"
)
bigDataCell %>% 
  filter(embryo.time > 100) %>%
  filter(embryo.time < 400) %>%
  ggplot(mapping = aes(x = embryo.time)) + 
  #geom_density(color = 'black', alpha = 0.75) +
  geom_histogram(bins = 50, color = 'white') + 
  ggtitle('Distribution of all Cell Data; t = 0-400')
  #xlab("Time (minutes post-fertilization)") + 
  #ylab("Density") + 
  #ggtitle("Distribution of cell information") + 
  #labs(fill = "Cell Identification") 
##### 8/30/22 #####
plots <- c()
cat_groups <- unique(gast_genes$Category)
cat_groups <- cat_groups[cat_groups != '']
for (i in 1:length(cat_groups)) { 
  new_lins <- lins %>% filter(gene %!in% c('act-1', 'act-2', 'act-3', 'act-4', 'rps-2', 'rps-4', 'rps-23')) %>% filter(group == cat_groups[i])
  adj_names = sort(setdiff(unique(new_lins$gene), "rps-23"))
  values = gg_color_hue(length(adj_names))
  names(values) = adj_names
  values = c(values, c('rps-23'="black"))
  plot <- lins %>%  
    # filter(group == cat_groups[i] | gene == 'rps-23') %>%
    filter(embryo.time < 400) %>%
    filter((embryo.time > 100)) %>%
    filter(gene %!in% c('rps-2', 'rps-4', 'act-1', 'act-2', 'act-3', 'act-4')) %>%
    #filter(gene %!in% excl_genes) %>%
    # group_by(gene, clade, embryo.time ) %>%
    group_by(gastrulation, gene, embryo.time) %>%
    summarize(mean_tpm = mean(tpm), std_dev = sd(tpm)) %>%
    mutate(mean_tpm, mean_tpm_adj = sapply(mean_tpm, function(x) { if (x <= 1) {return(1)} else{return(x)}})) %>%
    ggplot(mapping = aes(x = embryo.time, y = mean_tpm_adj, color = gene)) +
    ggtitle(glue('Cell expression of {(trimws(cat_groups[i], which = c("both", "left", "right"), whitespace = "[ \t\r\n]"))} during Gastrulation')) +
    
    xlab('Time (minutes post first cleavage)') +
    ylab('Mean TPM (log10)') +
    geom_jitter(alpha=0.5) +
    scale_y_continuous(trans='log10') +
    # geom_line() +
    geom_smooth(method = 'loess', se=F) + 
    scale_colour_manual(values=values) +
    facet_wrap(~gastrulation)
  plots[[i]] <- plot

  }


ggsave(
  filename = "no actin _ Internalizing cells vs not _ 100-400 _ compare genes in groups _ no err.pdf", 
  plot = marrangeGrob(plots, nrow=1, ncol = 1), 
  width = 10, height = 7, units = "in"
  #width = 1000, height = 600, units = "px"
)
some_df <- lins %>%  
  # filter(group == cat_groups[i] | gene == 'rps-23') %>%
  filter(embryo.time < 400) %>%
  filter((embryo.time > 100)) %>%
  filter(gene %!in% c('rps-2', 'rps-4', 'act-1', 'act-2', 'act-3', 'act-4')) %>%
  #filter(gene %!in% excl_genes) %>%
  # group_by(gene, clade, embryo.time ) %>%
  group_by(gastrulation, group, gene, embryo.time) %>%
  summarize(mean_tpm = mean(tpm), std_dev = sd(tpm))
write.csv(some_df,"gastrulation_gene_exp_by_time_point.csv", row.names = FALSE)


new_lins <- lins %>% filter(group != 'Housekeeping genes')
adj_names = sort(setdiff(unique(new_lins$group), "Housekeeping genes"))
values = gg_color_hue(length(adj_names))
names(values) = adj_names
values = c(values, c('Housekeeping genes'="black"))


plots <- c()


plot <- lins %>%  
  # filter(gastrulation == 'Internalizes during gastrulation') %>%
  filter(embryo.time < 400) %>%
  filter((embryo.time > 100)) %>%
  filter(gene != 'act-4') %>%
  #filter(gene %!in% excl_genes) %>%
  # group_by(gene, clade, embryo.time ) %>%
  group_by(gastrulation, group, embryo.time) %>%
  summarize(mean_tpm = mean(tpm), std_dev = sd(tpm)) %>%
  #filter()
  mutate(mean_tpm, mean_tpm_adj = sapply(mean_tpm, function(x) { if (x <= 1) {return(1)} else{return(x)}})) %>%
  # ggplot(mapping = aes(x = embryo.time, y = mean_tpm, color = group))+
  
  ggplot(mapping = aes(x = embryo.time, y = mean_tpm_adj, color = group)) +
  ggtitle(glue('Cell expression of gene groups during Gastrulation')) +
  
  xlab('Time (minutes post first cleavage)') +
  ylab('Mean TPM (log10)') +
  # ylab('Mean TPM') + 
  geom_jitter(alpha=0.5) +
  scale_y_continuous(trans='log10') +
  # geom_point() +
  geom_line() +
  # geom_smooth(method = 'loess', se=F) +
  # geom_errorbar(aes(ymin = mean_tpm - std_dev, ymax= mean_tpm + std_dev)) +
  # geom_errorbar(aes(ymin = mean_tpm_adj - std_dev, ymax= mean_tpm_adj + std_dev)) +
  
  scale_colour_manual(values=values) +
  # theme(legend.position="none") +
  # facet_wrap(~clade)
  facet_wrap(~gastrulation)

plots[[1]] <- plot

plot <- lins %>%  
  # filter(gastrulation == 'Internalizes during gastrulation') %>%
  filter(gene != 'act-4') %>%
  
  filter(embryo.time < 400) %>%
  filter((embryo.time > 100)) %>%
  #filter(gene %!in% excl_genes) %>%
  # group_by(gene, clade, embryo.time ) %>%
  group_by(gastrulation, group, embryo.time) %>%
  summarize(mean_tpm = mean(tpm), std_dev = sd(tpm)) %>%
  #filter()
  mutate(mean_tpm, mean_tpm_adj = sapply(mean_tpm, function(x) { if (x <= 1) {return(1)} else{return(x)}})) %>%
  # ggplot(mapping = aes(x = embryo.time, y = mean_tpm, color = gene))+
  
  ggplot(mapping = aes(x = embryo.time, y = mean_tpm_adj, color = group)) +
  ggtitle(glue('Cell expression of gene groups during Gastrulation')) +
  
  xlab('Time (minutes post first cleavage)') +
  ylab('Mean TPM (log10)') +
  # ylab('Mean TPM')
  geom_jitter(alpha=0.5) +
  scale_y_continuous(trans='log10') +
  # geom_point() +
  # geom_line() +
  geom_smooth(method = 'loess', se=F) +
  # geom_errorbar(aes(ymin = mean_tpm_adj - std_dev, ymax= mean_tpm_adj + std_dev)) +
  scale_colour_manual(values=values) +
  # theme(legend.position="none") +
  # facet_wrap(~clade)
  facet_wrap(~gastrulation)

plots[[2]] <- plot

ggsave(
  filename = "no_act-4 _ Internalizing cells vs not _ 100-400 _ compare groups _ no err.pdf", 
  plot = marrangeGrob(plots, nrow=1, ncol = 1), 
  width = 10, height = 7, units = "in"
  #width = 1000, height = 600, units = "px"
)
##### 8/29/22 #####


effect_genes <- new_lins %>%
  filter(group == 'Gastrulation genes') %>%
  filter(gastrulation == 'Internalizes during gastrulation') %>%
  filter(embryo.time < 400) %>%
  filter((embryo.time > 100)) %>%
  # group_by(gene, clade, embryo.time ) %>%
  group_by(gene, embryo.time) %>%
  summarize(mean_tpm = mean(tpm), std_dev = sd(tpm)) %>%
  #filter()
  mutate(mean_tpm, mean_tpm_adj = sapply(mean_tpm, function(x) { if (x <= 1) {return(1)} else{return(x)}})) %>%
  filter(median(mean_tpm) > 0) %>%
  ungroup() %>%
  select(gene)
effect_genes <- unique(unlist(effect_genes$gene))
excl_genes <- gast_genes[gast_genes%!in%effect_genes]

#adj_names = sort(setdiff(unique(effect_genes), "rps-23"))
adj_names = sort(setdiff(unique(new_lins$gene), "rps-23"))
values = gg_color_hue(length(adj_names))
names(values) = adj_names
values = c(values, c('rps-23'="black"))

#Time
plots <- c()

plot <- new_lins %>%  
  # filter(gastrulation == 'Internalizes during gastrulation') %>%
  filter(embryo.time < 400) %>%
  filter((embryo.time > 100)) %>%
  filter(gene %!in% excl_genes) %>%
  # group_by(gene, clade, embryo.time ) %>%
  group_by(gastrulation, gene, embryo.time) %>%
  summarize(mean_tpm = mean(tpm), std_dev = sd(tpm)) %>%
  #filter()
  mutate(mean_tpm, mean_tpm_adj = sapply(mean_tpm, function(x) { if (x <= 1) {return(1)} else{return(x)}})) %>%

  # ggplot(mapping = aes(x = embryo.time, y = mean_tpm, color = gene))+
  ggplot(mapping = aes(x = embryo.time, y = mean_tpm_adj, color = gene)) +
  # ggtitle(glue('Cell expression of 80 genes during Gastrulation')) +
  ggtitle(glue('Cell expression of 96 genes during Gastrulation')) +
  
  xlab('Time (minutes post first cleavage)') +
  ylab('Mean TPM (log10)') +
  # ylab('Mean TPM')
  geom_jitter(alpha=0.5) +
  scale_y_continuous(trans='log10') +
  # geom_point() +
  # geom_line() +
  geom_smooth(method = 'loess', se=F) +
  geom_errorbar(aes(ymin = mean_tpm - std_dev, ymax= mean_tpm + std_dev), width=0.05, position=position_dodge(0.05)) +
  scale_colour_manual(values=values) +
  # theme(legend.position="none") +
  # facet_wrap(~clade)
  facet_wrap(~gastrulation)
plots[[1]] <- plot
#Generation
plot <- new_lins %>%  
  # filter(gastrulation == 'Internalizes during gastrulation') %>%
  filter(embryo.time < 400) %>%
  filter((embryo.time > 100)) %>%
  filter(gene %!in% excl_genes) %>%
  # group_by(gene, clade, embryo.time ) %>%
  group_by(gastrulation, gene, generation_num) %>%
  summarize(mean_tpm = mean(tpm), std_dev = sd(tpm)) %>%
  #filter()
  mutate(mean_tpm, mean_tpm_adj = sapply(mean_tpm, function(x) { if (x <= 1) {return(1)} else{return(x)}})) %>%
  
  # ggplot(mapping = aes(x = embryo.time, y = mean_tpm, color = gene))+
  ggplot(mapping = aes(x = generation_num, y = mean_tpm_adj, color = gene)) +
  # ggtitle(glue('Cell expression of 80 genes during Gastrulation')) +
  ggtitle(glue('Cell expression of 96 genes during Gastrulation')) +
  
  xlab('Generation number (P0 == G1)') +
  ylab('Mean TPM (log10)') +
  # ylab('Mean TPM')
  geom_jitter(alpha=0.5) +
  scale_y_continuous(trans='log10') +
  # geom_point() +
  # geom_line() +
  geom_smooth(method = 'loess', se=F) +
  geom_errorbar(aes(ymin = mean_tpm - std_dev, ymax= mean_tpm + std_dev), width=0.05, position=position_dodge(0.05)) +
  scale_colour_manual(values=values) +
  # theme(legend.position="none") +
  # facet_wrap(~clade)
  facet_wrap(~gastrulation)
plots[[2]] <- plot

plot <- new_lins %>%  
  # filter(gastrulation == 'Internalizes during gastrulation') %>%
  filter(embryo.time < 400) %>%
  filter((embryo.time > 100)) %>%
  filter(gene %!in% excl_genes) %>%
  # group_by(gene, clade, embryo.time ) %>%
  group_by(gastrulation, gene, embryo.time) %>%
  summarize(mean_tpm = mean(tpm), std_dev = sd(tpm)) %>%
  #filter()
  # mutate(mean_tpm, mean_tpm_adj = sapply(mean_tpm, function(x) { if (x <= 1) {return(1)} else{return(x)}})) %>%
  
  ggplot(mapping = aes(x = embryo.time, y = mean_tpm, color = gene))+
  # ggplot(mapping = aes(x = embryo.time, y = mean_tpm_adj, color = gene)) +
  # ggtitle(glue('Cell expression of 80 genes during Gastrulation')) +
  ggtitle(glue('Cell expression of 96 genes during Gastrulation')) +
  
  xlab('Time (minutes post first cleavage)') +
  # ylab('Mean TPM (log10)') +
  ylab('Mean TPM') +
  geom_jitter(alpha=0.5) +
  # scale_y_continuous(trans='log10') +
  # geom_point() +
  geom_line() +
  # geom_smooth(method = 'loess', se=F) +
  geom_errorbar(aes(ymin = mean_tpm - std_dev, ymax= mean_tpm + std_dev), width=0.05, position=position_dodge(0.05)) +
  scale_colour_manual(values=values) +
  # theme(legend.position="none") +
  # facet_wrap(~clade)
  facet_wrap(~gastrulation)
plots[[3]] <- plot
#Generation
plot <- new_lins %>%  
  # filter(gastrulation == 'Internalizes during gastrulation') %>%
  filter(embryo.time < 400) %>%
  filter((embryo.time > 100)) %>%
  filter(gene %!in% excl_genes) %>%
  # group_by(gene, clade, embryo.time ) %>%
  group_by(gastrulation, gene, generation_num) %>%
  summarize(mean_tpm = mean(tpm), std_dev = sd(tpm)) %>%
  #filter()
  # mutate(mean_tpm, mean_tpm_adj = sapply(mean_tpm, function(x) { if (x <= 1) {return(1)} else{return(x)}})) %>%
  
  ggplot(mapping = aes(x = generation_num, y = mean_tpm, color = gene))+
  # ggplot(mapping = aes(x = generation_num, y = mean_tpm_adj, color = gene)) +
  # ggtitle(glue('Cell expression of 80 genes during Gastrulation')) +
  ggtitle(glue('Cell expression of 96 genes during Gastrulation')) +
  
  xlab('Generation number (P0 == G1)') +
  # ylab('Mean TPM (log10)') +
  ylab('Mean TPM') +
  geom_jitter(alpha=0.5) +
  # scale_y_continuous(trans='log10') +
  # geom_point() +
  geom_line() +
  # geom_smooth(method = 'loess', se=F) +
  geom_errorbar(aes(ymin = mean_tpm - std_dev, ymax= mean_tpm + std_dev), width=0.05, position=position_dodge(0.05)) +
  scale_colour_manual(values=values) +
  # theme(legend.position="none") +
  # facet_wrap(~clade)
  facet_wrap(~gastrulation)
plots[[4]] <- plot




ggsave(
  filename = "Filtered genes _ Internalizing cells vs not _ 100-400 _ rps-23 _ no actin.pdf", 
  plot = marrangeGrob(plots, nrow=1, ncol = 1), 
  width = 10, height = 7, units = "in"
  #width = 1000, height = 600, units = "px"
)

##### 8/25/22 Redo - internalizing cells only, line plots, 101 genes, rps-23 as black #####

adj_names = sort(setdiff(unique(dat$col_group), "Paid"))
values = gg_color_hue(length(adj_names))
names(values) = adj_names
values = c(values, c(Paid="black"))

adj_names = sort(setdiff(unique(lins$gene), "rps-23"))
values = gg_color_hue(length(adj_names))
names(values) = adj_names
values = c(values, c('rps-23'="black"))


lins %>%  
  filter(gastrulation == 'Internalizes during gastrulation') %>%
  filter(embryo.time < 400) %>%
  filter((embryo.time > 100)) %>%
  filter(gene %!in% c('rps-2', 'rps-4', 'act-4')) %>%
  group_by(gene, clade, embryo.time ) %>%
  summarize(mean_tpm = mean(tpm), std_dev = sd(tpm)) %>%
  # mutate(mean_tpm, mean_tpm_adj = sapply(mean_tpm, function(x) { if (x <= 1) {return(1)} else{return(x)}})) %>%
  
  ggplot(mapping = aes(x = embryo.time, y = mean_tpm, color = gene))+
  # scale_color_manual(values = c("rps-23" = "black")) +
  # scale_y_continuous(breaks = round(seq(0, max(output$TPM), by = 2500),1)) + 
  geom_jitter(alpha=0.1)+ 
  # scale_y_continuous(trans='log10') +
  geom_point() + 
  geom_line() + 
  # geom_smooth(method = 'loess', se=F) + 
  geom_errorbar(aes(ymin = mean_tpm - std_dev, ymax= mean_tpm + std_dev), width=0.05, position=position_dodge(0.05)) +
  scale_colour_manual(values=values) +
  ggtitle(glue('101 genes in internalizing cells during Gastrulation')) +
  xlab('Time (minutes post first cleavage)') +
  ylab('Mean TPM') +
  # theme(legend.position="none") + 
  #geom_line(data = rps, mapping = aes(x = embryo.time, y = mean_tpm, color = 'black')) +
  facet_wrap(~clade)

lins %>%  
  filter(gastrulation == 'Internalizes during gastrulation') %>%
  filter(embryo.time < 400) %>%
  filter((embryo.time > 100)) %>%
  filter(gene %!in% c('rps-2', 'rps-4', 'act-4')) %>%
  group_by(gene, clade, embryo.time ) %>%
  summarize(mean_tpm = mean(tpm), std_dev = sd(tpm)) %>%
  mutate(mean_tpm, mean_tpm_adj = sapply(mean_tpm, function(x) { if (x <= 1) {return(1)} else{return(x)}})) %>%
  
  ggplot(mapping = aes(x = embryo.time, y = mean_tpm_adj, color = gene))+
 
  geom_jitter(alpha=0.1)+ 
  scale_y_continuous(trans='log10') +
  geom_point() + 
  # geom_line() + 
  geom_smooth(method = 'loess', se=F) + 
  geom_errorbar(aes(ymin = mean_tpm_adj - std_dev, ymax= mean_tpm_adj + std_dev), width=0.05, position=position_dodge(0.05)) +
  scale_colour_manual(values=values) +
  ggtitle(glue('101 genes in internalizing cells during Gastrulation')) +
  xlab('Time (minutes post first cleavage)') +
  ylab('Adj. Mean TPM (Log10)') +

  facet_wrap(~clade)
##### 8/26/22 #####
threshold_median_eq_0 <- lins %>% 
  filter(gastrulation == 'Internalizes during gastrulation') %>%
  filter(group == 'Gastrulation genes') %>%
  group_by(gene, embryo.time) %>%
  summarize(mean_tpm = mean(tpm)) %>%
  filter(median(mean_tpm) > 0) %>%
  summarize(median = median(mean_tpm))

lins %>% 
  filter(gastrulation == 'Internalizes during gastrulation') %>%
  filter(group == 'Housekeeping genes') %>%
  group_by(gene, embryo.time) %>%
  summarize(mean_tpm = mean(tpm)) %>%
  filter(median(mean_tpm) > 0) %>%
  summarize(median = median(mean_tpm))

lins %>% 
  filter(embryo.time < 400) %>%
  filter(embryo.time > 100) %>%
  #filter(group == 'Gastrulation genes') %>%
  group_by(gene, embryo.time) %>%
  summarize(mean_tpm = mean(tpm), std_dev = sd(tpm)) %>%
  filter(median(mean_tpm) > 0) %>%
  mutate(mean_tpm, mean_tpm_adj = sapply(mean_tpm, function(x) { if (x <= 1) {return(1)} else{return(x)}})) %>%
  #summarize(median = median(mean_tpm))
  ggplot(mapping = aes(x = embryo.time, y = mean_tpm_adj, color = gene)) +
  geom_smooth(method = 'loess', se=F) + 
  scale_y_continuous(trans='log10') +
  #geom_errorbar(aes(ymin = mean_tpm_adj - std_dev, ymax= mean_tpm_adj + std_dev), width=0.05, position=position_dodge(0.05)) +
  # ggtitle(glue('{gene_frame$gene.name[i]} expression in internalizing cells during Gastrulation')) + 
  #xlab('Generation Number (P0 == G1)') + 
  ylab('Mean TPM')
  












# Generation number

lins %>%
  filter(embryo.time < 400) %>%
  filter(!is.na(tpm)) %>%
  filter(group == 'Gastrulation genes') %>%
  group_by(gene, clade, generation_num ) %>%
  summarize(mean_tpm = mean(tpm), std_dev = sd(tpm)) %>%
  
  ggplot(mapping = aes(x = generation_num, y = mean_tpm, color = gene)) + 
  # geom_line() + 
  geom_smooth(method = 'loess') + 
  geom_errorbar(aes(ymin = mean_tpm - std_dev, ymax= mean_tpm + std_dev), width=0.05, position=position_dodge(0.05)) +
  # ggtitle(glue('{gene_frame$gene.name[i]} expression in internalizing cells during Gastrulation')) + 
  xlab('Generation Number (P0 == G1)') + 
  ylab('Mean TPM')

# Embryo time

lins %>%
  filter(embryo.time < 400) %>%
  filter(!is.na(tpm)) %>%
  filter(group == 'Gastrulation genes') %>%
  group_by(group, gene, annotation_name, embryo.time ) %>%
  summarize(mean_tpm = mean(tpm), std_dev = sd(tpm)) %>%
  
  ggplot(mapping = aes(x = embryo.time, y = mean_tpm, color = gene)) + 
  # geom_line() + 
  geom_smooth(method = 'loess') + 
  geom_errorbar(aes(ymin = mean_tpm - std_dev, ymax= mean_tpm + std_dev), width=0.05, position=position_dodge(0.05)) +
  # ggtitle(glue('{gene_frame$gene.name[i]} expression in internalizing cells during Gastrulation')) + 
  xlab('Generation Number (P0 == G1)') + 
  ylab('Mean TPM') + 
  facet_wrap(~group)


ggsave(
  filename = "Housekeeping genes in internalizing cells.pdf", 
  plot = marrangeGrob(plots, nrow=1, ncol = 1), 
  width = 10, height = 7, units = "in"
  #width = 1000, height = 600, units = "px"
)

##### Figures of figures past #####






##### 8/25/22 #####
# 
# plots <- c()
# plot <- lins %>% 
#   filter(group == 'Housekeeping genes') %>%
#   filter(gene %!in% c('rps-16', 'rps-2', 'rpl-27', 'rpl-24.1', 'rpl-15', 'rps-17', 'rps-4', 'rps-26', 'rpl-33', 'rpl-36')) %>%
#   #filter(gene %in% c('rpl-15', 'rps-23')) %>%
#   group_by(gene, embryo.time ) %>%
#   summarize(mean_tpm = mean(tpm), std_dev = sd(tpm)) %>%
#   filter(embryo.time < 400) %>%
#   filter(embryo.time > 100) %>%
#   mutate(mean_tpm, mean_tpm_adj = sapply(mean_tpm, function(x) { if (x <= 1) {return(1)} else{return(x)}})) %>%
#   
#   ggplot(mapping = aes(x = embryo.time, y = mean_tpm, color = gene))+# + 
#   #scale_y_continuous(breaks = round(seq(0, max(output$TPM), by = 2500),1)) + 
#   geom_jitter(alpha=0.1)+ 
#   #coord_trans(y="log2") +
#   geom_point() + 
#   geom_smooth(method = 'loess', se=F) + 
#   #geom_errorbar(aes(ymin = mean_tpm - std_dev, ymax= mean_tpm + std_dev), width=0.05, position=position_dodge(0.05)) +
#   ggtitle(glue('House keeping genes in internalizing cells during Gastrulation')) + 
#   xlab('Time (minutes post first cleavage)') + 
#   ylab('Mean TPM')
# plots[[4]] <- plot

plot <- lins %>%  
  lins %>%
  filter(gastrulation == 'Internalizes during gastrulation') %>%
  filter(embryo.time < 400) %>%
  filter((embryo.time > 100)) %>%
  filter(gene %!in% c('rps-2', 'rps-4')) %>%
  group_by(gene, clade, embryo.time ) %>%
  summarize(mean_tpm = mean(tpm), std_dev = sd(tpm)) %>%
  mutate(mean_tpm, mean_tpm_adj = sapply(mean_tpm, function(x) { if (x <= 1) {return(1)} else{return(x)}})) %>%
  
  ggplot(mapping = aes(x = embryo.time, y = mean_tpm, color = gene))+
  scale_color_manual(values = c("rps-23" = "black")) +
  #scale_y_continuous(breaks = round(seq(0, max(output$TPM), by = 2500),1)) + 
  geom_jitter(alpha=0.1)+ 
  # scale_y_continuous(trans='log10') +
  geom_point() + 
  geom_line() + 
  #geom_smooth(method = 'loess', se=F) + 
  geom_errorbar(aes(ymin = mean_tpm - std_dev, ymax= mean_tpm + std_dev), width=0.05, position=position_dodge(0.05)) +
  # ggtitle(glue('101 genes in internalizing cells during Gastrulation')) + 
  # xlab('Time (minutes post first cleavage)') + 
  # ylab('Mean TPM') + 
  #theme(legend.position="none") + 
  geom_line(data = rps, mapping = aes(x = embryo.time, y = mean_tpm, color = 'black')) +
  facet_wrap(~clade) +
  


rps <- lins %>%  
  filter(gastrulation == 'Internalizes during gastrulation') %>%
  filter(embryo.time < 400) %>%
  filter((embryo.time > 100)) %>%
  filter(gene == 'rps-23') %>%
  group_by(gene, clade, embryo.time ) %>%
  summarize(mean_tpm = mean(tpm), std_dev = sd(tpm)) %>%
  mutate(mean_tpm, mean_tpm_adj = sapply(mean_tpm, function(x) { if (x <= 1) {return(1)} else{return(x)}}))

##### 8/24/22 #####

main_table %>%
  filter(d.name == 'BWM_posterior') %>%
  filter(gene == 'emb-9') %>%
  group_by(embryo.time) %>%
  summarize(mean_tpm = mean(tpm)) %>%
  ggplot(mapping = aes(x = embryo.time, y = mean_tpm)) + 
  geom_point() + 
  geom_smooth()
plots <- c()

for (i in 1:length(gene_frame$gene.name)) {
  
  
  plot <- lins %>%
    filter(gene == gene_frame$gene.name[i]) %>%
    #filter(embryo.time < 400) %>%
    group_by(clade, annotation_name, generation_num ) %>%
    summarize(mean_tpm = mean(tpm), std_dev = sd(tpm)) %>%
    
    ggplot(mapping = aes(x = generation_num, y = mean_tpm, color = annotation_name))+# + 
    geom_point() + 
    geom_line() + 
    geom_errorbar(aes(ymin = mean_tpm - std_dev, ymax= mean_tpm + std_dev), width=0.05, position=position_dodge(0.05)) +
    ggtitle(glue('{gene_frame$gene.name[i]} expression in internalizing cells during Gastrulation')) + 
    xlab('Generation Number (P0 == G1)') + 
    ylab('Mean TPM') + 
    theme(legend.position="none") + 
    facet_wrap(~clade)
  
  plots[[i]] <- plot
  
}

sessionDir <- "C:/Users/chawmm/Desktop/4D Transcriptome/for sam early embryogenesis"
setwd(sessionDir)
ggsave(
  filename = "Housekeeping genes in internalizing cells.pdf", 
  plot = marrangeGrob(plots, nrow=1, ncol = 1), 
  width = 10, height = 7, units = "in"
  #width = 1000, height = 600, units = "px"
)
##### 8/22/22 #####


i <- 1
plots <- c()
for (i in 1:length(group_list)) {
  title <- glue('Expression of {group_list[[i]]}')
  
  plot <- lins_main%>%
    filter(gene %in% genes[[i]]) %>%
    filter(embryo.time <= 400) %>%
    #filter(tpm > 0) %>%
    group_by(gene, clade, d.lineage, embryo.time) %>%
    summarize(mean_tpm = mean(tpm), std_dev = sd(tpm)) %>%
    
    ggplot(mapping = aes(x = embryo.time, y = mean_tpm, color = gene)) +
    xlab("Time (minutes post first-cleavage)") +
    ggtitle(title) +
    ylab("Transcripts per million (TPM)") +
    geom_errorbar(aes(ymin = mean_tpm - std_dev, ymax= mean_tpm + std_dev), width=5, position=position_dodge(0.05)) +
    geom_point(alpha = 0.6) +
    geom_smooth(method = 'loess') +
    facet_wrap(~clade)
  plots[[i]] <- plot
}

ggsave(
  filename = 'test_plot.pdf', 
  plot = marrangeGrob(plots, nrow=1, ncol = 1), 
  #width = 1000, height = 600, units = "px"
  width = 10, height = 7, units = "in"
)



plots <- c()
for (i in 1:length(group_list)) {
  title <- glue("Mean TPM by Founder Cell: {group_list[i]}")
  
  
  plot <- main_table %>%
    #filter(gene %in% genes[[i]]) %>%
    filter(!is.na(d.lineage)) %>%
    filter(clade %in% c('AB', 'MS', 'C', 'D', 'E')) %>%
    filter(!is.null(generation_num)) %>%
    #filter(embryo.time <= 400) %>%
    group_by(clade, generation_num,) %>%
    summarize(mean_time_mpfc = mean(embryo.time), std_dev = sd(embryo.time, na.rm = TRUE)) %>%
    ggplot(mapping = aes(x = generation_num, y = mean_time_mpfc, color = clade)) + 
    geom_point(alpha = 0.6) + 
    geom_line() + 
    xlab("Generation Number (P0 = G1)") +
    ggtitle('Generation vs time') +
    ylab("Time (Minutes post fertilization)") +
    geom_errorbar(aes(ymin = mean_time_mpfc - std_dev, ymax= mean_time_mpfc + std_dev), width=1, position=position_dodge(0.05))  
  
  
  plots[[i]] <- plot
  
}

ggsave(
  filename = 'TPM vs generation by family with zeroes no sd.pdf', 
  plot = marrangeGrob(plots, nrow=1, ncol = 1), 
  #width = 1000, height = 600, units = "px"
  width = 10, height = 7, units = "in"
)


##### 8/19/22 #####
sessionDir <- "C:/Users/chawmm/Desktop/4D Transcriptome/output/generation_number"
setwd(sessionDir)



i <- 1
plots <- c()
for (i in 1:length(group_list)) {
  title <- glue('Expression of {group_list[[i]]}')
  
  plot <- lins_main%>%
    filter(gene %in% genes[[i]]) %>%
    filter(embryo.time <= 400) %>%
    #filter(tpm > 0) %>%
    group_by(gene, clade, embryo.time) %>%
    summarize(mean_tpm = mean(tpm), std_dev = sd(tpm)) %>%
    
    ggplot(mapping = aes(x = embryo.time, y = mean_tpm, color = gene)) +
    xlab("Time (minutes post first-cleavage)") +
    ggtitle(title) +
    ylab("Transcripts per million (TPM)") +
    geom_errorbar(aes(ymin = mean_tpm - std_dev, ymax= mean_tpm + std_dev), width=5, position=position_dodge(0.05)) +
    geom_point(alpha = 0.6) +
    geom_smooth(method = 'loess') +
    facet_wrap(~clade)
  plots[[i]] <- plot
}

ggsave(
  filename = 'loess TPM vs time by family with zeroes.pdf', 
  plot = marrangeGrob(plots, nrow=1, ncol = 1), 
  #width = 1000, height = 600, units = "px"
  width = 10, height = 7, units = "in"
)


plots <- c()
for (i in 1:length(gene_list)) {
  title <- glue("Mean TPM by Founder Cell: {group_list[i]}")
  
  
  plot <- main_table %>%
    filter(gene %in% gene_list[[i]]) %>%
    filter(!is.na(d.lineage)) %>%
    filter(!is.null(generation_num)) %>%
    filter(clade %in% c('AB', 'MS', 'C', 'D', 'E')) %>%
    filter(embryo.time <= 400) %>%
    group_by(clade, gene, generation_num) %>%
    summarize(mean_tpm = mean(tpm), std_dev = sd(tpm, na.rm = TRUE)) %>%
    ggplot(mapping = aes(x = generation_num, y = mean_tpm, color = gene)) + 
    geom_point(alpha = 0.6) + 
    xlab("Generation Number (P0 = G1)") +
    ggtitle(title) +
    ylab("Transcripts per million (TPM)") +
    #geom_smooth(method = 'loess') +
    #geom_errorbar(aes(ymin = mean_tpm - std_dev, ymax= mean_tpm + std_dev), width=5, position=position_dodge(0.05)) + 
    facet_wrap(~clade)
  
  
  plots[[i]] <- plot
  
}

ggsave(
  filename = 'TPM vs generation by family with zeroes no sd.pdf', 
  plot = marrangeGrob(plots, nrow=1, ncol = 1), 
  #width = 1000, height = 600, units = "px"
  width = 10, height = 7, units = "in"
)



##### REST #####










founder_generation_num <- function(x){ #where x is the lineage/annotation name 
  x <- strsplit(x, '/')
  if (x[[1]][1] %in% "CDEcde") {
    return(x)
  }
}

y <- founder_generation_num(x)




title <- glue("Mean expression of {group_list[4]}")
lins_main%>%
  filter(founder.cell == 'AB') %>%
  filter(gene = 'hmr-1') %>%
  
  #group_by(gene, d.name, time.mpf) %>%
  #summarize(mean_tpm = mean(tpm), std_dev = sd(tpm)) %>%
  
  ggplot(mapping = aes(x = time.mpf, y = tpm, color = gene)) +
  xlab("Time (minutes post fertilization)") +
  #ggtitle(title) +
  ylab("Transcripts per million (TPM)") +
  #geom_errorbar(aes(ymin = mean_tpm - std_dev, ymax= mean_tpm + std_dev), width=5, position=position_dodge(0.05)) +
  geom_point(alpha = 0.6) +
  facet_wrap(~d.name)


# plots <- c()
# for (i in 1:length(group_list)) {
#   title <- glue("Mean TPM by Founder Cell: {desc_list[i]}")
#   
#   plot <- lins_only %>% 
#     filter(gene %in% group_list[[i]]) %>%
#     filter(tpm > 0) %>% 
#     filter(!is.na(founder.cell)) %>%
#     group_by(founder.cell, gene, time.mpfc) %>%
#     summarize(mean_tpm = mean(tpm), std_err = sd(tpm, na.rm = TRUE) / sqrt(n()) ) %>%
#     ggplot(mapping = aes(x = time.mpfc, y = mean_tpm, color = gene)) + 
#     geom_point() + 
#     ggtitle(title) + 
#     geom_errorbar(aes(ymin = mean_tpm - std_err, ymax= mean_tpm + std_err), width=5, position=position_dodge(0.05)) + 
#     facet_wrap(~founder.cell)
#   plots[[i]] <- plot
#   
#   
#   plot <- lins_only %>% 
#     filter(gene %in% group_list[[i]]) %>%
#     filter(tpm > 0) %>% 
#     filter(time.mpfc < 200) %>%
#     filter(!is.na(founder.cell)) %>%
#     group_by(founder.cell, gene, time.mpfc) %>%
#     summarize(mean_tpm = mean(tpm), std_err = sd(tpm, na.rm = TRUE) / sqrt(n()) ) %>%
#     ggplot(mapping = aes(x = time.mpfc, y = mean_tpm, color = gene)) + 
#     geom_point() + 
#     ggtitle(title) + 
#     geom_errorbar(aes(ymin = mean_tpm - std_err, ymax= mean_tpm + std_err), width=5, position=position_dodge(0.05)) + 
#     facet_wrap(~founder.cell)
#   
#   to_200_plots[[i]] <- plot
# }


# sessionDir <- "C:/Users/chawmm/Desktop/4D Transcriptome/output/plots_founder_cell"
# setwd(sessionDir)
# 
# filename <- glue("all-groups_x-time_y-tpm_non-zero.pdf")
# ggsave(
#   filename = filename, 
#   plot = marrangeGrob(plots, nrow=1, ncol = 1), 
#   #width = 1000, height = 600, units = "px"
#   width = 11, height = 8, units = "in"
# )
# 
# filename <- glue("all-groups_x-time_y-tpm_range-0-200.pdf")
# ggsave(
#   filename = filename, 
#   plot = marrangeGrob(to_200_plots, nrow=1, ncol = 1), 
#   #width = 1000, height = 600, units = "px"
#   width = 11, height = 8, units = "in"
# )
# 
# filename <- "data_x-1234_y-5678_params"
# 
# 
# time_distribution_name_lin <- data %>%
#   filter(tpm > 0) %>%
#   filter(time.mpf < 200) %>%
#   filter(founder.cell == 'AB') %>%
#   # filter(founder.cell %in% neworder) %>%
#   ggplot(mapping = aes(x = tpm)) +
#   geom_histogram(bins=50, color = 'black') +
#   ggtitle("Number of cells expressing cadherin superfamily genes (0 - 200 m.p.f)") +
#   xlab("Transcripts per Million (TPM)") +
#   ylab("Count") +
#   facet_wrap(~gene)
# # facet_wrap(~founder.cell) +
# # labs(fill = "Gene")
# time_distribution_name_lin

# 
# bigDataCell %>%
#   filter(is.na(cell.type) | 
#            cell.type %in% c("Body_wall_muscle","Hypodermis", "Coelomocyte", 
#                             "Ciliated_amphid_neuron", "Ciliated_non_amphid_neuron", 
#                             "Glia", "GLR", "Intestinal_and_rectal_muscle", "Intestine", 
#                             "Seam_cell", "Pharyngeal_muscle", "Pharyngeal_intestinal_valve", "Pharyngeal_neuron")) %>%
#   ggplot(mapping = aes(x = embryo.time)) + 
#   geom_histogram(color = "white") + 
#   #scale_y_continuous(trans = 'log10') + 
#   facet_wrap(~cell.type)

# bigDataCell %>%
#   filter(!is.na(lineage) & !is.na(plot.cell.type)) %>% 
#   
#   ggplot(mapping = aes(x = embryo.time)) + 
#   geom_histogram(color = "white") + 
#   ggtitle("Distribution of all cells with cell name and lineage") + 
#   scale_y_continuous(expand = c(0,0),
#                      limits=c(0,13500))
# 



# bdc <- bdc %>% 
#   mutate(linname = case_when(
#     !is.na(plot.cell.type) & !is.na(lineage) ~ "lineage and cell name",
#     !is.na(plot.cell.type) & is.na(lineage) ~ "cell name only",
#     is.na(plot.cell.type) & !is.na(lineage) ~ "lineage only")) %>%
#   mutate(adj.time = embryo.time+45)

  
#Scatter plot of TPM with standard deviation as error bar
title <- glue("Expression of {desc_list[[i]]}")
scatt_tpm_time_stddev <- lins_main%>%
  filter(gene %in% group_list[[i]]) %>%
  #filter(time.mpfc <= 400) %>%
  filter(tpm > 0) %>%


  ggplot(mapping = aes(x = time.mpfc, y = tpm, color = gene)) +
  xlab("Time (minutes post first-cleavage)") +
  ylab("Transcripts per million (TPM)") +
  ggtitle("Raw TPM") +
  #geom_errorbar(aes(ymin = mean_tpm - std_dev, ymax= mean_tpm + std_dev), width=5, position=position_dodge(0.05)) +
  geom_point(alpha = 0.6) +
  facet_wrap(~founder.cell)



# plots <- list()
# i <- 1
# for (i in 1:length(groups)) {
#   
#   #Histogram of cell counts by founder cell with time on x axis
#   title <- glue("Number of cells expressing {desc_list[[i]]}") 
# 
#   histo_time_cell_count_by_founder_cell <- lins_main %>%
#     filter(gene %in% group_list[[i]]) %>%
#     filter(time.mpfc <= 400) %>%
#     filter(tpm > 0) %>%
#     
#     ggplot(mapping= aes(x = time.mpfc, fill = gene)) + 
#     ggtitle(title)+
#     geom_histogram(bins = 50, color = 'white', alpha=0.6, position = 'identity') +
#     #ggtitle(title) + 
#     xlab("Time (minutes post first-cleavage)") + 
#     ylab("Count") +
#     facet_wrap(~founder.cell)
#   
#   #Scatter plot of TPM with standard deviation as error bar
#   title <- glue("Expression of {desc_list[[i]]}") 
#   scatt_tpm_time_stddev <- lins_main%>%
#     filter(gene %in% group_list[[i]]) %>%
#     filter(time.mpfc <= 400) %>%
#     filter(tpm > 0) %>%
#     group_by(gene, founder.cell, time.mpfc) %>%
#     summarize(mean_tpm = mean(tpm), std_dev = sd(tpm)) %>%
#     
#     ggplot(mapping = aes(x = time.mpfc, y = mean_tpm, color = gene)) + 
#     xlab("Time (minutes post first-cleavage)") + 
#     ggtitle("Mean TPM") + 
#     ylab("Transcripts per million (TPM)") +
#     geom_errorbar(aes(ymin = mean_tpm - std_dev, ymax= mean_tpm + std_dev), width=5, position=position_dodge(0.05)) + 
#     geom_point(alpha = 0.6) + 
#     facet_wrap(~founder.cell)
#   
# 
#   
# 
# }
#   
#   lins_main%>%
#     filter(gene %in% group_list[[i]]) %>%
#     filter(time.mpfc <= 400) %>%
#     filter(tpm > 0) %>%
#     ggplot(mapping = aes(x="", y = tpm) )+
#     geom_boxplot(fill = "#0c4c8a") +
#     theme_minimal() +
#     facet_wrap(~gene)
#     
#   #Histogram with TPM on the x axis. 
#   title <- glue("Number of cells by expression of {desc_list[[i]]")
#   histo_tpm_cell_count_by_founder_cell <- lins_main %>%
#     filter(gene %in% group_list[[i]]) %>%
#     filter(time.mpfc <= 400) %>%
#     filter(tpm > 0) %>%
#     
#     ggplot(mapping = aes(x = tpm, fill = gene)) + 
#     xlab("Transcripts per Million") + 
#     ylab("Counts") +
#     geom_histogram(bins=50, color = 'white', alpha=0.6, position = 'identity') +
#     
#     facet_wrap(~founder.cell)
# }
# 



for (i in 1:length(group_list)) { 
  temp_df <- lins_main[which(lins_main$group == group_list[i]),]
  filename <- glue('raw data - {group_list[i]}.csv')
  print(dim(temp_df))
  #write.csv(temp_df, filename, row.names = FALSE)
  
}

i <- 1


hist_plots <- list()
tpm_plots <- list()

for (i in 1:length(group_list)) { 
    title <- glue("Distribution of lineages expressing {group_list[i]}")
    histo_time_cell_count_by_founder_cell <- lins_main %>%
      filter(group == as.character(group_list[i])) %>%
      filter(founder.cell == 'AB') %>%
      filter(time.mpfc <= 300) %>%
      filter(tpm > 0) %>%
      filter(!is.na(founder.cell)) %>%

      ggplot(mapping= aes(x = time.mpfc))+#, fill = gene)) +
      ggtitle('Count of AB cells expressing cadherens, zero-exclusive ')+
      geom_histogram(bins = 50, color = 'white', alpha=0.6, position = 'identity') +
      xlab("Time (minutes post first-cleavage)") +
      ylab("Count") +
      facet_wrap(~founder.cell)
    
    hist_plots[[i]] <- histo_time_cell_count_by_founder_cell
    
    title <- glue("Mean expression of {group_list[i]}")
    scatt_tpm_time_stddev <- lins_main%>%
      filter(group == as.character(group_list[i])) %>%
      filter(time.mpfc <= 400) %>%
      filter(tpm > 0) %>%
      filter(!is.na(founder.cell)) %>%
      
      group_by(gene, founder.cell, time.mpfc) %>%
      summarize(mean_tpm = mean(tpm), std_dev = sd(tpm)) %>%

      ggplot(mapping = aes(x = time.mpfc, y = mean_tpm, color = gene)) +
      xlab("Time (minutes post first-cleavage)") +
      ggtitle(title) +
      ylab("Transcripts per million (TPM)") +
      geom_errorbar(aes(ymin = mean_tpm - std_dev, ymax= mean_tpm + std_dev), width=5, position=position_dodge(0.05)) +
      geom_point(alpha = 0.6) +
      facet_wrap(~founder.cell)
    
    tpm_plots[[i]] <- scatt_tpm_time_stddev
}
sessionDir <- "C:/Users/chawmm/Desktop/4D Transcriptome/output/plots_founder_cell"
setwd(sessionDir)

#filename <- glue("all-groups_x-time_y-tpm_non-zero.pdf")
ggsave(
  filename = 'histograms of counts by family.pdf', 
  plot = marrangeGrob(hist_plots, nrow=1, ncol = 1), 
  #width = 1000, height = 600, units = "px"
  width = 11, height = 8.5, units = "in"
)
ggsave(
  filename = 'TPM vs time by family.pdf', 
  plot = marrangeGrob(tpm_plots, nrow=1, ncol = 1), 
  #width = 1000, height = 600, units = "px"
  width = 10, height = 7, units = "in"
)
##### #####
##### Outlier Detection #####



outlier_det_data %>%
  filter(tpm > 0) %>%
  #filter(time.mpfc < 200) %>%
  group_by(gene, time.mpfc) %>%
  summarize(mean_tpm = mean(tpm), std_dev = sd(tpm) / n()) %>%

  ggplot(mapping = aes(x="", y = mean_tpm) )+
  geom_boxplot(fill = "#0c4c8a") +
  theme_minimal() +
  facet_wrap(~gene)
  
outlier_det_data %>%
  filter(tpm > 0) %>%
  #filter(time.mpfc < 200) %>%
  group_by(gene, time.mpfc) %>%
  ggplot(mapping = aes(x="", y = tpm) )+
  geom_boxplot(fill = "#0c4c8a") +
  theme_minimal() +
  facet_wrap(~gene)



is_outlier <- function(x) {
  return(x < quantile(x, 0.25) - 1.5 * IQR(x) | x > quantile(x, 0.75) + 1.5 * IQR(x))
}
outlier_det_data %>% 
  filter(tpm > 0) %>%
  group_by(gene) %>% 
  mutate(outlier = ifelse(is_outlier(tpm), TRUE, FALSE)) %>%
  ungroup() %>%
  group_by(time.mpfc, gene, outlier) %>%
  summarize(mean_tpm = mean(tpm), std_err = sd(tpm, na.rm = TRUE) / n()) %>%
  ggplot(mapping = aes(x = time.mpfc, y = mean_tpm, color = outlier)) + 
  geom_point() + 
  facet_wrap(~gene)
  

# outlier_det_data %>% 
#   filter(tpm > 0) %>% 
#   # filter(gene == 'cdh-12') %>%
#   group_by(time.mpfc, gene) %>%
#   summarize(mean_tpm = mean(tpm), std_err = sd(tpm, na.rm = TRUE) / n()) %>%
#   ggplot(mapping = aes(x=time.mpfc, y = mean_tpm) )+
#   geom_point() +
#   theme_minimal() + 
#   facet_wrap(~ gene)

# as.list(ggplot_build(boxplot)$layout$layout['gene'])
# 
# as.data.frame(ggplot_build(boxplot)$data[[1]]['outliers'])[row, col]








#Get ordered list of facet variables from box plot.
#used for finding outliers

# 
# 
# df3<-transform(df1,z1=ifelse(x1==y1,x1*y1,x1/y1))
# new <- outlier_det_data %>%
#   group_by(gene) %>%
#   transform(outlier_det_data, outlier = ifelse(abs(tpm - median(tpm)) > 2*sd(tpm), TRUE, FALSE))
# 
# ggplot(data = new, mapping = aes(x = time.mpf, y = tpm, color = outlier)) + 
#   geom_point(alpha = 0.5) + 
#   facet_wrap(~gene)
