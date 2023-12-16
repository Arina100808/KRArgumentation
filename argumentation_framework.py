import json


class ArgumentationFramework:
    def __init__(self, arg_framework_file):
        self.arg_framework_file = arg_framework_file
        self.arg_framework = None
        while self.arg_framework is None:
            try:
                self.arg_framework = self.open_json()
            except FileNotFoundError:
                print(f"Error: File {self.arg_framework_file} not found.")
                print("Provide correct file path:")
                self.arg_framework_file = input()
        self.arguments = self.arg_framework["Arguments"]
        self.attack_relations = self.arg_framework["Attack Relations"]

    def open_json(self):
        with open(self.arg_framework_file) as f:
            d = json.load(f)
            return d

    def get_attackers(self, arguments):
        attackers = {}
        for r in self.attack_relations:
            if r[1] in arguments:
                if r[0] not in attackers:
                    attackers[r[0]] = set()
                attackers[r[0]].add(r[1])
        return attackers
