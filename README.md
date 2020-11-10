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

This solver requires the [prettytable](https://pypi.org/project/prettytable/)
library to be installed.

Grammars are expected to be input in the same format as in [LL(1) Academy](http://ll1academy.cs.ucla.edu/). That is, each nonterminal should be on a separate line, with all of its productions separated by "`|`".

```
$ git clone https://github.com/jamieliu386/ll1solver.git
$ cd ll1solver
$ python3 solve.py
```

Type or copy/paste the grammar, and press Ctrl-d to analyze the grammar.
