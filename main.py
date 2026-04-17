import functools
from abc import ABC, abstractmethod
from argparse import ArgumentParser
from collections.abc import Callable
from pathlib import Path

from lupa import LuaRuntime
from typing import Optional, override


class OutputFuncSet(ABC):
    @abstractmethod
    def write_story_line(self, text: str):
        ...

    @abstractmethod
    def write_save_title(self, text: str):
        ...

    @abstractmethod
    def write_line(self, name: Optional[str], text: str):
        ...

    @abstractmethod
    def newline(self):
        ...


def parse_ast(ast_text: str, output_func_set: OutputFuncSet):
    lua = LuaRuntime(unpack_returned_tuples=True)
    lua.execute(ast_text)
    if lua.globals().astver != 2.0:
        raise ValueError('Artemis version is not 2.0 or not found')
    ast_name = lua.globals().astname
    if ast_name is None:
        ast_name = 'ast'
    ast = lua.globals().__getattribute__(ast_name)
    try:
        top_block = ast['label']['top']['block']
    except TypeError:
        raise ValueError('top block not found')
    current_block = top_block
    while current_block is not None:
        block = ast[current_block]
        for attr in block:
            assert type(attr) is int
            match block[attr][1]:
                case 'savetitle':
                    output_func_set.write_save_title(block[attr]['text'])
                case 'text':
                    break
                case 'excall':
                    with open(f'source/{block[attr]['file']}.ast', 'r', encoding='utf-8') as ex_f:
                        parse_ast(ex_f.read(), output_func_set)
                case _:
                    pass  # TODO: parse other options
        text = block['text']
        try:
            ja = text['ja'][1]
        except TypeError:
            current_block = block['linknext']
            continue
        if ja['name'] is not None:
            name = ja['name'][2]
        else:
            name = None
        for attr in ja:
            if type(attr) is int:
                if type(ja[attr]) is str:
                    if ja[attr] == '　':
                        break
                    output_func_set.write_line(name, ja[attr])
                try:
                    if ja[attr][1] == 'rt2':
                        output_func_set.newline()
                except TypeError and IndexError:
                    pass

        current_block = block['linknext']


class MarkdownOutput(OutputFuncSet):
    def __init__(self, file: Path, *args, **kwargs):
        self.file = open(file, *args, **kwargs)

    def __del__(self):
        self.file.close()

    @override
    def write_story_line(self, text: str):
        self.file.write(f'# {text}\n')

    @override
    def write_save_title(self, text: str):
        self.file.write(f'## {text}\n')

    @override
    def write_line(self, name: Optional[str], text: str):
        if name is None:
            self.file.write(text)
        else:
            self.file.write(f'{name}：{text}')

    @override
    def newline(self):
        self.file.write('  \n')


if __name__ == '__main__':
    md_output = MarkdownOutput(Path('output/transcipted.md'), 'w', encoding='utf-8')
    md_output.write_story_line('共通线')
    with open('source/0_kyo_01.ast', 'r', encoding='utf-8') as f:
        parse_ast(f.read(), md_output)
        # parse_ast('astver = 2.0\nast = {label = {top = {block = "1"}}}')
