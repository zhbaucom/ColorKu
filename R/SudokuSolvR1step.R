SudokuSolveR1step <- function(SudVec, NoC = "ColorKu"){
  Changes <- 0
  if(NoC == "ColorKu" && !all(SudVec[!is.na(SudVec)] %in% names(Number)))stop(paste("The following color(s) don't exist:", paste(SudVec[!is.na(SudVec)][!SudVec[!is.na(SudVec)] %in% names(Number)], collapse = ", ")))
  Orig <- matrix(SudVec, 9, 9, byrow = TRUE) 
  SudTab <- matrix(Number[SudVec], 9, 9, byrow = TRUE)
    if(NoC == "ColorKu")ConvSt <- Number[SudVec] else ConvSt <- SudVec
  Poss <- lapply(ConvSt, identity)
  dim(Poss) <- c(9,9)
  Poss <- t(Poss)

 
  Solved <- FALSE
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
  if(any(unlist(lapply(Poss, is.na))))warning("ERROR IN PUZZLE!!!")
  #Check to see if each row column and square can be narrowed down
  PossR <- PossC <- PossSq <- Poss
  for(i in 1:9){
    #Check for unique color in a row
    Tabi <- table(unlist(Poss[i,]))
    Tabi <- Tabi[!(as.numeric(names(Tabi)) %in% SudTab2[i,])]
    
    if(any(Tabi == 1)){
      Changes <- Changes + 1
      ri <- as.numeric(names(Tabi)[Tabi == 1])
      PossR[i,] <- lapply(Poss[i,], function(x){
        if(any(x %in% ri)) ri[ri %in% x] else x
      })
    }
    
    #Check for unique color in a column      
    Tabj <- table(unlist(Poss[,i]))
    Tabj <- Tabj[!(as.numeric(names(Tabj)) %in% SudTab2[,i])]
    if(any(Tabj == 1)){
      Changes <- Changes + 1
      rj <- as.numeric(names(Tabj)[Tabj == 1])
      PossC[,i] <- lapply(Poss[,i], function(x){
        if(any(x %in% rj)) rj[rj %in% x] else x
      })
    }
    
    #Check for unique color in a square
    Tabij <- table(unlist(Poss[squareInd(indMat[i,1]), squareInd(indMat[i,2])]))
    Tabij <- Tabij[!(as.numeric(names(Tabij)) %in% SudTab2[squareInd(indMat[i,1]), squareInd(indMat[i,2])])]
    if(any(Tabij == 1)){
      Changes <- Changes + 1
      rij <- as.numeric(names(Tabij)[Tabij == 1])
      PossSq[squareInd(indMat[i,1]), squareInd(indMat[i,2])] <- lapply(Poss[squareInd(indMat[i,1]), squareInd(indMat[i,2])], function(x){
        if(any(x %in% rij)) rij[rij %in% x] else x
      })
    }
    }
    
    #Compile All the new possiblities after going through rows, columns, and squares
    Poss <- map2(PossR, PossC, intersect) %>%
      map2(PossSq, intersect)
    dim(Poss) <- c(9,9)
    
    #Update matrix based on cells that only have one possible value
    SudTab <- matrix(unlist(lapply(Poss, function(x)if(length(x) == 1) x else NA)), 9, 9)
    
    #If the table is the same as previous get out of the loop.
    if(all(sum(is.na(SudTab), na.rm = T) == sum(is.na(SudTab2), na.rm = TRUE))){
      if(any(is.na(SudTab))){
        warning(paste("Puzzle is not logically solveable with", sum(is.na(SudTab), na.rm = T), "steps remaining. Broke after", i, "iterations."))
      }else{
        warning(paste("Puzzle solved after", i, "of", p, "iterations."))
      }
      break
    }

  
  list(
    OriginalPuzzle = Orig,
    CompletedPuzzle = apply(SudTab, 1:2, function(x){
      if(NoC == "ColorKu")ifelse(!is.na(x), names(Number[Number == x]), NA) else ifelse(!is.na(x), (Number[Number == x]), NA)
    })
  )
  
}

