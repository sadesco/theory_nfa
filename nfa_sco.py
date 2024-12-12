#!/usr/bin/env python3
import sys
import csv
import time
from tqdm import tqdm

# Read and process an NFA configuration file
def load_nfa_config(file_path):
    """Load the NFA configuration from a file and initialize relevant data structures."""
    global machine_name  # Name of the NFA
    global states        # List of states
    global alphabet      # List of input symbols
    global initial_state # Start state
    global final_states  # Accept states
    global transitions   # Transition table (dictionary)

    transitions = {}

    def parse_metadata(line, index):
        """Parse metadata lines (NFA name, states, symbols, start state, accept states)."""
        nonlocal machine_name, states, alphabet, initial_state, final_states
        if index == 0:
            machine_name = line.strip().split(',')[0]  # NFA name
        elif index == 1:
            states = list(filter(None, line.strip().split(',')))  # State names
        elif index == 2:
            alphabet = list(filter(None, line.strip().split(',')))  # Input symbols
        elif index == 3:
            initial_state = line.strip().split(',')[0]  # Start state
        elif index == 4:
            final_states = list(filter(None, line.strip().split(',')))  # Accept states

    def parse_transition(line):
        """Parse and store a single transition rule."""
        source, symbol, destination = line.split(',')[0:3]
        if source not in transitions:
            transitions[source] = []
        transitions[source].append((symbol, destination))

    # Read the file and process line by line
    with open(file_path) as file:
        for idx, line in tqdm(enumerate(file), desc='Loading NFA configuration...'):
            if idx < 5:
                parse_metadata(line, idx)  # Parse metadata lines
            else:
                parse_transition(line.strip())  # Parse transition rules

# Trace all paths through the NFA for a given input string
def process_input(input_string):
    """Simulate the NFA on an input string and find all possible and accepting paths."""
    frontier = [(initial_state, input_string, False, initial_state)]  # Stack to hold current exploration state
    total_paths = 0  # Total possible paths
    accepting_paths = 0  # Total accepting paths
    accept_sequences = []  # Sequences of states for accepting paths

    # Handle empty string input
    if input_string == '~$':
        if initial_state in final_states:
            accepting_paths += 1
            total_paths += 1
            accept_sequences.append(initial_state)

    # Process the input string through the NFA
    while frontier:
        current_state, remaining_input, is_epsilon, sequence = frontier.pop()

        # If no more input, check if the current state is an accepting state
        if remaining_input == '$':
            if current_state in final_states:
                accepting_paths += 1
                accept_sequences.append(sequence)

            if not is_epsilon:
                total_paths += 1

        # Expand transitions for the current state
        for symbol, next_state in transitions.get(current_state, []):
            if symbol == '~':  # Epsilon transition
                frontier.append((next_state, remaining_input, True, sequence + ',' + next_state))
            elif remaining_input and remaining_input[0] == symbol:  # Match input symbol
                frontier.append((next_state, remaining_input[1:], False, sequence + ',' + next_state))

    return total_paths, accepting_paths, accept_sequences

# Write results to an output file
def save_results(input_file, input_data, total_paths, accepting_paths, accept_sequences):
    """Write the results of the NFA simulation to a CSV file."""
    output_file = f"{input_file[:-4]}-{input_data}-output.csv"
    with open(output_file, 'w') as file:
        writer = csv.writer(file)
        writer.writerow(['input_file', 'NFA_name', 'input_string', 'possible_paths', 'accept_paths'])
        writer.writerow([input_file, machine_name, input_data, total_paths, accepting_paths])
        for sequence in accept_sequences:
            writer.writerow(sequence.split(','))

# Main function to handle user interaction and control flow
def main():
    """Main function to drive the NFA simulation."""
    input_file = input('Enter NFA file name: ')
    load_nfa_config(input_file)  # Load the NFA configuration

    user_input = input('Input a string: ')
    user_input += '$'  # Append end-of-input marker

    paths, accept_count, accept_seq = process_input(user_input)

    print(f"Total paths: {paths}, Accepting paths: {accept_count}")
    for seq in accept_seq:
        print(seq)

    save_results(input_file, user_input[:-1], paths, accept_count, accept_seq)

if __name__ == '__main__':
    main()
