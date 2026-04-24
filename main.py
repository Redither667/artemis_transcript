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
_face_translation: dict[str, str] = {'普通': '普通',
                                     '驚き': '一惊',
                                     'だるい': '懒倦',
                                     'きょとん': '茫然',
                                     '微笑み': '微笑',
                                     '困り笑い': '苦笑',
                                     'イタズラ笑み': '淘气地笑',
                                     'ウインク笑み': '眨眼笑',
                                     'ウインク': '眨眼',
                                     '軽蔑笑み': '轻蔑地笑',
                                     'ぶりっ子笑い': '做作的笑',
                                     '怒り笑い': '愤怒地笑',
                                     'ひきつり笑い': '勉强笑',
                                     '笑顔': '笑颜',
                                     '目閉じ笑み': '闭上眼睛笑',
                                     '目下閉じ': '闭上眼',
                                     '苛立ち': '着急',
                                     '悲しみ': '悲伤',
                                     '悲しい': '难过',
                                     'ドヤ顔': '嘚瑟',
                                     'ドヤ顔舌なめずり': '嘚瑟地舔舌头',
                                     '得意げ': '得意',
                                     '考える': '思考',
                                     '真剣': '认真',
                                     '慌てる': '慌张',
                                     '＞ワ＜': '＞ワ＜',
                                     '軽蔑': '轻蔑',
                                     'ため息': '叹息',
                                     '照れ': '害羞',
                                     '焦り': '焦虑',
                                     '怒り': '愤怒',
                                     'ガーン': '震惊',
                                     'もー': '真是——',
                                     'ジト目': '斜眼',
                                     '感激': '感激',
                                     '目そらし': '转移视线',
                                     'キラキラ': '闪闪发光的样子',
                                     '白目キョトン': '白眼茫然',
                                     '不安': '不安',
                                     'キス': '吻',
                                     'うっとりキス': '陶醉地吻',
                                     'ディープキス': '深吻',
                                     'うっとりディープキス': '陶醉地深吻',
                                     'うっとり': '陶醉',
                                     '目がぐるぐる': '头晕眼花',
                                     'かなしーよー': '好伤心啊——',
                                     '寝ぼけ': '半梦半醒',
                                     '悔しい': '懊恼',
                                     '不満': '不满',
                                     '呆れ': '无语',
                                     '叫ぶ': '喊叫',
                                     '怒り叫び': '愤怒地叫喊',
                                     'つーん': '撅嘴',
                                     'あーん': '张嘴',
                                     }
face_translation: dict[str, str] = {}
_face_translation1: dict[str, str] = {}
for k, v in _face_translation.items():
    _face_translation1[k] = v
    _face_translation1[f'{k}素'] = f'{v}（素）'
    _face_translation1[f'{k}表'] = f'{v}（表）'
for k, v in _face_translation1.items():
    face_translation[f'{k}Ａ'] = f'{v}Ａ'
    face_translation[f'{k}Ｂ'] = f'{v}Ｂ'
movie_translation: dict[str, str] = {'yukata_op': '播放由语开场',
                                     'op': '播放OP《Q.E.D》'}
trans: Translation = Translation(bg_translation,
                                 DictDefaultReturnKey[str](face_translation),
                                 DictDefaultReturnKey[str](movie_translation))


def test(out_getter: Callable[[str], OutputFuncSet], suffix: str):
    option: ParseOption = ParseOption(trans)
    output = out_getter(f'output/0-kyo.{suffix}')
    output.write_story_line('共通线')
    with open('source/0_kyo_01.ast', 'r', encoding='utf-8') as f:
        parse_ast(f.read(), output, option=option)

    output = out_getter(f'output/3-say-1.{suffix}')
    output.write_story_line('纱由美线Part Ⅰ')
    with open('source/3_say_01-01.ast', 'r', encoding='utf-8') as f:
        parse_ast(f.read(), output, option=option)

    output = out_getter(f'output/3-say-2.{suffix}')
    output.write_story_line('纱由美线Part Ⅱ')
    with open('source/3_say_02-01.ast', 'r', encoding='utf-8') as f:
        parse_ast(f.read(), output, option=option)

    output = out_getter(f'output/3-say-3.{suffix}')
    output.write_story_line('纱由美线Part Ⅲ')
    with open('source/3_say_03-01.ast', 'r', encoding='utf-8') as f:
        parse_ast(f.read(), output, option=option)

def test_hjump(out_getter: Callable[[str], OutputFuncSet], suffix: str):
    option: ParseOption = ParseOption(trans, hjump=True)
    output = out_getter(f'output/0-kyo.{suffix}')
    output.write_story_line('共通线')
    with open('source/0_kyo_01.ast', 'r', encoding='utf-8') as f:
        parse_ast(f.read(), output, option=option)

    output = out_getter(f'output/3-say-1-hjump.{suffix}')
    output.write_story_line('纱由美线Part Ⅰ')
    with open('source/3_say_01-01.ast', 'r', encoding='utf-8') as f:
        parse_ast(f.read(), output, option=option)

    output = out_getter(f'output/3-say-2-hjump.{suffix}')
    output.write_story_line('纱由美线Part Ⅱ')
    with open('source/3_say_02-01.ast', 'r', encoding='utf-8') as f:
        parse_ast(f.read(), output, option=option)

    output = out_getter(f'output/3-say-3-hjump.{suffix}')
    output.write_story_line('纱由美线Part Ⅲ')
    with open('source/3_say_03-01.ast', 'r', encoding='utf-8') as f:
        parse_ast(f.read(), output, option=option)


def md_test():
    test(lambda x: MarkdownOutput(Path(x), 'w', encoding='utf-8'), 'md')


def docx_test():
    test(lambda x: DocxOutput(Path(x)), 'docx')

def docx_test_hjump():
    test_hjump(lambda x: DocxOutput(Path(x)), 'docx')

if __name__ == '__main__':
    docx_test_hjump()
