import vector
import globals
import director
import battle

class Character:
	def __init__(self, name, pos, tiles, interaction_func = None):
		#objects.append(self)
		self.type = "character"
		self.speed = 0.03
		self.pos = vector.Vector(pos[0],pos[1])
		self.vel = vector.Vector(0,0)
		self.dir = 3
		self.clock = 1
		self.anim_speed = 60 #the higher the slower
		self.tiles = tiles
		self.name = name
		self.state = 0
		self.interaction_func = interaction_func
	def on_interaction(self):
		switch = {0:2, 1:3, 2:0, 3:1}
		self.dir = switch[globals.directory["player"].dir]
		if self.interaction_func:
			self.interaction_func(self)
	def check_map_collision(self, ppos):
		if self.vel.x <= 0:
			if globals.game_current_map.get_tile_solid(ppos.x, self.pos.y) or globals.game_current_map.get_tile_solid(ppos.x, self.pos.y + 0.9):
				ppos.x = int(ppos.x) + 1
				self.vel.x = 0
		else:
			if globals.game_current_map.get_tile_solid(ppos.x +1, self.pos.y) or globals.game_current_map.get_tile_solid(ppos.x +1, self.pos.y + 0.9):
				ppos.x = int(ppos.x)
				self.vel.x = 0
		if self.vel.y <= 0:
			if globals.game_current_map.get_tile_solid(ppos.x, ppos.y) or globals.game_current_map.get_tile_solid(ppos.x + 0.9, ppos.y):
				ppos.y = int(ppos.y) + 1
				self.vel.y = 0
		else:
			if globals.game_current_map.get_tile_solid(ppos.x, ppos.y +1) or globals.game_current_map.get_tile_solid(ppos.x + 0.9, ppos.y +1):
				ppos.y = int(ppos.y) 
				self.vel.y = 0
		return ppos
	def check_obj_collision(self, ppos):
		#for obj in objects:
		for obj in globals.game_current_map.objects:
			if obj == self:
				continue
			if ppos.x > obj.pos.x -1 and ppos.x < obj.pos.x +1 and self.pos.y > obj.pos.y -1 and self.pos.y < obj.pos.y +1:
				if self.vel.x <= 0:
					ppos.x = obj.pos.x + 1
					self.vel.x = 0
				else:
					ppos.x = obj.pos.x - 1
					self.vel.x = 0
				if obj.type == "door":
					obj.on_interaction()
					return None
			if ppos.x > obj.pos.x -1 and ppos.x < obj.pos.x +1 and ppos.y > obj.pos.y -1 and ppos.y < obj.pos.y +1:
				if self.vel.y <= 0:
					ppos.y = obj.pos.y + 1
					self.vel.y = 0
				else:
					ppos.y = obj.pos.y - 1
					self.vel.y = 0
				if obj.type == "door":
					obj.on_interaction()
					return None
		return ppos
	def step(self):
			# collision
		ppos = self.pos + self.vel
		ppos = self.check_obj_collision(ppos)
			# update after collision
		self.pos = ppos
	def pos_4_draw(self):
		return ((self.pos.x - globals.fOffsetX)* globals.nTileWid,(self.pos.y - 9/globals.nTileHei - globals.fOffsetY)* globals.nTileHei)
	def draw(self):
		pos = self.pos_4_draw()
			# shadow:
		self.tiles.draw_tile((pos[0]+1,pos[1]+3), 12)
			# determine direction of character
		if self.vel.y > 0:
			self.dir = 3
		if self.vel.y < 0:
			self.dir = 1
		if self.vel.x > 0:
			self.dir = 0
		if self.vel.x < 0:
			self.dir = 2
		if self.dir == 0:
			anim = (3,5,4)
		elif self.dir == 1:
			anim = (9,11,10)
		elif self.dir == 2:
			anim = (6,8,7)
		else:
			anim = (0,2,1)
		if self.vel.x != 0 or self.vel.y != 0: #moving
			if (self.clock < self.anim_speed/4):
				self.tiles.draw_tile(pos, anim[0])
			elif (self.clock >= self.anim_speed/2 and self.clock < 3*self.anim_speed/4):
				self.tiles.draw_tile(pos, anim[1])
			else:
				self.tiles.draw_tile(pos, anim[2])
		else: #standing
			self.tiles.draw_tile(pos, anim[2])
			#update clock
		self.clock += 1
		if self.clock == self.anim_speed:
			self.clock = 1
			# reset speed
		self.vel *= 0