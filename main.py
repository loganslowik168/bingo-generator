import glob
import time
import sys
import random
import os
import math
import table #table.py


def PromptForNumber(prompt, optional=False, default=0):
    while True:
        number=False
        user_input = input(prompt)
        if optional and len(user_input) == 0:
            return default
        try:
            number = int(user_input)  # Convert input to a float
            if number < 0:
                raise ValueError
            return number # Return the valid number
        except ValueError:
            print("Invalid input. Please enter a valid non-negative number.")
def PromptForYesNo(prompt, optional=False, default=0):
    while True:
        YES = ['y', 'yes', 'y\\', 'yes\\']
        NO = ['n', 'no', 'n\\', 'no\\']
        user_input = input(prompt)
        inp=user_input.lower()
        if inp in YES:
            return True
        elif inp in NO:
            return False
        else:
            print('Please enter y or n.')
def GenerateFilename(base, extension):
    i=1
    while os.path.exists(base+str(i)+extension):
        i+=1
    return base+str(i)+extension
def ClearOutputFiles(verbose=False):
    folder_path = 'output_cards/'
    files_to_delete = glob.glob(os.path.join(folder_path, 'card*.png'))

    for file in files_to_delete:
        os.remove(file)
        if verbose:
            print(f"Deleted: {file}")


#--------------
# Ensure the correct number of arguments are provided
if len(sys.argv) != 2:
    print("Usage: python script.py <file.txt>\nfile.txt should have one entry per line. Empty lines will be ignored")
    sys.exit(1)

file_path = sys.argv[1]
with open(file_path, 'r') as file:
    TILES = [line.strip() for line in file.readlines()]
# Gather user inputs
SQUARE_SIZE = PromptForNumber('Enter the dimension of the cards (3=>3x3, etc.): ')
NUMBER_OF_CARDS_TO_GENERATE = PromptForNumber('Enter the number of cards to generate: ')
SHOULD_FREE_SPACE = False
if SQUARE_SIZE % 2 != 0: #if there's an odd number of spaces ==> a center cell exists
    SHOULD_FREE_SPACE = PromptForYesNo('Should there be a FREE space generated in the middle of the board?: ')
CELL_SIZE = PromptForNumber('Enter Cell Size (optional, default=100): ', True, 100)
FONT_SIZE = PromptForNumber('Enter Font Size (optional, default=20): ', True, 20)

START_TIME = time.time()
#print('Deleting previous Bingo cards...')
ClearOutputFiles()
#print('Previous Bingo cards deleted.  Beginning generation of new cards')
NEEDED_TILES = SQUARE_SIZE * SQUARE_SIZE
for cardNum in range(1,NUMBER_OF_CARDS_TO_GENERATE+1):
    # Expand and shuffle the TILES to ensure all values are used before recycling
    tile_pool = []
    while len(tile_pool) < NEEDED_TILES:
        random.shuffle(TILES)  # Shuffle the TILES list
        tile_pool.extend(TILES)  # Append the shuffled TILES to the pool

    # Ensure we only take the exact amount of tiles needed
    tile_pool = tile_pool[:NEEDED_TILES]

    # Generate the grid by filling it with the tile_pool
    grid = []
    for i in range(SQUARE_SIZE):
        row = tile_pool[i * SQUARE_SIZE:(i + 1) * SQUARE_SIZE]
        grid.append(row)

    # create free space if desired
    if SHOULD_FREE_SPACE:
        CENTER = int(math.ceil(SQUARE_SIZE/2)-1)
        grid[CENTER][CENTER] = "FREE SPACE"
    table.create_table_image(grid, CELL_SIZE,FONT_SIZE,GenerateFilename('output_cards/card','.png'))

END_TIME = time.time()
print(NUMBER_OF_CARDS_TO_GENERATE, 'cards were generated in', END_TIME-START_TIME, 'seconds.')