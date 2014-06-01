"""
UTILITIES
--------------------
Static helper functions
"""


def remove_duplicate_urls(seq, idfun=None):
    """
    Remove unnessary duplicates from the list of URLs

    The function is borrowed from the nice gentlemen at http://www.peterbe.com/plog/uniqifiers-benchmark
    """

    if idfun is None:
        def idfun(x): return x
    seen = {}
    result = []
    for item in seq:
        marker = idfun(item)
        if marker in seen: continue
        seen[marker] = 1
        result.append(item)

    return result



def class_or_id(selector):
    """
    Ideally this will differentiate between classes and ids,
    maybe in the way jQuery does (#id, .class)
    """

    # @todo differentiate between IDs and classes
    if selector[0] == ".":
        return selector[1:]