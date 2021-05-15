import argparse
import pathlib

import sys
from whuts_solver import solver, generator


def log(message):
    print(message, file=sys.stderr, flush=True)


class UserError(Exception):
    def __init__(self, message, *args):
        super().__init__(message.format(*args))


def parse_args():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command', required=True)

    generate_parser = subparsers.add_parser('generate')
    generate_parser.add_argument('max_multiplicity', type=int)

    solve_parser = subparsers.add_parser('solve')
    solve_parser.add_argument('id', type=int)
    solve_parser.add_argument('-p', type=pathlib.Path)
    solve_parser.add_argument('a', type=int)
    solve_parser.add_argument('b', type=int)
    solve_parser.add_argument('c', type=int)

    subparsers.add_parser('list-solutions')

    return parser.parse_args()


def list_solutions():
    solutions = {}

    for i in pathlib.Path('solutions').iterdir():
        if i.name.startswith('solution-'):
            id = int(i.name.split('-')[1])

            if 'Solution:' in i.read_text():
                solutions[id] = i

    for i in sorted(solver.get_unfoldings()):
        s = solutions.get(i, '-')

        print(f'{i}: {s}')

    print(f'Solutions: {len(solutions)} / {len(solver.get_unfoldings())}')


def main(command, **kwargs):
    commands = {
        'generate': generator.generate,
        'solve': solver.solve,
        'list-solutions': list_solutions}

    commands[command](**kwargs)


def entry_point():
    try:
        main(**vars(parse_args()))
    except KeyboardInterrupt:
        log('Operation interrupted.')
        sys.exit(1)
    except UserError as e:
        log(f'error: {e}')
        sys.exit(2)
