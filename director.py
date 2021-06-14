import vector
import globals
import tiles
import battle
import pygame 

font1 = pygame.font.Font("assets/Emulogic-zrEw.ttf", 16)

class Director:
	_usercontrol = True
	_current_text = None
	_current_text2 = None
	def __init__(self):
		self.queue = []
	def step(self):
		if len(self.queue) == 0:
			Director._usercontrol = True
		else:
			Director._usercontrol = False
			if not self.queue[0].started:
				self.queue[0].start()
			else:
				self.queue[0].step()
				if self.queue[0].completed:
					self.queue.pop(0)
	def draw_text_box(self):
		if Director._current_text:
			tiles.tile_text_box.draw_tile((0, 7*16),0)
			tiles.tile_text_box.draw_tile((0, 8*16),6)
			tiles.tile_text_box.draw_tile((15*16, 7*16),2)
			tiles.tile_text_box.draw_tile((15*16, 8*16),8)
			for i in range(1,15):
				tiles.tile_text_box.draw_tile((i*16, 7*16),1)
			for i in range(1,15):
				tiles.tile_text_box.draw_tile((i*16, 8*16),7)
	def draw_text(self):
		if Director._current_text:
			globals.screen.blit(font1.render(Director._current_text, 0, (20, 20, 20)), (35,globals.height*globals.scalling -75))
		if Director._current_text2:
			globals.screen.blit(font1.render(Director._current_text2, 0, (20, 20, 20)), (35,globals.height*globals.scalling -50))
		
class Command_goto:
	def __init__(self, subject, x, y, duration):
		self.move = vector.Vector(x,y)
		self.clock = 0
		self.duration = duration
		self.subject = subject
		self.completed = False
		self.started = False
	def start(self):
		self.started = True
		self.start_pos = vector.Vector(self.subject.pos.x,self.subject.pos.y)
		self.end_pos = self.start_pos + self.move
	def step(self):
		self.clock += 1
		t = self.clock / self.duration
		self.subject.vel.x = (self.end_pos.x - self.start_pos.x) / self.duration
		self.subject.vel.y = (self.end_pos.y - self.start_pos.y) / self.duration
		if self.clock >= self.duration:
			self.subject.vel.x = 0
			self.subject.vel.y = 0
			self.completed = True

class Command_wait:
	def __init__(self, duration):
		self.started = False
		self.completed = False
		self.duration = duration
		self.clock = 0
	def start(self):
		self.started = True
	def step(self):
		self.clock += 1
		if self.clock >= self.duration:
			self.completed = True

class Command_dialog:
	def __init__(self, index, text, text2 = None):
		self.text = text
		self.text2 = text2
		self.index = index
		self.started = False
		self.completed = False
	def start(self):
		self.started = True
	def step(self):
			#draw text
		Director._current_text = self.text
		Director._current_text2 = self.text2
		if globals.action_pressed:
			Director._current_text = None
			Director._current_text2 = None
			self.completed = True

class Command_transition:
	def __init__(self):
		self.completed = False
		self.started = False
	def start(self):
		self.started = True
	def step(self):
		time_delay = 30
		for i in range(16):
			globals.game.fill((0,0,0),(i*16,16*0,16,16))
			globals.game.fill((0,0,0),(16*16-16-i*16,8*16,16,16))
			globals.screen.blit(pygame.transform.scale(globals.game, globals.screen.get_rect().size), (0, 0))
			pygame.display.update()
			pygame.time.wait(time_delay)
		for i in range(7):
			globals.game.fill((0,0,0),(16*16-16,16+i*16,16,16))
			globals.game.fill((0,0,0),(0,9*16-32-i*16,16,16))
			globals.screen.blit(pygame.transform.scale(globals.game, globals.screen.get_rect().size), (0, 0))
			pygame.display.update()
			pygame.time.wait(time_delay)
		for i in range(15):
			globals.game.fill((0,0,0),(16+i*16,16*1,16,16))
			globals.game.fill((0,0,0),(16*16-16-i*16-16,8*16-16,16,16))
			globals.screen.blit(pygame.transform.scale(globals.game, globals.screen.get_rect().size), (0, 0))
			pygame.display.update()
			pygame.time.wait(time_delay)
		for i in range(5):
			globals.game.fill((0,0,0),(16*16-16*2,16*2+i*16,16,16))
			globals.game.fill((0,0,0),(16*1,9*16-16*3-i*16,16,16))
			globals.screen.blit(pygame.transform.scale(globals.game, globals.screen.get_rect().size), (0, 0))
			pygame.display.update()
			pygame.time.wait(time_delay)
		for i in range(12):
			globals.game.fill((0,0,0),(16*2+i*16,16*2,16,16))
			globals.game.fill((0,0,0),(16*16-16*2-i*16-16,8*16-16*2,16,16))
			globals.screen.blit(pygame.transform.scale(globals.game, globals.screen.get_rect().size), (0, 0))
			pygame.display.update()
			pygame.time.wait(time_delay)
		for i in range(3):
			globals.game.fill((0,0,0),(16*16-16*3,16*3+i*16,16,16))
			globals.game.fill((0,0,0),(16*2,9*16-16*4-i*16,16,16))
			globals.screen.blit(pygame.transform.scale(globals.game, globals.screen.get_rect().size), (0, 0))
			pygame.display.update()
			pygame.time.wait(time_delay)
		for i in range(10):
			globals.game.fill((0,0,0),(16*3+i*16,16*3,16,16))
			globals.game.fill((0,0,0),(16*16-16*3-i*16-16,8*16-16*3,16,16))
			globals.screen.blit(pygame.transform.scale(globals.game, globals.screen.get_rect().size), (0, 0))
			pygame.display.update()
			pygame.time.wait(time_delay)
		for i in range(5):
			globals.game.fill((0,0,0),(16*3+i*16,16*4,16,16))
			globals.game.fill((0,0,0),(16*16-16*3-i*16-16,8*16-16*4,16,16))
			globals.screen.blit(pygame.transform.scale(globals.game, globals.screen.get_rect().size), (0, 0))
			pygame.display.update()
			pygame.time.wait(time_delay)
		self.completed = True

class Command_enter_battle:
	def __init__(self, name, level, class_, index, hp, attacks):
		self.completed = False
		self.started = False
		self.name = name
		self.level = level
		self.class_ = class_
		self.index = index
		self.hp = hp
		self.attacks = attacks
	def start(self):
		self.started = True
	def step(self):
		self.completed = True
		battle.enter_battle(self.name, self.level, self.class_, self.index, self.hp, self.attacks)