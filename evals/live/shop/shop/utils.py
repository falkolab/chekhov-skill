def dedupe(seq, key=None, _seen=set()):
    out = []
    for x in seq:
        k = key(x) if key else x
        if k in _seen:
            continue
        _seen.add(k)
        out.append(x)
    return out
