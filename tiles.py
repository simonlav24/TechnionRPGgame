
import globals
import pygame

class Tilemap:
	def __init__(self, file_name, tiles_amount, tile_size):
		self.tiles = pygame.image.load(file_name)
		self.tiles_amount_x = tiles_amount[0]
		self.tiles_amount_y = tiles_amount[1]
		self.tile_width = tile_size[0]
		self.tile_height = tile_size[1]
	def index2assetmap(self, index):
		loc = ( (index % self.tiles_amount_x)* self.tile_width , (index//self.tiles_amount_x)* self.tile_height )
		siz = (self.tile_width, self.tile_height)
		return (loc, siz)
	def draw_tile(self, pos, index):
		globals.game.blit(self.tiles, pos, self.index2assetmap(index) )


tile_player = Tilemap("assets/base_player_zenzor3.png", (3,5), (17,25))
tile_hadi = Tilemap("assets/hadi.png", (3,5), (17,25))
tile_map = Tilemap("assets/tech_tiles3.png", (16,9), (16,16))
tile_text_box = Tilemap("assets/text_box.png", (3,3), (16,16))