# trace-nfa

The nfa_sco.py program prompts the user to enter the name of the NFA file. Once the NFA data is loaded, the program will request the user to input a string to test. It will then display the total number of possible paths and the number of accepting paths on the screen.

## Extra work: NFA
1. The extra work involved developing a Python script that simulates the behavior of a Non-deterministic Finite Automaton (NFA). The NFA is defined through a configuration file containing metadata (NFA name, states, symbols, start state, and accept states) and transition rules. The script is designed to:

1. Load an NFA configuration from a CSV file.
2. imulate the NFA on a given input string.
3. Track the number of total paths and accepting paths.
4. Output the results to a CSV file, including the full state sequences for accepting paths.

The extra work also includes handling epsilon transitions (~), which are transitions that occur without consuming an input symbol.

## Why did I chose it?

I chose this extra work to better understand the workings of NFAs and to enhance my problem-solving skills in automata theory. Specifically, I felt I lacked a solid understanding of how NFAs handle multiple paths for a single input string, particularly when considering epsilon transitions.

This extra work helped me improve my understanding of NFAs, as it required me to simulate all possible state transitions and track whether any given path leads to an accepting state. This understanding is crucial for exams and homework dealing with automata and formal languages, especially when working on problems involving NFA construction, path analysis, and language recognition.

Specific homework and problem types that benefited:
1. Homework involving simulation of NFAs - TOC-HW4A -> specifically problem 3
2. Exam problems - Exam 01 - problem 5

## What files are what?

nfa_sco.py: This is the main Python script that simulates the NFA. It includes the following functions:

1. load_nfa_config(file_path): Loads the NFA configuration from a file.
2. process_input(input_string): Simulates the NFA on the given input string.
3. save_results(input_file, input_data, total_paths, accepting_paths, accept_sequences): Saves the results to a CSV file.
4. main(): The entry point of the program that orchestrates loading the NFA, processing the input, and saving the results.
