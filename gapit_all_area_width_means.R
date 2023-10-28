library(tidyverse)
library(GAPIT)
library(lme4)
library(lmerTest)
library(knitr)
library(kableExtra)

#MAF filter
# Create a function to filter columns
filter_columns <- function(df, threshold = 0.05) {
  filtered_cols <- c()
  total_rows <- nrow(df)
  
  for (col in names(df)) {
    col_values <- df[, col]
    value_counts <- table(col_values)
    
    # Sort the value counts in descending order
    sorted_counts <- sort(value_counts, decreasing = TRUE)
    
    # Calculate the proportion of the most common value
    most_common_prop <- sorted_counts[1] / total_rows
    
    # Check if the most common value is greater than the threshold
    if (most_common_prop > (1 - threshold)) {
      filtered_cols <- c(filtered_cols, col)
    }
  }
  
  # Filter the dataframe based on the selected columns
  filtered_df <- df[, -which(names(df) %in% filtered_cols)]
  return(filtered_df)
}



pa_in <- read_csv("./pod_traits_all_1019.csv")

pheno_cols <- c("Year", "Location", "NC_Accession","pod_area","pod_width", "Block")
pa_in <- pa_in[, pheno_cols]
pa_in$Block <- as.numeric(pa_in$Block)
pa_in_22 <- pa_in 
#%>%
  #subset(pa_in$Year== 2022)

gapit_names <- read.csv("./final_csvs/names_nospaces.csv")
gapit_names$NC_Accession <- gapit_names$taxa

merged_data_22 <- merge(pa_in_22, gapit_names, by = "NC_Accession", all.x = TRUE)
merged_data_22$NC_Accession <- merged_data_22$taxa.1
merged_data_22 <- merged_data_22[,1:6]
merged_data_22$Env <- paste(merged_data_22$Year, merged_data_22$Location, sep = "_")


envmodel_width <- lmer(pod_width ~ (1 | Env/Block) + (1 | NC_Accession) + (1 | NC_Accession:Env), data = merged_data_22)

envmodel_area <- lmer(pod_area ~ (1 | Env/Block) + (1 | NC_Accession) + (1 | NC_Accession:Env), data = merged_data_22)

#variance components
vc_width <- VarCorr(envmodel_width)
vc_area <- VarCorr(envmodel_area)

#AREA
VG_area <- unlist(vc_area$NC_Accession)
VGE_area <- unlist(vc_area$`NC_Accession:Env`)
Verr_area <- (sigma(envmodel_area)^2)
H2_area <- VG_area / (VG_area + VGE_area + Verr_area)


rea_area <- ranova(envmodel_area)
coeffs_area <- coef(envmodel_area)
ran_eff_area <- ranef(envmodel_area)

#WIDTH
VG_width <- unlist(vc_width$NC_Accession)
VGE_width <- unlist(vc_width$`NC_Accession:Env`)
Verr_width <- (sigma(envmodel_width)^2)
H2_width <- VG_width / (VG_width + VGE_width + Verr_width)


rea_width <- ranova(envmodel_width)
coeffs_width <- coef(envmodel_width)
ran_eff_width <- ranef(envmodel_width)

area_df <- as.data.frame(rea_area)
width_df <- as.data.frame(rea_width)

kable(area_df, format = "html", caption = "Pod Area Anova Results", digits = 2000) %>%
  kable_styling(full_width = FALSE)

kable(width_df, format = "html", caption = "Pod Width Anova Results", digits = 2000) %>%
  kable_styling(full_width = FALSE)
#yr_loc_mod <- lmer(pod_area ~  (1 | Location/Block) + (1 | NC_Accession/Location), data = merged_data_22)
#this pulls all the variability estimates out
#vc_yr <- VarCorr(yr_loc_mod)

#Heritability, ANOVA and BLUP extraction
#VGyr <- unlist(vc_yr$NC_Accession)
#VGL <- unlist(vc_yr$`Location:NC_Accession`) / 3 
#Verryr <- (sigma(yr_loc_mod)^2)
#H2_yr <- VGyr / (VGyr + VGL + Verryr)


#rea_yr <- ranova(yr_loc_mod)
#coeffs_yr <- coef(yr_loc_mod)
#ran_eff_yr <- ranef(yr_loc_mod)
m_area <- mean(merged_data_22$pod_area)
s_area <- sd(merged_data_22$pod_area)

distro_area <- ggplot(data = merged_data_22, aes(x = pod_area)) +
  geom_histogram(binwidth = 5, fill = "red", color = "black", alpha = 0.7) +
  labs(title = "Mean Pod Area by Plot", x = "Mean Pod Area (mm^2)", y = "Frequency") +
  geom_text(aes(x = m_area - 110, y= 75, label = paste("Mean =", round(m_area, 2))), vjust = -0.5, color = "black") +
  geom_text(aes(x = m_area - 50 , y = 75, label = paste("SD =", round(s_area, 2))), vjust = -0.5, color = "black") +
  geom_text(aes(x = m_area - 200, y = 100, label = "Bin Size = 5mm^2"), vjust = -0.5, color = "black")



distro_area +
  stat_function(fun = function(x) dnorm(x, mean = mean(merged_data_22$pod_area), sd = sd(merged_data_22$pod_area)) * length(merged_data_22$pod_area) * 5, color = "blue", size = 1)


m_width <- mean(merged_data_22$pod_width)
s_width <- sd(merged_data_22$pod_width)


distro_width <- ggplot(data = merged_data_22, aes(x = pod_width)) +
  geom_histogram(binwidth = .1, fill = "red", color = "black", alpha = 0.7) +
  labs(title = "Mean Pod Width by Plot", x = "Mean Pod Width (mm)", y = "Frequency") +
  geom_text(aes(x = m_width - 2, y= 75, label = paste("Mean =", round(m_width, 2))), vjust = -0.5, color = "black") +
  geom_text(aes(x = m_width - 1 , y = 75, label = paste("SD =", round(s_width, 2))), vjust = -0.5, color = "black") +
  geom_text(aes(x = m_width - 4, y = 115, label = "Bin Size = 0.1mm"), vjust = -0.5, color = "black")


distro_width +
  stat_function(fun = function(x) dnorm(x, mean = mean(merged_data_22$pod_width), sd = sd(merged_data_22$pod_width)) * length(merged_data_22$pod_width) * .1, color = "blue", size = 1)







area_width <- merged_data_22 %>%
  group_by(NC_Accession) %>%
  summarize(mean_pod_area = mean(pod_area), mean_pod_width = mean(pod_width))
area_width <- as.data.frame(area_width)
#GAPIT 
myY <- area_width %>%
  rename(taxa = NC_Accession)
vals_match <- myY$taxa



myGD <- as.data.frame(read_csv("C:/Users/nkgarrit/NC State PB&G Dropbox/Nick Garrity/GWAS/filter_num_trim.csv", col_names = TRUE))
myGD <- myGD[myGD$taxa %in% vals_match, ]
myGD2 <- myGD %>%
  mutate(across(2:last_col(), ~ . * 2))
myGM <- as.data.frame(read_csv("C:/Users/nkgarrit/NC State PB&G Dropbox/Nick Garrity/GWAS/gm_gapit.csv",col_names = TRUE))

myGAPIT <- GAPIT(
  Y = myY[,1:3],
  GD=myGD2,
  GM=myGM,
  PCA.total = 3,
  model = c("FarmCPU", "BLINK", "MLMM"),
  Multiple_analysis = TRUE,
  Phenotype.View=F
)

##GAPIT HTS and ILs
il_names <- read_csv("./predicted_pheno_il.csv", col_names = TRUE)
myY_il <- myY %>%
  merge(il_names, by = "taxa") %>%
  select(taxa, mean_pod_width, mean_pod_area)
vals_match_il <- myY_il$taxa

myGD <- as.data.frame(read_csv("C:/Users/nkgarrit/NC State PB&G Dropbox/Nick Garrity/GWAS/filter_num_trim.csv", col_names = TRUE))
myGD <- myGD[myGD$taxa %in% vals_match_il, ]
myGDIL <- myGD %>%
  mutate(across(2:last_col(), ~ . * 2))

constant_columns <- sapply(myGDIL, function(col) length(unique(col)) == 1)
if (any(constant_columns)) {
  cat("Constant columns found and excluded: ", colnames(myGDIL)[constant_columns], "\n")
  myGDIL <- myGDIL[, !constant_columns]
}
myGDIL <- filter_columns(myGDIL, threshold = 0.05)
col_filter <- colnames(myGDIL)
myGMIL <- myGM[myGM[,1] %in% col_filter,]
myGMIL <- as.data.frame(myGMIL)

myGAPIT <- GAPIT(
  Y = myY_il[,1:3],
  GD=myGDIL,
  GM=myGMIL,
  PCA.total = 2,
  model = c("FarmCPU", "BLINK", "MLMM"),
  Multiple_analysis = TRUE,
  Phenotype.View=F
)


##GAPIT Ns
n_names <- read_csv("./predicted_pheno_n.csv", col_names = TRUE)
myY_n <- myY %>%
  merge(n_names, by = "taxa") %>%
  select(taxa, mean_pod_width, mean_pod_area)


vals_match_n <- myY_n$taxa

myGD <- as.data.frame(read_csv("C:/Users/nkgarrit/NC State PB&G Dropbox/Nick Garrity/GWAS/filter_num_trim.csv", col_names = TRUE))
myGD <- myGD[myGD$taxa %in% vals_match_n, ]
myGDN <- myGD %>%
  mutate(across(2:last_col(), ~ . * 2))

constant_columns <- sapply(myGDN, function(col) length(unique(col)) == 1)
if (any(constant_columns)) {
  cat("Constant columns found and excluded: ", colnames(myGDN)[constant_columns], "\n")
  myGDN <- myGDN[, !constant_columns]
}


myGDN <- filter_columns(myGDN, threshold = 0.05)

col_filter <- colnames(myGDN)
myGMN <- myGM[myGM[,1] %in% col_filter,]
myGMN <- as.data.frame(myGMN)




myGAPIT <- GAPIT(
  Y = myY_n[,1:3],
  GD=myGDN,
  GM=myGMN,
  PCA.total = 2,
  model = c("FarmCPU", "BLINK", "MLMM"),
  Multiple_analysis = TRUE,
  Phenotype.View=F
)

kinship_matrix <- A.mat(myGD[,2:6270])
heatmap(kinship_matrix, Colv = NA, symm = TRUE, scale = "none", main = "Kin Mat heatmap")



