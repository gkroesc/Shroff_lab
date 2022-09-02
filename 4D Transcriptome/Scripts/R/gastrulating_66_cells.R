





gast_cells <- read.csv("C:/Users/chawmm/Desktop/4D Transcriptome/cell keys/66_gastrulating_cells.csv")

packer_s6 <- read.csv("C:/Users/chawmm/Desktop/4D Transcriptome/cell keys/packer_s6.csv")

gast_cells_joined <- gast_cells %>% 
  left_join( packer_s6, by = c("cell" = "cell"))
