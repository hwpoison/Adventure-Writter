from .adventureWordProcessor import adventureWordProcessor
from .adventureInterpreter import adventureInterpreter
from .adventureFileParser import adventureFileParser
from .source_Regex import SourceRegex
from .debug import dprint
import re

class AdventureCore(adventureInterpreter):
	"""
		loadDictionary : load dictionary words
		openAdventure : initialize game adventure
		finishAdventure : 
		registerAction :
		executeAction :
		resetActions :
		load_stage_file :
	"""
	def __init__(self):
		super(AdventureCore, self).__init__()
		self.in_game = False
		self.adventure_name = None
		self.game_vars = {}
		self.game_actions_names = {}
		self.game_actions = {}
		self.output_buffer = []
		self.game_status_message = None

		self.stage_history = []
		self.current_stage = False
		self.sentence_processor = adventureWordProcessor()

		self.file_manager = adventureFileParser()

	def loadDictionary(self, file):
		self.sentence_processor.load_dictionary(file)

	def openAdventure(self, adventure_name, adventure_dir=''):
		"""Load adventure and initialize game vars (for GUI)"""
		if(self.in_game):
			return False
		self.resetActions()
		self.reset_vars()
		adventure_content = self.load_stage_file(adventure_name, adv_dir=adventure_dir)
		if(adventure_content):
			dprint("[+]Adventure initialized!")
			self.in_game = True
			return True
		else:
			return False
	
	def finishAdventure(self):
		"""Finish the current adventure"""
		self.in_game = False

	def registerAction(self, action, content):
		dprint(f"[+]Registring: {action}")
		action_index = len(self.game_actions)+1
		self.game_actions[action_index] = content
		for action_name in action.split('|'):
			self.game_actions_names[action_name.strip()] = action_index

	def executeAction(self, sentence):
		# agregar or |
		print(f"\n[+]Executing action: {sentence}")
		sentence = sentence.lower()
		if(self.game_actions_names.get(sentence)):
			self.clear_output_buffer()
			self.interpret_block_code(
				self.game_actions[self.game_actions_names[sentence]])
			return True
		else:
			sentence = self.sentence_processor.process(sentence, self.game_actions_names)
			if(sentence):
				self.clear_output_buffer()
				self.interpret_block_code(
					self.game_actions[self.game_actions_names[sentence]])
				return True
		return False

	def resetActions(self):
		"""Reset game actions"""
		dprint("[+]Game actions reseted")
		self.game_actions_names = {}

	def load_stage_file(self, stage_name, adv_dir):
		"""Open and initialize stage variables"""
		parser_content = self.file_manager.load_stage_file(stage_name, adv_dir)
		if(parser_content is False):
			return 

		self.resetActions()
		for block_type, block_name, block_content, in parser_content:
			# #ROOM{}
			block_name = block_name.strip().lower()
			if(block_type == '#' and block_name == 'room'):
				"""Room specifications"""
				self.interpret_block_code(block_content)
				if(self.game_vars.get('stage_name')):
					self.current_stage = self.game_vars['stage_name']
				if(self.game_vars.get('adventure_name')):
					self.adventure_name = self.game_vars['adventure_name']
			
			# #LOAD_AGAIN{}
			if self.current_stage in self.stage_history:
				"""If loaded again"""
				if(block_type == '#' and block_name == 'load_again'):
					# Initialize scene variables
					self.interpret_block_code(block_content)
			
			# #LOAD{}
			elif(block_type == '#' and block_name == 'load'):
				# Initialize scene variables
				self.interpret_block_code(block_content)
			
			# !ACTION{}
			if(block_type == '!'):
				# Register actions
				self.registerAction(block_name, block_content)

		dprint(f"\n[+]Stage '{stage_name}' loaded.")
		self.stage_history.append(self.current_stage)
		return True

	def stage_call_function(self, string):
		"""Load a stage (& instruction)"""
		load_stage = re.findall(SourceRegex.load_function, string)
		if(load_stage):
			self.load_stage_file(load_stage[0][1], adv_dir=self.file_manager.current_directory)
  
if __name__ == '__main__':
	pass