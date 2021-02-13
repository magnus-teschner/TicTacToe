import pygame
import sys
import numpy
import time

pygame.init()
width = 600
height = 600
red = (255,0,0)
white = (0,0,0)
bg_color = (28,170,156)
line_color = (23, 145, 145)
line_width = 15
board_rows = 3
board_cols = 3
circle_rad = 60
circle_width = 15
circle_color = (239, 231, 200)
cross_width = 25
space = 55
cross_color = (66, 66, 66)



screen = pygame.display.set_mode((width, height))
screen.fill(bg_color)
pygame.display.set_caption("TIC TAC TOE")
board = numpy.zeros((board_rows, board_cols))

class Score:
	def __init__(self, screen, points, posX, posY):
		self.screen = screen
		self.points = points
		self.posX = posX
		self.posY = posY
		self.font = pygame.font.SysFont("monospace", 80, bold = True)
		self.label = self.font.render(self.points, 0, white)

	def show(self):
		self.screen.blit(self.label, (self.posX - self.label.get_rect().width // 2, self.posY))
	def increase(self):
		points = int(self.points) + 1
		self.points = str(points)
		self.label = self.font.render(self.points, 0, white)
	def restart(self):
		self.points = "0"
		self.label = self.font.render(self.points, 0, white)


score1 = Score(screen, "0", 175, -2)
score2 = Score(screen, "0",435 , -2)

def draw_lines():
	#1 Horizontale:
	# wo, farbe, startpunkt, endpunkt, dicke

	pygame.draw.line(screen, line_color, (0, 200), (600, 200), line_width)
	#2 Horizontale:
	pygame.draw.line(screen, line_color, (0, 400), (600, 400), line_width)
	#1 Vertikale:
	pygame.draw.line(screen, line_color, (200, 0), (200, 600), line_width)
	#2 Vertikale:
	pygame.draw.line(screen, line_color, (400, 0), (400, 600), line_width)

def draw_figures():
	for row in range(board_rows):
		for col in range(board_cols):
			if board[row][col] == 1:
				pygame.draw.circle(screen, circle_color, (int(col * 200 + 100), int(row * 200 + 100)),circle_rad, circle_width)
			elif board[row][col] == 2:
				pygame.draw.line(screen, cross_color, (col * 200 + space, row *200 + 200 - space), (col * 200 + 200 - space, row * 200 +space), cross_width)
				pygame.draw.line(screen, cross_color, (col * 200 + space, row * 200 + space),(col * 200 + 200 - space, row * 200 + 200 - space), cross_width)

def mark_square(row, col, player):
	board[row][col] = player

def avaible_square(row, col):
	return board[row][col] == 0

def is_board_full():
	for row in range(board_rows):
		for col in range(board_cols):
			if board[row][col] == 0:
				return False
	return True
def check_win(player):
	#vertical
	for col in range(board_cols):
		if board[0][col] == player and board[1][col] == player and board[2][col] == player:
			draw_vertical_winning_line(col, player)
			return True
	#horizontal
	for row in range(board_rows):
		if board[row][0] == player and board[row][1] == player and board[row][2] == player:
			draw_horizontal_winning_line(row, player)
			return True
	# ascending diagonal
	if board[2][0] == player and board[1][1] == player and board[0][2] == player:
		draw_asc_diagonal(player)
		return True
	#descending diagonal
	if board[0][0] == player and board[1][1] == player and board[2][2] == player:
		draw_desc_diagonal(player)
		return True
	return False

def draw_vertical_winning_line(col, player):
	pos_x = col * 200 + 100
	if player == 1:
		color = circle_color
	if player == 2:
		color = cross_color
	pygame.draw.line(screen, color, (pos_x, 15),(pos_x, height -15), 15)


def draw_horizontal_winning_line(row, player):
	pos_y = row * 200 + 100
	if player == 1:
		color = circle_color
	if player == 2:
		color = cross_color
	pygame.draw.line(screen, color, (15, pos_y), ( width - 15, pos_y), 15)

def draw_asc_diagonal(player):
	if player == 1:
		color = circle_color
	if player == 2:
		color = cross_color

	pygame.draw.line(screen, color, (15, height - 15), ( width - 15, 15), 15)

def draw_desc_diagonal(player):
	if player == 1:
		color = circle_color
	if player == 2:
		color = cross_color

	pygame.draw.line(screen, color, (15, 15), (width - 15, height - 15), 15)

def restart():
	screen.fill(bg_color)
	draw_lines()
	player = 1
	for row in range(board_rows):
		for col in range(board_cols):
			board[row][col] = 0




draw_lines()

player = 1
game_over = False

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
			mouse_x = event.pos[0]
			mouse_y = event.pos[1]

			clicked_row = int(mouse_y // 200)
			clicked_col = int(mouse_x // 200)

			if avaible_square(clicked_row, clicked_col):
				if player == 1:
					mark_square(clicked_row, clicked_col, 1)
					if check_win(player):
						score1.increase()
						score1.show()
						score2.show()
						game_over = True
					player = 2
				elif player == 2:
					mark_square(clicked_row, clicked_col, 2)
					if check_win(player):
						score2.increase()
						score2.show()
						score1.show()
						game_over = True
					player = 1
				draw_figures()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_r:
				restart()
				game_over = False
			if event.key == pygame.K_s:
				score1.restart()
				score2.restart()
				game_over = False


	pygame.display.update()