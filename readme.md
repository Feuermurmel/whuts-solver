# whuts-solver

## Setup

Create a virtualenv and install the _whuts-solver_ package from the local directory into it:

```
python3 -m venv venv
. venv/bin/activate
pip install -e .
```


## Running the Solver

The the solver can be run eiter with a specific unfolding ID:

```
Trying to solve unfolding 125 ...
Solution:
Unit cell dimensions: (2, 2, 4)
[[0, 0, 0], [0, 0, -1], [0, -1, -1], [0, -1, -2], [0, 0, 1], [-1, 0, 1], [0, 1, 0], [1, 1, 0]]
[[1, 1, 2], [1, 1, 3], [1, 2, 3], [1, 2, 4], [1, 1, 1], [0, 1, 1], [1, 0, 2], [2, 0, 2]]
```

Or it can be run without an unfolding ID to find solutions for all unfoldings:

```
$ whuts-solver 
Trying to solve unfolding 1 ...
Solution:
Unit cell dimensions: (2, 2, 2)
[[0, 0, 0], [0, 0, -1], [0, -1, -1], [0, -1, -2], [-1, -1, -2], [1, 0, 0], [1, 0, 1], [1, 1, 1]]

Trying to solve unfolding 2 ...
Solution:
Unit cell dimensions: (2, 2, 4)
[[0, 0, 0], [0, 0, -1], [0, -1, -1], [0, -1, -2], [0, 0, 1], [-1, 0, 1], [-1, 1, 1], [1, 0, 0]]
[[1, 1, 3], [1, 1, 4], [0, 1, 4], [0, 1, 5], [1, 1, 2], [1, 0, 2], [2, 0, 2], [1, 2, 3]]

Trying to solve unfolding 3 ...
[...]
```

Each solution consists of a unit cell dimension and a number of copies of the unfolding, rotated and translated in space. Each copy is represented by a list of coordinates of the individual cubes. The solution can be used to tile space by arranging copying it along each axis with a distance given by the unit cell dimensions.

A maximum number of copies of the unfolding to use can be specified, this may lead not solution being found for some unfoldings:

```
$ whuts-solver --max-copies=4 23 
Trying to solve unfolding 23 ...
No solution found. :(
```


## Other Dimensions

Finding tilings of other unfoldings of the cube and the square is also supported:

```
$ whuts-solver --cube
Trying to solve unfolding 1 ...
Solution:
Unit cell dimensions: [2, 6]
[[0, -1], [1, 0], [1, -1], [1, -2], [1, -3], [2, 0]]
[[1, 2], [0, 1], [0, 2], [0, 3], [0, 4], [-1, 1]]

Trying to solve unfolding 2 ...
Solution:
Unit cell dimensions: [6, 12]
[[0, 0], [0, 1], [1, 1], [2, 1], [3, 1], [0, 2]]
[[1, 10], [1, 11], [2, 11], [3, 11], [4, 11], [1, 12]]
[[5, 1], [5, 0], [4, 0], [3, 0], [2, 0], [5, -1]]
[[0, 11], [0, 10], [-1, 10], [-2, 10], [-3, 10], [0, 9]]
[[2, 8], [2, 9], [3, 9], [4, 9], [5, 9], [2, 10]]
[[1, 9], [1, 8], [0, 8], [-1, 8], [-2, 8], [1, 7]]
[[3, 6], [3, 7], [4, 7], [5, 7], [6, 7], [3, 8]]
[[2, 7], [2, 6], [1, 6], [0, 6], [-1, 6], [2, 5]]
[[4, 3], [4, 2], [3, 2], [2, 2], [1, 2], [4, 1]]
[[5, 2], [5, 3], [6, 3], [7, 3], [8, 3], [5, 4]]
[[3, 5], [3, 4], [2, 4], [1, 4], [0, 4], [3, 3]]
[[4, 4], [4, 5], [5, 5], [6, 5], [7, 5], [4, 6]]
```
