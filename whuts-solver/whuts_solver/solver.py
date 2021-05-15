import contextlib
import functools
import sys

import itertools
import json

import pkg_resources
import numpy as np
import exact_cover


@functools.lru_cache(None)
def get_unfoldings():
    with pkg_resources.resource_stream(__name__, 'cube-unfoldings.txt') as file:
        return dict(enumerate(json.load(file), 1))


def product(seq):
    result = 1

    for i in seq:
        result *= i

    return result


def iter_factorizations(n, num_factors, min_factor=1):
    """
    Factorize n into exactly num_factors factors. Yield each factorization as
    a sorted tuple of factors.
    """
    if num_factors == 0:
        if n == 1:
            yield ()
    else:
        for i in range(min_factor, n + 1):
            if not n % i:
                for f in iter_factorizations(n // i, num_factors - 1,  i):
                    yield i, *f


def iter_permutations_with_parity(n):
    """
    Yield all permutations of n elements together with its parity. The parity
    is represented as the integer 1 for even permutations and -1 for odd
    permutations.
    """
    seen_permutations = set()

    def walk_permutation(item, parity):
        if item not in seen_permutations:
            seen_permutations.add(item)
            yield item, parity

            for i in range(1, len(item)):
                item_list = list(item)
                item_list[0], item_list[i] = item_list[i], item_list[0]

                yield from walk_permutation(tuple(item_list), -parity)

    return walk_permutation(tuple(range(n)), 1)


def iter_orientations(n):
    """
    Yield all possible grid-aligned rotation transformations. Each
    transformation is represented as two tuples. The first tuple specifies a
    permutation to perform on the components of a coordinate, the second
    represents which axes to mirror, represented as a sequence of 1 and -1.
    """
    for permutation, parity in iter_permutations_with_parity(n):
        for mirrors in itertools.product(*([[1, -1]] * (n - 1))):
            yield permutation, (*mirrors, product(mirrors) * parity)


def iter_offsets(box):
    """
    Yield all possible positions in a the specified cuboid. The cuboid has its
    first corner in the origin and its last corner in the coordinates
    specified by the parameter box.
    """
    return itertools.product(*(range(i) for i in box))


def orient_cell(cell, orientation):
    permutation, mirrors = orientation

    return tuple(cell[p] * m for p, m in zip(permutation, mirrors))


def offset_cell(cell, offset):
    return tuple(a + b for a, b in zip(cell, offset))


def fold_cell(cell, box):
    return tuple(a % b for a, b in zip(cell, box))


def has_overlap(cells):
    occupied_cells = set()

    for i in cells:
        if i in occupied_cells:
            return True

        occupied_cells.add(i)

    return False


def iter_transformed_unfoldings(unfolding, box):
    """
    Take an unfolding and generate all possible transformed versions by
    rotation and transformation, folding cells into the box by wrapping them
    around to the opposite sides of the box. Yield all unique results.

    For each result, an unfolded and folded version of the transformed
    unfolding is returned.
    """
    seen_versions = set()

    for orientation in iter_orientations(len(box)):
        for offset in iter_offsets(box):
            version = [
                offset_cell(orient_cell(i, orientation), offset)
                for i in unfolding]

            folded_version = sorted(fold_cell(i, box) for i in version)

            if not has_overlap(folded_version):
                folded_version_tuple = tuple(folded_version)

                if folded_version_tuple not in seen_versions:
                    seen_versions.add(folded_version_tuple)

                    yield version, folded_version


def cell_index(cell, box):
    """
    Number all cells inside the box from 0 to the number of cells. Return the
    index of the specified cell.
    """
    index = 0

    for a, b in zip(cell, box):
        index = index * b + a

    return index


def generate_matrix(unfolding, box):
    """
    Create exact covering matrix from all possible transformed versions of the
    unfolding. Returns the matrix and a list with the transformed unfoldings
    that correspond to the rows of the matrix.
    """
    transformed_unfoldings = list(iter_transformed_unfoldings(unfolding, box))
    matrix = np.zeros((len(transformed_unfoldings), product(box)), dtype='int32')

    for i, (_, cells) in enumerate(transformed_unfoldings):
        for cell in cells:
            matrix[i, cell_index(cell, box)] = 1

    return matrix, [i for i, _ in transformed_unfoldings]


def solve_unfolding(id, max_copies):
    unfolding = get_unfoldings()[id]

    print(f'Trying to solve unfolding {id} ...')

    for num_copies in range(1, max_copies + 1):
        for box in iter_factorizations(len(unfolding) * num_copies, 3):
            matrix, transformed_unfoldings = generate_matrix(unfolding, box)
            solution = exact_cover.get_exact_cover(matrix)

            if len(solution):
                print('Solution:')
                print(f'Unit cell dimensions: {box}')

                for i in solution:
                    print(json.dumps(transformed_unfoldings[i]))

                return

    print('No solution found. :(')


def solve(id, max_copies):
    if id is None:
        for i in sorted(get_unfoldings()):
            solve_unfolding(i, max_copies)
            print()
    else:
        solve_unfolding(id, max_copies)
