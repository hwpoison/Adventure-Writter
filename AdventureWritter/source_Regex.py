
class SourceRegex:
    #Regex for parser File and Code
    instruction_types = r'\?else|\?|//|\"|:|&|END|STATUS|'
    asign_value_regx = r'(.*)\s+(=|add)\s+(.*)'
    load_function = r'(LOAD|CARGAR)\s+(.*)$'
    or_regx = r'or|\|\||\so'
    and_regx = r'and|&&|'  # fix /s x/s
    check_is_regx = r'is|es|'
    check_notis_regx = r'not is|is not|'
    check_in_regx = r'|in|en'
    code_blocks_regx = r'([#\!])([áéíóúa-zA-Z0-9_-\|-\s-]*)\{(.*?)\}'
    var_scope_value_regx = r'\$(.*?)\$'
    var_scope_regx = r'(\$.*?\$)'
    file_dir_resolution = r'(.*)\\(\w+)\.adventure'
    custom_instruction = r'{0}\s+(.*)'  # ex STATUS (TEXT)
