from random import randrange as rand
import pygame, sys

#set up the board layout
cell_size =	18
cols = 10
rows =	22
maxfps = 30

#define each of the tetris shape objects
tetris_piece = [
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

#define helper methods used in moving the pieces
def rotate_clock(piece):
	return [ [ piece[y][x]
			for y in xrange(len(piece)) ]
		for x in xrange(len(piece[0]) - 1, -1, -1) ]

def is_collsion(board, piece, offset):
	offx, offy = offset
	for y, row in enumerate(piece):
		for x, cell in enumerate(row):
			try:
				if cell and board[ y + offy ][ x + offx ]:
					return True
			except IndexError:
				return True
	return False