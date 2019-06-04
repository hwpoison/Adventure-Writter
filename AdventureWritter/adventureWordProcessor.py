import json
from .debug import dprint

class adventureWordProcessor():
	"""A rudimentary method to detect simple sentence consistencys"""
	def __init__(self):
		self.dictionary = {}

	def load_dictionary(self, filename):
		try:
			self.dictionary = json.loads(open(filename, 'r').read())
			dprint(f"[+]Dictionary {filename} loaded.")
		except FileNotFoundError:
			dprint(f"[-]Word dictionary {filename} not found")
		return {}

	def process(self, sentence, actions=[]):
		# dprint(f"[+]Scanning action {sentence}.")
		if(self.dictionary is None):
			dprint("[-]Word dictionary not initialized")
			return False
		for action in actions:
			if(self.compare(action, sentence)):
				return action

	def word_type(self, word):
		# return type and attributes
		for type_key, word_keys in self.dictionary.items():
			for tword, attrs_ in word_keys.items():
				if(tword == word or word in attrs_):
					return type_key, attrs_
		return 'sustantive', ['None']
	
	def check_consistency(self, sentence):
		#el perro | de perro |
		pattern = {'sustantive':
				[['verb', 'article'], ['verb', 'preposition', False]]
		}
		consistency = {}
		for word in sentence.split(' '):
			type_, attr_ = self.word_type(word)
			consistency[type_] = attr_, word
		consistency_list = [i for i in consistency.keys()]
		for index, type_ in enumerate(consistency_list):
			# print(index, type_)
			attrs = consistency[type_][0]
			if(type_ in pattern):
				#prev word
				prev, nxt = False, False
				if(index-1 >= 0):
					pre = consistency_list[index-1]
					if(pre in pattern[type_][0]):
						prev = pre
				#next word
				if(index+1 < len(consistency_list)):
					nex = consistency_list[index+1]
					if(nex in pattern[type_][1]):
						nxt = nex
				if(prev == 'article' and type_ == 'sustantive'):
					#check sex | la puerta != el puerta
					if(consistency[pre][0][0] not in consistency[type_][0]):
						return False
		if(consistency.get('verb') and consistency.get('sustantive')):
			return consistency['verb'][0][0], consistency['sustantive'][1]
		return consistency

	def compare(self, original, tocompare):
		for word in original.split(" "):
			if(word not in tocompare.split(" ")):
				return False
		return True

if __name__ == "__main__":
	processor = adventureWordProcessor()
	cmp = processor.compare("mirar techo", "mirar el techo")
	print(cmp)