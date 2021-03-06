# coding=utf-8
#
# This file is part of Hypothesis, which may be found at
# https://github.com/HypothesisWorks/hypothesis/
#
# Most of this work is copyright (C) 2013-2019 David R. MacIver
# (david@drmaciver.com), but it contains contributions by others. See
# CONTRIBUTING.rst for a full list of people who may hold copyright, and
# consult the git log if you need to determine who owns an individual
# contribution.
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file, You can
# obtain one at https://mozilla.org/MPL/2.0/.
#
# END HEADER

"""A module for miscellaneous useful bits and bobs that don't
obviously belong anywhere else. If you spot a better home for
anything that lives here, please move it."""


from __future__ import absolute_import, division, print_function

from hypothesis.internal.compat import array_or_list, hbytes


def replace_all(buffer, replacements):
    """Substitute multiple replacement values into a buffer.

    Replacements is a list of (start, end, value) triples.
    """

    result = bytearray()
    prev = 0
    offset = 0
    for u, v, r in replacements:
        result.extend(buffer[prev:u])
        result.extend(r)
        prev = v
        offset += len(r) - (v - u)
    result.extend(buffer[prev:])
    assert len(result) == len(buffer) + offset
    return hbytes(result)


ARRAY_CODES = ["B", "H", "I", "L", "Q"]
NEXT_ARRAY_CODE = dict(zip(ARRAY_CODES, ARRAY_CODES[1:]))


class IntList(object):
    """Class for storing a list of non-negative integers compactly.

    We store them as the smallest size integer array we can get
    away with. When we try to add an integer that is too large,
    we upgrade the array to the smallest word size needed to store
    the new value."""

    __slots__ = ("__underlying",)

    def __init__(self, values=()):
        for code in ARRAY_CODES:
            try:
                self.__underlying = array_or_list(code, values)
                break
            except OverflowError:
                pass
        else:
            raise ValueError("Could not create IntList for %r" % (values,))

    def __repr__(self):
        return "IntList(%r)" % (list(self),)

    def __len__(self):
        return len(self.__underlying)

    def __getitem__(self, i):
        return self.__underlying[i]

    def __iter__(self):
        return iter(self.__underlying)

    def __eq__(self, other):
        if self is other:
            return True
        if not isinstance(other, IntList):
            return NotImplemented
        return self.__underlying == other.__underlying

    def __ne__(self, other):
        if self is other:
            return False
        if not isinstance(other, IntList):
            return NotImplemented
        return self.__underlying != other.__underlying

    def append(self, n):
        while True:
            try:
                self.__underlying.append(n)
                return
            except OverflowError:
                assert n > 0
                self.__underlying = array_or_list(
                    NEXT_ARRAY_CODE[self.__underlying.typecode], self.__underlying
                )


def pop_random(random, values):
    """Remove a random element of values, possibly changing the ordering of its
    elements."""

    # We pick the element at a random index. Rather than removing that element
    # from the list (which would be an O(n) operation), we swap it to the end
    # and return the last element of the list. This changes the order of
    # the elements, but as long as these elements are only accessed through
    # random sampling that doesn't matter.
    i = random.randrange(0, len(values))
    values[i], values[-1] = values[-1], values[i]
    return values.pop()


def binary_search(lo, hi, f):
    """Binary searches in [lo , hi) to find
    n such that f(n) == f(lo) but f(n + 1) != f(lo).
    It is implicitly assumed and will not be checked
    that f(hi) != f(lo).
    """

    reference = f(lo)

    while lo + 1 < hi:
        mid = (lo + hi) // 2
        if f(mid) == reference:
            lo = mid
        else:
            hi = mid
    return lo
