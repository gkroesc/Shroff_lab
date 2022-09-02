#####_____Plots_____#####
#####Akaike vs geom_smooth#####

plot <- ggplot(data = cbind(data, predicted_model), mapping = aes(x, y)) +
  geom_point() +
  xlab(x) + 
  ylab(y) + 
  geom_smooth(method = 'loess') + 
  geom_line(aes(y=pred, color = 'red'))
#####Specify one color#####
adj_names = sort(setdiff(groupA, "individual to specify"))
values = gg_color_hue(length(adj_names))
names(values) = adj_names
values = c(values, c("individual to specify"="black"))

data %>%  
  # filter(group == cat_groups[i] | gene == 'rps-23') %>%
  filter(group %in% names(values)) %>%
  group_by() %>%
  ggplot(mapping = aes(x = x, y = y, color = color)) +
  ggtitle() +
  xlab() +
  ylab() +
  scale_colour_manual(values=values) +
  facet_wrap(~group)
#####Mult plots, save to pdf#####
plots <- c()

for (i in 1:length(groups)) { 

  plot <- data() %>%  
    # filter(group == cat_groups[i] | gene == 'rps-23') %>%
    filter() %>%
    group_by() %>%
    summarize() %>%
    ggplot(mapping = aes(x, y, color)) +
    ggtitle() +
    xlab() +
    ylab() +
    facet_wrap()
  plots[[i]] <- plot
  
}
ggsave(
  filename = "filename", 
  plot = marrangeGrob(plots, nrow=1, ncol = 1), 
  width = 10, height = 7, units = "in"
  #width = 1000, height = 600, units = "px"
)

#####Density plot##### 

bdc %>% 
  filter(!is.na(linname)) %>%
  ggplot(bdc, mapping = aes(x = adj.time, fill = linname)) + 
  geom_density(color = 'black', alpha = 0.75) +
  xlab("Time (minutes post-fertilization)") + 
  ylab("Density") + 
  ggtitle("Distribution of cell information") + 
  labs(fill = "Cell Identification") 

plot + scale_fill_discrete(name="Experimental\nCondition",
                    breaks=c("ctrl", "trt1", "trt2"),
                    labels=c("Control", "Treatment 1", "Treatment 2"))
#####alpha overlap#####
time_distribution_name_lin <- main_table %>%
  mutate(name_lin=mapply(name_lin_func, d.name, d.lineage)) %>%
  ggplot(mapping = aes(x = time.mpf, fill = name_lin)) +
  geom_histogram(bins=50, color = 'white', alpha=0.6, position = 'identity') +
  ggtitle("Distribution of data") +
  xlab("Time (minutes post-fertilization)") +
  ylab("Count")
time_distribution_name_lin

#####histogram#####
ggplot(data = data, mapping= aes(x = time.mpf, color = founder.cell )) + 
  geom_histogram(bins=50, color = 'white') + 
  ggtitle(title) + 
  xlab("Time (minutes post-fertilization)") + 
  ylab("Count") #+
# facet_wrap(~founder.cell)

#####Histogram with adjusted density plot#####
bigDataCell %>%
  ggplot(mapping = aes(x = embryo.time, fill = lin_name)) + 
  geom_histogram(binwidth = 40, color = 'white', alpha=0.6, position = 'identity') +
  geom_density(aes(y=40*..count..), colour="black", alpha = 0.6, adjust=4)  + 
  xlab("Time (minutes post first cleavage)") + 
  ylab('Count')
plot <- ggplot(data = output, mapping = aes(x = embryo.time, y=TPM)) + 
  ggtitle(title) + 
  scale_y_continuous(breaks = round(seq(0, max(output$TPM), by = 2500),1)) + 
  geom_jitter(alpha=0.1)+ 
  coord_trans(y="log2") + 
  xlab("Time (minutes post first-cleavage)") + 
  ylab("Transcripts per Million")

#####Average TPM only#####
ggplot(data = mean_tpm, mapping = aes(x=time, y=tpm, color = cell)) + 
  ggtitle("Average TPM vs Time")+
  xlab("Time (minutes pfc)") + 
  geom_line() + 
  ylab("TPM") + 
  facet_wrap(~ gene)

#####Average TPM with Loess Curve#####
ggplot(data = mean_tpm, mapping = aes(x=time, y=tpm, color = cell)) + 
  ggtitle("Average TPM vs Time")+
  xlab("Time (minutes pfc)") +
  geom_line() + 
  geom_smooth(method = "loess", se=F) + 
  ylab("TPM") + 
  facet_wrap(~ gene)

#####Loess curve only with SE#####
ggplot(data = mean_tpm, mapping = aes(x=time, y=tpm, color = cell)) + 
  ggtitle("Average TPM vs Time")+
  xlab("Time (minutes pfc)") + 
  geom_smooth(method = "loess") + 
  ylab("TPM") + 
  facet_wrap(~ gene)

#####Boxplot#####
ggplot(mapping = aes(x="", y = mean_tpm) )+
  geom_boxplot(fill = "#0c4c8a") +
  theme_minimal() +
  facet_wrap(~gene)

#####Errorbar#####
plot <- lins_only %>% 
  filter(gene %in% group_list[[i]]) %>%
  filter(tpm > 0) %>% 
  filter(time.mpfc < 200) %>%
  filter(!is.na(founder.cell)) %>%
  group_by(founder.cell, gene, time.mpfc) %>%
  summarize(mean_tpm = mean(tpm), std_err = sd(tpm, na.rm = TRUE) / sqrt(n()) ) %>%
  ggplot(mapping = aes(x = time.mpfc, y = mean_tpm, color = gene)) + 
  geom_point() + 
  ggtitle(title) + 
  geom_errorbar(aes(ymin = mean_tpm - std_err, ymax= mean_tpm + std_err), width=5, position=position_dodge(0.05)) + 
  facet_wrap(~founder.cell)

#####Two Parter#####

p1 <- data %>%
  filter(gene == 'rps-23') %>%
  filter(embryo.time < 400) %>%
  ggplot(mapping = aes(x = embryo.time, y = mean_tpm_adj, color = gene)) +
  geom_point(mapping = aes(x = embryo.time, y = mean_tpm_adj))

p2 <- data %>%  
  filter(gastrulation == 'Internalizes during gastrulation') %>%
  filter(embryo.time < 400) %>%
  geom_point(color = 'black', mapping = aes(x = embryo.time, y = mean_tpm_adj))

plot <- p1 + p2

#####_____Functions_____#####

#####Akaike Information Criterion Model#####
model <- loess.as(filt_tab$time.mpf, filt_tab$mean_tpm, degree = 1, criterion = c("aicc"))
pred <- predict(model)

#####Normalize#####
norm_func <- function(x, xmin, xmax) {((x - xmin) / (xmax - xmin))}
calc_tpm_func <- function(umi, t.umi) {(as.integer(umi) / as.integer(t.umi)) * 1000000}
`%!in%` <- Negate(`%in%`)

#####Assign Association, Values#####
outerfunc <- function(x){ #Where x = row of dataframe
  #scrapes data using mapply to get corresponding data for each case
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
#####Identify founder cell#####
founder_cell_func <- function(x){ #where x is lineage
  if (substr(x, 1, 2) == "AB" | substr(x, 1, 2) == "MS"){
    return (substr(x, 1, 2))
  }else{
    return (substr(x,1,1))
  }
}

#####Identify clade#####
clade_func <- function(x) { #Where x is a single cell in lineage name column
  if (is.na(x)) { return()}
  if (grepl(substr(x, 1, 2), 'ABMS')) {
    return (substr(x,1,2))
  }else{
    if (grepl(substr(x,1,1), 'ECD')) {
      return(substr(x,1,1))
    }
  }
}

#####Get generation number#####
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



#####Assign lineage or name identity#####
lin_or_name <- function(x) { #where x is a row of dataframe 
  d_name <- x['plot.cell.type']
  d_lin <- x['lineage']
  d_time <- x['embryo.time']
  d_numi <- x['n.umi']
  d_idx <- x['index']
  #print(d_name)
  #print(d_lin)
  if (!is.na(d_name) & !is.na(d_lin) ) {
    return( 'cell name and lineage')
    
  }else if(!is.na(d_name) & is.na(d_lin)) {
    return( 'lineage only')

  }else if(is.na(d_name) & !is.na(d_lin) ) {
    return ( 'cell name only')
    
  }else if(is.na(d_name) & is.na(d_lin) ) {
    return ('unidentified')
  }
}


#####Color Hues#####

# http://stackoverflow.com/questions/8197559/emulate-ggplot2-default-color-palette
gg_color_hue <- function(n) {
  hues = seq(15, 375, length=n+1)
  hcl(h=hues, l=65, c=100)[1:n]
}

adj_names = sort(setdiff(groups, extra_group))
values = gg_color_hue(length(adj_names))
names(values) = adj_names
values = c(values, c(extragroup="color"))

#####_____Data Manipulation_____#####
#####Join tables#####

joined <- main %>% 
  left_join( to_join, by = c("ID" = "Analogous ID"))
#####Apply function in dplyr#####
norm_mean_tpm <- mean_tpm %>%
  group_by(cell,gene) %>%
  summarize(time=time, norm_tpm = norm_tpm_func(tpm,min(tpm),max(tpm)))


#####dplyr mutation function#####
data%>%mutate(col, newcol = sapply(col, function(x) { if (x <= 1) {return(1)} else{return(x)}}))
  
#####Read 10xCellRanger Mtx#####
library(Matrix)
bigmm <- readMM("C:\\Users\\chawmm\\Desktop\\4D Transcriptome\\data\\GSE126954\\GSE126954_gene_by_cell_count_matrix.txt")

#####standard deviation#####
summarize(mean_tpm = mean(tpm), std_dev = sd(tpm, na.rm = TRUE))

#####standard error#####
summarize(mean_tpm = mean(tpm), std_err = sd(tpm, na.rm = TRUE) / sqrt(n()) )

#####Creating lineage/name groups and adjusting embryo time#####
bdc <- bdc %>% 
  mutate(linname = case_when(
    !is.na(plot.cell.type) & !is.na(lineage) ~ "lineage and cell name",
    !is.na(plot.cell.type) & is.na(lineage) ~ "cell name only",
    is.na(plot.cell.type) & !is.na(lineage) ~ "lineage only")) %>%
  mutate(adj.time = embryo.time+45)

#####robust dataframe to collect gene indices without losing order#####
gene_frame <- data.frame(gene.name = genes)#, group = descriptions)
gene_frame <- gene_frame %>% filter(gene.name %in% bigDataGene$gene_short_name)
gene_frame$gene.index = unlist(sapply(gene_frame$gene.name, function(x){return(which(bigDataGene$gene_short_name == x))}))
mm <- bigmm[gene_frame$gene.index,]
  