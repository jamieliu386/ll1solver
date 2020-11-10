# LL(1) Solver

This program accepts a context-free grammar from standard input and
generates/outputs an LL(1) parse table. For example:

Input:
```
A :== wBw | x | yxz
B :== ε | CxwA | wA
C :== yzzw
```

Output:
```
nullable map:
   A -> False
   B -> True
   C -> False
first map:
   A -> ['w', 'x', 'y']
   B -> ['w', 'y', 'ε']
   C -> ['y']
follow map:
   A -> ['$', 'w']
   B -> ['w']
   C -> ['x']
LL1 table:
+---+-------+---+------+---+---+
|   |   w   | x |  y   | z | $ |
+---+-------+---+------+---+---+
| A |  wBw  | x | yxz  |   |   |
| B | ε, wA |   | CxwA |   |   |
| C |       |   | yzzw |   |   |
+---+-------+---+------+---+---+
grammar is LL(1): False
```

## Usage

### System Prerequisites

- [Python 3](https://www.python.org/downloads/)
- This solver requires the [prettytable](https://pypi.org/project/prettytable/)
  library to be installed.

### Grammar Format

Grammars are expected to be in the same format as in [LL(1)
Academy](http://ll1academy.cs.ucla.edu/).
- Non-terminals are uppercase alphabetical characters [A-Z]
- Terminals are lowercase alphabetical characters [a-z]
- `ε` denotes the empty string
- `$` denotes the end of the input
- The start symbol is the first non-terminal in the grammar
- Each nonterminal should be on a separate line, with each of its productions
  separated by "`|`"

### Running the Solver

```
$ git clone https://github.com/jamieliu386/ll1solver.git
$ cd ll1solver
$ python3 solve.py
```

Type or copy/paste the grammar, and press Ctrl-d when finished to analyze the
grammar.
