
_uniqid = 0

def get_id():
    """return a basic uniq id"""
    global _uniqid
    _uniqid += 1
    return str(_uniqid)

def clean_attrs(attrs):
    for k,v in attrs.items():
        if isinstance(v, str): continue
        attrs[k] = "%s" % v
    return attrs