from argumentation_framework import ArgumentationFramework
from os.path import isfile, join
from os import listdir
import argparse
import random


class PreferredDiscussionGame(ArgumentationFramework):
    def get_interpretation(self, argument, player=None, attacked=None):
        if isinstance(self.arguments, dict):
            interpretation = self.arguments[argument]
        else:
            if player == "proponent":
                if attacked is None:
                    interpretation = f"I have an admissible labelling in which {argument} is labelled 'in'."
                else:
                    interpretation = f"{attacked} is labelled 'out' because {argument} is labelled 'in'."
            else:
                interpretation = (f"But then in your labelling it must also be the case that {attacked}’s "
                                  f"attacker {argument} is labelled 'out'. Why?")
        return interpretation

    def choose_argument_opponent(self, options):
        choice = 0
        print("\n\tConsider the following options:")
        options_list = []
        valid_choices = []

        i = 0
        for option in list(options.keys()):
            for attacked in options[option]:
                interpretation = self.get_interpretation(argument=option, player="opponent",
                                                         attacked=attacked)
                i += 1
                if isinstance(self.arguments, dict):
                    option_nr = option
                else:
                    option_nr = str(i)
                print(f"\t{option_nr}. {interpretation}")
                options_list.append((option, attacked))
                valid_choices.append(option_nr)
                if isinstance(self.arguments, dict):
                    break
        while choice not in valid_choices:
            choice = input("\tType argument number that you want to choose: ")
            if choice not in valid_choices:
                print("\tInvalid answer, try again.")
        if isinstance(self.arguments, dict):
            chosen_argument_attacked = next((t for t in options_list if t[0] == choice), None)
        else:
            chosen_argument_attacked = options_list[int(choice) - 1]
        return chosen_argument_attacked

    def play(self, claimed_argument):
        """
        computer = proponent (defending the given argument)
        user = opponent (trying to attack the given argument)
        """
        used_proponent = set()
        used_opponent = set()
        p = claimed_argument
        o = None

        while True:
            # for each round:

            # 1. proponent outputs an argument P that attacks O from previous round
            if o is not None:  # at the beginning, the proponent outputs claimed_argument
                options_proponent = list(self.get_attackers([o]).keys())  # can use the same argument twice
                # CHECK: if proponent is unable to make a move => opponent wins
                if len(options_proponent) == 0:
                    winner = "opponent"
                    print("\nProponent is unable to make a move.")
                    return winner
                p = random.choice(list(options_proponent))  # argument outputted by the proponent
            used_proponent.add(p)
            print(f"\nP: {self.get_interpretation(argument=p, player='proponent', attacked=o)}")

            # CHECK: if P was used by opponent => opponent wins
            if p in used_opponent:
                winner = "opponent"
                print("\nArgument chosen by proponent was used by opponent.")
                return winner

            # 2. the user can choose O that attacks any P outputted in previous rounds
            options_opponent = self.get_attackers(used_proponent)
            options_opponent = {key: value for key, value in options_opponent.items()
                                if key not in used_opponent}  # cannot use the same argument twice
            # CHECK: if opponent has no choices left => proponent wins
            if len(options_opponent.keys()) == 0:
                winner = "proponent"
                print("\nOpponent is unable to make a move.")
                return winner
            o, attacked = self.choose_argument_opponent(options_opponent)  # argument chosen by the opponent
            used_opponent.add(o)
            print(f"\nO: {self.get_interpretation(argument=o, player='opponent', attacked=attacked)}")

            # CHECK: if O was used by proponent => opponent wins
            if o in used_proponent:
                winner = "opponent"
                print("\nArgument chosen by opponent was used by proponent.")
                return winner


if __name__ == '__main__':
    folder = "arg_frameworks"
    # get file names of all tests
    all_tests = [f for f in listdir(folder) if isfile(join(folder, f))]
    all_tests.remove('.DS_Store')
    all_tests.sort()

    json_file = all_tests[3]
    af_file_path = f"{folder}/{json_file}"
    claimed_arg = "0"

    parser = argparse.ArgumentParser(description='Play a preferred discussion game against the computer, '
                                                 'based on a loaded AF.')
    parser.add_argument('file_path', type=str, nargs='?', default=af_file_path,
                        help='Path to the argumentation framework JSON file')
    parser.add_argument('claimed_argument', type=str, nargs='?', default=claimed_arg,
                        help='Claimed argument')
    args = parser.parse_args()

    af = PreferredDiscussionGame(args.file_path)

    af_arguments = af.arguments.keys() if isinstance(af.arguments, dict) else af.arguments
    while args.claimed_argument not in af_arguments:
        print(f"Error: There is no such argument {args.claimed_argument} in given AF {args.file_path}.")
        print("Provide correct argument:")
        args.claimed_argument = input()

    result_winner = af.play(args.claimed_argument)

    print(f"\n--- Winner: {result_winner} ---")
    result = "no " if result_winner == "opponent" else ""
    print(f"That is, there is {result}preferred labelling in which {args.claimed_argument} is labelled 'in'.")
