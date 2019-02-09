from itertools import islice

def chunk(it, size):
    """
    Split iterable `it` into `size` chunks
    https://stackoverflow.com/a/3125186
    """
    it = iter(it)
    return iter(lambda: tuple(islice(it, size)), ())
