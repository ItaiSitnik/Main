# Nonogram Solver
A simple C++ program to solve nonogram (https://nonogram.com/) puzzles

## Input format

Input file should be like this:

```
10
5
2 3
1 1
7
3 3
1 1 1
7
6 1
2 3 1
2 3 1
1
4 2
2 3 2
1 2 2
1 1 2
2 2 4
2 7
4 4
2
4
```

First line: dimension of the grid (let's say N, then the grid is NxN)   
Next N lines: information about the N lines   
Next N lines: information about the N columns   
Next N lines (NOT MANDATORY), each with N characters: the grid itself. Sometimes the initial grid already has some symbols, so you can use this option.

## Usage

To execute the solver, you must use the command './run' in the directory.
You can either pass a path to an input file or execute as it is and type the input yourself.

Example:
```
./run samples/inputs/hard1 (is going to execute with input file 'hard1')
./run (is going to execute without an input file, so you need to type one yourself)
```

## Output format

Output file will look like this:
```
X X O O O O O X X X
X O O X X O O O X X
X O X X X X X O X X
X O O O O O O O X X
X O O O X O O O X X
X X O X X X O X O X
X X X O O O O O O O
X X O O O O O O X O
X O O X X O O O X O
O O X X X O O O X O
```

In which X's are non-colored cells and O's are colored ones.
