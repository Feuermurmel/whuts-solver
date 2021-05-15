# whuts-solver

## Setup

Create a virtualenv and install the _whuts-solver_ package from the local directory into it:

```
python3 -m venv venv
. venv/bin/activate
pip install -e whuts-solver
```

Generate the Makefile which will run the solver for all unfoldings and unit cell dimensions up to a maximum number of copies of the unfolding (8 in this example):

```
whuts-solver generate 8 > Makefile
```


## Running the Solver

Run make to run the solver for all configurations (unfolding ID and unit cell dimensions). Set the number of processes to match the number of CPUs of your machine (4 in this example):

```
$ make -j 4
whuts-solver solve  1 1 1 8 > solutions/solution-1-1-1-8.txt
whuts-solver solve  2 1 1 8 > solutions/solution-2-1-1-8.txt
whuts-solver solve  4 1 1 8 > solutions/solution-4-1-1-8.txt
whuts-solver solve  3 1 1 8 > solutions/solution-3-1-1-8.txt
whuts-solver solve  5 1 1 8 > solutions/solution-5-1-1-8.txt
[...]
```

While it's running, use this command to show which solutions have already been found:

```
$ whuts-solver list-solutions
[...]
253: solutions/solution-253-2-4-4.txt
254: solutions/solution-254-2-2-8.txt
255: solutions/solution-255-2-2-8.txt
256: solutions/solution-256-2-4-4.txt
257: solutions/solution-257-2-2-4.txt
258: solutions/solution-258-2-2-8.txt
259: solutions/solution-259-2-4-4.txt
260: solutions/solution-260-2-4-4.txt
261: solutions/solution-261-2-4-4.txt
Solutions: 228 / 261
```

## Result Files

The file name of each result file contains the ID of the unfolding (39 in this example) and the dimensions of the unit cell (3 * 4 * 4 in this example):

```
solution-39-3-4-4.txt
```

Each generated file falls into one of these three cases:

This is an example of file which declares that no solution has been found to build a unit cell of the specific dimensions using the specific unfolding: 

```
$ cat solutions/solution-39-3-4-4.txt
[UNSAT]
Unfolding ID: 39
Box size: 3 4 4
Unique transformations: 192
```

This is an example of file which shows a solution of how to build a unit cell of the specific dimensions using the specific unfolding. Each line of coordinates represents one copy of the unfolding: 

```
$ cat solutions/solution-261-2-4-4.txt 
[SAT]
Unfolding ID: 261
Box size: 2 4 4
Unique transformations: 512

Solution:
[[0, 0, 0], [0, 0, -1], [0, 0, -2], [0, -1, -1], [0, 1, 0], [-1, 1, 0], [0, 0, 1], [1, 0, 0]]
[[1, 1, 3], [1, 2, 3], [1, 3, 3], [1, 2, 4], [1, 1, 2], [2, 1, 2], [1, 0, 3], [0, 1, 3]]
[[1, 3, 1], [1, 4, 1], [1, 5, 1], [1, 4, 2], [1, 3, 0], [2, 3, 0], [1, 2, 1], [0, 3, 1]]
[[0, 2, 2], [0, 2, 1], [0, 2, 0], [0, 1, 1], [0, 3, 2], [-1, 3, 2], [0, 2, 3], [1, 2, 2]]
```

This is an example of a fil which show that a solution for the unfolding has already been found and thus no attempt was made to find another one. The file points to another file which contains a solution (or points to another file):

```
$ cat solutions/solution-37-1-4-14.txt
[SAT]
Link: solutions/solution-37-1-2-28.txt
```
