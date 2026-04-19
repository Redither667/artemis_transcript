from artemis_transcript import *


def md_test():
    md_output = MarkdownOutput(Path('output/transcipted.md'), 'w', encoding='utf-8')
    md_output.write_story_line('共通线')
    with open('source/0_kyo_01.ast', 'r', encoding='utf-8') as f:
        parse_ast(f.read(), md_output)


def docx_test():
    docx_output = DocxOutput(Path('output/0-kyo.docx'))
    docx_output.write_story_line('共通线')
    with open('source/0_kyo_01.ast', 'r', encoding='utf-8') as f:
        parse_ast(f.read(), docx_output)

    docx_output = DocxOutput(Path('output/3-say-1.docx'))
    docx_output.write_story_line('纱由美线Part Ⅰ')
    with open('source/3_say_01-01.ast', 'r', encoding='utf-8') as f:
        parse_ast(f.read(), docx_output)

    docx_output = DocxOutput(Path('output/3-say-2.docx'))
    docx_output.write_story_line('纱由美线Part Ⅱ')
    with open('source/3_say_02-01.ast', 'r', encoding='utf-8') as f:
        parse_ast(f.read(), docx_output)

    docx_output = DocxOutput(Path('output/3-say-3.docx'))
    docx_output.write_story_line('纱由美线Part Ⅲ')
    with open('source/3_say_03-01.ast', 'r', encoding='utf-8') as f:
        parse_ast(f.read(), docx_output)

if __name__ == '__main__':
    docx_test()
