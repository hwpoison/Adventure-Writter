import re


from .debug import dprint


#interprete and execute code blocks 

class advInterpreter():
	"""docstring for adventureInterpreter"""
	def __init__(self):
		super(advInterpreter, self).__init__()
		self.game_vars = {}
		self.game_status_message = None
		self.output_buffer = []
		self.game_show_image = None
		self.regex = {
			'and':r' and | y |',
			'or':r' or| o | \|\| ',
			'is':r' is | es |',
			'not':r'is not| no es',
			'in':r'|in',
			'load_function':r'(LOAD|CARGAR)\s+(.*)$',	
			'code_blocks':r'([#\!\¡])([áéíóúa-zA-Z0-9_-\|-\s-]*)\{(.*?)\}',
			'instruction_types':r'\?else|\?|//|\"|:|&|END|STATUS|IMAGE|',
			'asign_value':r'(.*)\s+(=|add)\s+(.*)',
			'var_scope': r'(\$.*?\$)',
			'var_scope_value':r'\$(.*?)\$',
			'file_dir_resolution':r'(.*)\\(\w+)\.adventure',
			'custom_instruction':r'{0}\s+(.*)'
		}
	
	def reset_vars(self):
		self.game_vars = {}
		self.output_buffer = []
		self.game_show_image = None
		self.stage_history = []
		self.game_status_message = None

	def clear_output_buffer(self):
		self.output_buffer = []
		
	def var_process(self, string_value):
		"""Parse real var type and value from string"""
		# list
		list_t = re.findall(r"\[(.*)\]", string_value)
		if list_t:
			final_list = []
			for element in list_t[0].split(','):
				final_list.append(self.var_process(element.strip())[1])
			return ('list', final_list)

		# str
		str_t = re.findall(r"[\"|'](.*)['|\"]", string_value)
		if str_t:
			return ['str', str_t[0]]

		# booleans
		bool_t = re.findall(r"True|true|False|false", string_value)
		if bool_t:
			bool_t = True if bool_t[0].lower() == 'true' else False
			return ('bool', bool_t)

		return ('str', string_value)

	def check_game_var(self, key_var, to_compare, var_operator=''):
		"""Logic operation, value comparation"""
		dprint(f"[+]Checking if: {key_var}=>{var_operator}=>{to_compare}")
		game_value = self.game_vars.get(key_var)
		to_compare = self.var_process(to_compare)[1]

		if game_value:
			game_value = self.game_vars[key_var]
		#elif game_value is None:
		#	print(f"\t[!]Variable '{key_var}'' not declared.")
		#	game_value = False
		#	return game_value

		dprint(f'\t[+]Comparing {to_compare} {var_operator} {game_value}')
		
		if var_operator in self.regex['is']:
			dprint(f"\t\t[+]Equal operation {to_compare} -> {game_value}")
			return True if to_compare == game_value else False

		if var_operator in self.regex['not']:
			dprint(f"\t\t[+]Is not operation {to_compare} -> {game_value}")
			return True if to_compare != game_value else False

		elif var_operator in self.regex['in']:
			list = self.game_vars.get(to_compare)
			if list:
				dprint(f"\t\t[+]In operation {key_var} -> {list}")
				key_var = self.var_process(key_var)[1]
				return True if key_var in list else False

	def set_game_var(self, event):
		"""Var game setting manager"""
		var_asign_pattern = re.compile(self.regex['asign_value'])  # var=val
		var_format = var_asign_pattern.findall(event)
		if not var_format:
			dprint(f"[-]Format var asign error\n\t\t\t line:'{event}'")
			return False
		var_name = var_format[0][0]
		var_operation = var_format[0][1]
		var_type, var_value = self.var_process(
			var_format[0][2])  # list | str | bool
		dprint(f"[+]Setting: {var_name} {var_operation} {var_value}")
		if var_operation == '=' and var_type == 'list':  # List asign
			dprint(f"\t[>]Asigning list {var_value}")
			self.game_vars[var_name] = var_value
			return True
		elif var_operation == 'add':  # List add element
			dprint(f"\t[+]Adding element {var_value} to {var_name}")
			self.game_vars[var_name].append(var_value)
			return True
		elif var_operation == '=':
			self.game_vars[var_name] = var_value
			return True

	def string_manager(self, string):
		# String formating
		scope_vars = re.findall(self.regex['var_scope'], string)
		for svar in scope_vars:
			svalue = re.findall(self.regex['var_scope_value'], svar)[0]
			if(self.game_vars.get(svalue)):
				value = self.game_vars[svalue]
				if(len(value) <= 1):
					string = string.replace(svar, value[0])
				else:
					string = string.replace(svar, str(value))
		self.output_buffer.append(string)
		dprint(f"[+]PRINTING:{string[0:40]}...")
		return string

	def set_status_message(self, content):
		dprint("[+]Setting status message:", content)
		status_message = re.split(
			self.regex['custom_instruction'].format('STATUS'), content)
		if(status_message):
			self.game_status_message = status_message[0]

	def set_show_image(self, content):
		dprint("[+]Setting image show:", content)
		if(content):
			self.game_show_image = content.strip()
		else:
			dprint(f"[-]Image {content} not found!")
			
	def interpret_instruction(self, inst_type, content):
		"""Process game instruction"""
		if   inst_type == ':':  # asign varaible
			self.set_game_var(content)
		if   inst_type == '&':  # call scene
			self.callStage(content)
		elif inst_type == '':  # string
			self.string_manager(content)
		elif inst_type == 'END':  # end game
			self.finishAdventure()
		elif inst_type == 'STATUS':  # return status message
			self.set_status_message(content)
		elif inst_type == 'IMAGE':
			self.set_show_image(content)
		return False
		
	def if_struct_validation(self, params): #return True or False :p
		and_gate = self.regex['and']
		or_gate  = self.regex['or']

		is_operator = self.regex['is']
		not_operator =self.regex['not']
		in_operator = self.regex['in']

		logic_gates = re.compile(and_gate+or_gate)
		eq_operators= re.compile(is_operator + not_operator + in_operator)  # is, ==, is not, !=

		strip_list = lambda list: [e.strip() for e in list]
		strip_operators = lambda rgx, string: strip_list(rgx.split(string))

		#separate by logic gates
		logic_operators = strip_list(logic_gates.findall(params)) # and, or	
		params = strip_operators(logic_gates, params) # param1, param2 in param1 and param2

		return_status = None
		for num, operation in enumerate(params):
			if operation:
				params = strip_operators(eq_operators, operation)
				operators =  strip_list(eq_operators.findall(operation))
				if logic_operators and num>=1:
					if(return_status is False and logic_operators[0] in and_gate):#and
						break
					if(return_status and logic_operators[0] in or_gate):#or
						break
					logic_operators.pop(0)
				if operators:
					return_status = self.check_game_var(
						params[0], params[1], operators[0])
				
		return return_status

	def process_code_line(self, line):
		"""Process a line code"""
		if not line:  # empty line
			return False, False
		line = line.strip()
		ins_sign = re.match(self.regex['instruction_types'], line)
		sign, content = False, False
		if ins_sign:
			sign = line[:ins_sign.end()]
			content = line[ins_sign.end():]
		if(ins_sign == False
		   and tab_pattern.findall(line) == False
		   and line != ''):
			dprint("[!] Unrecognized line:", line, ":everprint")
		return sign, content

	def interpret_block_code(self, code):
		"""Analyze and execute block of code from a file"""
		if_index = {}  # tab level
		min_lvl = False
		for line in code.splitlines():
			tabs_count = re.match('\t+', line)
			tab_lvl = tabs_count.end() if tabs_count else 0
			inst_type, content = self.process_code_line(line)
			if inst_type == '?':  # If
				if not min_lvl:
					min_lvl = tab_lvl
				if_index[tab_lvl] = self.if_struct_validation(content)
			if inst_type == '?else':  # else
				c_ver = if_index[tab_lvl]
				if_index[tab_lvl] = False if c_ver is True else True

			if tab_lvl-1 in if_index and if_index[tab_lvl-1]:
				if(if_index.get(min_lvl) and if_index[min_lvl]):
					self.interpret_instruction(inst_type, content)
			if tab_lvl == min_lvl or min_lvl is False:
				self.interpret_instruction(inst_type, content)
		return True

if __name__ == '__main__':
	n = advInterpreter()
	code = """:variable_prueba = 'algo'
	:variable_2 = 13
	:variable_3 = 14
	:lista = [llave1, llave2]
	:silla_color = 4
	?llave2 in lista
		La silla es roja
	"""
	n.interpret_block_code(code)

	print(n.game_vars)
	print(n.output_buffer)