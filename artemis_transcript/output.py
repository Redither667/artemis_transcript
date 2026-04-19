from pathlib import Path
from typing import override, Optional

from artemis_transcript.core import OutputFuncSet


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
    def write_select_title(self, text: str):
        self.file.write(f'### {text}\n')

    @override
    def write_text(self, name: Optional[str], text: str, face: Optional[str] = None):
        if name is None:
            assert face is None
            self.file.write(text)
        else:
            if face is None:
                self.file.write(f'{name}：{text}')
            else:
                self.file.write(f'{name}:')
                self.write_text_in_parenthesis(face)
                self.file.write(text)

    @override
    def write_text_in_parenthesis(self, text: str):
        self.file.write(f'（*{text}*）')

    @override
    def write_italic_text(self, text: str):
        self.file.write(f'*{text}*')

    @override
    def newline(self):
        self.file.write('  \n')