from itertools import chain, combinations, product
from argumentation_framework import ArgumentationFramework
from os.path import isfile, join
from os import listdir
import argparse
import time


class AdmissibleSemantics(ArgumentationFramework):
    def conflict_free(self):
        cf = []
        if isinstance(self.arguments, dict):
            arguments = list(self.arguments.keys())
        else:
            arguments = self.arguments

        n = len(arguments) + 1
        powerset = chain.from_iterable(combinations(arguments, r) for r in range(n))
        all_subsets = [set(combination) for combination in powerset]

        for subset in all_subsets:
            possible_relations = list(product(subset, repeat=2))
            is_conflict_free = all(
                [list(attack) not in self.attack_relations for attack in possible_relations]
            )
            if is_conflict_free:
                cf.append(subset)
        return cf

    def s_defends_argument(self, s, argument):
        attackers = set(self.get_attackers([argument]).keys())
        for attacker in attackers:
            defenders = set(self.get_attackers([attacker]).keys())
            if not defenders & s:
                return False
        return True

    def admissible(self, cf):
        adm = []
        for s in cf:
            defends = True
            for argument in s:
                if not self.s_defends_argument(s, argument):
                    defends = False
                    break
            if defends:
                adm.append(s)
        return adm

    def credulous_admissible(self, argument):
        accepted = False
        cf = self.conflict_free()
        adm = self.admissible(cf)
        print(f"cf: {cf}")
        print(f"adm: {adm}")
        print(f"argument: {argument}")
        for s in adm:
            if argument in s:
                accepted = True
                return accepted
        return accepted


if __name__ == '__main__':
    folder = "arg_frameworks"

    # Get file names of all tests
    all_tests = [f for f in listdir(folder) if isfile(join(folder, f))]
    if '.DS_Store' in all_tests: all_tests.remove('.DS_Store')
    all_tests.sort()

    json_file = all_tests[1]
    af_file_path = f"{folder}/{json_file}"
    arg = "a"

    parser = argparse.ArgumentParser(description='Check whether the given argument is credulously acceptable '
                                                 'under the admissible semantics in a given AF')
    parser.add_argument('file_path', type=str, nargs='?', default=af_file_path,
                        help='Path to the argumentation framework JSON file')
    parser.add_argument('argument', type=str, nargs='?', default=arg, help='Argument')
    args = parser.parse_args()

    semantics = AdmissibleSemantics(args.file_path)

    af_arguments = semantics.arguments.keys() if isinstance(semantics.arguments, dict) else semantics.arguments
    while args.argument not in af_arguments:
        print(f"Error: There is no such argument {args.argument} in given AF {args.file_path}.")
        print("Provide correct argument:")
        args.argument = input()

    # Check whether the given argument is credulously acceptable under the admissible semantics in a given AF
    # and calculate running time
    start_time = time.time()
    accepted_adm = semantics.credulous_admissible(args.argument)
    running_time = time.time() - start_time
    print(f"--- Running time: {round(running_time*1000, 4)} milliseconds ---")

    # Print the results
    result1 = "Yes" if accepted_adm else "No"
    result2 = "" if accepted_adm else "not "

    print(f"\n{result1}, the given argument {args.argument} is {result2}credulously acceptable "
          f"under admissible semantics in a given AF.")
