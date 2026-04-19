from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional

from lupa import LuaRuntime


class OutputFuncSet(ABC):
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
    def write_text(self, name: Optional[str], text: str, face: Optional[str] = None):
        ...

    @abstractmethod
    def write_text_in_parenthesis(self, text: str):
        ...

    @abstractmethod
    def write_italic_text(self, text: str):
        ...

    @abstractmethod
    def newline(self):
        ...


def get_label_block(ast, label_name: str) -> str:
    label = ast['label'][label_name]
    assert label['label'] == 1
    return label['block']


class BlockType(Enum):
    text = auto()
    excall = auto()
    select = auto()


@dataclass
class Selection:
    label: str
    exp: str
    text: str
    display: str


@dataclass
class Fg:
    face: str


def parse_ast(ast_text: str, output: OutputFuncSet):
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
                    if block[attr]['file'] is not None:
                        with open(f'source/{block[attr]['file']}.ast', 'r', encoding='utf-8') as ex_file:
                            parse_ast(ex_file.read(), output)
                    elif block[attr]['label'] is not None and block[attr]['call'] == 0:
                        block_type = BlockType.excall
                case 'fg':
                    if (face := block[attr]['face']) is not None:
                        fgs[block[attr]['ch']] = Fg(face=face)
                case _:
                    pass  # TODO: parse other options
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
                if ja['name'] is not None:
                    name = ja['name'][2]
                    for key, fg in fgs.items():
                        if key != ja['name'][1]:
                            output.write_italic_text(f'{key}{fg.face}')
                            output.write_text(None, ' ')
                        else:
                            has_face = True
                    if len(fgs.keys()) > 1 or (ja['name'][1] not in fgs.keys() and len(fgs.keys()) == 1):
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
                                    output.write_text(name, ja[attr], fgs[ja['name'][1]].face)
                                else:
                                    output.write_text(name, ja[attr])
                        try:
                            if ja[attr][1] == 'rt2':
                                output.newline()
                        except TypeError and IndexError:
                            pass

                current_block = block['linknext']
            case BlockType.excall:
                current_block = block['linknext']
            case BlockType.select:
                selections: list[Selection] = []
                for attr in block:
                    assert type(attr) is int
                    match block[attr][1]:
                        case 'savetitle':
                            output.write_save_title(block[attr]['text'])
                        case 'select':
                            try:
                                selections.append(Selection(block[attr]['label'],
                                                            block[attr]['text'],
                                                            block[attr]['exp'], ''))
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
                    output.write_text(None, f'→ {ja[attr]}')
                    output.write_text_in_parenthesis(selection.exp)
                    selection.display = ja[attr]
                    selection_blocks[get_label_block(ast, selection.label)] = selection
                    output.newline()
                selection_flag = True
                current_block = block['linknext']