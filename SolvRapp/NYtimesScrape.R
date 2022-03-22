library(tidyverse)
library(rvest)
library(jsonlite)

NYtimes <- map(c("easy", "medium", "hard"), function(x){
  url <- paste("https://www.nytimes.com/puzzles/sudoku/", x, sep = "")
  webpage <- read_html(url)
  js <- webpage %>% 
    html_nodes("script") %>% 
    html_text()
  js1 <- gsub("window.gameData = ", "", js[1])
  js1 <- fromJSON(js1)
  Puz <- js1[[x]]$puzzle_data$puzzle
  ifelse(Puz == 0, NA, Puz)
})

names(NYtimes) <- c("easy", "medium", "hard")
