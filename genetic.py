import random
from board import Board # import board file
import time
import numpy as np

def printboard(b,size):
  for row in range(size):
    s = ""
    for col in range(size):
      if b.map[row][col] == 1:
        s += "1 "
      else:
        s += "- "
    print(s + "\n")
# create board so there's a queen per column
def genb(size):
  b = Board(size)
  # generate a board that has all 0s
  for row in range(size):
    for col in range(size):
      b.map[row][col] = 0

  #r = random.randint(0, size-1) # random row index
  # generating random 1s so that there is 1 queen per column
  for i in range(size):
    r = random.randint(0, size-1) # random row index
    b.map[r][i] = 1
    
  return b

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

# convert board to state 
def getstates(b, size):
  state = ''
  row = 0 # row position tracker
  col = 0 # column position tracker
  position = size # ex) highest grid level should be 5 in this case 

  # while column doesn't reach the end 
  while col != size:
    # if round a queen, go onto next column and update state
    if b.map[row][col] == 1:
      state += str(position)
      col += 1 
      row = 0 #reset row
      position = size # reset position
    else:
      position -= 1
      row += 1
      
  return state

# convert state to board
def getboards(state, size):
  b = Board(size)
  # generate a board that has all 0s
  for row in range(size):
    for col in range(size):
      b.map[row][col] = 0

  col2 = 0 # column position tracker
  # ex. 15431
  # 1 would be index 4, 2 would be index 3 and so on
  for i in range(size):
    if state[i] == "1":
      b.map[4][col2] = 1
    elif state[i] == "2":
      b.map[3][col2] = 1
    elif state[i] == "3":
      b.map[2][col2] = 1
    elif state[i] == "4":
      b.map[1][col2] = 1
    elif state[i] == "5":
      b.map[0][col2] = 1
    col2 += 1
  
  return b

# find number of attacking pairs
def geth(state, size):
  b = getboards(state, size)
  h = 0 # number of attacking pairs 
  h += b.get_fitness() + checkrows(b)
  return h
  
# find probabity of states
def getprob(states, size):
  total = 0
  prob = [] # list of probability
  hs = [] # list of h values
  for i in states:
    hvalue = 10 - geth(i, size) # subtract from 10 since there are 10 possible pairs 
    total += hvalue
    hs.append(hvalue)

  for i in hs:
    p = i/total
    prob.append(p)
    
  return prob

# returns cross-over states 
def crossover(states):
  nstates = [] # new list of states after cross-over
  for i in range(1,5):
    # every even number, the cross-over point is after the 2nd index
    if i % 2 != 0:
      s1 = states[(i*2) - 2]
      s2 = states[(i*2) - 1]
      p1 = s1[:1] + s2[2:]
      p2 = s2[:1] + s1[2:]
      nstates.append(p1)
      nstates.append(p2)
    # every odd number, the cross-over point is after the 3rd index
    else:
      s3 = states[(i*2) - 2]
      s4 = states[(i*2) - 1]
      p3 = s3[:2] + s4[3:]
      p4 = s4[:2] + s3[3:]
      nstates.append(p3)
      nstates.append(p4)
    
  return nstates
  
def main():
  start = time.time()
  size = 5
  solution = 'no solution'

  # Genetic Algo for 8 States 
  # generate board with 1 queen a column
  b1 = genb(size)
  b2 = genb(size)
  b3 = genb(size)
  b4 = genb(size)
  b5 = genb(size)
  b6 = genb(size)
  b7 = genb(size)
  b8 = genb(size)

  states = [] # list os all states
  
  state1 = getstates(b1, size)
  state2 = getstates(b2, size)
  state3 = getstates(b3, size)
  state4 = getstates(b4, size)
  state5 = getstates(b5, size)
  state6 = getstates(b6, size)
  state7 = getstates(b7, size)
  state8 = getstates(b8, size)
  states.append(state1)
  states.append(state2)
  states.append(state3)
  states.append(state4)
  states.append(state5)
  states.append(state6)
  states.append(state7)
  states.append(state8)

  # # test 
  # for i in states:
  #   print(i)

  while solution == "no solution":
    nstates = [] # list of states for us to edit
    prob = getprob(states, size) # list of probabilties 
  
    # Selection
    # nstates index 0-1 are a pair, 2-3 are a pair etc depending on the board
    for i in range(8):
      r = np.random.random(1)[0] # gets random decimal between 0 and 1
      if (0 <= r) and (r <= prob[0]):
        nstates.append(states[0])
      elif r <= (prob[0] + prob[1]):
        nstates.append(states[1])
      elif r <= (prob[0] + prob[1] + prob[2]):
        nstates.append(states[2])
      elif r <= (prob[0] + prob[1] + prob[2] + prob [3]):
        nstates.append(states[3])
      elif r <= (prob[0] + prob[1] + prob[2] + prob [3] + prob [4]):
        nstates.append(states[4])
      elif r <= (prob[0] + prob[1] + prob[2] + prob [3] + prob [4] + prob[5]):
        nstates.append(states[5])
      elif r <= (prob[0] + prob[1] + prob[2] + prob [3] + prob [4] + prob[5] + prob[6]):
        nstates.append(states[6])
      else:
        nstates.append(states[7])
    
    # Cross-over
    cross = []
    cross = crossover(nstates)
  
    # Mutation
    count = 0 # index of the state
    for i in cross:
      index = random.randint(0,4) # random column
      qindex = random.randint(1,5) # random location of the queen within column
      mutated = i[:index - 1] + str(qindex) + i[index - 1:]
      states[count] = mutated
      count +=1
  
    # Check fitness again
    for i in states:
      h = 10 - geth(i, size)
      # Checks if the board has no attacking pairs
      if h == 10:
        solution = i
        break

  
  # print("Solution: " + solution)
  end = time.time()
  print("Running time :", round((end-start) * 10**3), "ms")
  solu = getboards(solution, size)
  printboard(solu, size)

  

    
  # print('Original Board:\n')
  # b1.show_map() # display original board

  # # only checks columns and diagonals 
  # # dont need to check rows because board is for sure one each row
  # h = b1.get_fitness() 
  # print(h)

main()