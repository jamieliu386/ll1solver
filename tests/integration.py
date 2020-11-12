import pytest
from typing import NamedTuple, List, Dict
# from solve import parse_grammar
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
    )
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
        assert set(g.first[nt]) == set(test_grammar.first_sets[nt]), (
            f"different first set for {nt}"
        )
        
    # check LL1
    assert test_grammar.is_ll1 == g.is_ll1
