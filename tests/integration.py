import pytest
from typing import NamedTuple, List, Dict
from ..solve import parse_grammar

class TestGrammar(NamedTuple):
    grammar: str
    null_set: str
    first_sets: Dict[str, str]
    follow_sets: Dict[str, str]
    is_ll1: bool
    __test__ = False


test_grammars = [
    TestGrammar(
        grammar='''
        A :== wzw | wB | CAz
        B :== ε | yC
        C :== zAxx | BwC | xzC
        ''',
        null_set='B',
        first_sets=dict(
            A='wxyz', 
            B='y',
            C='wxyz'
        ),
        follow_sets=dict(
            A='xz$',
            B='wxz$',
            C='wxyz$'
        ),
        is_ll1=False
    ),
    TestGrammar(
        grammar='''
        A :== wB | BAwx
        B :== ywB
        ''',
        null_set='',
        first_sets=dict(
            A='wy', 
            B='y',
        ),
        follow_sets=dict(
            A='w$',
            B='wy$',
        ),
        is_ll1=True
    ),
    TestGrammar(
        grammar='''
        A :== xx | BA
        B :== zyAx | wBx
        ''',
        null_set='',
        first_sets=dict(
            A='wxz', 
            B='wz',
        ),
        follow_sets=dict(
            A='x$',
            B='wxz',
        ),
        is_ll1=True
    ),
    TestGrammar(
        grammar='''
        A :== xxx | yC
        B :== yB | ε | Aww
        C :== ByBw | BAxB
        ''',
        null_set='B',
        first_sets=dict(
            A='xy', 
            B='xy',
            C='xy'
        ),
        follow_sets=dict(
            A='wx$',
            B='wxy$',
            C='wx$'
        ),
        is_ll1=False
    ),
    TestGrammar(
        grammar='''
        A :== yCz
        B :== ε | zyA
        C :== yBCC | ε | wz
        ''',
        null_set='BC',
        first_sets=dict(
            A='y', 
            B='z',
            C='wy'
        ),
        follow_sets=dict(
            A='wyz$',
            B='wyz',
            C='wyz'
        ),
        is_ll1=False
    ),
    TestGrammar(
        grammar='''
        A :== C
        B :== ε | w | yCxz
        C :== wA | w | ByyA
        ''',
        null_set='B',
        first_sets=dict(
            A='wy', 
            B='wy',
            C='wy'
        ),
        follow_sets=dict(
            A='x$',
            B='y',
            C='x$'
        ),
        is_ll1=False
    ),
    TestGrammar(
        grammar='''
        A :== BBy | ε | BwC
        B :== C | yxCx | yBw
        C :== zCxw
        ''',
        null_set='A',
        first_sets=dict(
            A='yz', 
            B='yz',
            C='z'
        ),
        follow_sets=dict(
            A='$',
            B='wyz',
            C='wxyz$'
        ),
        is_ll1=False
    ),
    TestGrammar(
        grammar='''
        A :== wBw | x | yxz
        B :== ε | CxwA | wA
        C :== yzzw
        ''',
        null_set='B',
        first_sets=dict(
            A='wxy', 
            B='wy',
            C='y'
        ),
        follow_sets=dict(
            A='w$',
            B='w',
            C='x'
        ),
        is_ll1=False
    ),
]

@pytest.mark.parametrize('test_grammar', test_grammars)
def test(test_grammar):
    grammar_lines = [
        line.strip() 
        for line in test_grammar.grammar.split('\n') 
        if line.strip()]
    g = parse_grammar(grammar_lines)
    g.solve_grammar()

    # check nullable
    assert len(g.nts) == len(test_grammar.first_sets)
    assert set(k for k, v in g.nullable.items() if v) == set(test_grammar.null_set)
    
    for nt in g.nts:
        # check follow set
        assert set(g.follow[nt]) == set(test_grammar.follow_sets[nt]), (
            f"different follow set for {nt}"
        )
        
        # check first set
        assert set(g.get_nt_first_set(nt)) == set(test_grammar.first_sets[nt]), (
            f"different first set for {nt}"
        )
        
    # check LL1
    assert test_grammar.is_ll1 == g.is_ll1
