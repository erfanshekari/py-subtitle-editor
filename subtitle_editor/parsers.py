import io, re, os
from .exceptions import InvaidWEBVTTFile


class BaseParser:
    def __init__(self, file_input):
                
        self.input = open(file_input, 'rb')
        self.file_as_bytes = io.BytesIO(self.input.read())
        self.ary = []

        self.base_name = os.path.basename(file_input)

        self.block_id = 0
        self.target_expect = 'time' # options are, 'time', 'content'
        for line in self.file_as_bytes:
            line_as_string = line.decode('utf-8')
            if line != b'\r\n':
                number = self.search_number(line_as_string)
                time = self.search_time(line_as_string)
                if time:
                    self.ary.append({})
                    self.ary[self.block_id]['time'] = time
                    self.block_id += 1
                    self.target_expect = 'content'
                if self.target_expect == 'content' and not time and not number:
                    if self.ary[self.block_id -1].get('time', None):
                        if not self.ary[self.block_id -1].get('content', None):
                            self.ary[self.block_id -1]['content'] = ''
                        self.ary[self.block_id -1]['content'] += line_as_string

    def match_number(self, string):
        return re.match(r'^[0-9]+$', string)
    
    def search_number(self, line):
        search = self.match_number(line.strip())
        if search:
            try:
                return int(line.strip())
            except: return 


    def match_time(self, string):
        reg_time = r'(([+-]?(?=\.\d|\d)(?:\d+)?(?:\.?\d*))(?:[eE]([+-]?\d+))?(:([+-]?(?=\.\d|\d)(?:\d+)?(?:\.?\d*))(?:[eE]([+-]?\d+))?)+)'
        return re.match(reg_time, string)

    def search_time(self, line):
        search = self.match_time(line)
        if search:
            splited_times = line.strip().split('-->')
            if len(splited_times) != 2:return
            if bool(self.match_time(splited_times[0]) and self.match_time(splited_times[0])):
                return [splited_times[0].strip(), splited_times[1].strip()]

    @property
    def as_array(self):
        return self.ary

    @property
    def as_objects(self):
        if bool(self):
            objects = []
            for index, obj in enumerate(self.ary):
                if obj.get('time', None):
                    objects.append({
                        'id': index + 1,
                        'time': obj.get('time', None),
                        'content': obj.get('content', '')
                    })
            return objects



class SRTparser(BaseParser):
    def __init__(self, file_input=None):
        super(SRTparser, self).__init__(file_input)
        self.kind = 'srt'
    
    def __str__(self):
        return f'<SRTparser.class file={self.base_name} >'

    def __bool__(self):
        return bool(self.ary)


class WEBVTTparser(BaseParser):
    def __init__(self, file_input=None):
        super(WEBVTTparser, self).__init__(file_input)
        for first_line in self.file_as_bytes:
            if 'WEBVTT' not in first_line.decode():
                raise InvaidWEBVTTFile()
            break
        self.kind = 'webvtt'
    
    def __str__(self):
        return f'<WEBVTTparser.class file={self.base_name} >'

    def __bool__(self):
        return bool(self.ary)
