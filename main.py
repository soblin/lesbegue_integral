#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import math
import matplotlib.pyplot as plt
import itertools


class IntervalFunc:
    def __init__(self, xs, intervals):
        self.intervals_ = []
        for interval in intervals:
            if len(interval) == 0:
                continue
            if len(interval) == 1:
                print(f"[{xs[interval[0]]}] contains only one element")
                continue
            self.intervals_.append([xs[interval[0]], xs[interval[-1]]])

    def eval(self, x):
        for interval in self.intervals_:
            if x < interval[0] or x > interval[1]:
                continue
            else:
                return 1.0
        return 0.0


def main():
    """
    NOTE:
    to let this program work correctly, all of elements of ys must be <= n * (2^n).
    Also num_points must be large enough so that the inverse of [y0, y1] includes at least two points

    Bad cases:
    (1) n = 1, then ys >= 2 is ignored.
    (2) n = 100, and num_points = 10, then some of the inverse of [y0, y1] maybe [[x]].
    """
    n = 4
    num_points = 1000

    xs = np.linspace(0, 2.0, 1000, endpoint=True)
    ys = 1.5 * xs + np.sin(math.pi*xs)

    ymin, ymax = np.min(ys), np.max(ys)
    y_partitions = [1.0 * k / math.pow(2, n)
                    for k in range(1, n * int(math.pow(2, n))+1)]
    y_partitions.insert(0, ymin-0.01)

    vals, intervals = partition(xs, ys, y_partitions)
    interval_funcs = [IntervalFunc(xs, interval) for interval in intervals]
    ys_approx = [sum([1.0 * k / math.pow(2, n) * interval_funcs[k].eval(x) for k in range(0, n * int(math.pow(2, n)))])
                 for x in xs]
    fig, ax = plt.subplots()
    ax.plot(xs, ys, color="k")
    ax.plot(xs, ys_approx, color="k", linestyle="dashed")

    """
    colors = ["magenta", "cyan", "green", "blue"]
    for val, interval, color in zip(vals, intervals, itertools.cycle(colors)):
        # ignore empty interval
        if interval[-1] == []:
            continue

        y0, y1 = val[0], val[1]
        # dashed line of y range
        it_last = interval[-1][-1]
        ax.plot([xs[0], xs[it_last]], [ys[it_last], ys[it_last]],
                linestyle="dashed", color=color)

        # dashed line of x range
        for interval_ in interval:
            it_begin = interval_[0]
            it_end = interval_[-1]
            if it_begin == it_end:
                ax.plot([xs[it_begin], xs[it_begin]], [0, y1],
                        linestyle="dashed", color=color)
            else:
                if abs(ys[it_begin] - y1) < abs(ys[it_begin] - y0):
                    # it_begin corresponds to y1
                    ax.plot([xs[it_begin], xs[it_begin]], [0, y1],
                            linestyle="dashed", color=color)
                if abs(ys[it_end] - y1) < abs(ys[it_end] - y0):
                    # it_begin corresponds to y1
                    ax.plot([xs[it_end], xs[it_end]], [0, y1],
                            linestyle="dashed", color=color)
    """

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
        return [[]]
    if len(x) == 1:
        return [[x[0]]]
    # place where cond is broken
    breaks = []
    for i, (x0, x1) in enumerate(zip(x[:], x[1:])):
        if not cond(x0, x1):
            breaks.append(i+1)
    return [list(it) for it in np.split(x, breaks)]


def partition(xs, ys, y_partitions):
    assert len(xs) == len(ys)

    vals = []
    intervals = []
    for y0, y1 in zip(y_partitions[:], y_partitions[1:]):
        inv = np.where(np.logical_and(ys > y0, ys <= y1))[0]
        invs = group_by(inv, lambda x, y: (x+1) == y)
        intervals.append(invs)
        vals.append([y0, y1])

    return vals, intervals


if __name__ == '__main__':
    main()
