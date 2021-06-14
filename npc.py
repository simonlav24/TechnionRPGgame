import tiles
import character
import battle
import globals
import director

def hadi_interaction(self):
	if self.state == 0:
		globals.directory["director"].queue.append(director.Command_dialog(1,"hi, my name is "+self.name))
		globals.directory["director"].queue.append(director.Command_goto(self, 2,0,100))
	if self.state == 1:
		globals.directory["director"].queue.append(director.Command_dialog(1,"Lets battle!"))
		globals.directory["director"].queue.append(director.Command_transition())
		globals.directory["director"].queue.append(director.Command_enter_battle("hadi", 15, "CS", 1, 100, [battle.A_dont_understand, battle.A_ask_question]))
	self.state += 1

npc_hadi = character.Character("hadi", (478,341), tiles.tile_hadi, hadi_interaction)
npc_hadi.dir = 3

