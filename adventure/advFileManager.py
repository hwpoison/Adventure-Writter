import re

from adventure.debug import dprint


class advFileManager(object):
    """
            open_stage_file : open file, check integrity and extract blocks
            load_stage_file : dump stage content
    """

    def __init__(self):
        self.current_directory = False

    def open_stage_file(self, filename):
        """Open and read adventure file"""
        try:
            full_name = filename
            stage_content = open(full_name, "r", encoding="utf-8").read()
        except FileNotFoundError as error:
            dprint(f"[!]Stage file not found:",
                   filename)
            print(filename, " is not found")
            return False
        code_block = re.compile(r'([#\!\¡])([áéíóúa-zA-Z0-9_-\|-\s-]*)\{(.*?)\}',
                                re.MULTILINE | re.DOTALL)
        blocks = code_block.findall(stage_content)
        if blocks:
            return blocks
        return False

    def load_stage_file(self, stage_file, adv_dir=''):
        """Open stage file and initialize vars"""
        if adv_dir:
            dprint(f"[+]Setting current directory in {adv_dir}")
            self.current_directory = adv_dir
        if not self.current_directory:
            self.current_directory = ''
        full_name = f"{self.current_directory}\\{stage_file}.adventure"
        dprint(f"[+]Loading {full_name[-10:]}...")
        parser_content = self.open_stage_file(full_name)
        if not parser_content:
            dprint(
                "[!]Error to load stage, invalid content or empty file")
            return False
        return parser_content


if __name__ == '__main__':
    p = adventureFileParser()
    load = p.load_stage_file('habitacion0')
    print(load)
