import io, os


class IOHandler:
    def __init__(self, file_input:str):
        self.input_path = file_input
        self.buffer_ = b''
        support = ["utf-8", "cp1256"]
        try:
            with io.open(self.input_path, mode='rb') as source:
                source.read().decode(errors='strict')
            self.buffer_ = io.open(self.input_path, mode="rb").read()
            return
        except UnicodeDecodeError:
            """
                File Is Not Readable
            """
            for encoding in support:
                self.try_decode(self.input_path, encoding)
                if self.buffer_: break
                
    @property
    def io(self):
        if bool(self): return io.BytesIO(self.buffer_)

    @property
    def basename(self):
        if bool(self): return os.path.basename(self.input_path)

    def set_file(self, file_input:str, encoding:str):
        with io.open(file_input, mode="rb") as f:
            self.buffer_ += f.read().decode(errors="replace", encoding=encoding).encode()

    def try_decode(self, file_input:str, encoding:str=None):
        try:
            with io.open(file_input, mode='rb') as source:
                source.read().decode(errors='strict',encoding=encoding)
            self.set_file(file_input, encoding)
        except UnicodeDecodeError:
            return

    def __bool__(self): return bool(self.buffer_)

    def __str__(self): return f'<subtitle.editor.IOHandler ({self.basename})>'
