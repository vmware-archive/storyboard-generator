import itertools
from collections import Counter


def test_counter_repr():
    c = Counter({"value": 4})

    s = "foo {c} bar".format(c=c)

    assert "value" in c

def test_iters():
    lst = [1, 2, 3, 4, 5, 6]

    iterable = iter(lst)

    for i in iterable:
        if i == 3:
            look_ahead = next(iterable)
            print("lookahead", look_ahead)

        print("i", i)


def tree(iterable):
    myself = list(iterable)

    (leftside, rightside) = itertools.tee(iterable)

    try:
        me = next(rightside)
        return {me: tree(rightside), ".": myself}

    except StopIteration:
        return {".": myself}


def test_make_tree():
    from pprint import pprint
    lst = [1, 2, 3, 4, 5, 6]

    t = tree(iter(lst))

    pprint(t)
