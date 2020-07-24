import shlex


class Parser():

    def get_leading_spaces(self, string, space=' '):
        leading_spaces = (
            len(string) - len(string.lstrip(space))
        ) * space
        return leading_spaces

    def get_formatted_lines(self, lines):
        formatted_lines = [
            [
                self.get_leading_spaces(string=line)
            ] + shlex.split(line)
            for line in lines
        ]
        return formatted_lines

    def get_formatted_dct(self, formatted_lines):
        current_config = ''
        current_edit = ''
        formatted_dct = {}
        for index, line in enumerate(formatted_lines):
            if len(line) < 2:
                raise Exception(f'An invalid line exsits in config file, index = {index}, line = {line}.')
            indent, *values = line
            prefix = values[0]
            if prefix not in ['config', 'end', 'edit', 'next', 'set']:
                raise Exception(f'A line with unknown prefix exsits in config file, index = {index}, line = {line}.')
            if prefix == 'config':
                current_config = ' '.join(values)
                formatted_dct[current_config] = {}
                continue
            if prefix == 'edit':
                current_edit = ' '.join(values)
                formatted_dct[current_config][current_edit] = {}
                continue
            if prefix in ['next', 'end']:
                continue
            # Here, it should be true that prefix == 'set'
            current_set = ' '.join(values[0:2])
            formatted_dct[current_config][current_edit][current_set] = ' '.join(values[2:])
        return formatted_dct

    def get_reorganize_lines(self, formatted_lines):
        return [line[0] + shlex.join(line[1:]) for line in formatted_lines]


class IndentShellLine():

    def __init__(self, text, space=' ', line_feed_list=['\n', ]):
        self.space = space
        self.line_feed_list = line_feed_list
        for line_feed in self.line_feed_list:
            if line_feed in text[:-1]:
                raise Exception('A line feed exists in the line.')
        self.text = text
        self.indent = self.get_indent()
        self.formatted = self.get_formatted()

    def get_indent(self):
        indent = (
            len(self.text) - len(self.text.lstrip(self.space))
        ) * self.space
        return indent

    def get_formatted(self):
        formatted = shlex.split(self.text, posix=False)
        return formatted

    def rebuild(self):
        self.text = self.indent + ' '.join(self.formatted)
