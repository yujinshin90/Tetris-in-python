from random import randrange as rand
import pygame, sys

# set up the board layout
cell_size = 18
cols = 10
rows = 22
maxfps = 30

# define each of the tetris shape objects
tetris_pieces = [
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

colors = [
    (0,   0,   0  ),
    (255, 85,  85),
    (100, 200, 115),
    (120, 108, 245),
    (255, 140, 50 ),
    (50,  120, 52 ),
    (146, 202, 73 ),
    (150, 161, 218 ),
    (35,  35,  35)
]


# method to reset board: clears everything but the top row
def new_board():
    board = [[0 for x in xrange(cols)]
             for y in xrange(rows)]
    board += [[1 for x in xrange(cols)]]
    return board


# define helper methods used in moving the pieces
def rotate_clock(piece):
    return [[piece[y][x]
             for y in xrange(len(piece))]
            for x in xrange(len(piece[0]) - 1, -1, -1)]


# checks for collision and returns true if parts overlap, else false
def is_collision(board, piece, offset):
    offx, offy = offset
    for y, row in enumerate(piece):
        for x, cell in enumerate(row):
            try:
                if cell and board[y + offy][x + offx]:
                    return True
            except IndexError:
                return True
    return False


# clears row and returns an updated board
def clear_row(board, row):
    del board[row]
    return [[0 for i in xrange(cols)]] + board


# joins/ adds two boards together with the option of adding an offset
def join_board(b1, b2, offset):
    off_x, off_y = offset
    for y, row in enumerate(b2):
        for x, val in enumerate(row):
            b1[y + off_y - 1][x + off_x] += val
    return b1


class Tetris_App(object):
    def __init__(self):
        pygame.init()
        pygame.key.set_repeat(250, 25)
        self.disp_width = cell_size * (cols + 6)
        self.height = cell_size * rows
        self.board_width = cell_size * cols
        self.bground = [[8 if x % 2 == y % 2 else 0 for x in xrange(cols)] for y in xrange(rows)]

        # pygame related GUI stuff for board and game settings
        self.default_font = pygame.font.Font(pygame.font.get_default_font(), 12)
        self.screen = pygame.display.set_mode((self.disp_width, self.disp_height))
        pygame.event.set_blocked(pygame.MOUSEMOTION)

        self.next_piece = tetris_pieces[rand(len(tetris_pieces))]
        self.init_game()

    def disp_msg(self, msg, topleft):
        x, y = topleft
        for line in msg.splitlines():
            self.screen.blit(
                self.default_font.render(
                    line, False, (255, 255, 255), (0, 0, 0)),
                (x, y))
            y += 14

    def center_msg(self, msg):
        for i, line in enumerate(msg.splitlines()):
            msg_image = self.default_font.render(line, False, (255, 255, 255), (0, 0, 0))
            cx, cy = msg_image.get_size()
            cx //= 2  # floor division
            cy //= 2
            self.screen.blit(msg_image, (self.disp_width // 2 - cx, self.height // 2 - cy + 1 * 22))

    def new_piece(self):
        self.piece = self.next_piece[:]
        self.next_piece = tetris_pieces[rand(len(tetris_pieces))]
        self.piece_x = int(cols / 2 - len(self.piece[0]) / 2)
        self.piece_y = 0
        if is_collision(self.board, self.piece, (self.piece_x, self.piece_y)):
            self.gameover = True

    def init_game(self):
        self.board = new_board()
        self.new_piece()
        self.level = 1
        self.score = 0
        self.lines = 0
        pygame.time.set_timer(pygame.USEREVENT + 1, 1000)

    def draw_matrix(self, matrix, offset):
        off_x, off_y = offset
        for y, row in enumerate(matrix):
            for x, val in enumerate(row):
                if val:
                    pygame.draw.rect(
                        self.screen, colors[val].pygame.Rect(
                            (off_x + x) * cell_size,
                            (off_y + y) * cell_size.
                            cell_size,
                            cell_size), 0)

    def add_score(self, n):
        linescores = [0, 40, 100, 300, 1200]
        self.lines += n
        self.score += linescores[n] * self.level
        if self.lines >= self.level * 6:
            self.level += 1
            newdelay = 1000 - 50 * (self.level - 1)
            newdelay = 100 if newdelay < 100 else newdelay
            pygame.time.set_timer(pygame.USEREVENT + 1, newdelay)

    def move(self, off_x):
        if not self.gameover and not self.paused:
            new_x = self.piece_x + off_x
            if new_x < 0:
                new_x = 0
            if new_x > cols - len(self.stone[0]):
                new_x = cols - len(self.stone[0])
            if not is_collision(self.board, self.piece, (new_x, self.piece_y)):
                self.piece_x = new_x

    def drop(self, manual):
        if not self.gameover and not self.paused:
            self.score += 1 if manual else 0
            self.piece_y += 1
            if is_collision(self.board, self.piece, (self.piece_x, self.piece_y)):
                self.board = join_board(
                    self.board,
                    self.piece,
                    (self.piece_x, self.piece_y))
            self.new_piece()
            cleared_rows = 0
            while True:
                for i, row in enumerate(self.board[: -1]):
                    if 0 not in row:
                        self.board = clear_row(self.board, 1)
                        cleared_rows += 1
                        break
                    else:
                        break
            self.add_score(cleared_rows)
            return True
        return False

    def quick_drop(self):
        if not self.gameover and not self.paused:
            while not self.drop(True):
                pass

    def rotate(self):
        if not self.gameover and not self.paused:
            new_piece = rotate_clock(self.piece)
            if not is_collision(self.board, self.piece, (self.piece_x, self.piece_y)):
                self.piece = new_piece

    def pause(self):
        self.paused = not self.paused

    def start(self):
            if self.gameover:
                self.init_game()
                self.gameover = False

    def quit(self):
        self.center_msg("Good bye :(")
        pygame.display.update()
        sys.exit()

    def run(self):
        key_actions = {
            'ESCAPE':
                self.quit,
            'LEFT':
                lambda:self.move(-1),
            'RIGHT':
                lambda:self.move(+1),
            'DOWN':
                lambda:self.drop(True),
            'UP':
                self.rotate,
            'p':
                self.pause,
            'SPACE':
                self.start,
            'RETURN':
                self.quick_drop
        }
        self.gameover = False
        self.paused = False
        cpu = pygame.time.Clock()
        while 1:
            self.screen.fill((0,0,0))
            if self.gameover:
                self.center_msg("Game Over!\n Your score: %d\n\n Press space to continue" % self.score)
            else:
                if self.paused:
                    self.center_msg("Paused")
                else:
                    pygame.draw.line(self.screen,
                                     (255, 255, 255),
                                     (self.board_width+1, 0),
                                     (self.board_width+1, self.height-1))
                    self.disp_msg("Next: ", (self.board_width+cell_size, 2))

                    self.disp_msg("Score: %d\n\nLevel: %d\nLines: %d" %(self.score, self.level, self.lines),
                        (self.board_width+cell_size, cell_size*5))
                    self.draw_matrix(self.bground_grid, (0,0))
                    self.draw_matrix(self.board, (0,0))
                    self.draw_matrix(self.piece, (self.piece_x, self.piece_y))
                    self.draw_matrix(self.piece, (self.piece_x, self.piece_y))
                    self.draw_matrix(self.next_piece, (cols+1, 2))
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.USEREVENT+1:
                    self.drop(False)
                elif event.type == pygame.QUIT:
                    self.quit()
                elif event.type == pygame.KEYDOWN:
                    for key in key_actions:
                        if event.key == eval("pygame.K_" + key):
                            key_actions[key]()

            cpu.tick(maxfps)

if __name__ == "__main__":
    App = Tetris_App()
    App.run()
