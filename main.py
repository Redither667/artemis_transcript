from collections.abc import Callable

from artemis_transcript import *

bg_translation: dict[str, str] = {'ic_say_in': 'Another view of 纱由美...',
                                  'ic_say_out': 'Another view end of 纱由美...',
                                  'ic_let_in': 'Another view of 斑鸠...',
                                  'ic_let_out': 'Another view end of 斑鸠...',
                                  'ic_shi_in': 'Another view of 诗梦...',
                                  'ic_shi_out': 'Another view end of 诗梦...',
                                  'ic_tou_in': 'Another view of 冬桦...',
                                  'ic_tou_out': 'Another view end of 冬桦...',
                                  'ic_kan_in': 'Another view of 叶梦...',
                                  'ic_kan_out': 'Another view end of 叶梦...'}
trans: Translation = Translation(bg_translation)


def test(out_getter: Callable[[str], OutputFuncSet], suffix: str):
    output = out_getter(f'output/0-kyo.{suffix}')
    output.write_story_line('共通线')
    with open('source/0_kyo_01.ast', 'r', encoding='utf-8') as f:
        parse_ast(f.read(), output, translations=trans)

    output = out_getter(f'output/3-say-1.{suffix}')
    output.write_story_line('纱由美线Part Ⅰ')
    with open('source/3_say_01-01.ast', 'r', encoding='utf-8') as f:
        parse_ast(f.read(), output, translations=trans)

    output = out_getter(f'output/3-say-2.{suffix}')
    output.write_story_line('纱由美线Part Ⅱ')
    with open('source/3_say_02-01.ast', 'r', encoding='utf-8') as f:
        parse_ast(f.read(), output, translations=trans)

    output = out_getter(f'output/3-say-3.{suffix}')
    output.write_story_line('纱由美线Part Ⅲ')
    with open('source/3_say_03-01.ast', 'r', encoding='utf-8') as f:
        parse_ast(f.read(), output, translations=trans)


def md_test():
    test(lambda x: MarkdownOutput(Path(x), 'w', encoding='utf-8'), 'md')


def docx_test():
    test(lambda x: DocxOutput(Path(x)), 'docx')

if __name__ == '__main__':
    docx_test()
