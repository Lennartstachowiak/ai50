from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    Not(And(AKnight, AKnave)), Or(AKnave, AKnight),
    Implication(Not(And(AKnight, AKnave)), AKnave),
)

# Puzzle 1
knowledge1 = And(
    Not(And(AKnight, AKnave)), 
    Not(And(BKnight, BKnave)), 
    Or(AKnave, AKnight), 
    Or(BKnave, BKnight),
    # A says "We are both knaves."
    Implication(Not(And(AKnave,BKnave)),AKnave),
    Implication(AKnave,BKnight),
    # B says nothing.
)

# Puzzle 2
knowledge2 = And(
    Not(And(AKnight, AKnave)),
    Not(And(BKnight, BKnave)),
    Or(AKnave, AKnight),
    Or(BKnave, BKnight),
    # A says "We are the same kind."
    Implication(AKnight,BKnight),
    Implication(AKnave,BKnight),
    # B says "We are of different kinds."
    Implication(BKnight,AKnave),
    Implication(BKnave,AKnave)
)

# Puzzle 3
knowledge3 = And(
    Not(And(AKnight, AKnave)),
    Not(And(BKnight, BKnave)),
    Not(And(CKnight, CKnave)),
    Or(AKnave, AKnight),
    Or(BKnave, BKnight),
    Or(CKnave, CKnight),
    # A says either "I am a knight." or "I am a knave.", but you don't know which.
    Or(
        And(AKnight, Or(AKnight, AKnave)),
        And(AKnave, Not(Or(AKnight, AKnave))),
    ),
    # B says "A said 'I am a knave'."
    Implication(BKnight, AKnave),
    Implication(BKnave, AKnight),
    # B says "C is a knave."
    Implication(CKnave,BKnight),
    Implication(CKnight,BKnave),
    # C says "A is a knight."
    Implication(AKnight,CKnight),
    Implication(AKnave,CKnave)
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
