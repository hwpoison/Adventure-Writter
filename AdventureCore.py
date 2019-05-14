import re
import threading
"""
borrador
Avalible operators:
	Conditional operator:
		?: if conditional with (and,==, y)(or, ||, o)
			value1 is x : return True if value1 is x
			value1 not is x: return True if value1 not is x
			value1 in list : operation list
		?else: else conditional

	Load operator:
		&LOAD <stage name> : load and initialize stage

	Variable asignation:
		:var_name = var_value : Asign var in local scope (escene)
		[x];;var_name = var_value : Asign var in global scopre (all scenes)

	Coment code:
		//: Coment Line

	Finish Adventure:
		END : Finish game

	Game status message:
		STATUS <message> : set game_status_message var for GUI

Stages:
	* It is suggested Structured programming in TABULATIONS
	Stage file format: 
		.adventure

	Stage file structure:
		#LOAD{
		} // first routine that runs when loading the stage

		![ACTION NAME]{
		} //routine that is associated with an action (verb)
"""


class AdventureCore(object):
	"""
	Structure:
	__init__:
					*game_vars : All variables in game
					*game_actions : All actions availibles in actual stage
					*current_output: All screen prints for GUI output
					*current_directory: Actual adventure files directory
					*game_status_message: misc message from game (STATUS)
					*DEBUG_INFO: Print logic process in console
	"""

	def __init__(self):
		self.game_vars = {}
		self.game_actions = {}
		self.output_buffer = []
		self.stage_history = []

		self.current_stage = None
		self.current_adventure_dir = []
		self.adventure_name = None
		self.in_game = False
		self.game_status_message = False

		self.DEBUG_INFO = True
		self.define_regxs()

	def define_regxs(self):
		# Instructions
		self.instruction_types = r'\?else|\?|//|\"|:|&|END|STATUS|'
		self.asign_value_regx = r'(.*)\s+(=|add)\s+(.*)'
		self.load_function = r'(LOAD|CARGAR)\s+(.*)$'
		self.or_regx = r'or|\|\||o'
		self.and_regx = r'and|&&|y|'  # fix /s x/s
		self.check_is_regx = r'is|es|'
		self.check_notis_regx = r'not is|is not|'
		self.check_in_regx = r'|in|en'
		self.code_blocks_regx = r'([#\!][a-zA-Z0-9_\s-]*)(\n+|)\{(.*?)\}'
		self.var_scope_value_regx = r'\$(.*?)\$'
		self.var_scope_regx = r'(\$.*?\$)'
		self.file_dir_resolution = r'(.*)\\(\w+)\.adventure'
		self.custom_instruction = r'{0}\s+(.*)'  # ex STATUS (TEXT)

	def dprint(self, *args):
		# debug message print
		if(self.DEBUG_INFO):
			dmsg = ''.join([str(str_) for str_ in args])
			print(dmsg)
		elif(':everprint' in args):
			dmsg = ''.join([str(str_) for str_ in args[:len(args)-1]])
			print(dmsg)

	def var_process(self, string_value):
		"""Parse real var type and value from string"""
		# list
		list_ = re.findall(r"\[(.*)\]", string_value)
		if list_:
			final_list = []
			for element in list_[0].split(','):
				final_list.append(self.var_process(element.strip())[1])
			return ('list', final_list)

		# str
		str_ = re.findall(r"[\"|'](.*)['|\"]", string_value)
		if str_:
			return ['str', str_[0]]

		# booleans
		bool_ = re.findall(r"True|true|False|false", string_value)
		if bool_:
			bool_ = True if bool_[0].lower() == 'true' else False
			return ('bool', bool_)

		return ('str', string_value)

	def check_game_var(self, key_var, to_compare, var_operator=''):
		"""Logic operation, value comparation"""
		self.dprint(f"[+]Checking if: {key_var}=>{var_operator}=>{to_compare}")
		game_value = self.game_vars.get(key_var)
		to_compare = self.var_process(to_compare)[1]
		if(game_value):
			game_value = self.game_vars[key_var]
		elif(game_value is None):
			self.dprint(f"\t[!]Variable '{key_var}'' not declared.")
			game_value = False

		self.dprint(f'\t[+]Comparing {to_compare} {var_operator} {game_value}')
		if(var_operator == 'is'):
			self.dprint(f"\t\t[+]Equal operation {to_compare} -> {game_value}")
			return True if to_compare == game_value else False

		if(var_operator == 'is not'):
			self.dprint(f"\t\t[+]Is not operation {to_compare} -> {game_value}")
			return True if to_compare != game_value else False

		elif(var_operator == 'in'):
			list_ = self.game_vars.get(to_compare)
			if(list_):
				self.dprint(f"\t\t[+]In operation {key_var} -> {list_}")
				key_var = self.var_process(key_var)[1]
				return True if key_var in list_ else False
		print("indefinido")

	def set_game_var(self, event):
		"""Var game setting manager"""
		var_asign_pattern = re.compile(self.asign_value_regx)  # var=val
		var_format = var_asign_pattern.findall(event)
		if var_format == []:
			self.dprint(f"[-]Format var asign error\n\t\t\t line:'{event}'")
			return False
		var_name = var_format[0][0]
		var_operation = var_format[0][1]
		var_type, var_value = self.var_process(
			var_format[0][2])  # list | str | bool
		self.dprint(f"[+]Setting: {var_name} {var_operation} {var_value}")
		if(var_operation is '=' and var_type is 'list'):  # List asign
			self.dprint(f"\t[>]Asigning list {var_value}")
			self.game_vars[var_name] = var_value
			return True
		elif(var_operation == 'add'):  # List add element
			self.dprint(f"\t[+]Adding element {var_value} to {var_name}")
			self.game_vars[var_name].append(var_value)
			return True
		elif(var_operation == '='):
			self.game_vars[var_name] = var_value
			return True

	def string_manager(self, string):
		# String formating
		scope_vars = re.findall(self.var_scope_regx, string)
		for svar in scope_vars:
			svalue = re.findall(self.var_scope_value_regx, svar)[0]
			if(self.game_vars.get(svalue)):
				value = self.game_vars[svalue]
				if(len(value) <= 1):
					string = string.replace(svar, value[0])
				else:
					string = string.replace(svar, str(value))
		self.output_buffer.append(string)
		self.dprint("PRINTING:", string)
		return string

	def if_struct_validation(self, params):
		# If validator
		equality_disset_pattern = r'\s('
		equality_disset_pattern += self.check_notis_regx
		equality_disset_pattern += self.check_is_regx
		equality_disset_pattern += self.check_in_regx
		equality_disset_pattern += r')\s'
		if_disset = re.compile(r'\s'+self.and_regx+self.or_regx+r'\s')
		equality_disset = re.compile(equality_disset_pattern)
		gate_ops = if_disset.findall(params)  # split gate ops (and, or ...)
		# split comparation ops (is, is not..)
		operations = if_disset.split(params)

		actual_gate = None  # and|or
		return_status = False  # if return status
		for num, operation in enumerate(operations):
			if(operation):
				operation = equality_disset.split(operation.strip())
				if(len(operation) == 1):
					self.dprint(f"[+]Error in if '{params}'' analisis")
					return False
				if(actual_gate is not None
				   and actual_gate in self.and_regx
				   and return_status is False):
					break
				if(actual_gate is not None
				   and actual_gate in self.or_regx
				   and return_status is True):
					break
				return_status = self.check_game_var(
					operation[0], operation[2], operation[1])
				self.dprint(f"[IF]Result of '{operation}' is {return_status}")
				if(len(gate_ops) == 0):
					return return_status
				actual_gate = gate_ops[num-1]

		return return_status  # True | False

	def load_call_function(self, string):
		"""Load a stage (& instruction)"""
		load_stage = re.findall(self.load_function, string)
		if(load_stage):
			self.load_stage_file(load_stage[0][1])

	def interpret_instruction(self, inst_type, content):
		"""Process instruction"""
		if(inst_type == ':'):  # asign varaible
			self.set_game_var(content)
		if(inst_type == '&'):  # call scene
			self.load_call_function(content)
		elif(inst_type == ''):  # string
			self.string_manager(content)
		elif(inst_type == 'END'):  # end game
			self.finish_adventure()
		elif(inst_type == 'STATUS'):  # return status message
			self.set_status_message(content)
		return False

	def process_code_line(self, line):
		"""Process a line code"""
		if(line == ''):  # empty line
			return False, False
		line = line.strip()
		ins_sign = re.match(self.instruction_types, line)
		sign, content = False, False
		if(ins_sign):
			sign = line[:ins_sign.end()]
			content = line[ins_sign.end():]
		if(ins_sign is False
		   and tab_pattern.findall(line) is False
		   and line is not ''):
			self.dprint("[!] Unrecognized line:", line, ":everprint")
		return sign, content

	def interpret_block_code(self, code):
		"""Analyze and execute block of code from a file"""
		if_index = {}  # tab level
		min_lvl = False
		for line in code.split('\n'):
			tabs_count = re.match('\t+', line)
			tab_lvl = tabs_count.end() if tabs_count else 0
			inst_type, content = self.process_code_line(line)
			if(inst_type is '?'):  # If
				if(min_lvl is False):
					min_lvl = tab_lvl
				if_index[tab_lvl] = self.if_struct_validation(content)
			if(inst_type == '?else'):  # else
				c_ver = if_index[tab_lvl]
				if_index[tab_lvl] = False if c_ver is True else True
			if(tab_lvl-1 in if_index and if_index[tab_lvl-1]):
				if(if_index.get(min_lvl) and if_index[min_lvl]):
					self.interpret_instruction(inst_type, content)
			if(tab_lvl == min_lvl or min_lvl is False):
				self.interpret_instruction(inst_type, content)

	def parser_stage_file(self, filename):
		"""Open and read adventure file"""
		if(self.current_adventure_dir is None):
			self.current_adventure_dir = ''
		try:
			full_name = filename
			stage_content = open(full_name, "r", encoding="utf-8").read()
		except FileNotFoundError as error:
			self.dprint(f"[!]Stage file not found:",
						filename)
			return False

		code_block = re.compile(self.code_blocks_regx,
								re.MULTILINE | re.DOTALL)
		blocks = code_block.findall(stage_content)
		if(blocks):
			return blocks
		return False

	def load_stage_file(self, stage_name):
		"""Open stage file and initialize vars"""
		full_name = f"{self.current_adventure_dir}\\{stage_name}.adventure"
		print(f"[+]Loading {full_name[-10:]}...")
		parser_content = self.parser_stage_file(full_name)
		if(parser_content is False):
			self.dprint(
				"[!]Error to load stage, invalid content or empty file", ":everprint")
			return False
		self.reset_game_actions()  # reset availibles actions
		self.current_stage = stage_name
		# self.status_message = False
		for block in parser_content:
			type_event = block[0].strip().lower()
			# #ROOM{}
			if(type_event == '#room'):
				"""Room specifications"""
				self.interpret_block_code(block[2])
				if(self.game_vars.get('stage_name')):
					self.current_stage = self.game_vars['stage_name']
				if(self.game_vars.get('adventure_name')):
					self.adventure_name = self.game_vars['adventure_name']
			# #LOAD_AGAIN{}
			if self.current_stage in self.stage_history:
				"""If loaded again"""
				if(type_event == '#load_again'):
					# Initialize scene variables
					self.interpret_block_code(block[2])
			# #LOAD{}
			elif(type_event == '#load'):
				# Initialize scene variables
				self.interpret_block_code(block[2])
			# !ACTION{}
			if(type_event[0] == '!'):
				# Register actions
				print("Registring:", type_event, block[2])
				self.game_actions[block[0][1:].lower().strip()] = block[2]
		self.dprint(f"\n[+]Stage {stage_name} loaded. {len(self.game_actions)} actions loaded.", ':everprint')
		self.stage_history.append(self.current_stage)
		return True

	def open_adventure(self, adventure_dir, stage_name):
		"""Load adventure and initialize game vars (for GUI)"""
		if(self.in_game):
			return False
		self.in_game = True
		self.game_vars = {}
		self.output_buffer = []
		self.stage_history = []
		self.current_adventure_dir = adventure_dir
		return True if self.load_stage_file(stage_name) else False

	def execute_action(self, cmd):
		print(f"\nExecuting: {cmd}")
		if(self.game_actions.get(cmd)):
			self.output_buffer = []
			self.interpret_block_code(self.game_actions[cmd])
			return True
		return False

	def finish_adventure(self):
		"""Finish the current adventure"""
		self.in_game = False

	def reset_game_actions(self):
		"""Reset game actions"""
		self.dprint("[+]Game actions reseted")
		self.game_actions = {}

	def test_c(self):
		def test():
			print("BANG!!!!!")
		threading.Timer(10, test).start()

	def set_status_message(self, content):
		self.dprint("[+]Setting status message:", content)
		status_message = re.split(
			self.custom_instruction.format('STATUS'), content)
		if(status_message):
			self.game_status_message = status_message[0]

	def loopGame(self):
		# test loop
		self.DEBUG_INFO = True
		self.current_adventure_dir = ''
		self.load_stage_file('start')  # start
		self.test_c()
		while True:
			action = input(">")
			if(self.game_actions.get(action)):
				self.execute_action(self.game_actions[action])
			else:
				print(self.game_status_message)
				print("You cant do that")


if __name__ == '__main__':
	n = AdventureCore()
	n.loopGame()
