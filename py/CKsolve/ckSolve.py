import numpy as np
import pandas as pd
import random

################################## Helper Functions and values START ##############################################################
def square_find(x, y):
    if x in np.arange(0,3) and y in np.arange(0,3): return 0
    if x in np.arange(0,3) and y in np.arange(3,6): return 1
    if x in np.arange(0,3) and y in np.arange(6,9): return 2

    if x in np.arange(3,6) and y in np.arange(0,3): return 3
    if x in np.arange(3,6) and y in np.arange(3,6): return 4
    if x in np.arange(3,6) and y in np.arange(6,9): return 5

    if x in np.arange(6,9) and y in np.arange(0,3): return 6
    if x in np.arange(6,9) and y in np.arange(3,6): return 7
    if x in np.arange(6,9) and y in np.arange(6,9): return 8

squareInd = pd.DataFrame([[x , y, square_find(x, y)] for x in np.arange(9) for y in np.arange(9)], columns = ['x', 'y', 'square'])

def square_ind(x):
    sqdfs = squareInd.loc[squareInd.square == x,['x', 'y']]
    return np.unique(sqdfs.x), np.unique(sqdfs.y)

Colorz = np.array(["Red", "Orange", "Yellow", "Dark Green", "Light Green", "Dark Blue", "Light Blue", "Dark Purple", "Light Purple"])

#### PART of Cell update
def isn1(x):
    if pd.isnull(x):
        return 1
    else:
        return 0

def lg1(x):
    if len(x) == 1:
        return 1
    else:
        return 0


################################## Helper Functions and values END ##############################################################


class ckPuzzle:


    def __init__(self, puzzle_vector):
        p2 = [puzzle_vector[(i*9):(9*(i + 1))] for i in np.arange(9)]
        puzzdf = pd.DataFrame(p2)
        possdf = puzzdf.copy()
        self.puzzdf = puzzdf


    def solve1step(self):
        possdf = self.puzzdf.copy()
        puzzdf = self.puzzdf

        ## First pass
        for i in np.arange(9):
            for j in np.arange(9):
                if puzzdf.iloc[i, j] == None:
                    rvals = puzzdf.iloc[i,:].values
                    rvals = rvals[rvals != None]

                    cvals = puzzdf.iloc[:,j].values
                    cvals = cvals[cvals != None]

                    square = square_find(i, j)
                    sqi = squareInd.loc[squareInd.square == square,:]
                    svals = puzzdf.iloc[np.unique(sqi.x), np.unique(sqi.y)].values
                    svals = svals[svals != None]

                    nsc = [not(col in np.unique(np.concatenate((rvals, cvals, svals)))) for col in Colorz]
                    possdf.iloc[i,j] = Colorz[nsc]
                else:
                    possdf.iloc[i,j] = np.array([puzzdf.iloc[i,j]])

        ## Unique Color in each row, column, and square
        rowcols = []
        colcols = []
        sqcols = []
        for k in np.arange(9):
            icol = possdf.iloc[k,:]
            ucol, colcount = np.unique(np.concatenate(icol.values), return_counts = True)
            ucol = ucol[colcount == 1]

            rowcols.append(ucol)

            icol = possdf.iloc[:,k]
            ucol, colcount = np.unique(np.concatenate(icol.values), return_counts = True)
            ucol = ucol[colcount == 1]

            colcols.append(ucol)

            i, j = square_ind(k)

            icol = possdf.iloc[i,j]
            ucol, colcount = np.unique(np.concatenate(np.concatenate(icol.values)), return_counts = True)
            ucol = ucol[colcount == 1]

            sqcols.append(ucol)

        ## Check for unique colors in each cell and substitute
        for i in np.arange(9):
            for j in np.arange(9):
                cval = possdf.iloc[i,j]
                if len(cval) > 1:
                    sqnum = square_find(i,j)
                    icol = rowcols[i]
                    jcol = colcols[j]
                    kcol = sqcols[sqnum]
                    ucol = np.unique(np.concatenate((icol, jcol, kcol)))
                    ici = [ic in ucol for ic in cval]
                    if any(ici):
                        possdf.iloc[i,j] = cval[ici]

        self.possdf = possdf
        puzzna = self.puzzdf.applymap(isn1)
        possna = self.possdf.applymap(lg1)

        self.missx, self.missy = np.where((puzzna + possna) == 2)


    def errorCheck(self):
        rowcols = []
        colcols = []
        sqcols = []
        error_list = []
        for k in np.arange(9):
            icol = self.possdf.iloc[k,:]
            ucol, colcount = np.unique((np.concatenate([x for x in icol if len(x) == 1 ])), return_counts = True)
            if any(colcount >1):
                error_list.append("Problem with puzzle!\n Algorithm found multiple " + ', '.join(ucol[colcount > 1])+ " in row " + str(k))

            icol = self.possdf.iloc[:,k]
            ucol, colcount = np.unique((np.concatenate([x for x in icol if len(x) == 1 ])), return_counts = True)
            if any(colcount >1):
                error_list.append("Problem with puzzle!\n Algorithm found multiple " + ', '.join(ucol[colcount > 1])+ " in column " + str(k))

            i, j = square_ind(k)
            icol = np.concatenate(self.possdf.iloc[i,j].values)
            ucol, colcount = np.unique(np.concatenate([x for x in icol if len(x) == 1 ]), return_counts = True)
            if any(colcount >1):
                error_list.append("Problem with puzzle!\n Algorithm found multiple " + ', '.join(ucol[colcount > 1])+ " in square " + str(k))

        if len(error_list) > 0:
            return error_list
        else:
            return "No error"

    def complete_check(self):
        return not any(np.concatenate(self.possdf.applymap(lambda x: len(x) > 1).values))


    #### Check if any cells updated_cells
    def puzz_change(self):
        if len(self.missx) > 0:
            return True
        else:
            return False

    def puzzle_update(self, reveal = "one"):
        puzzdf2 = self.puzzdf.copy()
        if reveal == "one":
            k = random.randint(0, len(self.missx)-1)
            locx, locy = self.missx[k], self.missy[k]
            puzzdf2.iloc[locx, locy] = self.possdf.iloc[locx, locy][0]
            self.locx, self.locy = locx, locy
        if reveal == "all":
            self.locx, self.locy = self.missx, self.missy
            for k in np.arange(len(self.missx)):
                puzzdf2.iloc[self.missx[k], self.missy[k]] = self.possdf.iloc[self.missx[k], self.missy[k]][0]

        self.puzzdf_update = puzzdf2
        self.puzzdf_update_values = np.concatenate(self.puzzdf_update.values)



def puzzle_solver(puzzle_vector):
    cont = True
    while cont:
        mypuz = ckPuzzle(puzzle_vector)
        mypuz.solve1step()
        mypuz.puzzle_update(reveal = "all")
        cont = (mypuz.errorCheck() == "No error") and (mypuz.puzz_change()) and (not mypuz.complete_check())

        if cont:
            puzzle_vector = mypuz.puzzdf_update_values

    if (mypuz.errorCheck() != "No error"):
        return mypuz.errorCheck()
    if (not mypuz.puzz_change()) and (not mypuz.complete_check()):
        print("Logic got stuck at...")
        return mypuz.puzzdf_update
    if mypuz.complete_check():
        print("puzzle completed!")
        return mypuz.puzzdf_update
