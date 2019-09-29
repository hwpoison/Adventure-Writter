import configparser

from adventure.adventureCore import AdventureCore


TEST = False
if not TEST:
    # disable script debug messages
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
        #self.openAdventure("habitacion0", "test_adventure/")
        self.openAdventure("inicio", "La casa de Yoel/")
        if(TEST):
        	#test mode
            actions = ["toser", "toser"]
            for fragment in self.output_buffer:
                print(fragment)
            for i in actions:
                if(self.in_game is False):
                    return False
                self.executeAction(i)
                print("=" * 60)
                for fragment in self.output_buffer:
                    print(fragment)
                print("Actual game vars:", self.game_vars)
        else:
        	#normal mode
            while True:
                for fragment in self.output_buffer:
                    print(fragment)
                if(self.in_game is False):
                    return False
                action = input(">")
                if(action):
                    if not self.executeAction(action):
                    	print("No puedes hacer eso")


if __name__ == '__main__':
    game = Game()
    game.main()
