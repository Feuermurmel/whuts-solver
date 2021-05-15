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


def iter_permutations_with_parity(n):
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
    for permutation, parity in iter_permutations_with_parity(n):
        for mirrors in itertools.product(*([[1, -1]] * (n - 1))):
            yield permutation, (*mirrors, product(mirrors) * parity)


def iter_offsets(box):
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
    seen_transformed_cells = set()

    for orientation in iter_orientations(len(box)):
        for offset in iter_offsets(box):
            transformed_cells = [
                fold_cell(offset_cell(orient_cell(i, orientation), offset), box)
                for i in unfolding]

            if not has_overlap(transformed_cells):
                transformed_cells = sorted(transformed_cells)
                transformed_cells_tuple = tuple(transformed_cells)

                if transformed_cells_tuple not in seen_transformed_cells:
                    seen_transformed_cells.add(transformed_cells_tuple)

                    yield orientation, offset, transformed_cells


def cell_index(cell, box):
    index = 0

    for a, b in zip(cell, box):
        index = index * b + a

    return index


def get_matrix(unfolding, box):
    transformed_unfoldings = list(iter_transformed_unfoldings(unfolding, box))
    matrix = np.zeros((len(transformed_unfoldings), product(box)), dtype='int32')

    for i, (_, _, cells) in enumerate(transformed_unfoldings):
        for cell in cells:
            matrix[i, cell_index(cell, box)] = 1

    transformations = [
        (orientation, offset)
        for orientation, offset, _ in transformed_unfoldings]

    return transformations, matrix


def solve(p, id, a, b, c):
    if p and '[SAT]' in p.read_text():
        print('[SAT]')
        print(f'Link: {p}')
    else:
        unfolding = get_unfoldings()[id]
        box = a, b, c
        transformations, matrix = get_matrix(unfolding, box)

        print(f'Matrix shape: {matrix.shape}', file=sys.stderr)

        solution = exact_cover.get_exact_cover(matrix)
        has_solution = bool(len(solution))

        print('[SAT]' if has_solution else '[UNSAT]')
        print(f'Unfolding ID: {id}')
        print(f'Box size: {a} {b} {c}')
        print(f'Unique transformations: {len(transformations)}')

        if has_solution:
            print()
            print('Solution:')

            for i in solution:
                orientation, offset = transformations[i]

                transformed_cells = [
                    offset_cell(orient_cell(i, orientation), offset)
                    for i in unfolding]

                print(json.dumps(transformed_cells))
