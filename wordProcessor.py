import json


class WordProcess():
	"""A rudimentary method to detect simple sentence consistencys"""

	def __init__(self, words_file):
		self.dictionary = self.load_dictionary(words_file)

	def load_dictionary(self, filename):
		try:
			return json.loads(open(filename, 'r').read())
		except FileNotFoundError:
			print(f"[-]Word dictionary {filename} not found")
		return {}

	def word_type(self, word):
		# return type and attributes
		for word_, attr_ in self.dictionary['verb'].items():
			if(word == word_ or word in attr_):
				return {
					'word': word_,
					'attrs': attr_,
					'type': 'verb'
				}
		for word_, attr_ in self.dictionary.items():
			if(word_ == word or word in attr_):
				return {
					'word': word,
					'attrs': attr_[word],
					'type': word_
				}
		return {'type': False}

	def check_consistency(self, sentence):
		verb, item, article = False, False, False
		for word in sentence.split(' '):
			find = self.word_type(word)
			if(find['type'] == 'verb'):
				verb = find
			elif(find['type'] == 'item'):
				item = find
			elif(find['type'] == 'article'):
				article = find
			if(item and article):
				if item['attrs'][0] != article['attrs'][0]:
					return False
		return {
			'verb': verb['word'] if verb else False,
			'item': item['word'] if item else False,
			'article': article['word'] if article else False
		}

	def compare(self, original, tocompare):
		original = self.check_consistency(original)
		tocompare = self.check_consistency(tocompare)
		if(original and tocompare and original['verb'] and original['item']):
			if(original['verb'] == tocompare['verb']
					and original['item'] == tocompare['item']):
				if(original['article'] is False
						and tocompare['article']):
					return True
				elif(original['article']
						and tocompare['article'] is False):
					return True
				elif(original['article'] and tocompare['article']):
					return True
				elif(original['article'] is False
						and tocompare['article'] is False):
					return True
		return False


if __name__ == "__main__":
	processor = WordProcess('spanish_words.json')
	# print(processor.dictionary)
	a = "patear puerta"  # user input
	b = "patear la puerta"  # from file
	a = processor.compare(a, b)
	if(a):
		print("Son oraciones similares y validas")
	else:
		print("No lo son")
