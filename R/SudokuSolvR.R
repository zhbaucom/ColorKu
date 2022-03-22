funList <- list(step = SudokuSolveRpstep, complete = SudokuSolveRcomplete)

SudokuSolveR <- function(SudVec, method = "step", p = NULL, NoC = "ColorKu"){
  sudsolv <- funList[[method]]
  if(method == "step" && is.null(p))stop("Must choose p for number of steps")
  sudsolv(SudVec, p, NoC = NoC)
}
a <- system.time()
Sys.time()
