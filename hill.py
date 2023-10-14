import random
from board import Board # import board file
import time

def printboard(b,size):
  for row in range(size):
    s = ""
    for col in range(size):
      if b.map[row][col] == 1:
        s += "1 "
      else:
        s += "- "
    print(s + "\n")

def randomstate(b, r, q, size):
  row = r
  column = q

  # while the generated queen is the same as the current state. generate a new queen
  while row == r and column == q:
    row = random.randint(0, size-1) # generate random row
    for i in range(0, size-1):
      if b.map[row][i] == 1:
        column = i
        break

  return row, column # return the row and column that the randomized queen is in

# Checks each row for attacking pairs
# n(n-1)/2 -> n being the number of queens and equation should give number of pairs 
def checkrows(b):
  h = 0
  nq = 0 # number of queens
  # count number of pairs in each row
  for i in b.map:
    nq = i.count(1) # count number of ones
    pairs = (nq * (nq - 1)) / 2
    h += pairs
  return h

# Hill-climbing algorithm
def hillclimb(b, qrow, qcol):
  tempboard = b # editable board to check
  h = tempboard.get_fitness() # original heursitc of board
  temph = 12070628

  bsize = 0 # board size
  for i in b.map:
    bsize += 1
  bsize -= 1 # account for index values
  
  # check for top left neighbor
  # first column or first row indexes should not have a left neighbor
  if qcol != 0 and qrow != 0:
    # if neighbor is already a queen, no need to change anything
    if tempboard.map[qrow-1][qcol-1] != 1:
      # Swap placement
      tempboard.flip(qrow, qcol)
      tempboard.flip(qrow-1, qcol-1)
      
      # calculate pairs per diagonal / column
      temph = tempboard.get_fitness() 
      # calculate pairs per row
      temph += checkrows(tempboard)

      # if less attacking queens, update the board
      if temph < h: 
        b = tempboard
        h = temph
      else:
        # Swap the values back
        tempboard.flip(qrow, qcol)
        tempboard.flip(qrow-1, qcol-1)

  # check for top neighbor
  # first row should not have top neighbor
  if qrow !=  0:
    if tempboard.map[qrow-1][qcol] != 1:
      tempboard.flip(qrow, qcol)
      tempboard.flip(qrow-1, qcol)
      temph = tempboard.get_fitness()
      temph += checkrows(tempboard)
      if temph < h:
        b = tempboard
        h = temph
      else:
        tempboard.flip(qrow, qcol)
        tempboard.flip(qrow-1, qcol)

  # check for top right neighbor
  # first row and last column should not have top right neighbor
  if qrow !=  0 and qcol != bsize:
    if tempboard.map[qrow-1][qcol+1] != 1:
      tempboard.flip(qrow, qcol)
      tempboard.flip(qrow-1, qcol+1)
      temph = tempboard.get_fitness()
      temph += checkrows(tempboard)
      if temph < h:
        b = tempboard
        h = temph
      else:
        tempboard.flip(qrow, qcol)
        tempboard.flip(qrow-1, qcol+1)
  # check for left neighbor
  # first column should not have left neighbor
  if qcol !=  0:
    if tempboard.map[qrow][qcol-1] != 1:
      tempboard.flip(qrow, qcol)
      tempboard.flip(qrow, qcol-1)
      temph = tempboard.get_fitness()
      temph += checkrows(tempboard)
      if temph < h:
        b = tempboard
        h = temph
      else:
        tempboard.flip(qrow, qcol)
        tempboard.flip(qrow, qcol-1)

  # check for right neighbor
  # first column should not have left neighbor
  if qcol !=  bsize:
    if tempboard.map[qrow][qcol+1] != 1:
      tempboard.flip(qrow, qcol)
      tempboard.flip(qrow, qcol+1)
      temph = tempboard.get_fitness()
      temph += checkrows(tempboard)
      if temph < h:
        b = tempboard
        h = temph
      else:
        tempboard.flip(qrow, qcol)
        tempboard.flip(qrow, qcol+1)
      
  # check for bottom left neighbor
  # first column should not have left neighbor
  if qcol !=  0 and qrow != bsize:
    if tempboard.map[qrow+1][qcol-1] != 1:
      tempboard.flip(qrow, qcol)
      tempboard.flip(qrow+1, qcol-1)
      temph = tempboard.get_fitness()
      temph += checkrows(tempboard)
      if temph < h:
        b = tempboard
        h = temph
      else:
        tempboard.flip(qrow, qcol)
        tempboard.flip(qrow+1, qcol-1)
        
  # check for bottom neighbor
  # first column should not have left neighbor
  if qrow != bsize:
    if tempboard.map[qrow+1][qcol] != 1:
      tempboard.flip(qrow, qcol)
      tempboard.flip(qrow+1, qcol)
      temph = tempboard.get_fitness()
      temph += checkrows(tempboard)
      if temph < h:
        b = tempboard
        h = temph
      else:
        tempboard.flip(qrow, qcol)
        tempboard.flip(qrow+1, qcol)

  # check for bottom right neighbor
  # first column should not have left neighbor
  if qcol !=  bsize and qrow != bsize:
    if tempboard.map[qrow+1][qcol+1] != 1:
      tempboard.flip(qrow, qcol)
      tempboard.flip(qrow+1, qcol+1)
      temph = tempboard.get_fitness()
      temph += checkrows(tempboard)
      if temph < h:
        b = tempboard
        h = temph
      else:
        tempboard.flip(qrow, qcol)
        tempboard.flip(qrow+1, qcol+1)
        
  return b

# get_fitness will return the number of attacking pairs, assuming 1 queen per each row
# flip inverts
def main():
  start = time.time()
  size = 5
  b = Board(size) # will generate 5x5 board / is random every time
  # print('Original Board:\n')
  # b.show_map() # display original board

  # only checks columns and diagonals 
  # dont need to check rows because board is for sure one each row
  h = b.get_fitness() 
  # print(h)

  qrow = 0
  qcol = 0
  # row and column of the current state queen
  qrow, qcol = randomstate(b, qrow, qcol, size)

  newb = b
  while h > 0:
    newb = hillclimb(newb, qrow, qcol)
    h = newb.get_fitness()
    h += checkrows(newb)
    # restart procedure
    # if h is not 0, wipe the board and generate a new one
    if h != 0:
      newb = Board(size)

  end = time.time()
  print("Running time :", round((end-start) * 10**3), "ms")
  # print('Final map')
  printboard(newb, size)
main()