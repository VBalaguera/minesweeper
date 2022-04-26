# this is a simple minesweeper project for fun,
# exploring oop paradigms,
# general module implementation and usage,
# and other miscellaneous and useful resources


# title = 'minesweeper game'
# cells_left = int
# mines_count = int

from tkinter import *
import settings
import utils
from cells import Cell

# initializing tkinter
root = Tk()  # root uses a naming convention more useful for tkinter
root.configure(bg='black')

# override window settings;

root.geometry(f'{settings.WIDTH}x{settings.HEIGHT}')  # this method alters the window's size
# all windows are resizable, what to do then?
root.resizable(False, False)  # not allow to resize; one for weight and height respectively
root.title('minesweeper')  # window's title;

# creating elements:
# frame: a container for elements we will create in the future:
# it will contain other frames:
top_frame = Frame(
    root,
    bg='black',  # just to differentiate it
    width=settings.WIDTH,  # same as window's
    height=utils.height_prct(25) # 25% of HEIGHT
)

# where to start this frame:
top_frame.place(x=0, y=0)  # accepts px values for x and y

# left-side frame:
left_frame = Frame(
    root,
    bg='black',
    width=utils.weight_prct(25),  # 1/4 of total width
    height=utils.height_prct(75)  # we already covered 180px on a 720px, so
)
left_frame.place(x=0, y=utils.height_prct(25))


center_frame = Frame(
    root,
    bg='black',
    width=utils.weight_prct(75),
    height=utils.height_prct(75)
)
center_frame.place(
    x=utils.weight_prct(25),
    y=utils.height_prct(25)
)


# cells:
# c1 = Cell()
# c1.create_btn_obj(center_frame)
# c1.cell_btn_obj.grid(
#     column=0, row=0
# )
#
# c2 = Cell()
# c2.create_btn_obj(center_frame)
# c2.cell_btn_obj.grid(
#     # dynamically, how many px should this cell be positioned from any other cell?
#     column=0, row=1
# )

# TODO: change these quantities to 30x16;
#  that will require fixing the canvas width/height
for x in range(settings.COLUMNS_PRACTICE):  # columns
    for y in range(settings.ROWS_PRACTICE):  # rows
        c = Cell(x, y) # mandatory args
        c.create_btn_obj(center_frame)
        c.cell_btn_obj.grid(column=x, row=y)

# print(Cell.all)

# calling label from Cell class:
Cell.create_cell_count_label(left_frame)
Cell.cell_count_label_obj.place(x=0, y=0)
Cell.randomize_mines() # TODO: pay attention to this;

for c in Cell.all:
    if c.is_mine == True:
        print(c)

# run window
root.mainloop()  # opens a window, closable by clicking x

