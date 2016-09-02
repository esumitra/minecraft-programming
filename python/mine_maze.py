# minecraft maze generation using DFS and backtracking
import mcpi.minecraft as minecraft
import mcpi.block as block
import time
import numpy as np
import random
    
# maze to minecraft grid
def maze2grid(maze):
    (maze_i, maze_j, _) = np.shape(maze)
    # r x c cells => 2r+1 x 2c+1 grid array
    grid_maxi = 2 * maze_i + 1
    grid_maxj = 2 * maze_j + 1
    G = np.ones((grid_maxi, grid_maxj),dtype=np.uint8)
    for i in range(maze_i):
        for j in range(maze_j):
            # 1 = open, 0 = closed
            cellx = 2*i+1
            celly = 2*j+1
            cwalls = maze[i, j]
            G[cellx,celly] = 0
            # L
            if cwalls[0] == 0:
                G[cellx,celly-1] = 1
            else:
                G[cellx,celly-1] = 0
            # U
            if cwalls[1] == 0:
                G[cellx-1,celly] = 1
            else:
                G[cellx-1,celly] = 0
            # R
            if cwalls[2] == 0:
                G[cellx,celly+1] = 1
            else:
                G[cellx,celly+1] = 0
            # D
            if cwalls[3] == 0:
                G[cellx+1,celly] = 1
            else:
                G[cellx+1,celly] = 0
    return G

# maze generation
# modified from https://en.wikipedia.org/wiki/Maze_generation_algorithm#Python_code_example
def generate_maze(nr,nc):
    num_rows = nr
    num_cols = nc
    M = np.zeros((num_rows,num_cols,5), dtype=np.uint8)
    r = 0
    c = 0
    history = [(r,c)] 
    random.seed()
    while history: 
        M[r,c,4] = 1 # designate this location as visited
        # check if the adjacent cells are valid for moving to
        check = []
        if c > 0 and M[r,c-1,4] == 0:
            check.append('L')  
        if r > 0 and M[r-1,c,4] == 0:
            check.append('U')
        if c < num_cols-1 and M[r,c+1,4] == 0:
            check.append('R')
        if r < num_rows-1 and M[r+1,c,4] == 0:
            check.append('D')
            
        if len(check): # If there is a valid cell to move to.
            # Mark the walls between cells as open if we move
            history.append([r,c])
            move_direction = random.choice(check)
            if move_direction == 'L':
                M[r,c,0] = 1
                c = c-1
                M[r,c,2] = 1
            if move_direction == 'U':
                M[r,c,1] = 1
                r = r-1
                M[r,c,3] = 1
            if move_direction == 'R':
                M[r,c,2] = 1
                c = c+1
                M[r,c,0] = 1
            if move_direction == 'D':
                M[r,c,3] = 1
                r = r+1
                M[r,c,1] = 1
        else: # If there are no valid cells to move to.
            # retrace one step back in history if no move is possible
            r,c = history.pop()
         
    # Open the walls at the start and finish
    M[0,0,0] = 1
    M[num_rows-1,num_cols-1,2] = 1
    return M

# test mine-maze
def mine_maze_test():
    g = maze2grid(generate_maze(3,3))
    for r in g:
        print(r)

# maze grid builder
def build_maze_grid(mc,my_pos,maze):
    GAP = block.AIR.id
    WALL = block.GOLD_BLOCK.id
    FLOOR = block.GRASS.id
    origin_x = my_pos.x+1
    origin_y = my_pos.y
    origin_z = my_pos.z+1
    x = origin_x + 2
    z = origin_z + 2
    for row in maze:
        for cell in row:
            if cell == 0:
                b = GAP
            else:
                b = WALL
            mc.setBlock(x,origin_y,z,b)
            mc.setBlock(x,origin_y+1,z,b)
            mc.setBlock(x,origin_y+2,z,b)
            mc.setBlock(x,origin_y-1,z,FLOOR)
            x = x+1 
        z = z+1
        x = origin_x+2

# minecraft maze builder
def mine_maze(num_rows=5, num_cols=5):
    mc = minecraft.Minecraft.create()
    pos = mc.player.getTilePos()
    mc.postToChat("building maze in 5 seconds ...")
    time.sleep(4)
    mc.postToChat("building maze in 1 second ...")
    time.sleep(1)
    g = maze2grid(generate_maze(num_rows, num_cols))
    build_maze_grid(mc,pos, g)
    mc.postToChat("Maze built!")

# uncomment line below when ready to build!
# mine_maze()
