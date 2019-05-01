from AdventureParser import *


class AdventureCore(AdventureParser):
	def __init__(self):
		super().__init__()
		self.game_vars = {}
		self.game_actions = {}
		self.current_stage = None
		self.current_output = []
	
	def loopGame(self):
		self.current_directory = 'test_adventure\\'
		self.loadStage('test') #start
		while True:
			# self.exec_action("abrir puerta")
			# self.exec_action("volver")
			print(self.game_vars)
			print(self.current_stage)
			cmd = input(">")

if __name__ == '__main__':
	a = AdventureCore()
	a.loopGame()