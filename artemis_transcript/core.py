from abc import ABC, abstractmethod, ABCMeta, update_abstractmethods
from collections import UserDict
from dataclasses import dataclass, field
from enum import Enum, auto
from operator import methodcaller
from pathlib import Path
from typing import Optional, override, TYPE_CHECKING
from warnings import deprecated

from lupa import LuaRuntime


class DeferredOperation(ABCMeta):
    def __new__(cls, name, bases, attrs):
        assert '_stored_calls' not in attrs
        attrs['_stored_calls'] = list()

        def perform_calls(self, o):
            for i in self._stored_calls:
                i(o)

        attrs['perform_calls'] = perform_calls

        new_cls = ABCMeta.__new__(cls, name, bases, attrs)

        def store_call(func_name):
            def wrapper(self, *args, **kwargs):
                self._stored_calls.append(methodcaller(func_name, *args, **kwargs))

            return wrapper

        for method in new_cls.__abstractmethods__:
            setattr(new_cls, method, store_call(method))

        update_abstractmethods(new_cls)

        return new_cls


class OutputFormat(ABC):
    @abstractmethod
    def write_story_line(self, text: str):
        ...

    @abstractmethod
    def write_save_title(self, text: str):
        ...

    @abstractmethod
    def write_select_title(self, text: str):
        ...

    @abstractmethod
    def write(self, name: Optional[str], text: str, face: Optional[str] = None):
        ...

    @abstractmethod
    def write_text_in_parenthesis(self, text: str):
        ...

    @abstractmethod
    def write_italic(self, text: str):
        ...

    @abstractmethod
    def newline(self):
        ...

    @abstractmethod
    def new_paragraph(self):
        ...


class DeferredOutput(OutputFormat, metaclass=DeferredOperation):
    if TYPE_CHECKING:
        def perform_calls(self, output):
            pass

        def write_story_line(self, text: str):
            pass

        def write_save_title(self, text: str):
            pass

        def write_select_title(self, text: str):
            pass

        def write(self, name: Optional[str], text: str, face: Optional[str] = None):
            pass

        def write_text_in_parenthesis(self, text: str):
            pass

        def write_italic(self, text: str):
            pass

        def newline(self):
            pass

        def new_paragraph(self):
            pass


@deprecated('Use DeferredOutput instead')
class _GeneralOutput(OutputFormat):
    def __init__(self):
        self.text: list[methodcaller] = list()

    def write_to(self, output: OutputFormat):
        for text in self.text:
            text(output)

    @staticmethod
    def _store_call(func):
        def wrapper(self, *args, **kwargs):
            self.text.append(methodcaller(func.__name__, *args, **kwargs))
        return wrapper

    @override
    @_store_call
    def write_story_line(self, text: str):
        pass

    @override
    @_store_call
    def write_save_title(self, text: str):
        pass

    @override
    @_store_call
    def write_select_title(self, text: str):
        pass

    @override
    @_store_call
    def write(self, name: Optional[str], text: str, face: Optional[str] = None):
        pass

    @override
    @_store_call
    def write_text_in_parenthesis(self, text: str):
        pass

    @override
    @_store_call
    def write_italic(self, text: str):
        pass

    @override
    @_store_call
    def newline(self):
        pass

    @override
    @_store_call
    def new_paragraph(self):
        pass


def get_label_block(ast, label_name: str) -> str:
    label = ast['label'][label_name]
    assert label['label'] == 1
    return label['block']


class BlockType(Enum):
    text = auto()
    excall = auto()
    select = auto()
    skip = auto()


@dataclass
class Selection:
    label: str
    exp: str
    text: str
    display: str


@dataclass
class Fg:
    face: str


class DictDefaultReturnKey[T](UserDict[T, T]):
    @override
    def __getitem__(self, key: T):
        if key in self.keys():
            return UserDict.__getitem__(self, key)
        else:
            return key


@dataclass(frozen=True)
class Translation:
    bg: dict[str, str] = field(default_factory=dict)
    face: DictDefaultReturnKey[str] = field(default_factory=DictDefaultReturnKey),
    movie: DictDefaultReturnKey[str] = field(default_factory=DictDefaultReturnKey)
    hjump: str = '跳过h scene...'


@dataclass
class ParseOption:
    translation: Translation = field(default_factory=Translation)
    path: Path = field(default_factory=lambda: Path('source'))
    hjump: bool = False


def _deferred_parse_ast(ast_text: str, output: DeferredOutput, *, option: Optional[ParseOption] = None):
    if option is None:
        option: ParseOption = ParseOption()

    lua = LuaRuntime(unpack_returned_tuples=True)
    lua.execute(ast_text)
    if getattr(lua.globals(), 'astver') != 2.0:
        raise ValueError('Artemis version is not 2.0 or not found')
    ast_name = getattr(lua.globals(), 'astname')
    if ast_name is None:
        ast_name = 'ast'
    ast = lua.globals().__getattribute__(ast_name)
    try:
        top_block = get_label_block(ast, 'top')
    except TypeError:
        raise ValueError('top block not found')

    selection_flag: bool = False
    selection_blocks: dict[str, Selection] = {}

    current_block = top_block
    while current_block is not None:
        block = ast[current_block]
        block_type = BlockType.text

        fgs: dict[str, Fg] = dict()
        pre_content: list = list()
        for attr in block:
            assert type(attr) is int
            match block[attr][1]:
                case 'savetitle':
                    output.write_save_title(block[attr]['text'])
                case 'select':
                    block_type = BlockType.select
                case 'text':
                    break
                case 'excall':
                    if (file := block[attr]['file']) is not None:
                        with open(option.path / f'{file}.ast', 'r', encoding='utf-8') as ex_file:
                            deferred_parse_ast(ex_file.read(), output, option=option)
                        return
                    elif block[attr]['label'] is not None:
                        if option.hjump and block[attr]['cond'] == 's.conf.hjump==1':
                            output.write_italic(option.translation.hjump)
                            output.newline()
                            current_block = get_label_block(ast, block[attr]['label'])
                            block_type = BlockType.excall
                        elif block[attr]['call'] == 0:
                            block_type = BlockType.skip
                case 'fg':
                    if (face := block[attr]['face']) is not None:
                        fgs[block[attr]['ch']] = Fg(face=face)
                case 'bg':
                    if (file := block[attr]['file']) is not None and file in option.translation.bg.keys():
                        pre_content.append(option.translation.bg[file])
                case 'movie':
                    pre_content.append(option.translation.movie[block[attr]['file']])
                case _:
                    pass  # TODO: parse other options

        if len(pre_content) == 1:
            output.write_italic(pre_content[0])
            output.newline()
        elif len(pre_content) > 1:
            output.write_italic('，'.join(pre_content))
            output.newline()

        match block_type:
            case BlockType.text:
                if selection_flag and current_block in selection_blocks.keys():
                    output.write_select_title(selection_blocks[current_block].display)
                text = block['text']
                try:
                    ja = text['ja'][1]
                except TypeError:
                    current_block = block['linknext']
                    continue

                has_face: bool = False
                if (full_name := ja['name']) is not None:
                    name = full_name[2]
                    for key, fg in fgs.items():
                        if key != full_name[1]:
                            output.write_italic(f'{key}{option.translation.face[fg.face]}')
                            output.write(None, ' ')
                        else:
                            has_face = True
                    if len(fgs.keys()) > 1 or (full_name[1] not in fgs.keys() and len(fgs.keys()) == 1):
                        output.newline()
                else:
                    name = None
                for attr in ja:
                    if type(attr) is int:
                        if type(ja[attr]) is str:
                            if ja[attr] == '　':
                                # output.write_text(None, '')
                                break
                            else:
                                if has_face:
                                    output.write(name, ja[attr], option.translation.face[fgs[ja['name'][1]].face])
                                else:
                                    output.write(name, ja[attr])
                        try:
                            if ja[attr][1] == 'rt2':
                                output.newline()
                        except TypeError and IndexError:
                            pass

                current_block = block['linknext']

            case BlockType.excall:
                pass

            case BlockType.select:
                selections: list[Selection] = []
                for attr in block:
                    assert type(attr) is int
                    match block[attr][1]:
                        case 'savetitle':
                            output.write_save_title(block[attr]['text'])
                        case 'select':
                            try:
                                selections.append(
                                    Selection(block[attr]['label'], block[attr]['text'], block[attr]['exp'], ''))
                            except TypeError and IndexError:
                                pass
                        case 'text':
                            break
                        case _:
                            pass

                select = block['select']
                ja = select['ja']
                for attr, selection in zip(ja, selections):
                    assert type(attr) is int and type(ja[attr]) is str
                    output.write(None, f'→ {ja[attr]}')
                    output.write_text_in_parenthesis(selection.exp)
                    selection.display = ja[attr]
                    selection_blocks[get_label_block(ast, selection.label)] = selection
                    output.newline()
                selection_flag = True
                current_block = block['linknext']

            case BlockType.skip:
                current_block = block['linknext']

            case _:
                raise ValueError('Unreachable code! block_type is not a BlockType')

def deferred_parse_ast(ast_text: str, *, option: Optional[ParseOption] = None) -> DeferredOutput:
    deferred_output = DeferredOutput()
    _deferred_parse_ast(ast_text, deferred_output, option=option)
    return deferred_output

def parse_ast(ast_text: str, output: OutputFormat, *, option: Optional[ParseOption] = None):
    deferred_parse_ast(ast_text, option=option).perform_calls(output)
