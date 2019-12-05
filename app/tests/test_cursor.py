from ..cursor import *

def test_cursor_encode():
    res = encode_cursor([{'_score':'desc'},{'accession': 'asc'}],'SRP00001')
    assert res == 'X3Njb3JlfHxkZXNjfHx8YWNjZXNzaW9ufHxhc2N8fHx8U1JQMDAwMDE='

def test_cursor_decode():
    res = decode_cursor('X3Njb3JlfHxkZXNjfHx8YWNjZXNzaW9ufHxhc2N8fHx8U1JQMDAwMDE=')
    assert len(res) == 2
    assert res[1] == 'SRP00001'
    assert len(res[0]) == 2
