def get_dict_value_recurse(item, keys=[], default=None):
    v = item
    for k in keys:
        tmp = v.get(k, default)
        if tmp:
            v = tmp
        else:
            return default
    return v
