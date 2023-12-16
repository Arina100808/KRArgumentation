from preferred_discussion_game import ArgumentationFramework
from os.path import isfile, join
from graphviz import Digraph
from os import listdir
import os


def generate_argumentation_framework(af_file_path):
    # Create a new directory 'plots' if it doesn't exist
    plots_dir = 'plots'
    os.makedirs(plots_dir, exist_ok=True)

    af = ArgumentationFramework(af_file_path)

    arguments = af.arguments
    attack_relations = af.attack_relations

    # Create a new directed graph
    dot = Digraph(comment='Argumentation Framework')
    dot.attr(rankdir='LR')

    # Add arguments to the graph
    for argument in arguments:
        value = arguments[argument] if isinstance(arguments, dict) else argument
        dot.node(argument, value)

    # Add attack relations to the graph
    for relation in attack_relations:
        dot.edge(relation[0], relation[1])

    # Save the graph as a PNG file
    png_file_name = plots_dir + "/" + af_file_path.split('/')[1].split('.')[0]
    dot.render(png_file_name, format='png', cleanup=True)


if __name__ == '__main__':
    folder = "arg_frameworks"
    # Get file names of all tests
    all_tests = [f for f in listdir(folder) if isfile(join(folder, f))]
    all_tests.remove('.DS_Store')
    all_tests.sort()
    # Generate the argumentation frameworks and visualize them
    for file in all_tests:
        file_path = f"{folder}/{file}"
        generate_argumentation_framework(file_path)
