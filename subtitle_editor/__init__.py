import os
from .parsers import (
    WEBVTTparser,
    SRTparser
)
from .exceptions import InvaildFileInput


class SubtitleEditor:
    def __init__(self, input_file):
        self.input_path = input_file
        self.parsers = [
            {'type': 'srt', 'parser': SRTparser},
            {'type': 'webvtt', 'parser': WEBVTTparser},]
        self.parser = None
        self.input_base_name = os.path.basename(input_file)
        splited_base_name = self.input_base_name.split('.')
        for parser in self.parsers:
            if parser['type'] == splited_base_name[-1]:
                self.parser = parser['parser'](input_file)
        if not self.parser:
            raise InvaildFileInput()

        self.blocks = self.parser.as_objects

    def __bool__(self):
        return hasattr(self, 'blocks')

    def get_block_by_id(self, id):
        for obj in self.blocks:
            if obj.get('id', 0) == id: return obj

    def edit_block(self, id=None, timedelta=None, content=None):
        if not id: return
        if timedelta:
            self.blocks[id - 1]['time'] = timedelta
        if content:
            self.blocks[id - 1]['content'] = content
        return self.get_block_by_id(id)
    
    def blocks_to_webvtt(self, blocks):
        webvtt_string = 'WEBVTT\n\n'
        for block in blocks:
            id = block.get('id', None)
            time = block.get('time', None)
            content = block.get('content', None)
            content = content.strip()
            for index, value in enumerate(time):
                if ',' in value:
                    time[index] = value.replace(',','.')
            time = time[0] + ' --> ' + time[1]
            webvtt_string += f'{id}\n{time}\n{content}\n\n'
        return webvtt_string

    def blocks_to_srt(self, blocks):
        srt_string = ''
        for block in blocks:
            id = block.get('id', None)
            time = block.get('time', None)
            content = block.get('content', None)
            content = content.strip()
            time = time[0].replace('.', ',') + ' --> ' + time[1].replace('.', ',')
            srt_string += f'{id}\n{time}\n{content}\n\n'
        return srt_string

    def save_webvtt(self, path):
        file_save = open(path, 'wb')
        file_save.write(self.blocks_to_webvtt(self.blocks).encode())
        file_save.close()
        return os.path.abspath(path)

    def save_srt(self, path):
        file_save = open(path, 'wb')
        file_save.write(self.blocks_to_srt(self.blocks).encode())
        file_save.close()
        return os.path.abspath(path)

    def webvtt_as_bytes(self):
        return self.blocks_to_webvtt(self.blocks).encode()

    def srt_as_bytes(self):
        return self.blocks_to_srt(self.blocks).encode()