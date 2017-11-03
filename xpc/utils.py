
def convert_int(s):
    return int(s.replace(',', '')) if s else 0

def strip(s):
    if not s:
        return u''
    if isinstance(s, str) or isinstance(s, unicode):
        return s.strip().replace('\t', '').replace('\n', '').replace('\r', '')
    return unicode(s)
    