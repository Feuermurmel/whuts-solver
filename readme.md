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

A maximum number of copies of the unfolding to use can be specified, this may lead not solution being found for some unfoldings:

```
$ whuts-solver --max-copies=4 23 
Trying to solve unfolding 23 ...
No solution found. :(
```
