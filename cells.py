# cells
from tkinter import *
import random
import settings
import ctypes # docs: https://docs.python.org/3/library/ctypes.html
import pyautogui # docs https://pyautogui.readthedocs.io/en/latest/
import sys # docs: https://docs.python.org/3/library/sys.html


class Cell:
    all = []
    cell_count_label_obj = None  #
    cell_count = settings.CELL_COUNT

    def __init__(self, x, y, is_mine=False):
        self.is_mine = is_mine  # pay attention to is_mine;
        # this cell takes in another attr called:
        self.is_opened = False
        self.is_flagged = False #  cells flagged!
        self.cell_btn_obj = None  # None at first
        self.x = x
        self.y = y

        # here we append the obj to the Cell.all list!
        Cell.all.append(self)
        # testing it now;

    # creating instance method to assign afterwards:
    def create_btn_obj(self, location):
        btn = Button(
            location,  # location
            width=1,
            height=1,
            # todo: find a way to make these cells responsive?
            # text=f'{self.x},{self.y}'
            # TODO: improve button's styles;
        )
        # ASSIGN EVENTS TO EVERY CELL HERE:
        btn.bind('<Button-1>', self.left_click_actions)
        btn.bind('<Button-2>', self.right_click_actions)
        # todo: bind(key, function)
        # Button-1 = left click; Button-2 = right click!
        self.cell_btn_obj = btn

    @staticmethod  # this is a one time method; a static one
    # thus, the marking; also, it does not need self
    def create_cell_count_label(location):

        # using label because it's tkinter class' name!
        lbl = Label(
            location,
            bg='black',
            fg='white',
            padx=10,
            text=f"Cells left: {Cell.cell_count}",
            font=('Helvetica', 20, 'bold')
        )
        Cell.cell_count_label_obj = lbl
        # same as self.cell_btn_obj = btn

    def left_click_actions(self, event):
        # for events in tkinter assign too event to prevent errors
        # print(event) # bg info to use it for other purposes than here
        if self.is_mine:
            # highlight mine, you're dead
            self.show_mine()
        else:
            # todo: study this;
            # this clears empty spaces around cells!
            if self.surrounded_cells_mines_length == 0:
                for cell_obj in self.surrounded_cells:
                    cell_obj.show_cell()
            self.show_cell()
            # if cell_count is equal to cells left count, player wins:
            if Cell.cell_count == settings.MINES_PRACTICE:
                pyautogui.alert('Game is over', "You win!")

        # cancels any other action if cell.is_open
        self.cell_btn_obj.unbind('<Button-1>')
        # unbinding events
        self.cell_btn_obj.unbind('<Button-2>')

    def get_cell_by_axis(self, x, y):
        # returns a cell obj based on x, y values
        for cell in Cell.all:
            if cell.x == x and cell.y == y:
                return cell
                # we need to see what is happening in all
                # cells around any cell!

    @property  # todo: study this;
    def surrounded_cells(self):
        # print(self.get_cell_by_axis(0, 0))
        # showing coordinates for x, y
        # if we click 1,1,
        # we get 0,0, 0,1, 0,2,
        # 1,0, 1,2,
        # 2,0, 2,1, 2,2
        cells = [
            self.get_cell_by_axis(self.x - 1, self.y - 1),  # 0,0
            self.get_cell_by_axis(self.x - 1, self.y),  # 0,1
            self.get_cell_by_axis(self.x - 1, self.y + 1),  # 0,2
            self.get_cell_by_axis(self.x, self.y - 1),  # 1,0
            self.get_cell_by_axis(self.x + 1, self.y - 1),  # 2,0
            self.get_cell_by_axis(self.x + 1, self.y),  # 2,1
            self.get_cell_by_axis(self.x + 1, self.y + 1),  # 2,2
            self.get_cell_by_axis(self.x, self.y + 1)  # 1,2
        ]
        # print(surrounded_cells)
        # clicking on any cell placed right to any size, returns None on those negative values!
        # todo: delete all nones when clicking cells!
        # this is done through list comprehension!
        cells = [cell for cell in cells if cell is not None]
        return cells

    @property  # todo: study this
    def surrounded_cells_mines_length(self):
        # counts mines in surrounded_cells
        counter = 0
        for cell in self.surrounded_cells:
            if cell.is_mine:
                counter += 1
        return counter

    def show_cell(self):
        if not self.is_opened:
            # updating cell_count:
            Cell.cell_count -= 1
            # print(self.surrounded_cells_mines_length)
            # change text to mine_counting
            self.cell_btn_obj.configure(text=self.surrounded_cells_mines_length)
            # replace cell count text with updated count
            if Cell.cell_count_label_obj:
                Cell.cell_count_label_obj.config(text=f'Cells left: {Cell.cell_count}')

        # marks cell as open!
        self.is_opened = True

    def show_mine(self):
        self.cell_btn_obj.configure(text='💣')
        # todo: alternatives to ctypes, which is windows only? trying pyautogui
        # ctypes.windll.user32.MessageBox(0, 'You clicked a mine!', 'Game over', 0)
        pyautogui.alert('Game is over', "You clicked a bomb!")
        sys.exit
        # game is over
        # self.cell_btn_obj.configure(bg='red')
        #
        # # using ctypes instead
        # # Cell.cell_count_label_obj.config(text=f'Boom! Game over...')
        # # todo: bg does NOT change :/
        # print('mine here!!')

    def right_click_actions(self, event):
        # print(event)
        if not self.is_flagged:
            self.cell_btn_obj.configure(text='🚩 ', bg='yellow')
        # todo: bg, fg is not working here!!!
            self.is_flagged = True
        else:
            self.cell_btn_obj.configure(text='')
            self.is_flagged = False

    # todo: this is a static method;
    @staticmethod
    def randomize_mines():
        # turns some cells and turns them into mines;
        # on easy/practice mode; only 10 mines!!!
        # my_list = ['Al', 'Bea', 'Cal']
        # names = random.sample(my_list, 2)
        # # access that list and takes 2 names
        # print(names)
        # the logic here is:
        picked_cells = random.sample(
            Cell.all,  # passing all instances;
            settings.MINES_PRACTICE
            # because easy/practice difficulty!
            # TODO: change this to expert when width/height are fixed;
        )
        # print(picked_cells)
        # this is where the mines are
        for picked_cells in picked_cells:
            picked_cells.is_mine = True

    def __repr__(self):
        # represents class obj as string
        # todo: read https://www.educative.io/edpresso/what-is-the-repr-method-in-python
        return f'Cell({self.x}, {self.y})'
