import unittest

from adventure.advInterpreter import advInterpreter

interpreter_instance = advInterpreter()


class coreTest(unittest.TestCase):
    def test_var_process(self):
        self.assertEqual(interpreter_instance.var_process(
            "string"), ('str', "string"))
        self.assertEqual(interpreter_instance.var_process(
            "['string']"), ('list', ['string']))

    def test_check_game_var(self):
        interpreter_instance.game_vars['test_var'] = 'test_value'
        interpreter_instance.game_vars['test_list'] = ['test_var', 'var2']
        # 'is' operator
        self.assertEqual(
            interpreter_instance.check_game_var(
                key_var='test_var', to_compare='test_value', var_operator='is'),
            True)
        # 'is not' operator
        self.assertEqual(
            interpreter_instance.check_game_var(
                key_var='test_var', to_compare='test_value', var_operator='is not'),
            False)
        # 'in' operator
        self.assertEqual(
            interpreter_instance.check_game_var(
                key_var='test_var', to_compare='test_list', var_operator='in'),
            True)

    def test_set_game_var(self):
        # block code interpreter
        self.assertEqual(interpreter_instance.interpret_block_code(
            ":test_var = something"), True)

        # asign var
        self.assertEqual(interpreter_instance.interpret_instruction(
            ':', "test_var = test_value"), False)

        # call scene
        #self.assertEqual(interpreter_instance.stage_call_function("no_exists_escene"), False)

        # string manager
        self.assertEqual(interpreter_instance.string_manager("hello"), 'hello')

        # conditionals
        self.assertEqual(interpreter_instance.if_struct_validation(
            "test_var is test_value"), True)

        self.assertEqual(interpreter_instance.if_struct_validation(
            "test_var_u not is test_value"), False)

        self.assertEqual(interpreter_instance.if_struct_validation(
            "test_var in test_list"), True)


if __name__ == '__main__':
    unittest.main()
