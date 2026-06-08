#!/usr/bin/env python3
class CyclicList:
    def __init__(self, items):
        self._list = list(items)

    def next(self):
        if not self._list:
            return None
        self._list.append(self._list.pop(0))
        value = self._list[0]
        return value

    def previous(self):
        if not self._list:
            return None
        self._list.insert(0, self._list.pop())
        return self._list[0]

    def getList(self):
        return self._list




if __name__ == '__main__':
    seq = [i for i in range(10)]
    print(f"Input list: {seq}")

    c = CyclicList(seq)

    print(c.next())     # 0
    print(c.next())     # 1
    print(c.next())     # 2
    c.next()            # 3
    c.next()            # 4
    c.next()            # 5
    print(c.previous()) # 4
