library(tidyverse)

#Coloring for Plot
PColors <- c("Red", "Orange", "Yellow", "Dark Green", "Light Green", "Dark Blue", "Light Blue", "Dark Purple", "Light Purple","White")
hexCol <- c("#d62724", "#ff9443", "#eae22d", "#36763e", "#89ca42", "#324590", "#a2ccd5", "#662f9f", "#d2a9be", "#ffffff")

#Function Stuff
Color <- c("Red", "Orange", "Yellow", "Dark Green", "Light Green", "Dark Blue", "Light Blue", "Dark Purple", "Light Purple")
Number <- 1:9
names(Number) <- Color[1:9]

ind <- c(1, 4, 7)

indMat <- matrix(
  c(
    1, 1, 1, 4, 4, 4, 7, 7, 7,
    1, 4, 7, 1, 4, 7, 1, 4, 7
  ), ncol = 2
)

squareInd <- function(x){
  lb <- max(ind[ind <= x])
  ub <- lb + 2
  lb:ub
}


####1 step additional logic####

squareFind <- function(x, y){
  case_when(
    x %in% 1:3 & y %in% 1:3 ~ 1,
    x %in% 1:3 & y %in% 4:6 ~ 2,
    x %in% 1:3 & y %in% 6:9 ~ 3,
    
    x %in% 4:6 & y %in% 1:3 ~ 4,
    x %in% 4:6 & y %in% 4:6 ~ 5,
    x %in% 4:6 & y %in% 6:9 ~ 6,
    
    x %in% 6:9 & y %in% 1:3 ~ 7,
    x %in% 6:9 & y %in% 4:6 ~ 8,
    x %in% 6:9 & y %in% 6:9 ~ 9,
  )
}

sqRef <- list(
  data.frame(row = sort(rep(1:3, 3)), col = rep(1:3, 3)),
  data.frame(row = sort(rep(1:3, 3)), col = rep(4:6, 3)),
  data.frame(row = sort(rep(1:3, 3)), col = rep(7:9, 3)),
  
  data.frame(row = sort(rep(4:6, 3)), col = rep(1:3, 3)),
  data.frame(row = sort(rep(4:6, 3)), col = rep(4:6, 3)),
  data.frame(row = sort(rep(4:6, 3)), col = rep(7:9, 3)),
  
  data.frame(row = sort(rep(7:9, 3)), col = rep(1:3, 3)),
  data.frame(row = sort(rep(7:9, 3)), col = rep(4:6, 3)),
  data.frame(row = sort(rep(7:9, 3)), col = rep(7:9, 3))
)