#%%
from typing import NamedTuple, Dict, Tuple
from collections import Counter


class Coord(NamedTuple):
    x: int
    y: int


test_serial_numer = 8


def power_level(x: int, y: int, serial_number: int) -> int:
    rack_id = x + 10
    power = rack_id * y
    power += serial_number
    power *= rack_id
    power = (power // 100) % 10
    power -= 5
    return power


assert power_level(3, 5, 8) == 4
assert power_level(122, 79, 57) == -5
assert power_level(217, 196, 39) == 0
assert power_level(101, 153, 71) == 4
#%%


def largest_power(
    serial_number, size: int = 3, grid_shape: int = 300
) -> Tuple[int, int, int]:
    squares = Counter()

    powers = {
        (x, y): power_level(x, y, serial_number)
        for x in range(grid_shape)
        for y in range(grid_shape)
    }

    for x in range(grid_shape - size):
        for y in range(grid_shape - size):
            squares[x, y] = sum(
                powers[i, j] for i in range(x, x + size) for j in range(y, y + size)
            )
    ((x1, y1), v1), (_, v2) = squares.most_common(2)
    assert v1 > v2
    return x1, y1, v1


assert largest_power(18) == (33, 45, 29)
assert largest_power(42) == (21, 61, 30)
#%%
serial_number = 7803
largest_power(serial_number)

#%%


def largest_power_dynamic(
    serial_number, grid_size: int = 300
) -> Tuple[int, int, int, int]:
    squares = Counter()

    powers = np.array(
        [
            [power_level(x, y, serial_number) for x in range(grid_size)]
            for y in range(grid_size)
        ]
    )

    for win_size in range(1, grid_size + 1):
        print(win_size)

        for (x, y) in [
            (x, y)
            for x in range(grid_size - win_size)
            for y in range(grid_size - win_size)
        ]:
            if win_size % 2 == 0:
                squares[x, y, win_size] = sum(
                    squares[i, j, win_size / 2]
                    for i in range(x, x + win_size // 2 + 1, win_size // 2)
                    for j in range(y, y + win_size // 2 + 1, win_size // 2)
                )
            elif win_size % 3 == 0 and win_size >= 3:
                squares[x, y, win_size] = sum(
                    squares[i, j, win_size // 3]
                    for i in range(x, x + win_size // 3 + 1, win_size // 3)
                    for j in range(y, y + win_size // 3 + 1, win_size // 3)
                )
            elif win_size % 5 == 0 and win_size >= 5:
                squares[x, y, win_size] = sum(
                    squares[i, j, win_size // 5]
                    for i in range(x, x + win_size // 5 + 1, win_size // 5)
                    for j in range(y, y + win_size // 5 + 1, win_size // 5)
                )
            else:
                squares[x, y, win_size] = (
                    squares[x, y, win_size - 1]
                    + np.sum(powers[x + win_size, y : y + win_size])
                    + np.sum(powers[x : x + win_size - 1, y + win_size])
                )

    (x1, y1, s1), v1 = squares.most_common(1)
    return x1, y1, s1, v1


# Doesn't work for some reason
largest_power_dynamic(18)

#%%
import numpy as np
from scipy.signal import convolve2d


def largest_power_np(serial_number, grid_size: int = 300) -> Tuple[int, int, int, int]:
    maxv = float("-inf")
    powers = np.array(
        [
            [power_level(x, y, serial_number) for x in range(grid_size)]
            for y in range(grid_size)
        ]
    )

    for n in range(1, grid_size + 1):
        print(n)
        mat = np.ones((n, n))
        cnv = convolve2d(mat, powers, "valid")
        if np.max(cnv) > maxv:
            maxv = np.max(cnv)
            y, x = np.unravel_index(np.argmax(cnv), cnv.shape)
            s = n
            print(x, y, s, maxv)

    return int(x), int(y), int(s), int(maxv)


#%%
assert largest_power_np(18) == (90, 269, 16, 113)
assert largest_power_np(42) == (232, 251, 12, 119)
#%%
largest_power_np(7803)
#%%

# Using summed area table
# Not correct either...

def largest_power_sat(serial_number, grid_size: int = 300) -> Tuple[int, int, int, int]:
    powers = np.array(
        [
            [power_level(x, y, serial_number) for x in range(grid_size)]
            for y in range(grid_size)
        ]
    )

    sat = np.zeros((grid_size, grid_size))
    sat[0, 0] = powers[0, 0]
    for i in range(1, grid_size):
        sat[0, i] = powers[0, i] + sat[0, i - 1]
        sat[i, 0] = powers[i, 0] + sat[i - 1, 0]

    for i, j in [(i, j) for j in range(1, grid_size) for i in range(1, grid_size)]:
        sat[i, j] = powers[i, j] + sat[i, j - 1] + sat[i - 1, j] - sat[i - 1, j - 1]
    
    print(powers[:5, :5])
    print(sat[:5, :5])
    max_val = float("-inf")
    candidates = (0, 0, 0)

    for win_size in range(0, grid_size):
        for i, j in [
            (i, j)
            for i in range(win_size, grid_size)
            for j in range(win_size, grid_size)
        ]:
            left = sat[i, j - win_size]
            up = sat[i - win_size, j]
            diag = sat[i - win_size, j - win_size]

            val = sat[i, j] - left - up + diag

            if val > max_val:
                max_val = val
                candidates = (i - win_size, j - win_size, win_size + 1)

    x, y, s = candidates
    return int(x), int(y), int(s), int(max_val)


assert largest_power_sat(18) == (90, 269, 16, 113)
assert largest_power_sat(42) == (232, 251, 12, 119)

#%%
largest_power_sat(18, grid_size = 3)

#%%
