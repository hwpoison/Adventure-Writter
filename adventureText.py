import configparser

from adventure.advMain import advMain


TEST = True
if not TEST:
    # disable script debug messages
    config = configparser.ConfigParser()
    config.read('config.ini')
    is_debug = config['DEBUG']
    if(is_debug.getboolean('debug')):
        config['DEBUG']['debug'] = 'False'
    with open('config.ini', 'w') as configfile:
        config.write(configfile)


class Game(advMain):
    def __init__(self):
        super(Game, self).__init__()

    def main(self):
        self.loadDictionary("spanish_words.json")
        self.openAdventure("miniaventura_inicio", "test_adventure/")
        #self.openAdventure("inicio", "La casa de Yoel/")
        if(TEST):
        	#test mode
            actions = ["test2", "test3", "test3"]

            for fragment in self.output_buffer:
                print(fragment)
            for action in actions:
                if(self.in_game is False):
                    return False
                self.executeAction(action)
                print("=" * 60)
                print("[",action,"]")
                for fragment in self.output_buffer:
                    print(fragment)
                print()
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
