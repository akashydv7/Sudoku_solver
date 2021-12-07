import pygame as py
import time, sys 

# SET UP OF PYAGME
py.init()
width = 450
height = 500
win = py.display.set_mode((width, height))
py.display.set_caption("SUDOKU SOLVER")
font = py.font.Font('freesansbold.ttf', 25)
w = 50

# THEME
class Theme:
    def __init__(self, bg, text, tile, cur):
        self.bg = bg
        self.text = text
        self.tile = tile
        self.cursor = cur

# CREATING TWO THEME OBJECTS

light = Theme((51, 224, 255), (0, 0, 0), (255, 255, 255), (235, 25, 109))
dark = Theme((46, 51, 71), (255, 255, 255), (17, 17, 17), (235, 25, 109))
used = light

# delay in animation
delay = 0.05

# PRINT THE MATRIX
def print_matrix(grid):
    print("Grid : ")
    for row in grid:
        for e in row:
            print(e, end=" ")
        print("")

# Checks if value 'n' can be placed at position (row, col) in grid: 
def isvalid(grid, n, row, col):
    
    # if n is present in same row or col return False
    for x in range(9):
        if grid[row][x]==n:
            return False
    for x in range(9):
        if grid[x][col]==n:
            return False
    bx = (row//3)*3
    by = (col//3)*3
    
    # if n is present in same 3x3 block return False
    for i in range(3):
        for j in range(3):
            if grid[bx+i][by+j]==n:
                return False

    return True

# Finds empty cells in sudoku grid
def find(grid):
    for x in range(9):
        for y in range(9):
            if grid[x][y]==0:
                return (x, y)
    # if all cells are filled return None
    return None


def solve(grid):
    for event in py.event.get():
        if event.type == py.QUIT:
            py.quit()
            sys.exit()
    # find an empty cell
    f = find(grid)
    if f is None:
        return True   # if all cells are filled, grid is already solved
    x = f[0]
    y = f[1]
    py.draw.rect(win, used.cursor, (x*w, y*w, w, w), 4)
    py.display.update()
    # find value for empty cell in range [1, 9]
    for val in range(1, 10):
        if isvalid(grid, val, f[0], f[1]):
            grid[x][y] = val   # if a value is found assign it to the cell and solve the rest of the grid
            time.sleep(delay)
            draw()
            if solve(grid): # if the rest of the grid can be solved with this value in the cell return True
                return True
            grid[x][y]=0 # else assign 0 to the cell and look for next value (backtrack)
    return False

# Visualization using pygame
def draw():
    win.fill(used.bg)
    for i in range(9):
        for j, n in enumerate(grid[i]):
            py.draw.rect(win, used.tile, (i*w+1, j*w+1, w-1, w-1))
            if n==0:
                continue
            text = font.render(str(n), True, used.text)
            win.blit(text, (i*w+17, j*w+17))

    unsel = used.text
    py.draw.rect(win, unsel, (width-75, height-40, 60, 30), 3, 3)
    py.draw.rect(win, unsel, (width-72, height-37, 30, 24))
    if stage==2:
        t = font.render("Solving...", True, used.text)
    elif stage==3:
        t = font.render("Solved", True, used.text)
    else:
        t = font.render("Press Space to Solve", True, used.text)
    win.blit(t, (10, 460))
    py.display.update()



if __name__ == "__main__":

    # Sudoku grid to be solved initalized as 2-D array
    gn = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0], 
    [6, 0, 0, 1, 9, 5, 0, 0, 0], 
    [0, 9, 8, 0, 0, 0, 0, 6, 0], 
    [8, 0, 0, 0, 6, 0, 0, 0, 3], 
    [4, 0, 0, 8, 0, 3, 0, 0, 1], 
    [7, 0, 0, 0, 2, 0, 0, 0, 6], 
    [0, 6, 0, 0, 0, 0, 2, 8, 0], 
    [0, 0, 0, 4, 1, 9, 0, 0, 5], 
    [0, 0, 0, 0, 8, 0, 0, 7, 9]]
    
    grid = [[gn[x][y] for x in range(9)]for y in range(9)]

    stage = 1
    run = True
    while run:
        mouse = py.mouse.get_pos()
        for event in py.event.get():
            if event.type == py.QUIT:
                run = False
                py.quit()   
                sys.exit()
            # Theme switch
            if event.type == py.MOUSEBUTTONDOWN:
                if 400<=mouse[0]<=450 and 450<=mouse[1]<500:
                    if used==light:
                        used=dark
                    else:
                        used=light

                    print("changed")
        keys = py.key.get_pressed()
        draw()
        # Press SPACE to solve
        if keys[py.K_SPACE]:
            stage = 2
            solve(grid)
            stage = 3
