# file with some setting of the game 

# settings for main window
width, height = 10, 20

# settings for cell object
stylesheet_for_cell = 'QPushButton {\nbackground-color: _____;\nborder: none;' +\
            '\nborder: none;\n}' +\
            'QPushButton:hover {\nbackground-color: _____;\n}\n' +\
            'QPushButton:disabled {\nbackground-color: _____;\n}'

cell_size = 44

# this is the coordinates of the spawn point
start_point = (2, 4)

# this is the formula which return number of the points,
# which depends on the number of filled rows in the grid
riser = lambda x: 17 + int(127 * x / 100) + 3 ** x

# interval in ms to call shifting shape method
# one ms equals to one second
fall_speed = lambda x: 1000 - 100 * x