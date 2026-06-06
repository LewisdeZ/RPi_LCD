#!/usr/bin/env python3
class Cycle:
    '''
    Cycle through keys of a dictionary, returning the values.
    '''
    def __init__(self, c):
        self._c = c
        self._index = -1

    def next(self):
        self._index += 1
        if self._index>=len(self._c):
            self._index = 0
        return self._c[self._index]

    def previous(self):
        self._index -= 1
        if self._index < 0:
            self._index = len(self._c)-1
        return self._c[self._index]




if __name__ == '__main__':
    seq = [i for i in range(10)]

    c = Cycle(seq)

    print(c.next())     # 0
    print(c.next())     # 1
    print(c.next())     # 2
    c.next()            # 3
    c.next()            # 4
    c.next()            # 5
    print(c.previous()) # 4
