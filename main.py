#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import math
import matplotlib.pyplot as plt


def main():
    xs = np.linspace(0, 2.0, 100, endpoint=True)
    ys = 1.5 * xs + np.sin(math.pi*xs)
    ymin, ymax = np.min(ys), np.max(ys)
    # not to exclude start/end points
    y_partitions = np.linspace(ymin-0.01, ymax+0.01, 10, endpoint=True)
    partition(xs, ys, y_partitions)
    fig, ax = plt.subplots()
    ax.plot(xs, ys)
    ax.grid(True)
    ax.set_aspect('equal')
    ax.set_xlim(0, max(1.0, ymax))
    ax.set_ylim(0, ymax*1.1)
    plt.show()


def group_by(x, cond):
    """
    # use the index of right element of pair to partition
    [1| 0, 1, 2, 3| 2, 2, 3, 4, 5] => breaks = [1, 5]
    [1| 0, 1, 2, 3| 2, 2, 3, 4, 5| 4] => breaks = [1, 5, 10]
    """
    if len(x) == 0:
        return []
    if len(x) == 1:
        return [[0]]
    # place where cond is broken
    breaks = []
    for i, (x0, x1) in enumerate(zip(x[:], x[1:])):
        if not cond(x0, x1):
            breaks.append(i+1)
    return np.split(x, breaks)


def partition(xs, ys, y_partitions):
    assert len(xs) == len(ys)

    for y0, y1 in zip(y_partitions[:], y_partitions[1:]):
        inv = np.where(np.logical_and(ys > y0, ys <= y1))[0]
        invs = group_by(inv, lambda x, y: (x+1) == y)
        print(f'[{y0}, {y1}] => {invs}')


if __name__ == '__main__':
    main()
