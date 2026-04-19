from artemis_transcript import *

if __name__ == '__main__':
    md_output = MarkdownOutput(Path('output/transcipted.md'), 'w', encoding='utf-8')
    md_output.write_story_line('共通线')
    with open('source/0_kyo_01.ast', 'r', encoding='utf-8') as f:
        parse_ast(f.read(), md_output)
        # parse_ast('astver = 2.0\nast = {label = {top = {block = "1"}}}')
