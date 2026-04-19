from artemis_transcript import *


def md_test():
    md_output = MarkdownOutput(Path('output/transcipted.md'), 'w', encoding='utf-8')
    md_output.write_story_line('共通线')
    with open('source/0_kyo_01.ast', 'r', encoding='utf-8') as f:
        parse_ast(f.read(), md_output)


def docx_test():
    docx_output = DocxOutput(Path('output/transcipted.docx'))
    docx_output.write_story_line('共通线')
    with open('source/0_kyo_01.ast', 'r', encoding='utf-8') as f:
        parse_ast(f.read(), docx_output)

if __name__ == '__main__':
    docx_test()
