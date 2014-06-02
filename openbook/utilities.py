"""
UTILITIES
--------------------
Static helper functions
"""


def remove_duplicate_urls(seq, id_fun=None):
    """
    Remove unnecessary duplicates from the list of URLs

    The function is borrowed from the nice gentlemen at http://www.peterbe.com/plog/uniqifiers-benchmark
    """

    if id_fun is None:
        def id_fun(x):
            return x
    seen = {}
    result = []
    for item in seq:
        marker = id_fun(item)
        if marker in seen:
            continue
        seen[marker] = 1
        result.append(item)

    return result


def class_or_id(selector):
    """
    Differentiate between classes and ids in the way jQuery does (#id, .class)
    """

    if selector[0] == '.':
        soup_selector = 'class'
    elif selector[0] == '#':
        soup_selector = 'id'
    else:
        soup_selector = ''

    return [soup_selector, selector[1:]]