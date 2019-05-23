from AdventureWritter.adventureCore import AdventureCore
import configparser
#disable script debug messages
config = configparser.ConfigParser()
config.read('config.ini')
is_debug = config['DEBUG']
if(is_debug.getboolean('debug')):
	config['DEBUG']['debug'] = 'False'
with open('config.ini', 'w') as configfile:
	config.write(configfile)


class Game(AdventureCore):
	def __init__(self):
		super(Game, self).__init__()

	def main(self):

		self.loadDictionary("spanish_words.json")
		self.openAdventure("habitacion0", "test_adventure/")
		while self.in_game:
			action = input(">")
			if(action):
				self.executeAction(action)


if __name__ == '__main__':
	game = Game()
	game.main()