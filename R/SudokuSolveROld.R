
SudokuSolveR <- function(SudVec){
  Changes <- 0
  if(!all(SudVec[!is.na(SudVec)] %in% names(Number)))stop(paste("The following color(s) don't exist:", paste(SudVec[!is.na(SudVec)][!SudVec[!is.na(SudVec)] %in% names(Number)], collapse = ", ")))
  
  SudTab <- Orig <- matrix(Number[SudVec], 9, 9, byrow = TRUE)
  Poss <- lapply(Number[SudVec], function(x)x)
  dim(Poss) <- c(9,9)
  Poss <- t(Poss)
  ItList <- list()
  It <- 0
  while(any(is.na(SudTab))){
    Solved <- FALSE
    It <- It+1
    SudTab2 <- ItList[[1]] <-  SudTab
    
    for(i in 1:9){
      if(Solved)break
      for(j in 1:9){
        if(is.na(SudTab[i,j])){
          square <- c(SudTab[squareInd(i),squareInd(j)])
          PosOut <- Number[!(Number %in% unique(c(SudTab[i,], SudTab[,j], square)))]
          if(length(PosOut) == 1){
            Changes <- Changes + 1 
            Poss[[i,j]] <- PosOut
            SudTab <- matrix(unlist(lapply(Poss, function(x)if(length(x) == 1) x else NA)), 9, 9)
            
            Solved <- TRUE
            break
          }else Poss[[i,j]] <- PosOut
        }
        
      }
    }
    if(Solved)next
    i <- 1
    for(i in 1:9){
      Tabi <- table(unlist(Poss[i,]))
      Tabi <- Tabi[!(as.numeric(names(Tabi)) %in% SudTab2[i,])]
      
      if(any(Tabi == 1)){
        Changes <- Changes + 1
        ri <- as.numeric(names(Tabi)[Tabi == 1])
        Poss[i,] <- lapply(Poss[i,], function(x){
          if(any(x %in% ri)) ri[ri %in% x] else x
        })
        SudTab <- matrix(unlist(lapply(Poss, function(x)if(length(x) == 1) x else NA)), 9, 9)
        
        Solved <- TRUE
        break

      }
      Tabj <- table(unlist(Poss[,i]))
      Tabj <- Tabj[!(as.numeric(names(Tabj)) %in% SudTab2[,i])]
      if(any(Tabj == 1)){
        Changes <- Changes + 1
        rj <- as.numeric(names(Tabj)[Tabj == 1])
        Poss[,i] <- lapply(Poss[,i], function(x){
          if(any(x %in% rj)) rj[rj %in% x] else x
        })
        SudTab <- matrix(unlist(lapply(Poss, function(x)if(length(x) == 1) x else NA)), 9, 9)
        
        Solved <- TRUE
        break

      }
      
      Tabij <- table(unlist(Poss[squareInd(indMat[i,1]), squareInd(indMat[i,2])]))
      Tabij <- Tabij[!(as.numeric(names(Tabij)) %in% SudTab2[squareInd(indMat[i,1]), squareInd(indMat[i,2])])]
      if(any(Tabij == 1)){
        Changes <- Changes + 1
        rij <- as.numeric(names(Tabij)[Tabij == 1])
        Poss[squareInd(indMat[i,1]), squareInd(indMat[i,2])] <- lapply(Poss[squareInd(indMat[i,1]), squareInd(indMat[i,2])], function(x){
          if(any(x %in% rij)) rij[rij %in% x] else x
        })
        SudTab <- matrix(unlist(lapply(Poss, function(x)if(length(x) == 1) x else NA)), 9, 9)
        Solved <- TRUE
        break

      }
    }
    if(Solved)next
    
    
    SudTab <- matrix(unlist(lapply(Poss, function(x)if(length(x) == 1) x else NA)), 9, 9)
    
    if(all(sum(is.na(SudTab), na.rm = T) == sum(is.na(SudTab2), na.rm = TRUE))){
      break
    }

  }

  ItList[[i]] <- SudTab
  list(
    Iterations = It, 
    ItList = ItList,
    CompletedPuzzle = apply(SudTab, 1:2, function(x)ifelse(!is.na(x), names(Number[Number == x]), NA))
  )
  
  }

