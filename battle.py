
import globals

class Attack:
	def __init__(self, name, damage):
		self.name = name
		self.damage = damage
	def __str__(self):
		return self.name
	def __repr__(self):
		return str(self)
class S_attack (Attack):
	pass
	
A_ask_question = Attack("Ask question", 10)
A_dont_understand = Attack("Dont understand", 20)
A_confusion = S_attack("Confusion", -1)

### initialize
battle_turn = "player"
battle_rival_name = "empty"
battle_rival_level = 1001 #empty level
battle_rival_sprite_index = 0
battle_rival_hp = 100
battle_rival_attacks = [A_ask_question, A_dont_understand]



def enter_battle(rivel_name, rival_level, rival_class ,rival_sprite, rival_hp, rival_attacks):
	global battle_rival_name, battle_rival_level, battle_rival_class, battle_rival_sprite_index, battle_rival_hp, battle_rival_attacks
	battle_rival_name = rivel_name
	battle_rival_level = rival_level
	battle_rival_sprite_index = rival_sprite
	battle_rival_class = rival_class
	battle_rival_hp = rival_hp
	battle_rival_attacks = rival_attacks
	
	globals.game_current_screen = "battle"
	
def print_battle():
	print("name", battle_rival_name)
	print("level", battle_rival_level)
	print("class", battle_rival_class)
	print("sprite index", battle_rival_sprite_index)
	print("hp", battle_rival_hp)
	print("attacks", battle_rival_attacks)

def battle_step():
	pass

def battle_draw():
	#background:
	globals.game.fill((200,200,200), (0,0,globals.width,globals.height) )





