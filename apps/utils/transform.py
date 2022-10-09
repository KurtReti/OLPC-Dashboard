import itertools
import re


def grouper(iterable, chunk_size):
    """
    Group iterable into tuples of size chunk_size (https://alexwlchan.net/2018/12/iterating-in-fixed-size-chunks/)
    :param iterable: object that is iterable
    :param chunk_size: int
    :return: generator of tuples of length chunk_size

    """
    it = iter(iterable)
    while True:
        chunk = tuple(itertools.islice(it, chunk_size))
        if not chunk:
            break
        yield chunk


def remove_trailing_slash(pathname):
    return re.sub('/$', '', pathname)
