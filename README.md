# ColorKu 

## The Story

Over Christmas break I noticed my family really getting into the board game ColorKu. It has the exact same rules as Sudoku, except instead of numbers it uses colored balls. When someone got stuck miserably stuck in the puzzle the reaction was to go to the solutions card. This didn't jive well for me because it gave you information beyond where you worked to get the puzzle to. Instead I wanted a way to tell me if there is a findable cell given my level of logic. I then created an R Shiny web application, [Sudoku SolveR](https://zhbaucom.shinyapps.io/SolvRapp/), that will provide that answer.

![alt text](https://github.com/zhbaucom/ColorKu/tree/main/imgs/readmeIMG/SudokuSolveR.png "")

Data entry is the annoying part of the application. Although I have included a number of ColorKu puzzles and NY Times Sudoku puzzles, you still need to go through block by block to update how much of the puzzle you've completed. The solution, **deep learning**.

To more efficiently transfer data from a game board to the application it'd be nice to take a picture of the board and have it read the cells automatically. I was able to do this using python `opencv` library. It first identifies the edges of the board, reforms the board into a perfect square, then I'm able to resize so I know the exact pixel in the middle of each cell.

![alt text](https://github.com/zhbaucom/ColorKu/tree/main/imgs/readmeIMG/board.png "")

![alt text](https://github.com/zhbaucom/ColorKu/tree/main/imgs/readmeIMG/boardsquare.png "")

Next, I create a square around each cell and save the cell image. It is then fed through a convolution neural network to identify cell color. I decided on deep learning over other color identification because it allowed me to predict the correct color under different lightings. To fit the neural network I used `tensorflow` and `keras` libraries.

To test out accurate the color identifier is, use the `testBall.py` script.

![alt text](https://github.com/zhbaucom/ColorKu/tree/main/imgs/readmeIMG/boardsolved.png "")
