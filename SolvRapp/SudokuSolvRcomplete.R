library(purrr)
Color <- c("Red", "Orange", "Yellow", "Dark Green", "Light Green", "Dark Blue", "Light Blue", "Dark Purple", "Light Purple")
Number <- 1:9
names(Number) <- Color

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


Changes <- 0


SudokuSolveRcomplete <- function(SudVec, NoC = "ColorKu"){
  if(NoC == "ColorKu" && !all(SudVec[!is.na(SudVec)] %in% names(Number)))stop(paste("The following color(s) don't exist:", paste(SudVec[!is.na(SudVec)][!SudVec[!is.na(SudVec)] %in% names(Number)], collapse = ", ")))
  Orig <- matrix(SudVec, 9, 9, byrow = TRUE) 
  SudTab <- matrix(Number[SudVec], 9, 9, byrow = TRUE)
  if(NoC == "ColorKu")ConvSt <- Number[SudVec] else ConvSt <- SudVec
  Poss <- lapply(ConvSt, identity)
  dim(Poss) <- c(9,9)
  Poss <- t(Poss)
  ItList <- list()
  It <- 0
  while(any(is.na(SudTab))){
    Solved <- FALSE
    It <- It+1
    SudTab2 <- SudTab
    #Compute All Possible Colors Each Cell
    for(i in 1:9){
      for(j in 1:9){
        if(is.na(SudTab[i,j])){
          square <- c(SudTab[squareInd(i),squareInd(j)])
          PosOut <- Number[!(Number %in% unique(c(SudTab[i,], SudTab[,j], square)))]
          Poss[[i,j]] <- PosOut
        }
      }
    }
    
    ##############NEW LENGTH 2 LOGIC##################
    
    l2 <- map(Poss, ~length(.x) == 2)
    dim(l2) <- c(9,9)
    
    
    
    
    if(sum(unlist(l2))>1){
      
      l2cell <- as.data.frame(which(l2 == TRUE, arr.ind = TRUE))
      l2cell <- cbind(l2cell, square = squareFind(l2cell[,1], l2cell[,2]))
      l2cell$id <- 1:nrow(l2cell)
      l2bd <- l2cell
      i <- 1
      
      
      
      while(nrow(l2bd) > 1){
        
        l2f <- l2bd[i,]
        l2s <- l2bd[-i,]
        l2s <- cbind(l2s, matchRow = (l2s$row %in% l2f$row),  matchCol = (l2s$col %in% l2f$col), matchSq = (l2s$square %in% l2f$square))
        l2s$am <- l2s$matchCol | l2s$matchRow | l2s$matchSq
        
        if(any(l2s$am)){
          l2ss <- l2s[l2s$am,]
          AnyEq <- map2_lgl(l2ss$row, l2ss$col, function(x, y){
            all(Poss[[x,y]] %in% Poss[[l2f$row[1], l2f$col[1]]])
          })
          if(any(AnyEq) && sum(AnyEq) == 1){
            l2ssMatch <- l2ss[AnyEq,]
            
            ####ROW FIX
            if(l2ssMatch$matchRow){
              RemNums <- Poss[[l2ssMatch$row, l2ssMatch$col]]
              Poss[l2ssMatch$row, !(1:9 %in% c(l2ss$col, l2f$col))] <- map(Poss[l2ssMatch$row, !(1:9 %in% c(l2ss$col, l2f$col))], function(x){
                x[!(x %in% RemNums)]
              })
            }
            ####COL FIX
            if(l2ssMatch$matchCol){
              RemNums <- Poss[[l2ssMatch$row, l2ssMatch$col]]
              Poss[!(1:9 %in% c(l2ss$row, l2f$row)), l2ssMatch$col] <- map(Poss[!(1:9 %in% c(l2ss$row, l2f$row)), l2ssMatch$col], function(x){
                x[!(x %in% RemNums)]
              })
            }
            ####SQUARE FIX
            if(l2ssMatch$matchSq){
              RemNums <- Poss[[l2ssMatch$row, l2ssMatch$col]]
              PosInd <- sqRef[[l2ssMatch$square]] %>%
                filter(!(row %in% c(l2ssMatch$row, l2f$row)) | !(col %in% c(l2ssMatch$col, l2f$col)) )
              
              
              Poss[cbind(PosInd$row, PosInd$col)] <- map(Poss[cbind(PosInd$row, PosInd$col)], function(x){
                x[!(x %in% RemNums)]
              })
            }
            
            l2bd <- l2bd %>%
              filter(!(id %in% l2ssMatch$id))
          }
        }
        
        l2bd <- l2bd %>%
          filter(!(id %in% l2f$id))
        
        
        
      }
      
    }
    
    
    ##################################################
    
    
    
    #Check to see if each row column and square can be narrowed down
    PossR <- PossC <- PossSq <- Poss
    for(i in 1:9){
      #Check for unique color in a row
      Tabi <- table(unlist(Poss[i,]))
      Tabi <- Tabi[!(as.numeric(names(Tabi)) %in% SudTab2[i,])]
      
      if(any(Tabi == 1)){
        Changes <- Changes + 1
        ri <- as.numeric(names(Tabi)[Tabi == 1])
        Poss[i,] <- lapply(Poss[i,], function(x){
          if(any(x %in% ri)) ri[ri %in% x] else x
        })
      }
      
      #Check for unique color in a column      
      Tabj <- table(unlist(Poss[,i]))
      Tabj <- Tabj[!(as.numeric(names(Tabj)) %in% SudTab2[,i])]
      if(any(Tabj == 1)){
        Changes <- Changes + 1
        rj <- as.numeric(names(Tabj)[Tabj == 1])
        Poss[,i] <- lapply(Poss[,i], function(x){
          if(any(x %in% rj)) rj[rj %in% x] else x
        })
      }
      
      #Check for unique color in a square
      Tabij <- table(unlist(Poss[squareInd(indMat[i,1]), squareInd(indMat[i,2])]))
      Tabij <- Tabij[!(as.numeric(names(Tabij)) %in% SudTab2[squareInd(indMat[i,1]), squareInd(indMat[i,2])])]
      if(any(Tabij == 1)){
        Changes <- Changes + 1
        rij <- as.numeric(names(Tabij)[Tabij == 1])
        Poss[squareInd(indMat[i,1]), squareInd(indMat[i,2])] <- lapply(Poss[squareInd(indMat[i,1]), squareInd(indMat[i,2])], function(x){
          if(any(x %in% rij)) rij[rij %in% x] else x
        })
      }
    }

    
    #Update matrix based on cells that only have one possible value
    SudTab <- matrix(unlist(lapply(Poss, function(x)if(length(x) == 1) x else NA)), 9, 9)
    
    #If the table is the same as previous get out of the loop.
    if(all(sum(is.na(SudTab), na.rm = T) == sum(is.na(SudTab2), na.rm = TRUE))){
      break
    }
    ItList[[It]] <- SudTab
  }
  

  list(
    Iterations = It,
    OriginalPuzzle = Orig,
    ItList = ItList,
    CompletedPuzzle = apply(SudTab, 1:2, function(x){
      if(NoC == "ColorKu")ifelse(!is.na(x), names(Number[Number == x]), NA) else ifelse(!is.na(x), (Number[Number == x]), NA)
    })
  )
  
}

