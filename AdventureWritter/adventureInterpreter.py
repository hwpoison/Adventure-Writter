from .source_Regex import SourceRegex
from .debug import dprint
import re


class adventureInterpreter():
	"""docstring for adventureInterpreter"""
	def __init__(self):
		super(adventureInterpreter, self).__init__()
		self.game_vars = {}
		self.game_status_message = None
		self.output_buffer = []
	
	def reset_vars(self):
		self.game_vars = {}
		self.output_buffer = []
		self.game_status_message = None

	def clear_output_buffer(self):
		self.output_buffer = []
		
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
		dprint(f"[+]Checking if: {key_var}=>{var_operator}=>{to_compare}")
		game_value = self.game_vars.get(key_var)
		to_compare = self.var_process(to_compare)[1]
		if(game_value):
			game_value = self.game_vars[key_var]
		elif(game_value is None):
			dprint(f"\t[!]Variable '{key_var}'' not declared.")
			game_value = False
			return game_value

		dprint(f'\t[+]Comparing {to_compare} {var_operator} {game_value}')
		if(var_operator == 'is'):
			dprint(f"\t\t[+]Equal operation {to_compare} -> {game_value}")
			return True if to_compare == game_value else False

		if(var_operator == 'is not'):
			dprint(f"\t\t[+]Is not operation {to_compare} -> {game_value}")
			return True if to_compare != game_value else False

		elif(var_operator == 'in'):
			list_ = self.game_vars.get(to_compare)
			if(list_):
				dprint(f"\t\t[+]In operation {key_var} -> {list_}")
				key_var = self.var_process(key_var)[1]
				return True if key_var in list_ else False

	def set_game_var(self, event):
		"""Var game setting manager"""
		var_asign_pattern = re.compile(SourceRegex.asign_value_regx)  # var=val
		var_format = var_asign_pattern.findall(event)
		if var_format == []:
			dprint(f"[-]Format var asign error\n\t\t\t line:'{event}'")
			return False
		var_name = var_format[0][0]
		var_operation = var_format[0][1]
		var_type, var_value = self.var_process(
			var_format[0][2])  # list | str | bool
		dprint(f"[+]Setting: {var_name} {var_operation} {var_value}")
		if(var_operation is '=' and var_type is 'list'):  # List asign
			dprint(f"\t[>]Asigning list {var_value}")
			self.game_vars[var_name] = var_value
			return True
		elif(var_operation == 'add'):  # List add element
			dprint(f"\t[+]Adding element {var_value} to {var_name}")
			self.game_vars[var_name].append(var_value)
			return True
		elif(var_operation == '='):
			self.game_vars[var_name] = var_value
			return True

	def string_manager(self, string):
		# String formating
		scope_vars = re.findall(SourceRegex.var_scope_regx, string)
		for svar in scope_vars:
			svalue = re.findall(SourceRegex.var_scope_value_regx, svar)[0]
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
			SourceRegex.custom_instruction.format('STATUS'), content)
		if(status_message):
			self.game_status_message = status_message[0]
			
	def interpret_instruction(self, inst_type, content):
		"""Process game instruction"""
		if(inst_type == ':'):  # asign varaible
			self.set_game_var(content)
		if(inst_type == '&'):  # call scene
			self.stage_call_function(content)
		elif(inst_type == ''):  # string
			self.string_manager(content)
		elif(inst_type == 'END'):  # end game
			self.finish_adventure()
		elif(inst_type == 'STATUS'):  # return status message
			self.set_status_message(content)
		return False
		
	def if_struct_validation(self, params):
		# If validator
		equality_disset_pattern = r'\s('
		equality_disset_pattern += SourceRegex.check_notis_regx
		equality_disset_pattern += SourceRegex.check_is_regx
		equality_disset_pattern += SourceRegex.check_in_regx
		equality_disset_pattern += r')\s'
		if_disset = re.compile(r'\s'+SourceRegex.and_regx+SourceRegex.or_regx+r'\s')
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
					dprint(f"[+]Error in if '{params}'' analisis")
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
				dprint(f"[IF]Result of '{operation}' is {return_status}")
				if(len(gate_ops) == 0):
					return return_status
				actual_gate = gate_ops[num-1]

		return return_status  # True | False

	def process_code_line(self, line):
		"""Process a line code"""
		if(line == ''):  # empty line
			return False, False
		line = line.strip()
		ins_sign = re.match(SourceRegex.instruction_types, line)
		sign, content = False, False
		if(ins_sign):
			sign = line[:ins_sign.end()]
			content = line[ins_sign.end():]
		if(ins_sign is False
		   and tab_pattern.findall(line) is False
		   and line is not ''):
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

if __name__ == '__main__':
	n = adventureInterpreter()
	n.interpret_block_code(":variable_prueba = 'algo'")
	n.interpret_block_code("PRINT 'Parece funcionar bien'")
	print(n.game_vars)