from grammar import Grammar

G = Grammar(
    terminal={"+", "-", "*", "/", "i", "(", ")"},
    non_terminal={"A", "M", "V"},
    rules=[
        ("A", ["M"]),
        ("A", ["A", "+", "M"]),
        ("A", ["A", "-", "M"]),
        ("M", ["V"]),
        ("M", ["M", "*", "V"]),
        ("M", ["M", "/", "V"]),
        ("V", ["i"]),
        ("V", ["(", "A", ")"]),
    ],
    start="A",
)

Sentence = "i*(i+i-i)"
Sentence = [G.get_symbol(char) for char in Sentence]


def test_canonical_reduction():
    siter = iter(Sentence)
    seq = G.create_empty_sequence()
    read_next = lambda: seq.append(next(siter))
    reduce_use = lambda no: seq.reduce_tail(G.get_rule(no))

    read_next()  # i
    reduce_use(6)  # V::=i
    reduce_use(3)  # M::=V
    read_next()  # *
    read_next()  # (
    read_next()  # i
    reduce_use(6)  # V::=i
    reduce_use(3)  # M::=V
    reduce_use(0)  # A::=M
    read_next()  # +
    read_next()  # i
    reduce_use(6)  # V::=i
    reduce_use(3)  # M::=V
    reduce_use(1)  # A::=A+M
    read_next()  # -
    read_next()  # i
    reduce_use(6)  # V::=i
    reduce_use(3)  # M::=V
    reduce_use(2)  # A::=A-M
    read_next()  # )
    reduce_use(7)  # V::=(A)
    reduce_use(4)  # M::=M*V
    reduce_use(0)  # A::=M

    tree = seq.get_tree()
    assert (
        tree.walk_tree()
        == "[A[M[M[V[i]]][*][V[(][A[A[A[M[V[i]]]][+][M[V[i]]]][-][M[V[i]]]][)]]]]"
    )


def test_left_most_derivation():
    seq = G.create_sentence_from_start()
    derive_use = lambda no: seq.restricted_derive("left-most", G.get_rule(no))

    derive_use(0)  # A::=M
    derive_use(4)  # M::=M*V
    derive_use(3)  # M::=V
    derive_use(6)  # V::=i
    derive_use(7)  # V::=(A)
    derive_use(2)  # A::=A-M
    derive_use(1)  # A::=A+M
    derive_use(0)  # A::=M
    derive_use(3)  # M::=V
    derive_use(6)  # V::=i
    derive_use(3)  # M::=V
    derive_use(6)  # V::=i
    derive_use(3)  # M::=V
    derive_use(6)  # V::=i

    assert seq.curr_symbols() == Sentence

    tree = seq.get_tree()
    assert (
        tree.walk_tree()
        == "[A[M[M[V[i]]][*][V[(][A[A[A[M[V[i]]]][+][M[V[i]]]][-][M[V[i]]]][)]]]]"
    )


def test_right_most_derivation():
    seq = G.create_sentence_from_start()
    derive_use = lambda no: seq.restricted_derive("right-most", G.get_rule(no))

    derive_use(0)
    derive_use(4)
    derive_use(7)
    derive_use(2)
    derive_use(3)
    derive_use(6)
    derive_use(1)
    derive_use(3)
    derive_use(6)
    derive_use(0)
    derive_use(3)
    derive_use(6)
    derive_use(3)
    derive_use(6)

    assert seq.curr_symbols() == Sentence

    tree = seq.get_tree()
    assert (
        tree.walk_tree()
        == "[A[M[M[V[i]]][*][V[(][A[A[A[M[V[i]]]][+][M[V[i]]]][-][M[V[i]]]][)]]]]"
    )
