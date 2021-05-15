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
        default=12,
        help='Maximum number of copies of the unfolding to use to try to '
             'build a unit cell. Defaults to a value that allows a tiling to '
             'be found for all unfoldings.')

    parser.add_argument(
        '--cube',
        dest='n',
        action='store_const',
        default=3,
        const=2,
        help='Find tilings of the unfoldings of the 3-cube instead of the '
             'hypercube (4-cube).')

    parser.add_argument(
        '--square',
        dest='n',
        action='store_const',
        const=1,
        help='Find tilings of the unfoldings of the square (2-cube) instead '
             'of the hypercube (4-cube). This is mostly a joke. :)')

    return parser.parse_args()


def entry_point():
    try:
        solver.solve(**vars(parse_args()))
    except KeyboardInterrupt:
        log('Operation interrupted.')
        sys.exit(1)
