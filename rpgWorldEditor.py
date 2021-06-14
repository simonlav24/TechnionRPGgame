import pygame
import vector
import math
import random
pygame.init()
myfont = pygame.font.SysFont("Comic Sans MS", 10)
scalling = 2

index2draw = 0
indexes = [0,1]

WORLD_TO_EDIT = "maps/campus"
#WORLD_TO_EDIT = "maps/campus_layer2"
LAYER0 = "maps/campus"

if WORLD_TO_EDIT == "maps/campus_layer2":
	layer = True
else:
	layer = False


#nLevelWid, nLevelHei = 64, 16
#width, height = 256 , 144 
width, height = 500 , 300
nTileWid, nTileHei = 16, 16
fcamX, fcamY, fOffsetX, fOffsetY = 0,0,0,0
nVisTileX, nVisTileY = width // nTileWid, height // nTileHei

screen = pygame.display.set_mode((width*scalling,height*scalling))
win = pygame.Surface((width, height))
#asset:
#tilemap = pygame.image.load("assets/tile_map_test3.png")
tilemap = pygame.image.load("assets/tech_tiles3.png")
tilemap_a_s_w = 16
tilemap_a_s_h = 16
tilemap_a_wid = 16
tilemap_a_hei = 9

def index2assetmap(index, size_w, size_h, asset_w, asset_h):
	loc = ( (index % asset_w)* size_w , (index//asset_w)* size_h )
	siz = (size_w, size_h)
	return (loc, siz)

# map handelling
f = open(WORLD_TO_EDIT,"r")
lines = f.readlines()
measurments = lines[0].split()
nLevelWid, nLevelHei = int(measurments[0]), int(measurments[1])
map = []
map_solid = []
for i in lines[1:]:
	row = i.split(",")
	for tile in row:
		if tile == '\n':
			continue
		a_x, b_x = tile.split()
		tile_id, is_solid = int(a_x), int(b_x)
		map.append(tile_id)
		map_solid.append(is_solid)
f.close()

f = open(LAYER0,"r")
lines = f.readlines()
measurments = lines[0].split()
nLevelWid, nLevelHei = int(measurments[0]), int(measurments[1])
map_l0 = []
for i in lines[1:]:
	row = i.split(",")
	for tile in row:
		if tile == '\n':
			continue
		a_x, b_x = tile.split()
		tile_id, is_solid = int(a_x), int(b_x)
		map_l0.append(tile_id)
f.close()


def get_tile(map2d,x,y):
	if x >= 0 and x < nLevelWid and y >= 0 and y < nLevelHei:
		return map2d[int(y) * nLevelWid + int(x)]
	else:
		return 0
		
def get_tile_solid(x,y):
	if x >= 0 and x < nLevelWid and y >= 0 and y < nLevelHei:
		return map_solid[int(y) * nLevelWid + int(x)] == 1
	else:
		return False

def draw_map(map2d):
	global fOffsetX, fOffsetY
	fOffsetX = fcamX - nVisTileX / 2
	fOffsetY = fcamY - nVisTileY / 2
	if fOffsetX < 0:
		fOffsetX = 0
	if fOffsetY < 0:
		fOffsetY = 0
	if fOffsetX > nLevelWid - nVisTileX:
		fOffsetX = nLevelWid - nVisTileX
	if fOffsetY > nLevelHei - nVisTileY:
		fOffsetY = nLevelHei - nVisTileY
	fTileOffsetX = (fOffsetX - int(fOffsetX)) * nTileWid
	fTileOffsetY = (fOffsetY - int(fOffsetY)) * nTileHei

	for x in range(-1, nVisTileX +1):
		for y in range(-1, nVisTileY +1):
		
			index = get_tile(map2d, x + fOffsetX,y + fOffsetY)
			win.blit(tilemap, (x*nTileWid - fTileOffsetX,y*nTileHei - fTileOffsetY), index2assetmap(index, tilemap_a_s_w, tilemap_a_s_h, tilemap_a_wid, tilemap_a_hei))
			solid = get_tile_solid(x + fOffsetX,y + fOffsetY)
			if solid == 1:
				win.fill( (255,0,0), ( (x*nTileWid - fTileOffsetX,y*nTileHei - fTileOffsetY), (2,2) ) )

################################################################################ player
class Player:
	def __init__(self):
		self.speed = 0.25
		self.pos = vector.Vector(480,345)
		self.vel = vector.Vector(0,0)
		self.size = 1
	def step(self):
		global fcamX, fcamY
		# input
		if pygame.key.get_pressed()[pygame.K_UP]:
			self.vel += vector.Vector(0, -self.speed)
		if pygame.key.get_pressed()[pygame.K_DOWN]:
			self.vel += vector.Vector(0,  self.speed)
		if pygame.key.get_pressed()[pygame.K_RIGHT]:
			self.vel += vector.Vector( self.speed, 0)
		if pygame.key.get_pressed()[pygame.K_LEFT]:
			self.vel += vector.Vector(-self.speed, 0)

		# update after collision
		self.pos += self.vel
		# cam update
		fcamX, fcamY = self.pos.x, self.pos.y
		# reset speed
		self.vel *= 0
		# draw self
		self.draw()
		
	def draw(self):
		win.fill((255,0,0), (((self.pos.x - fOffsetX)* nTileWid,(self.pos.y - fOffsetY)* nTileHei), (nTileWid*self.size, nTileHei*self.size)))
		

# mouse to draw:
def mouse_check():
	global index2draw
	mouse_pos = pygame.mouse.get_pos()
	m_x = mouse_pos[0]
	m_y = mouse_pos[1]
	index_of_mouse = (int((m_x/scalling)/nTileWid + fOffsetX) , int((m_y/scalling)/nTileHei + fOffsetY) )
	#draw:
	#win.fill((255,0,0), (  ((index_of_mouse[0] - fOffsetX)*nTileWid , (index_of_mouse[1] - fOffsetY)*nTileHei) , (nTileWid , nTileHei)))
	win.blit(tilemap,   ((index_of_mouse[0] - fOffsetX)*nTileWid , (index_of_mouse[1] - fOffsetY)*nTileHei) , index2assetmap(index2draw, tilemap_a_s_w, tilemap_a_s_h, tilemap_a_wid, tilemap_a_hei))
	index_of_mouse = (int((m_x/scalling)/nTileWid + fOffsetX) , int((m_y/scalling)/nTileHei + fOffsetY) )
	#label:
	label = myfont.render(str(index_of_mouse)+str(index2draw), 1, (10,10,10))
	win.blit(label, (0, 0))
	
	if pygame.mouse.get_pressed()[0]:
		if index2draw >= 0:
			map[index_of_mouse[1] * nLevelWid + index_of_mouse[0]] = index2draw
		if index2draw == -1: #make solid
			map_solid[index_of_mouse[1] * nLevelWid + index_of_mouse[0]] = 1
		if index2draw == -2: #make non solid
			map_solid[index_of_mouse[1] * nLevelWid + index_of_mouse[0]] = 0

def update_map():
	file = open(WORLD_TO_EDIT, 'w')
	file.write(str(nLevelWid) + " " + str(nLevelHei) + "\n")
	for i in range(nLevelWid * nLevelHei):
		if i % (nLevelWid ) == 0 and i != 0:
			file.write("\n")
		string = str(map[i]) + " " + str(map_solid[i]) + " ,"
		file.write(string)
	file.write("\n")
	file.close()

p = Player()
run = True
while run:
	pygame.time.delay(1)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_a:
				index2draw -= 1
			if event.key == pygame.K_d:
				index2draw += 1
			if event.key == pygame.K_w:
				index2draw -= tilemap_a_s_w
			if event.key == pygame.K_s:
				index2draw += tilemap_a_s_w
			if event.key == pygame.K_r:
				index2draw = 0
	keys = pygame.key.get_pressed()
	if keys[pygame.K_ESCAPE]:
		run = False
	# background
	win.fill((255,255,255))
	
	# draw map
	if layer:
		draw_map(map_l0)
	draw_map(map)
	
	# steps
	p.step()
	mouse_check()
	screen.blit(pygame.transform.scale(win, screen.get_rect().size), (0, 0))
	pygame.display.update() 
update_map()
pygame.quit()