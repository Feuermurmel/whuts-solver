import argparse
import sys

from whuts_solver import solver


def log(message):
    print(message, file=sys.stderr, flush=True)


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        'id',
        type=int,
        nargs='?',
        help='ID of the unfolding.')

    parser.add_argument(
        '--max-copies',
        type=int,
        default=8,
        help='Maximum number of copies of the unfolding to use to try to '
             'build a unit cell.')

    return parser.parse_args()


def entry_point():
    try:
        solver.solve(**vars(parse_args()))
    except KeyboardInterrupt:
        log('Operation interrupted.')
        sys.exit(1)
