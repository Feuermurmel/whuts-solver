from whuts_solver.solver import get_unfoldings


def iter_factorizations(x, n):
    if n == 0:
        if x == 1:
            yield ()
    else:
        for i in range(1, x + 1):
            if not x % i:
                for factorization in iter_factorizations(x // i, n - 1):
                    yield i, *factorization


def generate(max_multiplicity):
    targets = []

    print('.DEFAULT_GOAL := all')

    for id, unfolding in sorted(get_unfoldings().items()):
        previous_target = ''

        for multiplicity in range(1, max_multiplicity + 1):
            cell_count = len(unfolding) * multiplicity

            factorizations = \
                sorted(set(tuple(sorted(i)) for i in iter_factorizations(cell_count, 3)))

            for a, b, c in factorizations:
                target = f'solutions/solution-{id}-{a}-{b}-{c}.txt'
                p_arg = previous_target and f'-p {previous_target}'

                print(f'{target}: {previous_target}')
                print(f'\t@ mkdir -p solutions')
                print(f'\twhuts-solver solve {p_arg} {id} {a} {b} {c} > $@')
                print()

                targets.append(target)
                previous_target = target

    print('.PHONY: all')
    print('all: \\')

    for i in targets:
        print(f'    {i} \\')
