"""只消费一次的资料流及行字节计量。"""
from .storage import encode

class OnceRows:
    def __init__(self,rows):self._rows=iter(rows);self.started=False;self.closed=False;self.read_bytes=0
    def __iter__(self):
        if self.started:raise RuntimeError('资料流已消费')
        self.started=True
        try:
            for row in self._rows:
                if self.closed:return
                self.read_bytes+=len(encode(row));yield row
        finally:self.close()
    def close(self):self.closed=True
