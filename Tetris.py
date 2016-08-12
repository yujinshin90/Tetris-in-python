from random import randrange as rand
import pygame, sys

#set up the board layout
cell_size =	18
cols = 10
rows =	22
maxfps = 30

#define each of the tetris shape objects
tetris_shapes = [
	[[1, 1, 1],
	 [0, 1, 0]],
	
	[[0, 1, 1],
	 [1, 1, 0]],
	
	[[1, 1, 0],
	 [0, 1, 1]],
	
	[[1, 0, 0],
	 [1, 1, 1]],
	
	[[0, 0, 1],
	 [1, 1, 1]],
	
	[[1, 1, 1, 1]],
	
	[[1, 1],
	 [1, 1]]
]

#methd to reset board: clears everything but the top row
def new_board():
	board = [[0 for x in xrange(cols)]
				for y in xrange(rows)]
	board += [[0 for x in xrange(cols)]]
	return board
