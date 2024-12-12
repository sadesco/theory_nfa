#!/usr/bin/env python3
import time
import sys
import csv
from tqdm import tqdm


def load_nfa_config(file_path):
    """load the NFA configuration from a file and initialize relevant data structures"""
    global machine_name  # name of the NFA
    global states        # list of states
    global alphabet      # list of input symbols
    global initial_state # start state
    global final_states  # accept states
    global transitions   # transition table 

    transitions = {}

    def parse_metadata(line, index):
        """parse metadata lines (NFA name, states, symbols, start state, accept states)"""
        if index == 0:
            global machine_name  
            machine_name = line.strip().split(',')[0]  # NFA name
        elif index == 1:
            global states  
            states = list(filter(None, line.strip().split(',')))  # state names
        elif index == 2:
            global alphabet  
            alphabet = list(filter(None, line.strip().split(',')))  # input symbols
        elif index == 3:
            global initial_state  
            initial_state = line.strip().split(',')[0]  # start state
        elif index == 4:
            global final_states  
            final_states = list(filter(None, line.strip().split(',')))  # accept states



    def parse_transition(line):
        """parse and store a single transition rule"""
        source, symbol, destination = line.split(',')[0:3]
        if source not in transitions:
            transitions[source] = []
        transitions[source].append((symbol, destination))
    
     # read the file and process line by line
    with open(file_path) as file:
        for idx, line in tqdm(enumerate(file), desc='Loading NFA configuration...'):
            if idx < 5:
                parse_metadata(line, idx)  # parse metadata lines
            else:
                parse_transition(line.strip())  # parse transition rules



def process_input(input_string):
    """simulate the NFA on an input string and find all possible and accepting paths"""
    frontier = [(initial_state, input_string, False, initial_state)]  # stack to hold current exploration state
    total_paths = 0  # total possible paths
    accepting_paths = 0  # total accepting paths
    accept_sequences = []  # sequences of states for accepting paths

    # handle empty string input
    if input_string == '~$':
        if initial_state in final_states:
            accepting_paths += 1
            total_paths += 1
            accept_sequences.append(initial_state)

    # process the input string through the NFA
    while frontier:
        current_state, remaining_input, is_epsilon, sequence = frontier.pop()

        # if no more input, check if the current state is an accepting state
        if remaining_input == '$':
            if current_state in final_states:
                accepting_paths += 1
                accept_sequences.append(sequence)

            if not is_epsilon:
                total_paths += 1

        # expand transitions for the current state
        for symbol, next_state in transitions.get(current_state, []):
            if symbol == '~':  # epsilon transition
                # if epsilon transition, do not consume input and just transition
                frontier.append((next_state, remaining_input, True, sequence + ',' + next_state))
            elif remaining_input and remaining_input[0] == symbol:  # match input symbol
                # if input symbol matches, move to the next state and consume the symbol
                frontier.append((next_state, remaining_input[1:], False, sequence + ',' + next_state))

    return total_paths, accepting_paths, accept_sequences




def save_results(input_file, input_data, total_paths, accepting_paths, accept_sequences):
    """write the results of the NFA simulation to a CSV file"""
    output_file = f"{input_file[:-4]}_{input_data}_output.csv"
    with open(output_file, 'w') as file:
        writer = csv.writer(file)
        writer.writerow(['input_file', 'NFA_name', 'input_string', 'possible_paths', 'accept_paths'])
        writer.writerow([input_file, machine_name, input_data, total_paths, accepting_paths])
        for sequence in accept_sequences:
            writer.writerow(sequence.split(','))



def main():
    """main function to drive the NFA simulation"""
    input_file = input('Enter NFA file name: ')
    load_nfa_config(input_file)  # load the NFA configuration

    user_input = input('Input a string: ')
    user_input += '$'  # append end-of-input marker

    paths, accept_count, accept_seq = process_input(user_input)

    print(f"Total paths: {paths}, Accepting paths: {accept_count}")
    for seq in accept_seq:
        print(seq)

    save_results(input_file, user_input[:-1], paths, accept_count, accept_seq)

if __name__ == '__main__':
    main()