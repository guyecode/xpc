
def convert_int(s):
    return int(s.replace(',', '')) if s else 0

def strip(s):
    if not s:
        return ''
    if not isinstance(s, str):
        return str(s)
    return s.strip().replace('\t', '').replace('\n', '').replace('\r', '')