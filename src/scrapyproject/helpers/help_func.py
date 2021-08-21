import re

def remove_tags(text=''):
    return re.sub(r'\<[^>]*\>', '', str(text))

def clear_str(s=''):
    if isinstance(s, type(None)):
        return ''
    if isinstance(s, str):
        return remove_tags(s).strip()
    return s