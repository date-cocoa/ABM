library(tidyverse)
library(viridis)

setwd('~/Desktop/ABM/')
data <- read_csv('./df.csv')

data <- 
  data %>% 
  select(-X1) %>% 
  mutate(
    'x' = rep(0:9, 10),
    'y' = rep(seq(0, 9, 1), each=10)
  )

my_theme <-
  theme_bw(base_family = "HiraKakuProN-W3") + 
  theme(axis.text = element_text(size = 0), legend.position="none",
        axis.title = element_text(size = 0), axis.ticks.length=unit(0, "cm"))
theme_set(my_theme) # set theme

library(RColorBrewer)
# Define the number of colors you want
nb.cols <- 100
mycolors <- colorRampPalette(brewer.pal(8, "Set2"))(nb.cols)

data %>% 
  ggplot() +
  geom_point(aes(x = x, y = y, color = `0`), size = 15) +
  scale_fill_manual(mycolors)


data %>% 
  ggplot() +
  geom_point(aes(x = x, y = y, color = `10000`), size = 15) +
  scale_fill_manual(mycolors)

             