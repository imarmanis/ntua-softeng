def unique_stripped(l):
    """Strip (ie remove all surrounding whitespace from) all elements of l and
    then remove duplicates and empty strings, returning a set"""
    stripped = (x.strip() for x in l)
    return set(x for x in stripped if x)
