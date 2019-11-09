"""enconde and decode a cursor

Given a list of sort items (dicts) and a tiebreaker ID,
create a cursor that can be encoded/decoded for use in 
search_after (or search_before) queries.

>>> encode_cursor([{'_score':'desc'},{'accession': 'asc'}],'SRP00001')
b'X3Njb3JlfHxkZXNjfHx8YWNjZXNzaW9ufHxhc2N8fHx8U1JQMDAwMDE=\n'

>>>  decode_cursor(b'X3Njb3JlfHxkZXNjfHx8YWNjZXNzaW9ufHxhc2N8fHx8U1JQMDAwMDE=\n')
([{b'_score': b'desc'}, {b'accession': b'asc'}], b'SRP00001')
"""
import base64


def encode_cursor(sort_dict: list, resp) -> str:
    sort_items = []
    for d in sort_dict:
        sort_items.append("{}||{}".format(*d.popitem()))
    cursor_string = "|||".join(sort_items) + "||||{}".format(resp)
    return base64.b64encode(cursor_string.encode('UTF-8')).decode('UTF-8')



def decode_cursor(cursor_string: str):
    (kvs, id) = base64.b64decode(cursor_string.encode('UTF-8')).split(b"||||")
    sort_items = kvs.split(b'|||')
    sort_dict = []
    for item in sort_items:
        sort_dict.append(dict((item.split(b'||'),)))
    return (sort_dict, id.decode('UTF-8'))
