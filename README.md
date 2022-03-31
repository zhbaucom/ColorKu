# ColorKu 

## The Story

My family is really getting into the board game ColorKu. It has the exact same rules as Sudoku, except instead of numbers it uses colored balls. Typically, when someone gets miserably stuck, the reaction is to go to the solutions card. This doesn't jive well for me because it gives you information beyond where you worked to on the puzzle. Instead I wanted a way to know if there is a findable cell given my level of logic. I then created an R Shiny web application, [Sudoku SolveR](https://zhbaucom.shinyapps.io/SolvRapp/), that will provide that answer.

![alt text](https://github.com/zhbaucom/ColorKu/blob/main/imgs/readmeIMG/SudokuSolveR.png?raw=true)

Data entry is the annoying part of the application. Although I have included a number of ColorKu puzzles and NY Times Sudoku puzzles, you still need to go through block by block to update how much of the puzzle you've completed. 

The solution: **deep learning**.

To more efficiently transfer data from a game board to the application it'd be nice to take a picture of the board and have it read the cells automatically. I was able to do this using python `opencv` library. It first identifies the edges of the board, reforms the board into a perfect square, then resize so I know the exact pixel in the middle of each cell.

![alt text](https://github.com/zhbaucom/ColorKu/blob/main/imgs/readmeIMG/board.png)

![alt text](https://github.com/zhbaucom/ColorKu/blob/main/imgs/readmeIMG/boardsquare.png)

Next, I create a square around each cell and save the cell image. It is then fed through a convolution neural network to identify cell color. I decided on deep learning over other color identification because it allowed me to predict the correct color under different lightings. To fit the neural network I used `tensorflow` and `keras` libraries.

To test out how accurate the color identifier is, use the `testBall.py` script.

![alt text](https://github.com/zhbaucom/ColorKu/blob/main/imgs/readmeIMG/boardSolved.png)

Still not perfect, but a great start. To get more accurate results we could use more training data under different lighting coniditions. Another option is to predict the whole board at once, instead of doing it 1 by 1. To do this, each cell would have shared NN parameters, but before the final prediction, we add a layer to connect each end layer node. When the NN is fit to each cell independently, under one lighting scenario an empty cell may look very similar to another lighting scenarios orange. By connecting a final layer for the whole 9x9 grid, it would allow the algorithm to look at other cells that have high probability of being orange or empty and see where a given cell is more likely to fit. This will allow for better control of different lighting situations, but will also require much more data.
