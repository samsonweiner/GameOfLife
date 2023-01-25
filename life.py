from tkinter import *
from tkinter import ttk
from math import floor

#Globals
root = Tk()

#Main Grid
class GraphWindow(Canvas):
    def __init__(self, title="Game of Life", width=1000, height=900):
        super().__init__(root, width=width, height=height)
        root.title(title)

        self.start = False

        self.width = width
        self.height = height
        self.grid = self.setup_board()

        self.pack()
        self.bind("<Button-1>", self.toggle_cell_event)

    def setup_board(self):
        grid = []
        for i in range(10, self.width - 10, 20):
            column = []
            for j in range(10, self.height - 110, 20):
                cell = self.create_rectangle((i, j, i+20, j+20), fill="white", tags=('dead'), outline="#D3D3D3", width=2)
                column.append(cell)
            grid.append(column)
        button1 = ttk.Button(root, text="Start", command=self.start_game)
        button2 = ttk.Button(root, text="Reset", command=self.reset_game)
        button3 = ttk.Button(root, text="Glider Gun", command=self.glider_gun)
        button1.place(x=self.width/2 - 80, y=self.height - 70)
        button2.place(x=self.width/2 + 20, y=self.height - 70)
        button3.place(x=self.width/2 + 120, y = self.height - 70)
        return grid

    def check_neighbors(self, obj):
        coords = self.coords(obj)
        x, y = floor((coords[0]-10)/20), floor((coords[1]-10)/20)
        neighbors = {'alive': 0, 'dead': 0}
        if x == 0:
            neighbors[self.gettags(self.grid[x+1][y])[0]] += 1
            if y != 0:
                neighbors[self.gettags(self.grid[x][y-1])[0]] += 1
                neighbors[self.gettags(self.grid[x+1][y-1])[0]] += 1
            if y != len(self.grid[x]) - 1:
                neighbors[self.gettags(self.grid[x][y+1])[0]] += 1
                neighbors[self.gettags(self.grid[x+1][y+1])[0]] += 1
        elif x == len(self.grid) - 1:
            neighbors[self.gettags(self.grid[x-1][y])[0]] += 1
            if y != 0:
                neighbors[self.gettags(self.grid[x][y-1])[0]] += 1
                neighbors[self.gettags(self.grid[x-1][y-1])[0]] += 1
            if y != len(self.grid[x]) - 1:
                neighbors[self.gettags(self.grid[x][y+1])[0]] += 1
                neighbors[self.gettags(self.grid[x-1][y+1])[0]] += 1
        else:
            neighbors[self.gettags(self.grid[x-1][y])[0]] += 1
            neighbors[self.gettags(self.grid[x+1][y])[0]] += 1
            if y != 0:
                neighbors[self.gettags(self.grid[x][y-1])[0]] += 1
                neighbors[self.gettags(self.grid[x-1][y-1])[0]] += 1
                neighbors[self.gettags(self.grid[x+1][y-1])[0]] += 1
            if y != len(self.grid[x]) - 1:
                neighbors[self.gettags(self.grid[x][y+1])[0]] += 1
                neighbors[self.gettags(self.grid[x-1][y+1])[0]] += 1
                neighbors[self.gettags(self.grid[x+1][y+1])[0]] += 1
        return [neighbors['alive'], neighbors['dead']]

    def toggle_cell_event(self, event):
        if self.start == False:
            x, y = self.canvasx(event.x), self.canvasy(event.y)
            if x >= 10 and x < self.width - 10 and y >= 10 and y < self.height - 110:
                cell = self.grid[floor((x-10)/20)][floor((y-10)/20)]
                self.itemconfigure(cell, fill="black")
                self.addtag('alive', 'withtag', cell)
                self.dtag(cell, 'dead')

    def toggle_cell_object(self, obj):
        if self.start == False:
            self.itemconfigure(obj, fill="black")
            self.addtag('alive', 'withtag', obj)
            self.dtag(obj, 'dead')
    
    def start_game(self):
        print('STARTING')
        self.start = True
        self.single_move()
    
    def single_move(self):
        cur_alive = self.find_withtag('alive')
        cur_dead = self.find_withtag('dead')
        if len(self.find_withtag('alive')) == 0:
            self.reset_game()
        else:
            next_alive = set()
            for cell in cur_alive:
                nbrs = self.check_neighbors(cell)
                if nbrs[0] == 2 or nbrs[0] == 3:
                    next_alive.add(cell)
            for cell in cur_dead:
                nbrs = self.check_neighbors(cell)
                if nbrs[0] == 3:
                    next_alive.add(cell)
                    #print('HERE', len(next_alive))
            self.itemconfigure('all', fill='white')
            self.addtag('dead', 'withtag', 'alive')
            self.dtag('all', 'alive')
            for cell in next_alive:
                self.addtag('alive', 'withtag', cell)
                self.dtag(cell, 'dead')
            self.itemconfigure('alive', fill="black")
            self.after(50, self.single_move)

    def reset_game(self):
        print('RESETING')
        self.start = False
        self.itemconfigure('all', fill="white")
        self.addtag('dead', 'withtag', 'alive')
        self.dtag('all', 'alive')

    def glider_gun(self):
        print('Inputting Glider Gun')
        if self.start == False:
            self.toggle_cell_object(self.grid[3][5])
            self.toggle_cell_object(self.grid[3][6])
            self.toggle_cell_object(self.grid[4][5])
            self.toggle_cell_object(self.grid[4][6])

            self.toggle_cell_object(self.grid[37][3])
            self.toggle_cell_object(self.grid[37][4])
            self.toggle_cell_object(self.grid[38][3])
            self.toggle_cell_object(self.grid[38][4])

            self.toggle_cell_object(self.grid[13][5])
            self.toggle_cell_object(self.grid[13][6])
            self.toggle_cell_object(self.grid[13][7])
            self.toggle_cell_object(self.grid[14][4])
            self.toggle_cell_object(self.grid[15][3])
            self.toggle_cell_object(self.grid[16][3])
            self.toggle_cell_object(self.grid[14][8])
            self.toggle_cell_object(self.grid[15][9])
            self.toggle_cell_object(self.grid[16][9])
            self.toggle_cell_object(self.grid[18][4])
            self.toggle_cell_object(self.grid[19][5])
            self.toggle_cell_object(self.grid[19][6])
            self.toggle_cell_object(self.grid[19][7])
            self.toggle_cell_object(self.grid[20][6])
            self.toggle_cell_object(self.grid[18][8])
            self.toggle_cell_object(self.grid[17][6])

            self.toggle_cell_object(self.grid[23][3])
            self.toggle_cell_object(self.grid[23][4])
            self.toggle_cell_object(self.grid[23][5])
            self.toggle_cell_object(self.grid[24][3])
            self.toggle_cell_object(self.grid[24][4])
            self.toggle_cell_object(self.grid[24][5])
            self.toggle_cell_object(self.grid[25][2])
            self.toggle_cell_object(self.grid[25][6])
            self.toggle_cell_object(self.grid[27][1])
            self.toggle_cell_object(self.grid[27][2])
            self.toggle_cell_object(self.grid[27][6])
            self.toggle_cell_object(self.grid[27][7])




graph = GraphWindow()
root.mainloop()


