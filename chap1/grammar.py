from typing import Literal


class Symbol:
    def __init__(self, name: str) -> None:
        self.__name = name

    def __repr__(self) -> str:
        return self.__name


class Grammar:
    def __init__(
        self,
        terminal: set[str],
        non_terminal: set[str],
        rules: list[tuple[str, list[str]]],
        start: str,
    ) -> None:
        if len(terminal & non_terminal) != 0:  # intersect
            raise Exception("Terminal and non-terminal sets have an intersection")
        if start not in non_terminal:
            raise Exception("The start symbol is not in the set of non-terminals")

        self.__terminal_set = {name: Symbol(name) for name in terminal}
        self.__non_terminal_set = {name: Symbol(name) for name in non_terminal}
        self.__rules = list[Rule]()
        self.__start = self.__non_terminal_set[start]

        for rule_left, rule_rights in rules:
            rule_left_symbol = self.__find_rule_left_symbol(non_terminal, rule_left)
            rule_right_symbols = self.__find_rule_right_symbols(
                terminal, non_terminal, rule_rights
            )

            self.__rules.append(Rule(rule_left_symbol, rule_right_symbols))

    def __find_rule_left_symbol(self, non_terminal: set[str], rule_left: str):
        if rule_left not in non_terminal:
            raise Exception(
                "Nonexistent symbol appears on the left-hand side of the rule"
            )
        rule_left_symbol = self.__non_terminal_set[rule_left]
        return rule_left_symbol

    def __find_rule_right_symbols(
        self, terminal: set[str], non_terminal: set[str], rule_rights: list[str]
    ):
        rule_right_symbols = list[Symbol]()
        for rule_right in rule_rights:
            if rule_right in terminal:
                rule_right_symbols.append(self.__terminal_set[rule_right])
            elif rule_right in non_terminal:
                rule_right_symbols.append(self.__non_terminal_set[rule_right])
            else:
                raise Exception(
                    "Nonexistent symbol appears on the right-hand side of the rule"
                )
        return rule_right_symbols

    def get_rules(self):
        return self.__rules

    def get_rule(self, no: int):
        return self.__rules[no]

    def get_symbol(self, name: str):
        if name in self.__terminal_set:
            return self.__terminal_set[name]
        elif name in self.__non_terminal_set:
            return self.__non_terminal_set[name]
        else:
            return None

    def create_empty_sequence(self):
        return Sequence(self, [])

    def create_sentence_from_start(self):
        return Sequence(self, [self.__start])

    def is_terminal(self, symbol: Symbol):
        return symbol in self.__terminal_set.values()

    def is_non_terminal(self, symbol: Symbol):
        return symbol in self.__non_terminal_set.values()


class Rule:
    def __init__(self, left: Symbol, right: list[Symbol]) -> None:
        self.left = left
        self.right = right

    def __repr__(self) -> str:
        return f"{self.left}::={''.join([str(symbol) for symbol in self.right])}"


class TreeNode:
    def __init__(self, symbol: Symbol) -> None:
        self.symbol = symbol
        self.children = list[TreeNode]()

    def walk_tree(tree: "TreeNode"):
        return (
            "["
            + str(tree.symbol)
            + "".join([child.walk_tree() for child in tree.children])
            + "]"
        )


class Sequence:
    def __init__(self, grammar: Grammar, symbols: list[Symbol]) -> None:
        self.__grammar = grammar

        self.__curr_nodes = list[TreeNode]()
        for symbol in symbols:
            self.__curr_nodes.append(TreeNode(symbol))

        self.__root: TreeNode | None = (
            self.__curr_nodes[0] if len(self.__curr_nodes) == 1 else None
        )

    def derive(self, pos: int, rule: Rule):
        father_node = self.__curr_nodes[pos]
        if father_node.symbol != rule.left:
            raise Exception(
                f"Rule mismatch, expect {rule.left}, got {father_node.symbol}"
            )

        child_nodes = [TreeNode(symbol) for symbol in rule.right]
        father_node.children = child_nodes

        self.__curr_nodes.remove(father_node)

        for no, child_node in enumerate(child_nodes):
            self.__curr_nodes.insert(pos + no, child_node)

    def restricted_derive(
        self,
        restriction: Literal["left-most", "right-most"],
        rule: Rule,
    ):
        pos = self.__get_non_terminal_pos_at(restriction)
        if pos == -1:
            raise Exception(
                f"No non-terminal found for '{restriction}' in the current sentence"
            )
        self.derive(pos, rule)

    def __get_non_terminal_pos_at(
        self, restriction: Literal["left-most", "right-most"]
    ):
        if restriction == "left-most":
            curr_nodes = list(enumerate(self.__curr_nodes))
        elif restriction == "right-most":
            curr_nodes = list(reversed(list(enumerate(self.__curr_nodes))))
        else:
            raise Exception(
                "Invalid value for 'restriction'. Must be 'left-most' or 'right-most'"
            )

        pos = -1
        for no, curr_node in curr_nodes:
            curr_symbol = curr_node.symbol
            if self.__grammar.is_non_terminal(curr_symbol):
                pos = no
                break
        return pos

    def reduce(self, pos: int, rule: Rule):
        child_nodes = self.__curr_nodes[pos : pos + len(rule.right)]
        for child_node, expect_symbol in zip(child_nodes, rule.right):
            if child_node.symbol != expect_symbol:
                raise Exception(
                    f"Rule mismatch, expect {expect_symbol}, got {child_node.symbol}"
                )

        father_node = TreeNode(rule.left)
        father_node.children = child_nodes

        for child_node in child_nodes:
            self.__curr_nodes.remove(child_node)

        self.__curr_nodes.insert(pos, father_node)

        if len(self.__curr_nodes) == 1:
            self.__root = self.__curr_nodes[0]

    def reduce_tail(
        self,
        rule: Rule,
    ):
        pos = len(self.__curr_nodes) - len(rule.right)
        self.reduce(pos, rule)

    def append(self, symbol: Symbol):
        self.__curr_nodes.append(TreeNode(symbol))

    def get_tree(self):
        return self.__root

    def curr_symbols(self):
        return [node.symbol for node in self.__curr_nodes]
