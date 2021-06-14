import vector
import globals
import director

class Object:
	def step(self):
		pass
	def draw(self):
		pass

class Door (Object):
	def __init__(self, location, map_to):
		self.type = "door"
		self.map_to = map_to
		self.pos = vector.Vector(location[0],location[1])
	def on_interaction(self):
		globals.switch_maps(self.map_to)

class Sign (Object):
	def __init__(self, location, text, text2=None):
		self.type = "sign"
		self.pos = vector.Vector(location[0], location[1])
		self.text = text
		self.text2 = text2
	def on_interaction(self):
		globals.directory["director"].queue.append(director.Command_dialog(1,self.text, self.text2))