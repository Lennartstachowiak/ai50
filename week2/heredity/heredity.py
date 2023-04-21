import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    p = {}
    for person in people:
        # Get person data
        person_amount_of_genes = 0
        if person in one_gene:
            person_amount_of_genes = 1
        if person in two_genes:
            person_amount_of_genes = 2
        person_has_trait = False
        if person in have_trait:
            person_has_trait = True
        father = people[person]["father"]
        mother = people[person]["mother"]
        parents = [mother, father]

        if all(parent != None for parent in parents):
            # Get probability for person with parents
            parent_probs = []
            for parent in parents:
                if parent in two_genes:
                    parent_probs.append(1 - PROBS["mutation"])
                    continue
                if parent in one_gene:
                    parent_probs.append(.5)
                    continue
                parent_probs.append(PROBS["mutation"])

            # Get result of calculation for given gene amount
            if person_amount_of_genes == 0:
                prob_to_have_gene = (1-parent_probs[0])*(1-parent_probs[1])
            if person_amount_of_genes == 1:
                prob_to_have_gene = parent_probs[0]*(1-parent_probs[1]) + \
                    (1-parent_probs[0])*parent_probs[1]
            if person_amount_of_genes == 2:
                prob_to_have_gene = parent_probs[0]*parent_probs[1]
        else:
            # Get probability for persons without parents
            prob_to_have_gene = PROBS["gene"][person_amount_of_genes]

        prob_has_trait = PROBS["trait"][person_amount_of_genes][person_has_trait]
        prob = prob_to_have_gene * prob_has_trait
        p[person] = prob

    # Multiply all probabilities of each person together
    p_sum = 1
    for prob in p.values():
        p_sum *= prob
    return p_sum


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for person in probabilities.keys():
        person_amount_of_genes = 0
        if person in one_gene:
            person_amount_of_genes = 1
        if person in two_genes:
            person_amount_of_genes = 2
        person_has_trait = False
        if person in have_trait:
            person_has_trait = True

        probabilities[person]["gene"][person_amount_of_genes] += p
        probabilities[person]["trait"][person_has_trait] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person, values in probabilities.items():
        for type, type_values in values.items():
            type_sum = sum(type_values.values())
            for key, value in type_values.items():
                if type_sum != 0:
                    probabilities[person][type][key] = value/type_sum


if __name__ == "__main__":
    main()
