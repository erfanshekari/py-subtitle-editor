import re
from .exceptions import InvaidWEBVTTFile
from .io import IOHandler

class BaseParser:
    def __init__(self, input:IOHandler):
        self.io = input
        self.ary = []
        self.base_name = self.io.basename

        """
            This Block Read Input File Line By Line
            ----> When We Find A "-->" In Line We Know It's A New Block So We Increment Block ID By One
            ----> Any String After Time And Bofore Next Block Will Be Consider As Current Block Text Content
            ----> (self.expect_target) This Property Lock On Block Target Field, Chocies Are : "time" and "content"
            -------------------------------------------------------------------------------------------------
            <Read Start
        """
        self.block_id = 0
        self.expect_target = 'time' # options are, 'time', 'content'
        for line in self.io.io:
            line_as_string = line.decode('utf-8')
            if line != b'\r\n':
                number = self.search_number(line_as_string)
                time = self.search_time(line_as_string)
                if time:
                    self.ary.append({})
                    self.ary[self.block_id]['timetrack'] = time
                    self.block_id += 1
                    self.expect_target = 'content'
                if self.expect_target == 'content' and not time and not number:
                    if self.ary[self.block_id -1].get('timetrack', None):
                        if not self.ary[self.block_id -1].get('content', None):
                            self.ary[self.block_id -1]['content'] = ''
                        self.ary[self.block_id -1]['content'] += line_as_string
        """
            Read End />
        """

    def match_number(self, string) -> re.Match:
        return re.match(r'^[0-9]+$', string)
    
    def search_number(self, line) -> int:
        search = self.match_number(line.strip())
        if search:
            try:
                return int(line.strip())
            except: pass
        return None

    def match_time(self, string) -> re.Match:
        reg_time = r'(([+-]?(?=\.\d|\d)(?:\d+)?(?:\.?\d*))(?:[eE]([+-]?\d+))?(:([+-]?(?=\.\d|\d)(?:\d+)?(?:\.?\d*))(?:[eE]([+-]?\d+))?)+)'
        return re.match(reg_time, string)

    def search_time(self, line) -> list:
        search = self.match_time(line)
        if search:
            splited_times = line.strip().split('-->')
            if len(splited_times) != 2:return None
            if bool(self.match_time(splited_times[0]) and self.match_time(splited_times[0])):
                return (lambda T: [S.replace(",", ".") for S in T] if "," in T[0] or "," in T[1] else T)(splited_times)
        return None

    @property
    def as_array(self) -> list:
        return self.ary

    @property
    def as_objects(self) -> dict:
        if bool(self):
            blocks = []
            for index, obj in enumerate(self.ary):
                if obj.get('timetrack', None):
                    """

                        Block Example:
                        {
                            "id": "1",
                            "timetrack": ["00:00:00.000", "00:00:00.000"],
                            "content": "content as Text String..."
                        }
                    """
                    blocks.append({
                        'id': index + 1,
                        'timetrack': obj.get('timetrack', None),
                        'content': obj.get('content', '')
                    })
            return blocks


class SRTparser(BaseParser):
    def __init__(self, input:IOHandler):
        super(SRTparser, self).__init__(input)
        self.kind = 'srt'
    
    def __str__(self):
        return f'<SRTparser.class file={self.base_name} >'

    def __bool__(self):
        return bool(self.ary)


class WEBVTTparser(BaseParser):
    def __init__(self, input:IOHandler):
        super(WEBVTTparser, self).__init__(input)
        for first_line in self.file_as_bytes:
            if 'WEBVTT' not in first_line.decode():
                raise InvaidWEBVTTFile()
            break
        self.kind = 'webvtt'
    
    def __str__(self):
        return f'<WEBVTTparser.class file={self.base_name} >'

    def __bool__(self):
        return bool(self.ary)
