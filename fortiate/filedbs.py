"""
WARNING: THESE CLASS ARE NOT YET USABLE.

Here are some class for indent or json file related class.
They may act or be used like a DB.
"""


class TextFile():
    """
    Shell examples:

    >>> text_file = TextFile(file_path=r'/text/file/path/my_file.txt')
    >>> print(text_file.lines[0])
    the first line of my_file.txt

    >>> print(text_file.lines[1])
    the second line of my_file.txt

    >>> print(text_file.stripped_lines[0])
    the first line of my_file.txt
    >>> exit()

    """
    def __init__(self, file_path, encoding='utf-8'):
        self.file_path = file_path
        with open(file=self.file_path, encoding=encoding) as file:
            self.lines = file.readlines()
        self.stripped_lines = [line.strip() for line in self.lines]

    def __repr__(self):
        return f'A text file, living at {self.file_path}'

    def __str__(self):
        return f'A text file, living at {self.file_path}'


class IndentLine():
    """
    A line with indent.
    """
    def __init__(self, line, indent='    '):
        self.line = line
        self.indent = 0
        for index, word in enumerate(line):
            if word != ' ':
                self.indent = index
                break

    def __str__(self):
        return self.line

    def __repr__(self):
        return self.line


class IndentTextFile(TextFile):
    """
    Description of index and text of a line.
    """

    def __init__(self, file_path, encoding='utf-8'):
        super().__init__(file_path=file_path, encoding=encoding)

    def __repr__(self):
        return f'A indent text file, living at {self.file_path}'

    def __str__(self):
        return f'A indent text file, living at {self.file_path}'


class FortiConfigBlock():
    """
    Config blcok of Forti devices.
    """
    def __init__(self, lines):
        self.head = lines[0]
        self.foot = lines[-1]
        self.body = lines[1:-1]

    def __repr__(self):
        return self.text

    def __str__(self):
        return self.text


class FortiConfig():
    """FortiConfig"""

    def __init__(self, file_path, head, encoding='utf-8', foot='end', ignore_lines=('')):
        self.file_path = file_path
        self.head = head
        self.encoding = encoding
        self.foot = foot
        self.ignore_lines = ignore_lines
        with open(file=self.file_path, encoding=self.encoding) as file:
            lines_strip = [line.strip() for line in file.readlines()]
        # Find head
        found_head = False
        for index, line in enumerate(lines_strip):
            if line == head:
                found_head = True
                index_head = index
                break
        if not found_head:
            raise Exception('There is no head found in this file.')
        # Find foot
        found_foot = False
        for index, line in enumerate(lines_strip[index_head + 1:]):
            if line == foot:
                found_foot = True
                index_foot = index
                break
        if not found_foot:
            raise Exception('There is no foot found in this file.')
        # Cut the lines before head and lines after foot
        lines_head_to_foot = lines_strip[index_head:index_head + index_foot + 2]
        self.lines = []
        for index, line in enumerate(lines_head_to_foot):
            if line.startswith('set', 0):
                self.lines.append(line)
                continue
            elif line.startswith('edit', 0):
                self.lines.append(line)
                continue
            elif line == 'next':
                self.lines.append(line)
                continue
            elif line in self.ignore_lines:
                pass
            elif line == self.head:
                self.lines.append(line)
                continue
            elif line == self.foot:
                self.lines.append(line)
                continue
            else:
                raise Exception(f'An invalid line is found at the file, index = {index}, line = {line}')
