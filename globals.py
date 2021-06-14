import pygame
width, height = 256 , 144 #size of unscalled screen
nTileWid, nTileHei = 16, 16 #size of single tile
scalling = 3
def initialize():
	global directory
	directory = {}
	
	global game_current_screen
	game_current_screen = "map"
	
	global game_current_map
	game_current_map = None
	
	global fOffsetX, fOffsetY
	fOffsetX, fOffsetY = 0, 0
	
	global action_pressed
	action_pressed = False
	
	global game
	game = pygame.Surface((width, height))
	
	global screen
	screen = pygame.display.set_mode((width * scalling,height * scalling))
	
	global player_name, player_class, player_max_hp, player_hp
	player_name = "empty"
	player_class = "EE"
	player_max_hp = 100
	player_hp = 100
	
