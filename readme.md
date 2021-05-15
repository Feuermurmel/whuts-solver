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

Run make to run the solver for all configurations (unfolding ID and unit cell dimensions). Set the number of processes to match the number of CPUs of your machine (4 in this example):

```
make -j 4
```

While it's running, use this command to show which solutions have already been found:

```
whuts-solver list-solutions
```
