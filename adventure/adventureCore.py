from .adventureWordProcessor import adventureWordProcessor
from .adventureInterpreter import adventureInterpreter
from .adventureFileParser import adventureFileParser
from adventure.source_Regex import SourceRegex
from adventure.debug import dprint
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
        #Adventure in progress
        self.in_game = False
        # Adventure name
        self.adventure_name = None
        # General vars
        self.game_vars = {}

        # Availible game actions
        self.game_actions = {}
        # Executed actions
        self.executed_actions = []

        # Print output buffer
        self.output_buffer = []
        # Game status (STATUS instruction)
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
        adventure_content = self.load_stage_file(
            adventure_name, adv_dir=adventure_dir)
        if(adventure_content):
            dprint("[+]Adventure initialized!")
            self.in_game = True
            return True
        else:
            return False

    def finishAdventure(self):
        """Finish the current adventure"""
        self.in_game = False

    def registerAction(self, action, content, once=False):
        dprint(f"[+]Registring: {action}")
        action_index = len(self.game_actions)+1
        self.game_actions[action_index] = {
            'name': [i.strip() for i in action.split('|')],
            'instructions': content,
            'once': once
        }

    def executeAction(self, sentence):
        dprint(f"\n[+]Executing action: {sentence}")
        self.clear_output_buffer()
        sentence = sentence.lower()
        for index in self.game_actions:
            game_action = self.game_actions[index]
            if(sentence in game_action['name']
               or self.sentence_processor.process(sentence, game_action['name'])):
                if(game_action['once'] is True and index in self.executed_actions):
                    return False
                dprint(f"[+]Action {sentence} is found")
                self.interpret_block_code(game_action['instructions'])
                self.executed_actions.append(index)
                return True
        return None

    def resetActions(self):
        """Reset game actions"""
        dprint("[+]Game actions reseted")
        self.game_actions = {}

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

            # !!ACTION  run only once
            if(block_type == '¡'):
                self.registerAction(block_name, block_content, once=True)

        dprint(f"\n[+]Stage '{stage_name}' loaded.")
        self.stage_history.append(self.current_stage)
        return True

    def stage_call_function(self, string):
        """Load a stage (& instruction)"""
        load_stage = re.findall(SourceRegex.load_function, string)
        if(load_stage):
            self.load_stage_file(
                load_stage[0][1], adv_dir=self.file_manager.current_directory)
            return True
        return False


if __name__ == '__main__':
    pass
