import pygame
import vector
import math
import random
pygame.init()
import globals
globals.initialize()
from battle import *

""" TO DO LIST:
- maybe multiple choice text
- plot
- gameplay
- combat system
"""

# screen parameters
fcamX, fcamY= 0,0
nVisTileX, nVisTileY = globals.width // globals.nTileWid, globals.height // globals.nTileHei
fTileOffsetX, fTileOffsetY = 0,0

def sort_key(element):
	if element.type in ["door"]:
		return -1
	return element.pos.y
################################################################################ tile maps definitions
import tiles
################################################################################ maps and layers
class Map:
	def __init__(self, file_name, tiles):
		f = open(file_name,"r")
		lines = f.readlines()
		measurments = lines[0].split()
		self.nLevelWid, self.nLevelHei = int(measurments[0]), int(measurments[1])
		self.map = []
		self.map_solid = []
		self.tiles = tiles
		self.initial_pos = (1,1)
		self.initial_dir = 0
		self.secondary = None
		self.objects = []
		for i in lines[1:]:
			row = i.split(",")
			for tile in row:
				if tile == '\n':
					continue
				a_x, b_x = tile.split()
				tile_id, is_solid = int(a_x), int(b_x)
				self.map.append(tile_id)
				self.map_solid.append(is_solid)
		f.close()
	def get_tile(self, x, y):
		if x >= 0 and x < self.nLevelWid and y >= 0 and y < self.nLevelHei:
			return self.map[int(y) * self.nLevelWid + int(x)]
		else:
			return 0
	def get_tile_solid(self, x, y):
		if x >= 0 and x < self.nLevelWid and y >= 0 and y < self.nLevelHei:
			return self.map_solid[int(y) * self.nLevelWid + int(x)] == 1
		else:
			return False
	def draw(self):
		global fTileOffsetX, fTileOffsetY
		globals.fOffsetX = fcamX - nVisTileX / 2
		globals.fOffsetY = fcamY - nVisTileY / 2
		if globals.fOffsetX < 0:
			globals.fOffsetX = 0
		if globals.fOffsetY < 0:
			globals.fOffsetY = 0
		if globals.fOffsetX > self.nLevelWid - nVisTileX:
			globals.fOffsetX = self.nLevelWid - nVisTileX
		if globals.fOffsetY > self.nLevelHei - nVisTileY:
			globals.fOffsetY = self.nLevelHei - nVisTileY
		fTileOffsetX = (globals.fOffsetX - int(globals.fOffsetX)) * globals.nTileWid
		fTileOffsetY = (globals.fOffsetY - int(globals.fOffsetY)) * globals.nTileHei
	
		for x in range(-1, nVisTileX +1):
			for y in range(-1, nVisTileY +1):
				index = self.get_tile(x + globals.fOffsetX,y + globals.fOffsetY)
				pos = (x*globals.nTileWid - fTileOffsetX,y*globals.nTileHei - fTileOffsetY)
				self.tiles.draw_tile(pos, index)

def switch_maps(new_map):
	global game_current_map
	game_current_map = new_map
	player.pos.x = new_map.initial_pos[0]
	player.pos.y = new_map.initial_pos[1]
	player.dir = new_map.initial_dir
globals.directory["switch_maps"] = switch_maps
################################################################################ objects
from objects import *
################################################################################ Director
from director import *
################################################################################ Character
from character import *
################################################################################ player
class Player (Character):
	def check_input(self):
		if Director._usercontrol:
			if pygame.key.get_pressed()[pygame.K_UP]:
				self.vel.y -= self.speed
				self.dir = 1
			if pygame.key.get_pressed()[pygame.K_DOWN]:
				self.vel.y += self.speed
				self.dir = 3
			if pygame.key.get_pressed()[pygame.K_RIGHT]:
				self.vel.x += self.speed
				self.dir = 0
			if pygame.key.get_pressed()[pygame.K_LEFT]:
				self.vel.x -= self.speed
				self.dir = 2
	def pos_4_draw(self):
		return ((self.pos.x - globals.fOffsetX)* globals.nTileWid,(self.pos.y - 9/globals.nTileHei - globals.fOffsetY)* globals.nTileHei)
	def step(self):
		global fcamX, fcamY
			# input
		self.check_input()
			# collision
		ppos = self.pos + self.vel
		ppos = self.check_map_collision(ppos)
		ppos = self.check_obj_collision(ppos)
			# update after collision
		if ppos:
			self.pos = ppos
			#interaction
		if globals.action_pressed and Director._usercontrol:
			if self.dir == 0:
				interaction_pos = vector.Vector(self.pos.x + 1.5, self.pos.y + 0.5)
			elif self.dir == 1:
				interaction_pos = vector.Vector(self.pos.x + 0.5, self.pos.y - 0.5)
			elif self.dir == 2:
				interaction_pos = vector.Vector(self.pos.x - 0.5, self.pos.y + 0.5)
			else:
				interaction_pos = vector.Vector(self.pos.x + 0.5, self.pos.y + 1.5)
			for obj in globals.game_current_map.objects:
				if obj == self:
					continue
				if interaction_pos.x > obj.pos.x and interaction_pos.x < obj.pos.x + 1 and interaction_pos.y > obj.pos.y and interaction_pos.y < obj.pos.y + 1:
					obj.on_interaction()
			# cam update
		fcamX, fcamY = self.pos.x, self.pos.y
################################################################################ game setup
import npc
# player initialize
player = Player("zenzor", (0,0), tiles.tile_player)
globals.directory["player"] = player

# maps initialize
map_world = Map("maps/map01", tiles.tile_map)
map_home = Map("maps/map_home", tiles.tile_map)
map_campus = Map("maps/campus", tiles.tile_map)

#big map
map_campus.initial_pos = (480,345)
map_campus_layer2 = Map("maps/campus_layer2", tiles.tile_map)
map_campus.secondary = map_campus_layer2
#big map objects
map_campus.objects = [player, npc.npc_hadi, Sign((481,345),"Oh great penis of Ulman","Teach me your wisdom")]


globals.game_current_map = map_campus
player.pos = vector.Vector(globals.game_current_map.initial_pos[0],globals.game_current_map.initial_pos[1])

main_director = Director()
globals.directory["director"] = main_director

################################################################################ game loop
run = True
while run:
	pygame.time.delay(1)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_z:#z
				globals.action_pressed = True
			if event.key == pygame.K_c:#c
				main_director.queue.append(Command_transition())
				main_director.queue.append(Command_enter_battle("hadi", 15, "CS", 1, 100, [A_dont_understand, A_ask_question]))
			if event.key == pygame.K_s:#s
				enter_battle("hadi", 15, 1, 100, [A_dont_understand, A_ask_question])
				print_battle()
			if event.key == pygame.K_d:#d
				globals.game_current_screen = "map"
			if event.key == pygame.K_f:#f
				print(player.pos)
				print(globals.game_current_screen)
	keys = pygame.key.get_pressed()
	if keys[pygame.K_ESCAPE]:
		run = False

	###################### steps
	if globals.game_current_screen == "map":
		#steps for map
		main_director.step()
		
		for obj in globals.game_current_map.objects:
			obj.step()
	if globals.game_current_screen == "battle":
		#steps for battle
		battle_step()
	###################### draw
	if globals.game_current_screen == "map":
		#draw map screen
		globals.game_current_map.draw()
		
		globals.game_current_map.objects.sort(key = sort_key)
		for obj in globals.game_current_map.objects:
			obj.draw()
			#draw secondary maps:
		if globals.game_current_map.secondary:
			globals.game_current_map.secondary.draw()
	
	if globals.game_current_screen == "battle":
		#draw battle screen
		battle_draw()
	
	###################### action reset
	globals.action_pressed = False
	
	###################### screen manegement and text
	main_director.draw_text_box()
	globals.screen.blit(pygame.transform.scale(globals.game, globals.screen.get_rect().size), (0, 0))
	main_director.draw_text()
	pygame.display.update()
	#pygame.time.wait(1)
pygame.quit()