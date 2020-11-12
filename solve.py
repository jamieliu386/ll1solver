from collections import defaultdict
from typing import Dict, List, Set, Tuple
from copy import deepcopy
from prettytable import PrettyTable

EPSILON = "ε"


def is_t(sym: str) -> bool:
    return sym.islower() and sym != EPSILON


def is_nt(sym: str) -> bool:
    return not sym.islower()


class Grammar:
    def __init__(self) -> None:
        self.start_symbol = None
        self.nts = []
        self.ts = []
        self.prods = defaultdict(set)  # dict(nt: str -> Set[prod: str])
        self.nullable = defaultdict(bool)  # dict(nt: str -> nullable: bool)
        self.first = defaultdict(set)  # dict(nt: str -> Set[t: str])
        self.follow = defaultdict(set)  # dict(nt: str -> Set[t: str])
        self.ll1_table = {}
        self.is_ll1 = True
        return

    def __repr__(self) -> str:
        TAB = "   "
        result = ""

        result += "nullable map:\n"
        for nt in self.nts:
            result += f"{TAB}{nt} -> {self.nullable[nt]}\n"

        result += "first map:\n"
        for nt in self.nts:
            remove_epsilon = deepcopy(self.first[nt])
            remove_epsilon.discard(EPSILON)
            result += f"{TAB}{nt} -> {sorted(list(remove_epsilon))}\n"

        result += "follow map:\n"
        for nt in self.nts:
            result += f"{TAB}{nt} -> {sorted(list(self.follow[nt]))}\n"

        result += "LL1 table:\n"
        table = PrettyTable()
        table.field_names = ["", *self.ts, "$"]
        for nt in self.nts:
            row = self.ll1_table[nt]
            cols = []
            for t in [*self.ts, "$"]:
                prods = list(row[t])
                cols.append(", ".join(prods))
                if len(prods) > 1:
                    self.is_ll1 = False
            table.add_row([nt, *cols])
        result += table.get_string()

        result += f"\ngrammar is LL(1): {self.is_ll1}\n"
        return result

    def solve_grammar(self) -> None:
        self.fixed_point_nullable()
        self.fixed_point_first_set()
        self.fixed_point_follow_set()
        self.compute_ll1_table()
        print(self)

    def add_nt(self, nt: str) -> None:
        self.nts.append(nt)

    def add_t(self, t: str) -> None:
        self.ts.append(t)

    def add_prod(self, nt: str, prod: str) -> None:
        self.prods[nt].add(prod)

    def nullable_first_pass(self) -> Tuple[Dict[str, bool], Dict[str, List[List[str]]]]:
        nullable = {}
        depends = defaultdict(list)
        for nt in self.nts:
            nullable[nt] = False
        for nt in self.nts:
            for prod in self.prods[nt]:
                if prod == EPSILON:
                    nullable[nt] = True
                    break
                if prod.isupper():
                    depends[nt].append([*prod])
        return nullable, depends

    def all_nullable(self, nullable: Set[str], dep_list: List[str]) -> bool:
        for d in dep_list:
            if not nullable[d]:
                return False
        return True

    def iterate_nullable(
        self, nullable: Set[str], depends: Dict[str, List[List[str]]]
    ) -> Set[str]:
        for nt, dependencies in depends.items():
            if nullable[nt]:
                continue
            for dep_list in dependencies:
                if self.all_nullable(nullable, dep_list):
                    nullable[nt] = True
                    break
        return nullable

    def fixed_point_nullable(self) -> None:
        prev, depends = self.nullable_first_pass()
        curr = self.iterate_nullable(deepcopy(prev), depends)
        while prev != curr:
            prev, curr = curr, self.iterate_nullable(deepcopy(curr), depends)
        self.nullable = curr

    def first_set_first_pass(self) -> Tuple[Dict[str, Set[str]], Dict[str, Set[str]]]:
        first_set = defaultdict(set)
        depends = defaultdict(set)
        for nt in self.nts:
            first_set[nt] = set()
            for prod in self.prods[nt]:
                if prod == EPSILON:
                    first_set[nt].add(prod)
                    continue
                for symbol in prod:
                    if is_t(symbol):
                        first_set[nt].add(symbol)
                        break
                    if is_nt(symbol):
                        depends[nt].add(symbol)
                        if not self.nullable[symbol]:
                            break
        return first_set, depends

    def iterate_first_set(
        self, first_set: Dict[str, Set[str]], depends: Dict[str, Set[str]]
    ) -> Dict[str, Set[str]]:
        for nt in self.nts:
            for d in depends[nt]:
                first_set[nt] |= first_set[d]
                if not self.nullable[nt]:
                    first_set[nt].discard(EPSILON)
        return first_set

    def fixed_point_first_set(self) -> None:
        prev, depends = self.first_set_first_pass()
        curr = self.iterate_first_set(deepcopy(prev), depends)
        while prev != curr:
            prev, curr = curr, self.iterate_first_set(deepcopy(curr), depends)
        self.first = curr

    def prod_first_set(self, prod: str) -> Set[str]:
        first_set = set()
        if prod == EPSILON:
            first_set.add(EPSILON)
            return first_set
        for symbol in prod:
            if is_t(symbol):
                first_set.add(symbol)
                first_set.discard(EPSILON)
                break
            if is_nt(symbol):
                first_set |= self.first[symbol]
                if not self.nullable[symbol]:
                    first_set.discard(EPSILON)
                    break
        return first_set

    def follow_set_first_pass(self) -> Tuple[Dict[str, Set[str]], Dict[str, Set[str]]]:
        follow_set = defaultdict(set)
        depends = defaultdict(set)
        follow_set[self.start_symbol].add("$")
        for nt in self.nts:
            for prod in self.prods[nt]:
                for i, symbol in enumerate(prod):
                    if symbol == EPSILON or is_t(symbol):
                        continue
                    first_of_rest = self.prod_first_set(prod[i + 1 :])
                    if EPSILON in first_of_rest or i == len(prod) - 1:
                        depends[symbol].add(nt)
                        first_of_rest.discard(EPSILON)
                    follow_set[symbol] |= first_of_rest
        return follow_set, depends

    def iterate_follow_set(
        self, follow_set: Dict[str, Set[str]], depends: Dict[str, Set[str]]
    ) -> Dict[str, Set[str]]:
        for nt in self.nts:
            for d in depends[nt]:
                follow_set[nt] |= follow_set[d]
        return follow_set

    def fixed_point_follow_set(self) -> None:
        prev, depends = self.follow_set_first_pass()
        curr = self.iterate_follow_set(deepcopy(prev), depends)
        while prev != curr:
            prev, curr = curr, self.iterate_follow_set(deepcopy(curr), depends)
        self.follow = curr

    def compute_ll1_table(self) -> None:
        for nt in self.nts:
            row = {}
            for t in self.ts:
                row[t] = set()
            row["$"] = set()
            self.ll1_table[nt] = row
        for nt in self.nts:
            for prod in self.prods[nt]:
                first_of_p = self.prod_first_set(prod)
                for symbol in first_of_p:
                    if symbol == EPSILON:
                        for f in self.follow[nt]:
                            self.ll1_table[nt][f].add(prod)
                    else:
                        self.ll1_table[nt][symbol].add(prod)


def parse_grammar(lines: List[str]) -> Grammar:
    g = Grammar()
    for line in lines:
        nt, productions = line.split(":==")
        nt = nt.strip()
        productions = [s.strip() for s in productions.split("|")]
        if g.start_symbol is None:
            g.start_symbol = nt
        g.add_nt(nt)
        for prod in productions:
            g.add_prod(nt, prod)
            for sym in prod:
                if is_t(sym) and sym != EPSILON:
                    g.add_t(sym)
    g.nts = sorted(list(set(g.nts)))
    g.ts = sorted(list(set(g.ts)))
    return g


def main():
    contents = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        if len(line.strip()) != 0:
            contents.append(line)
    g = parse_grammar(contents)
    g.solve_grammar()


if __name__ == "__main__":
    main()
