from .cursor import *

def test_cursur_encode():
    res = encode_cursor([{'_score':'desc'},{'accession': 'asc'}],'SRP00001')
    assert res == b'X3Njb3JlfHxkZXNjfHx8YWNjZXNzaW9ufHxhc2N8fHx8U1JQMDAwMDE=\n'

def test_cursor_decode():
    res = decode_cursor(b'X3Njb3JlfHxkZXNjfHx8YWNjZXNzaW9ufHxhc2N8fHx8U1JQMDAwMDE=\n')
    assert len(res) == 2
    assert res[1] == b'SRP00001'
    assert len(res[0]) == 2
