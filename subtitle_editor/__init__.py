import os
from .parsers import (
    WEBVTTparser,
    SRTparser
)
from .exceptions import InvaildFileInput
from .io import IOHandler

class SubtitleEditor:
    def __init__(self, input_file:str):
        self.input_path = input_file

        self.source = IOHandler(input_file)
        if not self.source:
            raise InvaildFileInput()

        self.parsers = [
            {'type': 'srt', 'parser': SRTparser},
            {'type': 'webvtt', 'parser': WEBVTTparser},]
        self.parser = None
        splited_base_name = self.source.basename.split('.')
        for parser in self.parsers:
            if parser['type'] == splited_base_name[-1]:
                self.parser = parser['parser'](self.source)

        if not self.parser:
            raise InvaildFileInput()

        self.blocks = self.parser.as_objects

    def __bool__(self): return hasattr(self, 'blocks')

    def __str__(self): return f'<SubtitleEditor ({self.source.name})>'

    def get_block_by_id(self, id) -> dict:
        for obj in self.blocks:
            if obj.get('id', 0) == id: return obj

    def edit_block(self, id=None, timetrack=None, content=None) -> dict:
        if not id: return
        if timetrack:
            self.blocks[id - 1]['time'] = timetrack
        if content:
            self.blocks[id - 1]['content'] = content
        return self.get_block_by_id(id)
    
    def blocks_to_webvtt(self, blocks) -> str:
        webvtt_string = 'WEBVTT\n\n'
        for block in blocks:
            id = block.get('id', None)
            timetrack = block.get('timetrack', None)
            content = block.get('content', None)
            content = content.strip()
            timetrack = timetrack[0] + ' --> ' + timetrack[1]
            webvtt_string += f'{id}\n{timetrack}\n{content}\n\n'
        return webvtt_string

    def blocks_to_srt(self, blocks) -> str:
        srt_string = ''
        for block in blocks:
            id = block.get('id', None)
            timetrack = block.get('timetrack', None)
            content = block.get('content', None)
            content = content.strip()
            timetrack = timetrack[0].replace('.', ',') + ' --> ' + timetrack[1].replace('.', ',')
            srt_string += f'{id}\n{timetrack}\n{content}\n\n'
        return srt_string

    def save_webvtt(self, path:str) -> str:
        file_save = open(path, 'wb')
        file_save.write(self.blocks_to_webvtt(self.blocks).encode())
        file_save.close()
        return os.path.abspath(path)

    def save_srt(self, path:str) -> str:
        file_save = open(path, 'wb')
        file_save.write(self.blocks_to_srt(self.blocks).encode())
        file_save.close()
        return os.path.abspath(path)
    
    @property
    def webvtt_as_bytes(self) -> bytes:
        return self.blocks_to_webvtt(self.blocks).encode()

    @property
    def srt_as_bytes(self) -> bytes:
        return self.blocks_to_srt(self.blocks).encode()
