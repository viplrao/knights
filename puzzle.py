from logic import *
from typing import Union
AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Shut mypy up
Statement = Union[Symbol, And, Or, Biconditional, Implication]

# Each character is either a knight or a knave (not neither)
ACommon = And(
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave))
)

BCommon = And(
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave))
)

CCommon = And(
    Or(CKnight, CKnave),
    Not(And(CKnight, CKnave))
)


# Puzzle 0
# A says "I am both a knight and a knave."
ASays: Statement = And(AKnight, AKnave)
knowledge0 = And(
    ACommon,
    # Either:
    Or(
        # A is both
        And(AKnight, ASays),
        # Or A is lying (and a knave)
        And(AKnave, Not(ASays))
    )
)


# Puzzle 1
# A says "We are both knaves."
# B says nothing.
ASays = And(AKnave, BKnave)
knowledge1 = And(
    ACommon,
    BCommon,
    # Either:
    Or(
        # A is telling the truth
        And(AKnight, ASays),
        # Or A is lying
        And(AKnave, Not(ASays))
    )
)


# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
ASays = Or(And(AKnight, BKnight), And(AKnave, BKnave))
BSays: Statement = Or(And(AKnight, Not(BKnight)), And(AKnave, Not(BKnave)))
knowledge2 = And(
    ACommon,
    BCommon,
    # Who's right?:
    Or(
        And(AKnight, ASays, BKnight, BSays),
        And(BKnight, BSays)
    ),

)


# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."

BSays = CKnave
CSays = AKnight
knowledge3 = And(
    ACommon,
    BCommon,
    CCommon,
    # B is a Knight if A said it was a Knave and was telling the truth (think about it - a knave will never proclaim it's a knave)
    Biconditional(And(AKnight, AKnave), BKnight),
    # If B is a Knight, then C is a Knave
    Biconditional(BKnight, CKnave),
    # If C is a Knave, then so is A
    Biconditional(CKnave, AKnight),
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
