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

#method to reset board: clears everything but the top row
def new_board():
	board = [[0 for x in xrange(cols)]
				for y in xrange(rows)]
	board += [[1 for x in xrange(cols)]]
	return board

#define helper methods used in moving the pieces
def rotate_clock(piece):
	return [ [ piece[y][x]
			for y in xrange(len(piece)) ]
		for x in xrange(len(piece[0]) - 1, -1, -1) ]

#checks for collision and returns true if parts overlap, else false
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

#clears row and returns an updated board
def clear_row(board, row):
	del board[row]
	return[[0 for i in xrange(cols)]] + board

#joins/ adds two boards together with the option of adding an offset
def join_board(b1, b2, offset):
	off_x, off_y = offset
	for y, row in enumerate(b2):
		for x, val in enumerate(row):
			b1[y+off_y-1][x+off_x] += val
	return b1

class Tetris_App(object):
	def __init__(self):
